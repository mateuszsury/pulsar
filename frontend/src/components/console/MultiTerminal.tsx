import { useCallback, useRef } from 'react'
import { Columns2, Rows2, Grid2x2, Square, Link, Unlink } from 'lucide-react'
import { Button } from '../common/Button'
import { Tooltip } from '../common/Tooltip'
import { Terminal } from './Terminal'
import { TerminalPane } from './TerminalPane'
import { useLayoutStore, selectVisiblePanes, SplitMode } from '../../stores/layoutStore'
import { useDeviceStore } from '../../stores/deviceStore'

export function MultiTerminal() {
  const splitMode = useLayoutStore(state => state.splitMode)
  const setSplitMode = useLayoutStore(state => state.setSplitMode)
  const linkedScroll = useLayoutStore(state => state.linkedScroll)
  const setLinkedScroll = useLayoutStore(state => state.setLinkedScroll)
  const activePaneId = useLayoutStore(state => state.activePaneId)
  const setActivePane = useLayoutStore(state => state.setActivePane)
  const assignDevice = useLayoutStore(state => state.assignDevice)
  const visiblePanes = useLayoutStore(selectVisiblePanes)

  const devices = useDeviceStore(state => state.devices)
  const connectedDevices = devices.filter(d => d.state === 'connected')

  // Refs for linked scrolling
  const paneRefs = useRef<Map<string, (lines: number) => void>>(new Map())

  const handleLinkedScroll = useCallback((sourcePaneId: string, lines: number) => {
    if (!linkedScroll) return

    paneRefs.current.forEach((scrollFn, paneId) => {
      if (paneId !== sourcePaneId) {
        scrollFn(lines)
      }
    })
  }, [linkedScroll])

  // Handle drag and drop
  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.dataTransfer.dropEffect = 'move'
  }, [])

  const handleDrop = useCallback((e: React.DragEvent, paneId: string) => {
    e.preventDefault()
    const port = e.dataTransfer.getData('text/plain')
    if (port) {
      assignDevice(paneId, port)
    }
  }, [assignDevice])

  // Single terminal mode - use the original Terminal component
  if (splitMode === 'single') {
    return (
      <div className="flex flex-col h-full">
        <div className="flex items-center justify-between px-3 py-1 border-b border-vscode-border bg-vscode-sidebar">
          <span className="text-xs uppercase tracking-wider text-vscode-text-dim">
            Terminal
          </span>
          <LayoutControls
            splitMode={splitMode}
            setSplitMode={setSplitMode}
            linkedScroll={linkedScroll}
            setLinkedScroll={setLinkedScroll}
          />
        </div>
        <div className="flex-1 overflow-hidden">
          <Terminal />
        </div>
      </div>
    )
  }

  // Multi-terminal mode
  const gridClasses = {
    horizontal: 'grid grid-cols-2 gap-1',
    vertical: 'grid grid-rows-2 gap-1',
    grid: 'grid grid-cols-2 grid-rows-2 gap-1',
  }

  return (
    <div className="flex flex-col h-full">
      {/* Header with layout controls */}
      <div className="flex items-center justify-between px-3 py-1 border-b border-vscode-border bg-vscode-sidebar">
        <div className="flex items-center gap-2">
          <span className="text-xs uppercase tracking-wider text-vscode-text-dim">
            Multi-Terminal
          </span>
          <span className="text-xs text-vscode-accent">
            {visiblePanes.filter(p => p.devicePort).length}/{visiblePanes.length} assigned
          </span>
        </div>

        <div className="flex items-center gap-2">
          {/* Device assignment dropdown */}
          {connectedDevices.length > 0 && (
            <select
              className="text-xs bg-vscode-input border border-vscode-border rounded px-1 py-0.5"
              value=""
              onChange={(e) => {
                if (e.target.value && activePaneId) {
                  assignDevice(activePaneId, e.target.value)
                }
              }}
            >
              <option value="">Assign device...</option>
              {connectedDevices.map(d => (
                <option key={d.port} value={d.port}>
                  {d.port}
                </option>
              ))}
            </select>
          )}

          <LayoutControls
            splitMode={splitMode}
            setSplitMode={setSplitMode}
            linkedScroll={linkedScroll}
            setLinkedScroll={setLinkedScroll}
          />
        </div>
      </div>

      {/* Terminal grid */}
      <div className={`flex-1 p-1 ${gridClasses[splitMode as keyof typeof gridClasses]}`}>
        {visiblePanes.map((pane) => (
          <div
            key={pane.id}
            className="min-h-0"
            onDragOver={handleDragOver}
            onDrop={(e) => handleDrop(e, pane.id)}
          >
            <TerminalPane
              pane={pane}
              isActive={pane.id === activePaneId}
              onActivate={() => setActivePane(pane.id)}
              linkedScroll={linkedScroll}
              onScroll={(lines) => handleLinkedScroll(pane.id, lines)}
            />
          </div>
        ))}
      </div>
    </div>
  )
}

// Layout controls component
interface LayoutControlsProps {
  splitMode: SplitMode
  setSplitMode: (mode: SplitMode) => void
  linkedScroll: boolean
  setLinkedScroll: (linked: boolean) => void
}

function LayoutControls({ splitMode, setSplitMode, linkedScroll, setLinkedScroll }: LayoutControlsProps) {
  return (
    <div className="flex items-center gap-1">
      <div className="w-px h-4 bg-vscode-border mx-1" />

      <Tooltip content="Single terminal">
        <Button
          icon
          size="sm"
          variant={splitMode === 'single' ? 'default' : 'ghost'}
          onClick={() => setSplitMode('single')}
        >
          <Square size={14} />
        </Button>
      </Tooltip>

      <Tooltip content="Split horizontal (2 side by side)">
        <Button
          icon
          size="sm"
          variant={splitMode === 'horizontal' ? 'default' : 'ghost'}
          onClick={() => setSplitMode('horizontal')}
        >
          <Columns2 size={14} />
        </Button>
      </Tooltip>

      <Tooltip content="Split vertical (2 stacked)">
        <Button
          icon
          size="sm"
          variant={splitMode === 'vertical' ? 'default' : 'ghost'}
          onClick={() => setSplitMode('vertical')}
        >
          <Rows2 size={14} />
        </Button>
      </Tooltip>

      <Tooltip content="Grid (2x2)">
        <Button
          icon
          size="sm"
          variant={splitMode === 'grid' ? 'default' : 'ghost'}
          onClick={() => setSplitMode('grid')}
        >
          <Grid2x2 size={14} />
        </Button>
      </Tooltip>

      {splitMode !== 'single' && (
        <>
          <div className="w-px h-4 bg-vscode-border mx-1" />
          <Tooltip content={linkedScroll ? "Disable linked scroll" : "Enable linked scroll"}>
            <Button
              icon
              size="sm"
              variant={linkedScroll ? 'default' : 'ghost'}
              onClick={() => setLinkedScroll(!linkedScroll)}
            >
              {linkedScroll ? <Link size={14} /> : <Unlink size={14} />}
            </Button>
          </Tooltip>
        </>
      )}
    </div>
  )
}
