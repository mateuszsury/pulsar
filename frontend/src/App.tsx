import { useEffect } from 'react'
import { Sidebar } from './components/layout/Sidebar'
import { Header } from './components/layout/Header'
import { TabBar } from './components/layout/TabBar'
import { Terminal } from './components/console/Terminal'
import { FileBrowser } from './components/files/FileBrowser'
import { CodeEditor } from './components/editor/CodeEditor'
import { DeviceInfo } from './components/tools/DeviceInfo'
import { FolderSync } from './components/tools/FolderSync'
import { FirmwareFlasher } from './components/tools/FirmwareFlasher'
import { WiFiManager } from './components/tools/WiFiManager'
import { LibraryManager } from './components/tools/LibraryManager'
import { useDeviceStore, selectSelectedDevice } from './stores/deviceStore'
import { useSettingsStore } from './stores/settingsStore'
import { useWebSocket } from './hooks/useWebSocket'

function App() {
  const selectedDevice = useDeviceStore(selectSelectedDevice)
  const { activePanel, sidebarWidth } = useSettingsStore()
  const { connect } = useWebSocket()

  useEffect(() => {
    // Connect to WebSocket on mount
    connect()
  }, [connect])

  return (
    <div className="flex flex-col h-screen bg-vscode-bg text-vscode-text overflow-hidden">
      {/* Header */}
      <Header />

      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar */}
        <div
          className="flex-shrink-0 bg-vscode-sidebar border-r border-vscode-border overflow-hidden"
          style={{ width: sidebarWidth }}
        >
          <Sidebar />
        </div>

        {/* Main content */}
        <div className="flex-1 flex flex-col overflow-hidden">
          {/* Tab bar */}
          <TabBar />

          {/* Content area */}
          <div className="flex-1 flex overflow-hidden">
            {/* Editor area */}
            <div className="flex-1 overflow-hidden">
              {activePanel === 'editor' && <CodeEditor />}
              {activePanel === 'files' && <FileBrowser />}
              {activePanel === 'info' && <DeviceInfo />}
              {activePanel === 'sync' && <FolderSync />}
            </div>
          </div>

          {/* Terminal panel */}
          <div className="h-64 border-t border-vscode-border">
            <Terminal />
          </div>
        </div>
      </div>

      {/* Status bar */}
      <div className="h-6 flex items-center justify-between px-2 bg-vscode-button text-white text-xs">
        <div className="flex items-center gap-4">
          {selectedDevice ? (
            <>
              <span className="flex items-center gap-1">
                <span className="w-2 h-2 rounded-full bg-green-400" />
                {selectedDevice.port}
              </span>
              <span>{selectedDevice.machine || 'MicroPython'}</span>
            </>
          ) : (
            <span className="text-white/70">No device connected</span>
          )}
        </div>
        <div className="flex items-center gap-4">
          <span>Pulsar</span>
        </div>
      </div>

      {/* Tool modals */}
      <FirmwareFlasher />
      <WiFiManager />
      <LibraryManager />
    </div>
  )
}

export default App
