import { useState } from 'react'
import { Terminal } from './Terminal'
import { LogViewer } from './LogViewer'
import { useDeviceStore, selectSelectedDevice } from '../../stores/deviceStore'

type TabType = 'terminal' | 'logs'

export function ConsoleTab() {
  const [activeTab, setActiveTab] = useState<TabType>('terminal')
  const selectedDevice = useDeviceStore(selectSelectedDevice)

  return (
    <div className="flex flex-col h-full">
      {/* Tabs */}
      <div className="flex items-center border-b border-vscode-border">
        <button
          className={`px-3 py-1.5 text-sm ${
            activeTab === 'terminal'
              ? 'text-vscode-text border-b-2 border-vscode-accent'
              : 'text-vscode-text-dim hover:text-vscode-text'
          }`}
          onClick={() => setActiveTab('terminal')}
        >
          Terminal
        </button>
        <button
          className={`px-3 py-1.5 text-sm ${
            activeTab === 'logs'
              ? 'text-vscode-text border-b-2 border-vscode-accent'
              : 'text-vscode-text-dim hover:text-vscode-text'
          }`}
          onClick={() => setActiveTab('logs')}
        >
          Logs
        </button>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-hidden">
        {activeTab === 'terminal' && <Terminal />}
        {activeTab === 'logs' && selectedDevice && (
          <LogViewer port={selectedDevice.port} />
        )}
        {activeTab === 'logs' && !selectedDevice && (
          <div className="flex items-center justify-center h-full text-vscode-text-dim">
            Select a device to view logs
          </div>
        )}
      </div>
    </div>
  )
}
