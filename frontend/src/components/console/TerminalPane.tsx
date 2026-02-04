import { useEffect, useRef, useCallback, useState } from 'react'
import { Terminal as XTerm } from '@xterm/xterm'
import { FitAddon } from '@xterm/addon-fit'
import { Square, Trash2, RotateCcw, Lock, Unlock, X } from 'lucide-react'
import { Button } from '../common/Button'
import { Tooltip } from '../common/Tooltip'
import { useDeviceStore } from '../../stores/deviceStore'
import { useConsoleStore } from '../../stores/consoleStore'
import { useSettingsStore } from '../../stores/settingsStore'
import { useLayoutStore, PaneConfig } from '../../stores/layoutStore'
import { useWebSocket } from '../../hooks/useWebSocket'
import { api } from '../../services/api'
import { TERMINAL_CONFIG } from '../../config/terminal'
import '@xterm/xterm/css/xterm.css'

interface TerminalPaneProps {
  pane: PaneConfig
  isActive: boolean
  onActivate: () => void
  linkedScroll?: boolean
  onScroll?: (lines: number) => void
}

export function TerminalPane({ pane, isActive, onActivate, linkedScroll, onScroll }: TerminalPaneProps) {
  const terminalRef = useRef<HTMLDivElement>(null)
  const xtermRef = useRef<XTerm | null>(null)
  const fitAddonRef = useRef<FitAddon | null>(null)
  const inputBufferRef = useRef('')
  const savedInputRef = useRef('')

  const port = pane.devicePort
  const devices = useDeviceStore(state => state.devices)
  const device = devices.find(d => d.port === port)
  const { terminalFontSize, terminalLineHeight } = useSettingsStore()

  const clearOutput = useConsoleStore(state => state.clearOutput)
  const execute = useConsoleStore(state => state.execute)
  const interruptDevice = useConsoleStore(state => state.interrupt)
  const navigateHistory = useConsoleStore(state => state.navigateHistory)
  const appendInput = useConsoleStore(state => state.appendInput)
  const scrollLock = useConsoleStore(state => state.scrollLock)
  const setScrollLock = useConsoleStore(state => state.setScrollLock)
  const setHasNewOutput = useConsoleStore(state => state.setHasNewOutput)

  const assignDevice = useLayoutStore(state => state.assignDevice)

  const { subscribe, sendInput } = useWebSocket()
  const [inputMode] = useState<'line' | 'raw'>('line')

  const isScrollLocked = port ? scrollLock.get(port) ?? false : false

  // Initialize terminal
  useEffect(() => {
    if (!terminalRef.current) return

    if (xtermRef.current) {
      xtermRef.current.dispose()
      xtermRef.current = null
    }

    const xterm = new XTerm({
      theme: TERMINAL_CONFIG.theme,
      fontFamily: TERMINAL_CONFIG.fontFamily,
      fontSize: terminalFontSize ?? TERMINAL_CONFIG.fontSize,
      lineHeight: terminalLineHeight ?? TERMINAL_CONFIG.lineHeight,
      cursorBlink: true,
      cursorStyle: 'block',
      allowProposedApi: true,
    })

    const fitAddon = new FitAddon()
    xterm.loadAddon(fitAddon)

    xterm.open(terminalRef.current)
    fitAddon.fit()

    xtermRef.current = xterm
    fitAddonRef.current = fitAddon

    if (!port) {
      xterm.writeln('\x1b[90mNo device assigned\x1b[0m')
      xterm.writeln('\x1b[90mDrag a device here or select from dropdown\x1b[0m')
    }

    const resizeObserver = new ResizeObserver(() => {
      fitAddon.fit()
    })
    resizeObserver.observe(terminalRef.current)

    return () => {
      resizeObserver.disconnect()
      xterm.dispose()
      xtermRef.current = null
      fitAddonRef.current = null
    }
  }, [port])

  // Clear current line and replace with text
  const replaceCurrentLine = useCallback((newText: string) => {
    if (!xtermRef.current) return

    const xterm = xtermRef.current
    const currentLen = inputBufferRef.current.length

    if (currentLen > 0) {
      xterm.write('\b \b'.repeat(currentLen))
    }

    inputBufferRef.current = newText
    xterm.write(newText)
  }, [])

  // Keyboard shortcuts
  useEffect(() => {
    if (!xtermRef.current) return

    const xterm = xtermRef.current

    xterm.attachCustomKeyEventHandler((event) => {
      if (!port) return true

      // Ctrl+L - Clear
      if (event.ctrlKey && event.key === 'l') {
        event.preventDefault()
        handleClear()
        return false
      }

      // Ctrl+R - Soft reset
      if (event.ctrlKey && event.key === 'r' && !event.shiftKey) {
        event.preventDefault()
        handleReset()
        return false
      }

      // Up arrow - History up
      if (event.key === 'ArrowUp' && !event.ctrlKey) {
        event.preventDefault()
        if (savedInputRef.current === '' && inputBufferRef.current) {
          savedInputRef.current = inputBufferRef.current
        }
        const histCmd = navigateHistory(port, 'up')
        if (histCmd !== null) {
          replaceCurrentLine(histCmd)
        }
        return false
      }

      // Down arrow - History down
      if (event.key === 'ArrowDown' && !event.ctrlKey) {
        event.preventDefault()
        const histCmd = navigateHistory(port, 'down')
        if (histCmd !== null) {
          replaceCurrentLine(histCmd)
        } else {
          replaceCurrentLine(savedInputRef.current)
          savedInputRef.current = ''
        }
        return false
      }

      // Ctrl+Up/Down - Scroll with linked scroll support
      if (event.ctrlKey && (event.key === 'ArrowUp' || event.key === 'ArrowDown')) {
        event.preventDefault()
        const lines = event.key === 'ArrowUp' ? -3 : 3
        xterm.scrollLines(lines)
        if (linkedScroll && onScroll) {
          onScroll(lines)
        }
        return false
      }

      // Escape - Cancel input
      if (event.key === 'Escape') {
        event.preventDefault()
        replaceCurrentLine('')
        return false
      }

      return true
    })
  }, [port, navigateHistory, replaceCurrentLine, linkedScroll, onScroll])

  // Handle input
  useEffect(() => {
    if (!xtermRef.current || !port) return

    const xterm = xtermRef.current

    const dataHandler = xterm.onData((data) => {
      if (inputMode === 'raw') {
        sendInput(port, data)
        return
      }

      for (const char of data) {
        if (char === '\r' || char === '\n') {
          const command = inputBufferRef.current
          inputBufferRef.current = ''
          savedInputRef.current = ''
          xterm.write('\r\n')

          if (command.trim()) {
            appendInput(port, command)
            execute(port, command)
          }
        } else if (char === '\x7f' || char === '\b') {
          if (inputBufferRef.current.length > 0) {
            inputBufferRef.current = inputBufferRef.current.slice(0, -1)
            xterm.write('\b \b')
          }
        } else if (char === '\x03') {
          interruptDevice(port)
          inputBufferRef.current = ''
        } else if (char >= ' ' || char === '\t') {
          inputBufferRef.current += char
          xterm.write(char)
        }
      }
    })

    return () => {
      dataHandler.dispose()
    }
  }, [port, inputMode, sendInput, execute, interruptDevice, appendInput])

  // Subscribe to output
  useEffect(() => {
    if (!port) return

    subscribe(port)

    if (xtermRef.current) {
      xtermRef.current.writeln(`\r\n\x1b[1;32mConnected to ${port}\x1b[0m\r\n`)
    }

    const unsubscribe = useConsoleStore.subscribe((state) => {
      const pending = state.pendingOutput.get(port)
      if (pending && xtermRef.current) {
        const text = useConsoleStore.getState().getPendingOutput(port)
        if (text) {
          xtermRef.current.write(text)
          if (!isScrollLocked) {
            xtermRef.current.scrollToBottom()
          }
        }
      }
    })

    return () => {
      unsubscribe()
    }
  }, [port, subscribe, isScrollLocked])

  const handleClear = useCallback(() => {
    if (xtermRef.current) {
      xtermRef.current.clear()
      xtermRef.current.writeln('\x1b[1;34m=== Cleared ===\x1b[0m\r\n')
    }
    if (port) {
      clearOutput(port)
    }
  }, [port, clearOutput])

  const handleInterrupt = useCallback(async () => {
    if (port) {
      await interruptDevice(port)
    }
  }, [port, interruptDevice])

  const handleReset = useCallback(async () => {
    if (port) {
      if (xtermRef.current) {
        xtermRef.current.writeln('\r\n\x1b[1;33mSoft reset...\x1b[0m')
      }
      await api.reset(port, true)
    }
  }, [port])

  const toggleScrollLock = useCallback(() => {
    if (port) {
      setScrollLock(port, !isScrollLocked)
      if (isScrollLocked && xtermRef.current) {
        xtermRef.current.scrollToBottom()
        setHasNewOutput(port, false)
      }
    }
  }, [port, isScrollLocked, setScrollLock, setHasNewOutput])

  const handleRemoveDevice = useCallback(() => {
    assignDevice(pane.id, null)
  }, [pane.id, assignDevice])

  return (
    <div
      className={`flex flex-col h-full border ${isActive ? 'border-vscode-accent' : 'border-vscode-border'}`}
      onClick={onActivate}
    >
      {/* Mini header */}
      <div className="flex items-center justify-between px-2 py-0.5 bg-vscode-sidebar border-b border-vscode-border">
        <div className="flex items-center gap-1">
          <span className="text-xs text-vscode-text-dim truncate max-w-24">
            {port || 'Empty'}
          </span>
          {device && (
            <span className={`w-2 h-2 rounded-full ${device.state === 'connected' ? 'bg-green-500' : 'bg-gray-500'}`} />
          )}
        </div>

        <div className="flex items-center gap-0.5">
          <Tooltip content="Interrupt">
            <Button icon size="xs" variant="ghost" onClick={handleInterrupt} disabled={!port}>
              <Square size={10} />
            </Button>
          </Tooltip>

          <Tooltip content="Reset">
            <Button icon size="xs" variant="ghost" onClick={handleReset} disabled={!port}>
              <RotateCcw size={10} />
            </Button>
          </Tooltip>

          <Tooltip content={isScrollLocked ? "Unlock scroll" : "Lock scroll"}>
            <Button
              icon
              size="xs"
              variant={isScrollLocked ? "default" : "ghost"}
              onClick={toggleScrollLock}
              disabled={!port}
            >
              {isScrollLocked ? <Lock size={10} /> : <Unlock size={10} />}
            </Button>
          </Tooltip>

          <Tooltip content="Clear">
            <Button icon size="xs" variant="ghost" onClick={handleClear} disabled={!port}>
              <Trash2 size={10} />
            </Button>
          </Tooltip>

          {port && (
            <Tooltip content="Remove device">
              <Button icon size="xs" variant="ghost" onClick={handleRemoveDevice}>
                <X size={10} />
              </Button>
            </Tooltip>
          )}
        </div>
      </div>

      {/* Terminal area */}
      <div className="flex-1 overflow-hidden">
        <div ref={terminalRef} className="h-full" />
      </div>
    </div>
  )
}
