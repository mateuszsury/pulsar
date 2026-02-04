import { RefreshCw, Settings, Cpu, Wifi, Zap, Package } from 'lucide-react'
import { Button } from '../common/Button'
import { Tooltip } from '../common/Tooltip'
import { useDeviceStore } from '../../stores/deviceStore'
import { useSettingsStore } from '../../stores/settingsStore'

export function Header() {
  const { fetchPorts, loading } = useDeviceStore()
  const { activeToolPanel, setActiveToolPanel } = useSettingsStore()

  const toggleTool = (tool: 'flasher' | 'wifi' | 'library') => {
    setActiveToolPanel(activeToolPanel === tool ? null : tool)
  }

  return (
    <header className="flex items-center justify-between h-10 px-4 bg-vscode-sidebar border-b border-vscode-border">
      {/* Logo/Title */}
      <div className="flex items-center gap-2">
        <Cpu size={18} className="text-vscode-accent" />
        <span className="font-semibold text-vscode-text">Pulsar</span>
      </div>

      {/* Actions */}
      <div className="flex items-center gap-1">
        <Tooltip content="Refresh ports">
          <Button
            icon
            variant="ghost"
            onClick={() => fetchPorts()}
            disabled={loading}
          >
            <RefreshCw size={16} className={loading ? 'animate-spin' : ''} />
          </Button>
        </Tooltip>

        <div className="w-px h-4 bg-vscode-border mx-1" />

        <Tooltip content="Firmware Flasher">
          <Button
            icon
            variant={activeToolPanel === 'flasher' ? 'primary' : 'ghost'}
            onClick={() => toggleTool('flasher')}
          >
            <Zap size={16} />
          </Button>
        </Tooltip>

        <Tooltip content="WiFi Manager">
          <Button
            icon
            variant={activeToolPanel === 'wifi' ? 'primary' : 'ghost'}
            onClick={() => toggleTool('wifi')}
          >
            <Wifi size={16} />
          </Button>
        </Tooltip>

        <Tooltip content="Library Manager">
          <Button
            icon
            variant={activeToolPanel === 'library' ? 'primary' : 'ghost'}
            onClick={() => toggleTool('library')}
          >
            <Package size={16} />
          </Button>
        </Tooltip>

        <div className="w-px h-4 bg-vscode-border mx-1" />

        <Tooltip content="Settings">
          <Button icon variant="ghost">
            <Settings size={16} />
          </Button>
        </Tooltip>
      </div>
    </header>
  )
}
