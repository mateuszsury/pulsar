import { DeviceCard } from './DeviceCard'
import { DeviceInfo } from '../../services/api'

interface DeviceListProps {
  devices: DeviceInfo[]
  selectedPort: string | null
  onSelect: (port: string) => void
  onDisconnect: (port: string) => void
}

export function DeviceList({ devices, selectedPort, onSelect, onDisconnect }: DeviceListProps) {
  if (devices.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-8 text-vscode-text-dim">
        <p>No devices connected</p>
        <p className="text-xs mt-1">Select a port to connect</p>
      </div>
    )
  }

  return (
    <div className="space-y-1">
      {devices.map(device => (
        <DeviceCard
          key={device.port}
          device={device}
          isSelected={device.port === selectedPort}
          onSelect={() => onSelect(device.port)}
          onDisconnect={() => onDisconnect(device.port)}
        />
      ))}
    </div>
  )
}
