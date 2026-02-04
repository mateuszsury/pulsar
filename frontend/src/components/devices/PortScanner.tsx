import { useState, useEffect } from 'react'
import { RefreshCw, Usb, Power } from 'lucide-react'
import { Modal } from '../common/Modal'
import { Button } from '../common/Button'
import { api, PortInfo } from '../../services/api'

interface PortScannerProps {
  isOpen: boolean
  onClose: () => void
  onConnect: (port: string, baudrate?: number) => Promise<boolean>
}

export function PortScanner({ isOpen, onClose, onConnect }: PortScannerProps) {
  const [ports, setPorts] = useState<PortInfo[]>([])
  const [loading, setLoading] = useState(false)
  const [selectedPort, setSelectedPort] = useState<string | null>(null)
  const [baudrate, setBaudrate] = useState(115200)

  const baudrates = [9600, 19200, 38400, 57600, 115200, 230400, 460800, 921600]

  const scanPorts = async () => {
    setLoading(true)
    const result = await api.getPorts()
    if (result.data) {
      setPorts(result.data)
    }
    setLoading(false)
  }

  useEffect(() => {
    if (isOpen) {
      scanPorts()
    }
  }, [isOpen])

  const handleConnect = async () => {
    if (!selectedPort) return

    const success = await onConnect(selectedPort, baudrate)
    if (success) {
      onClose()
    }
  }

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="Connect to Device"
      footer={
        <>
          <Button variant="ghost" onClick={onClose}>
            Cancel
          </Button>
          <Button
            variant="primary"
            onClick={handleConnect}
            disabled={!selectedPort}
          >
            <Power size={14} className="mr-1" />
            Connect
          </Button>
        </>
      }
    >
      <div className="space-y-4">
        {/* Port list */}
        <div>
          <div className="flex items-center justify-between mb-2">
            <label className="text-sm font-medium text-vscode-text">
              Available Ports
            </label>
            <Button
              icon
              size="sm"
              variant="ghost"
              onClick={scanPorts}
              disabled={loading}
            >
              <RefreshCw size={14} className={loading ? 'animate-spin' : ''} />
            </Button>
          </div>

          <div className="space-y-1 max-h-48 overflow-auto">
            {ports.map(port => (
              <div
                key={port.port}
                className={`flex items-center gap-2 px-3 py-2 rounded cursor-pointer ${
                  selectedPort === port.port
                    ? 'bg-vscode-selection'
                    : 'hover:bg-vscode-hover'
                }`}
                onClick={() => setSelectedPort(port.port)}
              >
                <Usb size={14} className="text-vscode-text-dim flex-shrink-0" />
                <div className="flex-1 min-w-0">
                  <div className="text-sm font-medium truncate">{port.port}</div>
                  <div className="text-xs text-vscode-text-dim truncate">
                    {port.description || 'Unknown device'}
                  </div>
                </div>
                {port.vid && port.pid && (
                  <div className="text-xs text-vscode-text-dim">
                    {port.vid.toString(16).padStart(4, '0')}:{port.pid.toString(16).padStart(4, '0')}
                  </div>
                )}
              </div>
            ))}

            {ports.length === 0 && !loading && (
              <div className="text-center py-4 text-vscode-text-dim">
                No ports found
              </div>
            )}

            {loading && (
              <div className="text-center py-4 text-vscode-text-dim">
                Scanning...
              </div>
            )}
          </div>
        </div>

        {/* Baudrate selection */}
        <div>
          <label className="block text-sm font-medium text-vscode-text mb-2">
            Baud Rate
          </label>
          <select
            className="select"
            value={baudrate}
            onChange={e => setBaudrate(Number(e.target.value))}
          >
            {baudrates.map(rate => (
              <option key={rate} value={rate}>
                {rate.toLocaleString()}
              </option>
            ))}
          </select>
        </div>
      </div>
    </Modal>
  )
}
