import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { TERMINAL_CONFIG } from '../config/terminal'

type Panel = 'editor' | 'files' | 'info' | 'sync'
type ToolPanel = 'flasher' | 'wifi' | 'library' | null

interface SettingsState {
  // UI state
  activePanel: Panel
  activeToolPanel: ToolPanel
  sidebarWidth: number
  terminalHeight: number

  // Editor settings
  fontSize: number
  tabSize: number
  wordWrap: boolean
  minimap: boolean

  // Terminal settings
  terminalFontSize: number
  terminalLineHeight: number

  // Device settings
  defaultBaudrate: number
  autoConnect: boolean

  // Actions
  setActivePanel: (panel: Panel) => void
  setActiveToolPanel: (panel: ToolPanel) => void
  setSidebarWidth: (width: number) => void
  setTerminalHeight: (height: number) => void
  setFontSize: (size: number) => void
  setTabSize: (size: number) => void
  setWordWrap: (enabled: boolean) => void
  setMinimap: (enabled: boolean) => void
  setTerminalFontSize: (size: number) => void
  setTerminalLineHeight: (height: number) => void
  setDefaultBaudrate: (baudrate: number) => void
  setAutoConnect: (enabled: boolean) => void
}

export const useSettingsStore = create<SettingsState>()(
  persist(
    (set) => ({
      // Initial values
      activePanel: 'editor',
      activeToolPanel: null,
      sidebarWidth: 250,
      terminalHeight: 250,
      fontSize: 14,
      tabSize: 4,
      wordWrap: true,
      minimap: false,
      terminalFontSize: TERMINAL_CONFIG.fontSize,
      terminalLineHeight: TERMINAL_CONFIG.lineHeight,
      defaultBaudrate: 115200,
      autoConnect: false,

      // Actions
      setActivePanel: (panel) => set({ activePanel: panel }),
      setActiveToolPanel: (panel) => set({ activeToolPanel: panel }),
      setSidebarWidth: (width) => set({ sidebarWidth: Math.max(150, Math.min(400, width)) }),
      setTerminalHeight: (height) => set({ terminalHeight: Math.max(100, Math.min(500, height)) }),
      setFontSize: (size) => set({ fontSize: Math.max(10, Math.min(24, size)) }),
      setTabSize: (size) => set({ tabSize: Math.max(2, Math.min(8, size)) }),
      setWordWrap: (enabled) => set({ wordWrap: enabled }),
      setMinimap: (enabled) => set({ minimap: enabled }),
      setTerminalFontSize: (size) => set({ terminalFontSize: Math.max(10, Math.min(24, size)) }),
      setTerminalLineHeight: (height) => set({ terminalLineHeight: Math.max(1.0, Math.min(2.0, height)) }),
      setDefaultBaudrate: (baudrate) => set({ defaultBaudrate: baudrate }),
      setAutoConnect: (enabled) => set({ autoConnect: enabled }),
    }),
    {
      name: 'thonnyv2-settings',
    }
  )
)
