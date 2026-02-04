import { useEffect, useRef, useCallback, useState } from 'react'
import { Terminal as XTerm } from '@xterm/xterm'
import { FitAddon } from '@xterm/addon-fit'
import { Play, Square, Trash2, RotateCcw, Lock, Unlock, Download, ChevronDown, Power } from 'lucide-react'
import { Button } from '../common/Button'
import { Tooltip } from '../common/Tooltip'
import { Modal } from '../common/Modal'
import { useDeviceStore, selectSelectedDevice } from '../../stores/deviceStore'
import { useConsoleStore } from '../../stores/consoleStore'
import { useSettingsStore } from '../../stores/settingsStore'
import { useWebSocket } from '../../hooks/useWebSocket'
import { api } from '../../services/api'
import { TERMINAL_CONFIG } from '../../config/terminal'
import '@xterm/xterm/css/xterm.css'

export function Terminal() {
  const terminalRef = useRef<HTMLDivElement>(null)
  const xtermRef = useRef<XTerm | null>(null)
  const fitAddonRef = useRef<FitAddon | null>(null)
  const inputBufferRef = useRef('')
  const lastPortRef = useRef<string | null>(null)
  const savedInputRef = useRef('') // For history navigation

  const selectedDevice = useDeviceStore(selectSelectedDevice)
  const { terminalFontSize, terminalLineHeight } = useSettingsStore()
  const clearOutput = useConsoleStore(state => state.clearOutput)
  const execute = useConsoleStore(state => state.execute)
  const interruptDevice = useConsoleStore(state => state.interrupt)
  const navigateHistory = useConsoleStore(state => state.navigateHistory)
  const appendInput = useConsoleStore(state => state.appendInput)
  const appendSystemMessage = useConsoleStore(state => state.appendSystemMessage)
  const exportLogs = useConsoleStore(state => state.exportLogs)
  const startSession = useConsoleStore(state => state.startSession)
  const scrollLock = useConsoleStore(state => state.scrollLock)
  const setScrollLock = useConsoleStore(state => state.setScrollLock)
  const hasNewOutput = useConsoleStore(state => state.hasNewOutput)
  const setHasNewOutput = useConsoleStore(state => state.setHasNewOutput)
  const disconnect = useDeviceStore(state => state.disconnect)

  const { subscribe, sendInput } = useWebSocket()
  const [inputMode] = useState<'line' | 'raw'>('line')
  const [showPasteModal, setShowPasteModal] = useState(false)
  const [pasteContent, setPasteContent] = useState('')

  const port = selectedDevice?.port
  const isScrollLocked = port ? scrollLock.get(port) ?? false : false
  const hasNew = port ? hasNewOutput.get(port) ?? false : false

  // Initialize terminal once
  useEffect(() => {
    if (!terminalRef.current) return

    // Clean up existing terminal if any
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
      allowProposedApi: true, // Enable clipboard API
    })

    const fitAddon = new FitAddon()
    xterm.loadAddon(fitAddon)

    xterm.open(terminalRef.current)
    fitAddon.fit()

    xtermRef.current = xterm
    fitAddonRef.current = fitAddon

    // Welcome message
    xterm.writeln('\x1b[1;34m=== Pulsar Terminal ===\x1b[0m')
    xterm.writeln('Connect to a device to start')
    xterm.writeln('')
    xterm.writeln('\x1b[90mKeyboard shortcuts:\x1b[0m')
    xterm.writeln('\x1b[90m  Ctrl+C: Interrupt  |  Ctrl+L: Clear  |  Ctrl+R: Soft Reset\x1b[0m')
    xterm.writeln('\x1b[90m  Ctrl+S: Save Logs  |  Up/Down: History  |  Escape: Cancel\x1b[0m')
    xterm.writeln('')

    // Handle resize
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
  }, [])

  // Handle paste with confirmation for multi-line
  const handlePaste = useCallback(async () => {
    if (!port) return

    try {
      const text = await navigator.clipboard.readText()
      if (!text) return

      // Sanitize: remove null bytes, normalize line endings
      const sanitized = text.replace(/\0/g, '').replace(/\r\n/g, '\n').replace(/\r/g, '\n')
      const lines = sanitized.split('\n')

      if (lines.length > 5) {
        // Show confirmation for multi-line paste
        setPasteContent(sanitized)
        setShowPasteModal(true)
      } else {
        // Direct paste for small content
        executePaste(sanitized)
      }
    } catch (err) {
      console.error('Failed to read clipboard:', err)
    }
  }, [port])

  const executePaste = useCallback((text: string) => {
    if (!port || !xtermRef.current) return

    const lines = text.split('\n')
    const xterm = xtermRef.current

    // For single line, just add to buffer
    if (lines.length === 1) {
      inputBufferRef.current += text
      xterm.write(text)
      return
    }

    // For multi-line, execute each line
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i]
      if (i === lines.length - 1 && line === '') continue // Skip trailing empty line

      inputBufferRef.current = line
      xterm.write(line)

      if (i < lines.length - 1) {
        xterm.write('\r\n')
        if (line.trim()) {
          appendInput(port, line)
          execute(port, line)
        }
        inputBufferRef.current = ''
      }
    }
  }, [port, execute, appendInput])

  const confirmPaste = useCallback(() => {
    executePaste(pasteContent)
    setShowPasteModal(false)
    setPasteContent('')
  }, [pasteContent, executePaste])

  // Clear current line and replace with text
  const replaceCurrentLine = useCallback((newText: string) => {
    if (!xtermRef.current) return

    const xterm = xtermRef.current
    const currentLen = inputBufferRef.current.length

    // Clear current input
    if (currentLen > 0) {
      xterm.write('\b \b'.repeat(currentLen))
    }

    // Write new text
    inputBufferRef.current = newText
    xterm.write(newText)
  }, [])

  // Handle keyboard shortcuts
  useEffect(() => {
    if (!xtermRef.current) return

    const xterm = xtermRef.current

    // Custom key event handler for shortcuts
    xterm.attachCustomKeyEventHandler((event) => {
      if (!port) return true

      // Ctrl+L - Clear terminal
      if (event.ctrlKey && event.key === 'l') {
        event.preventDefault()
        handleClear()
        return false
      }

      // Ctrl+R - Soft reset (without shift) or Hard reset (with shift)
      if (event.ctrlKey && event.key === 'r') {
        event.preventDefault()
        if (event.shiftKey) {
          handleHardReset()
        } else {
          handleReset()
        }
        return false
      }

      // Ctrl+S - Save logs
      if (event.ctrlKey && event.key === 's') {
        event.preventDefault()
        handleSaveLogs()
        return false
      }

      // Ctrl+D - Disconnect
      if (event.ctrlKey && event.key === 'd') {
        event.preventDefault()
        handleDisconnect()
        return false
      }

      // Ctrl+V - Paste
      if (event.ctrlKey && event.key === 'v') {
        event.preventDefault()
        handlePaste()
        return false
      }

      // Escape - Cancel input
      if (event.key === 'Escape') {
        event.preventDefault()
        replaceCurrentLine('')
        return false
      }

      // Up arrow - History up (without ctrl)
      if (event.key === 'ArrowUp' && !event.ctrlKey) {
        event.preventDefault()
        // Save current input on first up press
        if (savedInputRef.current === '' && inputBufferRef.current) {
          savedInputRef.current = inputBufferRef.current
        }
        const histCmd = navigateHistory(port, 'up')
        if (histCmd !== null) {
          replaceCurrentLine(histCmd)
        }
        return false
      }

      // Down arrow - History down (without ctrl)
      if (event.key === 'ArrowDown' && !event.ctrlKey) {
        event.preventDefault()
        const histCmd = navigateHistory(port, 'down')
        if (histCmd !== null) {
          replaceCurrentLine(histCmd)
        } else {
          // Restore saved input
          replaceCurrentLine(savedInputRef.current)
          savedInputRef.current = ''
        }
        return false
      }

      // Ctrl+Up - Scroll up
      if (event.ctrlKey && event.key === 'ArrowUp') {
        event.preventDefault()
        xterm.scrollLines(-3)
        return false
      }

      // Ctrl+Down - Scroll down
      if (event.ctrlKey && event.key === 'ArrowDown') {
        event.preventDefault()
        xterm.scrollLines(3)
        return false
      }

      // Ctrl+End - Jump to bottom
      if (event.ctrlKey && event.key === 'End') {
        event.preventDefault()
        xterm.scrollToBottom()
        if (port) setHasNewOutput(port, false)
        return false
      }

      return true // Allow default handling
    })

    return () => {
      // Note: attachCustomKeyEventHandler doesn't return a disposable
    }
  }, [port, navigateHistory, handlePaste, replaceCurrentLine, setHasNewOutput])

  // Handle input based on port
  useEffect(() => {
    if (!xtermRef.current) return

    const xterm = xtermRef.current

    const dataHandler = xterm.onData((data) => {
      if (!port) return

      if (inputMode === 'raw') {
        sendInput(port, data)
        return
      }

      // Line mode
      for (const char of data) {
        if (char === '\r' || char === '\n') {
          // Execute command
          const command = inputBufferRef.current
          inputBufferRef.current = ''
          savedInputRef.current = '' // Clear saved input
          xterm.write('\r\n')

          if (command.trim()) {
            appendInput(port, command)
            execute(port, command)
          }
        } else if (char === '\x7f' || char === '\b') {
          // Backspace
          if (inputBufferRef.current.length > 0) {
            inputBufferRef.current = inputBufferRef.current.slice(0, -1)
            xterm.write('\b \b')
          }
        } else if (char === '\x03') {
          // Ctrl+C
          interruptDevice(port)
          inputBufferRef.current = ''
        } else if (char >= ' ' || char === '\t') {
          // Regular printable character or tab
          inputBufferRef.current += char
          xterm.write(char)
        }
      }
    })

    return () => {
      dataHandler.dispose()
    }
  }, [port, inputMode, sendInput, execute, interruptDevice, appendInput])

  // Subscribe to device output via WebSocket
  useEffect(() => {
    if (port) {
      subscribe(port)
      startSession(port)

      // Show connection message
      if (xtermRef.current && lastPortRef.current !== port) {
        xtermRef.current.writeln(`\r\n\x1b[1;32mConnected to ${port}\x1b[0m\r\n`)
        appendSystemMessage(port, `Connected to ${port}`)
        lastPortRef.current = port
      }
    }
  }, [port, subscribe, startSession, appendSystemMessage])

  // Subscribe directly to console store for output updates
  useEffect(() => {
    if (!port) return

    // Subscribe to store changes - check pending output on every state change
    const unsubscribe = useConsoleStore.subscribe((state) => {
      const pending = state.pendingOutput.get(port)
      if (pending && xtermRef.current) {
        // Get and clear pending output
        const text = useConsoleStore.getState().getPendingOutput(port)
        if (text) {
          console.log('[Terminal] Writing output:', text.substring(0, 50))
          xtermRef.current.write(text)

          // Auto-scroll if not locked
          if (!isScrollLocked) {
            xtermRef.current.scrollToBottom()
          }
        }
      }
    })

    return () => {
      unsubscribe()
    }
  }, [port, isScrollLocked])

  const handleClear = useCallback(() => {
    if (xtermRef.current) {
      xtermRef.current.clear()
      xtermRef.current.writeln('\x1b[1;34m=== Terminal Cleared ===\x1b[0m\r\n')
    }
    if (port) {
      clearOutput(port)
      appendSystemMessage(port, 'Terminal cleared')
    }
  }, [port, clearOutput, appendSystemMessage])

  const handleInterrupt = useCallback(async () => {
    if (port) {
      await interruptDevice(port)
      appendSystemMessage(port, 'Interrupted')
    }
  }, [port, interruptDevice, appendSystemMessage])

  const handleReset = useCallback(async () => {
    if (port) {
      if (xtermRef.current) {
        xtermRef.current.writeln('\r\n\x1b[1;33mSending soft reset...\x1b[0m')
      }
      appendSystemMessage(port, 'Soft reset')
      await api.reset(port, true)
    }
  }, [port, appendSystemMessage])

  const handleHardReset = useCallback(async () => {
    if (port) {
      if (xtermRef.current) {
        xtermRef.current.writeln('\r\n\x1b[1;31mSending hard reset...\x1b[0m')
      }
      appendSystemMessage(port, 'Hard reset')
      await api.reset(port, false)
    }
  }, [port, appendSystemMessage])

  const handleDisconnect = useCallback(async () => {
    if (port) {
      if (xtermRef.current) {
        xtermRef.current.writeln('\r\n\x1b[1;33mDisconnecting...\x1b[0m')
      }
      appendSystemMessage(port, 'Disconnected')
      await disconnect(port)
    }
  }, [port, disconnect, appendSystemMessage])

  const handleSaveLogs = useCallback(() => {
    if (!port) return

    const logs = exportLogs(port)
    const blob = new Blob([JSON.stringify(logs, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${port.replace(/[^a-zA-Z0-9]/g, '_')}_${new Date().toISOString().split('T')[0]}.json`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)

    if (xtermRef.current) {
      xtermRef.current.writeln('\r\n\x1b[1;32mLogs saved to file\x1b[0m')
    }
    appendSystemMessage(port, 'Logs exported')
  }, [port, exportLogs, appendSystemMessage])

  const handleRunCode = useCallback(async () => {
    if (!port) return

    // Example: run current input buffer
    const code = inputBufferRef.current.trim()
    if (code) {
      inputBufferRef.current = ''
      appendInput(port, code)
      await execute(port, code)
    }
  }, [port, execute, appendInput])

  const toggleScrollLock = useCallback(() => {
    if (port) {
      setScrollLock(port, !isScrollLocked)
      if (isScrollLocked && xtermRef.current) {
        // When unlocking, scroll to bottom
        xtermRef.current.scrollToBottom()
        setHasNewOutput(port, false)
      }
    }
  }, [port, isScrollLocked, setScrollLock, setHasNewOutput])

  const scrollToBottom = useCallback(() => {
    if (xtermRef.current) {
      xtermRef.current.scrollToBottom()
    }
    if (port) {
      setHasNewOutput(port, false)
    }
  }, [port, setHasNewOutput])

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="flex items-center justify-between px-3 py-1 border-b border-vscode-border">
        <div className="flex items-center gap-2">
          <span className="text-xs uppercase tracking-wider text-vscode-text-dim">
            Terminal
          </span>
          {port && (
            <span className="text-xs text-vscode-accent">{port}</span>
          )}
        </div>

        <div className="flex items-center gap-1">
          <Tooltip content="Run (Enter)">
            <Button icon size="sm" variant="ghost" onClick={handleRunCode} disabled={!port}>
              <Play size={14} />
            </Button>
          </Tooltip>

          <Tooltip content="Interrupt (Ctrl+C)">
            <Button icon size="sm" variant="ghost" onClick={handleInterrupt} disabled={!port}>
              <Square size={14} />
            </Button>
          </Tooltip>

          <Tooltip content="Soft Reset (Ctrl+R)">
            <Button icon size="sm" variant="ghost" onClick={handleReset} disabled={!port}>
              <RotateCcw size={14} />
            </Button>
          </Tooltip>

          <Tooltip content="Disconnect (Ctrl+D)">
            <Button icon size="sm" variant="ghost" onClick={handleDisconnect} disabled={!port}>
              <Power size={14} />
            </Button>
          </Tooltip>

          <div className="w-px h-4 bg-vscode-border mx-1" />

          <Tooltip content={isScrollLocked ? "Scroll Lock ON - Click to unlock" : "Scroll Lock OFF - Click to lock"}>
            <Button
              icon
              size="sm"
              variant={isScrollLocked ? "default" : "ghost"}
              onClick={toggleScrollLock}
              className={isScrollLocked ? "text-yellow-400" : ""}
            >
              {isScrollLocked ? <Lock size={14} /> : <Unlock size={14} />}
            </Button>
          </Tooltip>

          {hasNew && (
            <Tooltip content="New output - Click to scroll down">
              <Button icon size="sm" variant="ghost" onClick={scrollToBottom} className="text-green-400 animate-pulse">
                <ChevronDown size={14} />
              </Button>
            </Tooltip>
          )}

          <div className="w-px h-4 bg-vscode-border mx-1" />

          <Tooltip content="Save Logs (Ctrl+S)">
            <Button icon size="sm" variant="ghost" onClick={handleSaveLogs} disabled={!port}>
              <Download size={14} />
            </Button>
          </Tooltip>

          <Tooltip content="Clear (Ctrl+L)">
            <Button icon size="sm" variant="ghost" onClick={handleClear}>
              <Trash2 size={14} />
            </Button>
          </Tooltip>
        </div>
      </div>

      {/* Terminal - always rendered */}
      <div className="flex-1 overflow-hidden">
        <div ref={terminalRef} className="h-full" />
      </div>

      {/* Paste confirmation modal */}
      <Modal
        isOpen={showPasteModal}
        onClose={() => setShowPasteModal(false)}
        title="Paste Multi-line Content"
      >
        <div className="space-y-4">
          <p className="text-sm text-vscode-text-dim">
            You're about to paste {pasteContent.split('\n').length} lines. Each line will be executed as a separate command.
          </p>
          <pre className="p-2 bg-vscode-bg rounded text-xs max-h-48 overflow-auto">
            {pasteContent.split('\n').slice(0, 10).join('\n')}
            {pasteContent.split('\n').length > 10 && '\n...'}
          </pre>
          <div className="flex justify-end gap-2">
            <Button variant="ghost" onClick={() => setShowPasteModal(false)}>
              Cancel
            </Button>
            <Button onClick={confirmPaste}>
              Paste & Execute
            </Button>
          </div>
        </div>
      </Modal>
    </div>
  )
}
