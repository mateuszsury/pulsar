import { useCallback, useMemo } from 'react'

export interface KeyboardShortcut {
  key: string
  ctrl?: boolean
  shift?: boolean
  alt?: boolean
  description: string
  action: string
}

export const DEFAULT_SHORTCUTS: KeyboardShortcut[] = [
  { key: 'c', ctrl: true, description: 'Interrupt execution', action: 'interrupt' },
  { key: 'd', ctrl: true, description: 'Soft EOF / disconnect', action: 'disconnect' },
  { key: 'l', ctrl: true, description: 'Clear terminal', action: 'clear' },
  { key: 'r', ctrl: true, description: 'Soft reset device', action: 'softReset' },
  { key: 'r', ctrl: true, shift: true, description: 'Hard reset device', action: 'hardReset' },
  { key: 's', ctrl: true, description: 'Save logs to file', action: 'saveLogs' },
  { key: 'v', ctrl: true, description: 'Paste from clipboard', action: 'paste' },
  { key: 'ArrowUp', description: 'Previous command in history', action: 'historyUp' },
  { key: 'ArrowDown', description: 'Next command in history', action: 'historyDown' },
  { key: 'ArrowUp', ctrl: true, description: 'Scroll terminal up', action: 'scrollUp' },
  { key: 'ArrowDown', ctrl: true, description: 'Scroll terminal down', action: 'scrollDown' },
  { key: 'End', ctrl: true, description: 'Jump to bottom', action: 'scrollToBottom' },
  { key: 'Escape', description: 'Cancel current input', action: 'cancelInput' },
  { key: 'r', ctrl: true, alt: true, description: 'Search command history', action: 'searchHistory' },
]

export interface ShortcutHandlers {
  interrupt?: () => void
  disconnect?: () => void
  clear?: () => void
  softReset?: () => void
  hardReset?: () => void
  saveLogs?: () => void
  paste?: () => void
  historyUp?: () => void
  historyDown?: () => void
  scrollUp?: () => void
  scrollDown?: () => void
  scrollToBottom?: () => void
  cancelInput?: () => void
  searchHistory?: () => void
}

export function matchesShortcut(
  event: KeyboardEvent,
  shortcut: KeyboardShortcut
): boolean {
  const keyMatches = event.key === shortcut.key ||
    event.key.toLowerCase() === shortcut.key.toLowerCase()

  const ctrlMatches = !!shortcut.ctrl === (event.ctrlKey || event.metaKey)
  const shiftMatches = !!shortcut.shift === event.shiftKey
  const altMatches = !!shortcut.alt === event.altKey

  return keyMatches && ctrlMatches && shiftMatches && altMatches
}

export function useKeyboardShortcuts(
  handlers: ShortcutHandlers,
  shortcuts: KeyboardShortcut[] = DEFAULT_SHORTCUTS
) {
  const shortcutMap = useMemo(() => {
    const map = new Map<string, KeyboardShortcut>()
    for (const shortcut of shortcuts) {
      const key = `${shortcut.ctrl ? 'ctrl+' : ''}${shortcut.shift ? 'shift+' : ''}${shortcut.alt ? 'alt+' : ''}${shortcut.key}`
      map.set(key, shortcut)
    }
    return map
  }, [shortcuts])

  const handleKeyEvent = useCallback((event: KeyboardEvent): boolean => {
    // Find matching shortcut
    for (const shortcut of shortcuts) {
      if (matchesShortcut(event, shortcut)) {
        const handler = handlers[shortcut.action as keyof ShortcutHandlers]
        if (handler) {
          handler()
          return true // Handled
        }
      }
    }
    return false // Not handled
  }, [handlers, shortcuts])

  // For xterm.js attachCustomKeyEventHandler
  // Return false to prevent default behavior, true to allow it
  const xtermKeyHandler = useCallback((event: KeyboardEvent): boolean => {
    // Check if this is one of our shortcuts
    for (const shortcut of shortcuts) {
      if (matchesShortcut(event, shortcut)) {
        const handler = handlers[shortcut.action as keyof ShortcutHandlers]
        if (handler) {
          handler()
          return false // Prevent default xterm handling
        }
      }
    }
    return true // Allow default xterm handling
  }, [handlers, shortcuts])

  return {
    handleKeyEvent,
    xtermKeyHandler,
    shortcuts,
    shortcutMap,
  }
}

// Helper to format shortcut for display
export function formatShortcut(shortcut: KeyboardShortcut): string {
  const parts: string[] = []
  if (shortcut.ctrl) parts.push('Ctrl')
  if (shortcut.shift) parts.push('Shift')
  if (shortcut.alt) parts.push('Alt')

  let key = shortcut.key
  if (key === 'ArrowUp') key = '↑'
  else if (key === 'ArrowDown') key = '↓'
  else if (key === 'Escape') key = 'Esc'
  else key = key.toUpperCase()

  parts.push(key)
  return parts.join('+')
}
