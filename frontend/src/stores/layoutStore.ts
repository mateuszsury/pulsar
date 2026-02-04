import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export type SplitMode = 'single' | 'horizontal' | 'vertical' | 'grid'

export interface PaneConfig {
  id: string
  devicePort: string | null
  position: number // 0-3 for grid positions
}

interface LayoutState {
  // Multi-terminal layout
  panes: PaneConfig[]
  splitMode: SplitMode
  linkedScroll: boolean
  activePaneId: string | null

  // Actions
  setSplitMode: (mode: SplitMode) => void
  assignDevice: (paneId: string, port: string | null) => void
  setActivePane: (paneId: string | null) => void
  setLinkedScroll: (linked: boolean) => void
  swapPanes: (paneId1: string, paneId2: string) => void
  getPaneCount: () => number
  getPane: (paneId: string) => PaneConfig | undefined
  getPaneByPort: (port: string) => PaneConfig | undefined
}

// Generate default panes
function generateDefaultPanes(): PaneConfig[] {
  return [
    { id: 'pane-0', devicePort: null, position: 0 },
    { id: 'pane-1', devicePort: null, position: 1 },
    { id: 'pane-2', devicePort: null, position: 2 },
    { id: 'pane-3', devicePort: null, position: 3 },
  ]
}

export const useLayoutStore = create<LayoutState>()(
  persist(
    (set, get) => ({
      panes: generateDefaultPanes(),
      splitMode: 'single',
      linkedScroll: false,
      activePaneId: 'pane-0',

      setSplitMode: (mode) => {
        set({ splitMode: mode })
        // Ensure we have enough panes
        const currentPanes = get().panes
        if (currentPanes.length < 4) {
          set({ panes: generateDefaultPanes() })
        }
      },

      assignDevice: (paneId, port) => {
        set(state => {
          const panes = state.panes.map(pane => {
            if (pane.id === paneId) {
              return { ...pane, devicePort: port }
            }
            // Remove from other panes if assigning (device can only be in one pane)
            if (port && pane.devicePort === port) {
              return { ...pane, devicePort: null }
            }
            return pane
          })
          return { panes }
        })
      },

      setActivePane: (paneId) => {
        set({ activePaneId: paneId })
      },

      setLinkedScroll: (linked) => {
        set({ linkedScroll: linked })
      },

      swapPanes: (paneId1, paneId2) => {
        set(state => {
          const panes = [...state.panes]
          const idx1 = panes.findIndex(p => p.id === paneId1)
          const idx2 = panes.findIndex(p => p.id === paneId2)

          if (idx1 !== -1 && idx2 !== -1) {
            const port1 = panes[idx1].devicePort
            const port2 = panes[idx2].devicePort
            panes[idx1] = { ...panes[idx1], devicePort: port2 }
            panes[idx2] = { ...panes[idx2], devicePort: port1 }
          }

          return { panes }
        })
      },

      getPaneCount: () => {
        const mode = get().splitMode
        switch (mode) {
          case 'single': return 1
          case 'horizontal': return 2
          case 'vertical': return 2
          case 'grid': return 4
          default: return 1
        }
      },

      getPane: (paneId) => {
        return get().panes.find(p => p.id === paneId)
      },

      getPaneByPort: (port) => {
        return get().panes.find(p => p.devicePort === port)
      },
    }),
    {
      name: 'thonnyv2-layout',
    }
  )
)

// Selector for visible panes based on split mode
export const selectVisiblePanes = (state: LayoutState): PaneConfig[] => {
  const count = state.splitMode === 'single' ? 1 :
                state.splitMode === 'horizontal' ? 2 :
                state.splitMode === 'vertical' ? 2 : 4
  return state.panes.slice(0, count)
}
