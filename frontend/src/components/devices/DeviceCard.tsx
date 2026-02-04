import { Cpu, PowerOff, RotateCcw, Square } from 'lucide-react'
import { Button } from '../common/Button'
import { Tooltip } from '../common/Tooltip'
import { DeviceInfo } from '../../services/api'
import { api } from '../../services/api'

interface DeviceCardProps {
  device: DeviceInfo
  isSelected: boolean
  onSelect: () => void
  onDisconnect: () => void
}

export function DeviceCard({ device, isSelected, onSelect, onDisconnect }: DeviceCardProps) {
  const stateColors = {
    connected: 'bg-vscode-success',
    connecting: 'bg-vscode-warning animate-pulse',
    disconnected: 'bg-vscode-text-dim',
    busy: 'bg-vscode-warning animate-pulse',
    error: 'bg-vscode-error',
  }

  const handleReset = async (e: React.MouseEvent) => {
    e.stopPropagation()
    await api.reset(device.port, true)
  }

  const handleInterrupt = async (e: React.MouseEvent) => {
    e.stopPropagation()
    await api.interrupt(device.port)
  }

  return (
    <div
      className={`rounded p-2 cursor-pointer transition-colors ${
        isSelected ? 'bg-vscode-selection' : 'hover:bg-vscode-hover'
      }`}
      onClick={onSelect}
    >
      <div className="flex items-center gap-2">
        <div className={`w-2 h-2 rounded-full ${stateColors[device.state]}`} />
        <Cpu size={14} className="text-vscode-accent" />
        <span className="flex-1 font-medium truncate">{device.port}</span>
      </div>

      <div className="mt-1 ml-4 text-xs text-vscode-text-dim">
        {device.machine || device.platform || 'MicroPython'}
      </div>

      {device.state === 'connected' && (
        <div className="flex items-center gap-1 mt-2 ml-4">
          <Tooltip content="Interrupt (Ctrl+C)">
            <Button icon size="sm" variant="ghost" onClick={handleInterrupt}>
              <Square size={12} />
            </Button>
          </Tooltip>

          <Tooltip content="Soft Reset">
            <Button icon size="sm" variant="ghost" onClick={handleReset}>
              <RotateCcw size={12} />
            </Button>
          </Tooltip>

          <Tooltip content="Disconnect">
            <Button
              icon
              size="sm"
              variant="ghost"
              onClick={(e) => {
                e.stopPropagation()
                onDisconnect()
              }}
            >
              <PowerOff size={12} className="text-vscode-error" />
            </Button>
          </Tooltip>
        </div>
      )}

      {device.error && (
        <div className="mt-1 ml-4 text-xs text-vscode-error truncate">
          {device.error}
        </div>
      )}
    </div>
  )
}
