import { useState } from 'react'
import { ChevronDown, ChevronRight, Usb, Plus, Power } from 'lucide-react'
import { Button } from '../common/Button'
import { Tooltip } from '../common/Tooltip'
import { DeviceCard } from '../devices/DeviceCard'
import { PortScanner } from '../devices/PortScanner'
import { useDevices } from '../../hooks/useDevices'

export function Sidebar() {
  const {
    ports,
    devices,
    selectedPort,
    selectPort,
    connect,
    disconnect,
    loading,
  } = useDevices()

  const [portsExpanded, setPortsExpanded] = useState(true)
  const [devicesExpanded, setDevicesExpanded] = useState(true)
  const [showScanner, setShowScanner] = useState(false)

  return (
    <div className="flex flex-col h-full text-sm">
      {/* Devices Section */}
      <div className="flex-shrink-0">
        <div
          className="flex items-center gap-1 px-2 py-1.5 text-xs uppercase tracking-wider text-vscode-text-dim cursor-pointer hover:bg-vscode-hover"
          onClick={() => setDevicesExpanded(!devicesExpanded)}
        >
          {devicesExpanded ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
          <span className="flex-1">Connected Devices</span>
          <span className="text-vscode-accent">{devices.length}</span>
        </div>

        {devicesExpanded && (
          <div className="px-1 pb-2">
            {devices.length === 0 ? (
              <div className="px-2 py-4 text-center text-vscode-text-dim">
                No devices connected
              </div>
            ) : (
              devices.map(device => (
                <DeviceCard
                  key={device.port}
                  device={device}
                  isSelected={device.port === selectedPort}
                  onSelect={() => selectPort(device.port)}
                  onDisconnect={() => disconnect(device.port)}
                />
              ))
            )}
          </div>
        )}
      </div>

      {/* Available Ports Section */}
      <div className="flex-1 overflow-auto">
        <div
          className="flex items-center gap-1 px-2 py-1.5 text-xs uppercase tracking-wider text-vscode-text-dim cursor-pointer hover:bg-vscode-hover"
          onClick={() => setPortsExpanded(!portsExpanded)}
        >
          {portsExpanded ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
          <span className="flex-1">Available Ports</span>
          <Tooltip content="Scan ports">
            <Button
              icon
              size="sm"
              variant="ghost"
              onClick={(e) => {
                e.stopPropagation()
                setShowScanner(true)
              }}
            >
              <Plus size={14} />
            </Button>
          </Tooltip>
        </div>

        {portsExpanded && (
          <div className="px-1 pb-2">
            {ports
              .filter(p => !devices.some(d => d.port === p.port))
              .map(port => (
                <div
                  key={port.port}
                  className="flex items-center gap-2 px-2 py-1.5 rounded hover:bg-vscode-hover cursor-pointer group"
                  onClick={() => connect(port.port)}
                >
                  <Usb size={14} className="text-vscode-text-dim" />
                  <div className="flex-1 min-w-0">
                    <div className="text-vscode-text truncate">{port.port}</div>
                    <div className="text-xs text-vscode-text-dim truncate">
                      {port.description || 'Unknown device'}
                    </div>
                  </div>
                  <Button
                    icon
                    size="sm"
                    variant="ghost"
                    className="opacity-0 group-hover:opacity-100"
                    disabled={loading}
                    onClick={(e) => {
                      e.stopPropagation()
                      connect(port.port)
                    }}
                  >
                    <Power size={14} className="text-vscode-success" />
                  </Button>
                </div>
              ))}

            {ports.length === 0 && (
              <div className="px-2 py-4 text-center text-vscode-text-dim">
                No ports found
              </div>
            )}
          </div>
        )}
      </div>

      {/* Port Scanner Modal */}
      <PortScanner
        isOpen={showScanner}
        onClose={() => setShowScanner(false)}
        onConnect={connect}
      />
    </div>
  )
}
