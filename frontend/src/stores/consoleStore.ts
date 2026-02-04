import { create } from 'zustand'
import { api, REPLResult } from '../services/api'

export interface LogEntry {
  timestamp: string
  type: 'output' | 'input' | 'system'
  text: string
}

interface ConsoleState {
  // Raw output buffer per device (single string for efficient terminal writing)
  outputs: Map<string, string>

  // New output that hasn't been displayed yet
  pendingOutput: Map<string, string>

  // Log entries with timestamps for export
  logEntries: Map<string, LogEntry[]>

  // Session start times per device
  sessionStart: Map<string, string>

  // Current command history per device
  history: Map<string, string[]>
  historyIndex: Map<string, number>

  // Scroll lock state per device
  scrollLock: Map<string, boolean>
  hasNewOutput: Map<string, boolean>

  // Execution state
  executing: Map<string, boolean>

  // Current input buffer per device (for history navigation)
  currentInput: Map<string, string>

  // Actions
  appendOutput: (port: string, text: string) => void
  appendInput: (port: string, text: string) => void
  appendSystemMessage: (port: string, text: string) => void
  getPendingOutput: (port: string) => string
  clearOutput: (port: string) => void
  execute: (port: string, code: string) => Promise<REPLResult | null>
  interrupt: (port: string) => Promise<void>
  addToHistory: (port: string, command: string) => void
  navigateHistory: (port: string, direction: 'up' | 'down') => string | null
  searchHistory: (port: string, query: string) => string[]
  setScrollLock: (port: string, locked: boolean) => void
  getScrollLock: (port: string) => boolean
  setHasNewOutput: (port: string, hasNew: boolean) => void
  setCurrentInput: (port: string, input: string) => void
  getCurrentInput: (port: string) => string
  getLogEntries: (port: string) => LogEntry[]
  exportLogs: (port: string) => { device: string; session_start: string; session_end: string; entries: LogEntry[] }
  startSession: (port: string) => void
}

const MAX_OUTPUT_SIZE = 500000 // 500KB max output
const MAX_HISTORY = 100
const MAX_LOG_ENTRIES = 10000

export const useConsoleStore = create<ConsoleState>((set, get) => ({
  outputs: new Map(),
  pendingOutput: new Map(),
  logEntries: new Map(),
  sessionStart: new Map(),
  history: new Map(),
  historyIndex: new Map(),
  scrollLock: new Map(),
  hasNewOutput: new Map(),
  executing: new Map(),
  currentInput: new Map(),

  appendOutput: (port, text) => {
    set(state => {
      const outputs = new Map(state.outputs)
      const pendingOutput = new Map(state.pendingOutput)
      const logEntries = new Map(state.logEntries)
      const hasNewOutput = new Map(state.hasNewOutput)

      // Append to full output buffer
      let current = outputs.get(port) ?? ''
      current += text

      // Limit output size
      if (current.length > MAX_OUTPUT_SIZE) {
        current = current.slice(-MAX_OUTPUT_SIZE)
      }

      outputs.set(port, current)

      // Also add to pending output for terminal display
      const pending = (pendingOutput.get(port) ?? '') + text
      pendingOutput.set(port, pending)

      // Add to log entries
      const entries = logEntries.get(port) ?? []
      entries.push({
        timestamp: new Date().toISOString(),
        type: 'output',
        text,
      })
      // Limit log entries
      if (entries.length > MAX_LOG_ENTRIES) {
        entries.splice(0, entries.length - MAX_LOG_ENTRIES)
      }
      logEntries.set(port, entries)

      // Mark new output if scroll locked
      if (state.scrollLock.get(port)) {
        hasNewOutput.set(port, true)
      }

      return { outputs, pendingOutput, logEntries, hasNewOutput }
    })
  },

  appendInput: (port, text) => {
    set(state => {
      const logEntries = new Map(state.logEntries)
      const entries = logEntries.get(port) ?? []
      entries.push({
        timestamp: new Date().toISOString(),
        type: 'input',
        text,
      })
      if (entries.length > MAX_LOG_ENTRIES) {
        entries.splice(0, entries.length - MAX_LOG_ENTRIES)
      }
      logEntries.set(port, entries)
      return { logEntries }
    })
  },

  appendSystemMessage: (port, text) => {
    set(state => {
      const logEntries = new Map(state.logEntries)
      const entries = logEntries.get(port) ?? []
      entries.push({
        timestamp: new Date().toISOString(),
        type: 'system',
        text,
      })
      if (entries.length > MAX_LOG_ENTRIES) {
        entries.splice(0, entries.length - MAX_LOG_ENTRIES)
      }
      logEntries.set(port, entries)
      return { logEntries }
    })
  },

  getPendingOutput: (port) => {
    const pending = get().pendingOutput.get(port) ?? ''
    // Clear pending after reading
    set(state => {
      const pendingOutput = new Map(state.pendingOutput)
      pendingOutput.set(port, '')
      return { pendingOutput }
    })
    return pending
  },

  clearOutput: (port) => {
    set(state => {
      const outputs = new Map(state.outputs)
      const pendingOutput = new Map(state.pendingOutput)
      outputs.set(port, '')
      pendingOutput.set(port, '')
      return { outputs, pendingOutput }
    })
  },

  execute: async (port, code) => {
    set(state => {
      const executing = new Map(state.executing)
      executing.set(port, true)
      return { executing }
    })

    try {
      // Add to history
      get().addToHistory(port, code)

      const result = await api.execute(port, code)

      if (result.data) {
        // Append output
        if (result.data.output) {
          get().appendOutput(port, result.data.output)
        }
        if (result.data.error) {
          get().appendOutput(port, `Error: ${result.data.error}`)
        }
        return result.data
      }

      if (result.error) {
        get().appendOutput(port, `Error: ${result.error}`)
      }

      return null
    } finally {
      set(state => {
        const executing = new Map(state.executing)
        executing.set(port, false)
        return { executing }
      })
    }
  },

  interrupt: async (port) => {
    await api.interrupt(port)
    get().appendOutput(port, '^C')
  },

  addToHistory: (port, command) => {
    if (!command.trim()) return

    set(state => {
      const history = new Map(state.history)
      const historyIndex = new Map(state.historyIndex)

      const current = history.get(port) ?? []

      // Don't add duplicate consecutive commands
      if (current[current.length - 1] !== command) {
        const newHistory = [...current, command]
        if (newHistory.length > MAX_HISTORY) {
          newHistory.shift()
        }
        history.set(port, newHistory)
      }

      // Reset index to end
      historyIndex.set(port, (history.get(port)?.length ?? 0))

      return { history, historyIndex }
    })
  },

  navigateHistory: (port, direction) => {
    const { history, historyIndex } = get()
    const portHistory = history.get(port) ?? []
    let index = historyIndex.get(port) ?? portHistory.length

    if (direction === 'up' && index > 0) {
      index--
    } else if (direction === 'down' && index < portHistory.length) {
      index++
    }

    set(state => {
      const newIndex = new Map(state.historyIndex)
      newIndex.set(port, index)
      return { historyIndex: newIndex }
    })

    return portHistory[index] ?? null
  },

  searchHistory: (port, query) => {
    const portHistory = get().history.get(port) ?? []
    if (!query) return portHistory.slice(-10)
    const lowerQuery = query.toLowerCase()
    return portHistory.filter(cmd =>
      cmd.toLowerCase().includes(lowerQuery)
    ).slice(-10)
  },

  setScrollLock: (port, locked) => {
    set(state => {
      const scrollLock = new Map(state.scrollLock)
      const hasNewOutput = new Map(state.hasNewOutput)
      scrollLock.set(port, locked)
      if (!locked) {
        hasNewOutput.set(port, false)
      }
      return { scrollLock, hasNewOutput }
    })
  },

  getScrollLock: (port) => {
    return get().scrollLock.get(port) ?? false
  },

  setHasNewOutput: (port, hasNew) => {
    set(state => {
      const hasNewOutput = new Map(state.hasNewOutput)
      hasNewOutput.set(port, hasNew)
      return { hasNewOutput }
    })
  },

  setCurrentInput: (port, input) => {
    set(state => {
      const currentInput = new Map(state.currentInput)
      currentInput.set(port, input)
      return { currentInput }
    })
  },

  getCurrentInput: (port) => {
    return get().currentInput.get(port) ?? ''
  },

  getLogEntries: (port) => {
    return get().logEntries.get(port) ?? []
  },

  exportLogs: (port) => {
    const entries = get().logEntries.get(port) ?? []
    const sessionStart = get().sessionStart.get(port) ?? new Date().toISOString()
    return {
      device: port,
      session_start: sessionStart,
      session_end: new Date().toISOString(),
      entries,
    }
  },

  startSession: (port) => {
    set(state => {
      const sessionStart = new Map(state.sessionStart)
      const logEntries = new Map(state.logEntries)
      sessionStart.set(port, new Date().toISOString())
      logEntries.set(port, [])
      return { sessionStart, logEntries }
    })
  },
}))
