/**
 * Shared terminal configuration for consistent styling across all terminal components.
 */

export const TERMINAL_CONFIG = {
  /** Font family for terminal text */
  fontFamily: 'Consolas, Menlo, Monaco, "Courier New", monospace',

  /** Default font size in pixels */
  fontSize: 13,

  /** Line height multiplier (improved from 1.2 for better readability) */
  lineHeight: 1.4,

  /** Terminal theme colors (VS Code dark theme) */
  theme: {
    background: '#1e1e1e',
    foreground: '#cccccc',
    cursor: '#cccccc',
    cursorAccent: '#1e1e1e',
    selectionBackground: '#264f78',
    black: '#000000',
    red: '#f14c4c',
    green: '#4ec9b0',
    yellow: '#dcdcaa',
    blue: '#3794ff',
    magenta: '#c586c0',
    cyan: '#4ec9b0',
    white: '#cccccc',
    brightBlack: '#858585',
    brightRed: '#f14c4c',
    brightGreen: '#4ec9b0',
    brightYellow: '#dcdcaa',
    brightBlue: '#3794ff',
    brightMagenta: '#c586c0',
    brightCyan: '#4ec9b0',
    brightWhite: '#ffffff',
  },
} as const

export type TerminalConfig = typeof TERMINAL_CONFIG
