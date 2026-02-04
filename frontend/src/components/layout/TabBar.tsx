import { Code, FolderTree, Info, FolderSync, Zap, Wifi } from 'lucide-react'
import { useSettingsStore } from '../../stores/settingsStore'
import { Button } from '../common/Button'
import { Tooltip } from '../common/Tooltip'

export function TabBar() {
  const { activePanel, setActivePanel, setActiveToolPanel } = useSettingsStore()

  const tabs = [
    { id: 'editor' as const, label: 'Editor', icon: Code },
    { id: 'files' as const, label: 'Files', icon: FolderTree },
    { id: 'info' as const, label: 'Device', icon: Info },
    { id: 'sync' as const, label: 'Sync', icon: FolderSync },
  ]

  return (
    <div className="flex items-center h-9 px-2 bg-vscode-sidebar border-b border-vscode-border">
      {/* Main tabs */}
      {tabs.map(tab => (
        <button
          key={tab.id}
          className={`flex items-center gap-1.5 px-3 h-full text-sm transition-colors ${
            activePanel === tab.id
              ? 'text-vscode-text border-b-2 border-vscode-accent'
              : 'text-vscode-text-dim hover:text-vscode-text'
          }`}
          onClick={() => setActivePanel(tab.id)}
        >
          <tab.icon size={14} />
          {tab.label}
        </button>
      ))}

      {/* Spacer */}
      <div className="flex-1" />

      {/* Tool buttons */}
      <div className="flex items-center gap-1">
        <Tooltip content="Firmware Flasher">
          <Button
            icon
            size="sm"
            variant="ghost"
            onClick={() => setActiveToolPanel('flasher')}
          >
            <Zap size={14} />
          </Button>
        </Tooltip>

        <Tooltip content="WiFi Manager">
          <Button
            icon
            size="sm"
            variant="ghost"
            onClick={() => setActiveToolPanel('wifi')}
          >
            <Wifi size={14} />
          </Button>
        </Tooltip>
      </div>
    </div>
  )
}
