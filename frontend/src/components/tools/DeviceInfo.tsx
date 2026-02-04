import { useState, useCallback } from 'react'
import { Cpu, RefreshCw, HardDrive, Info } from 'lucide-react'
import { Button } from '../common/Button'
import { useDeviceStore, selectSelectedDevice } from '../../stores/deviceStore'
import { api, ChipInfo } from '../../services/api'

export function DeviceInfo() {
  const selectedDevice = useDeviceStore(selectSelectedDevice)
  const [chipInfo, setChipInfo] = useState<ChipInfo | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const port = selectedDevice?.port

  const loadChipInfo = useCallback(async () => {
    if (!port) return

    setLoading(true)
    setError(null)

    try {
      const result = await api.getChipInfo(port)
      if (result.data) {
        setChipInfo(result.data)
      } else {
        setError(result.error || 'Failed to get chip info')
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Error')
    } finally {
      setLoading(false)
    }
  }, [port])

  if (!selectedDevice) {
    return (
      <div className="p-4 text-vscode-text-dim">
        Connect to a device to see info
      </div>
    )
  }

  return (
    <div className="p-4 space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-medium flex items-center gap-2">
          <Info size={16} />
          Device Information
        </h3>
        <Button
          size="sm"
          variant="ghost"
          onClick={loadChipInfo}
          disabled={loading}
        >
          <RefreshCw size={14} className={loading ? 'animate-spin' : ''} />
          {chipInfo ? 'Refresh' : 'Load Info'}
        </Button>
      </div>

      {/* MicroPython Info */}
      <div className="space-y-2">
        <h4 className="text-xs uppercase tracking-wider text-vscode-text-dim">
          Connection
        </h4>
        <div className="grid grid-cols-2 gap-2 text-sm">
          <div className="text-vscode-text-dim">Port:</div>
          <div className="font-mono">{selectedDevice.port}</div>

          <div className="text-vscode-text-dim">Baudrate:</div>
          <div className="font-mono">{selectedDevice.baudrate}</div>

          <div className="text-vscode-text-dim">Status:</div>
          <div className={`font-mono ${
            selectedDevice.state === 'connected' ? 'text-green-400' :
            selectedDevice.state === 'error' ? 'text-red-400' : ''
          }`}>
            {selectedDevice.state}
          </div>

          {selectedDevice.firmware && (
            <>
              <div className="text-vscode-text-dim">Firmware:</div>
              <div className="font-mono text-xs">{selectedDevice.firmware}</div>
            </>
          )}

          {selectedDevice.machine && (
            <>
              <div className="text-vscode-text-dim">Machine:</div>
              <div className="font-mono text-xs">{selectedDevice.machine}</div>
            </>
          )}
        </div>
      </div>

      {/* Chip Info (from esptool) */}
      {chipInfo && (
        <div className="space-y-2 pt-2 border-t border-vscode-border">
          <h4 className="text-xs uppercase tracking-wider text-vscode-text-dim flex items-center gap-2">
            <Cpu size={12} />
            Hardware (esptool)
          </h4>
          <div className="grid grid-cols-2 gap-2 text-sm">
            {chipInfo.chip && (
              <>
                <div className="text-vscode-text-dim">Chip:</div>
                <div className="font-mono">{chipInfo.chip}</div>
              </>
            )}

            {chipInfo.mac_address && (
              <>
                <div className="text-vscode-text-dim">MAC:</div>
                <div className="font-mono text-xs">{chipInfo.mac_address}</div>
              </>
            )}

            {chipInfo.flash_size && (
              <>
                <div className="text-vscode-text-dim flex items-center gap-1">
                  <HardDrive size={12} />
                  Flash:
                </div>
                <div className="font-mono">{chipInfo.flash_size}</div>
              </>
            )}

            {chipInfo.crystal && (
              <>
                <div className="text-vscode-text-dim">Crystal:</div>
                <div className="font-mono">{chipInfo.crystal}</div>
              </>
            )}

            {chipInfo.features.length > 0 && (
              <>
                <div className="text-vscode-text-dim">Features:</div>
                <div className="font-mono text-xs">
                  {chipInfo.features.join(', ')}
                </div>
              </>
            )}
          </div>
        </div>
      )}

      {error && (
        <div className="p-2 bg-red-900/30 border border-red-700 rounded text-sm text-red-300">
          {error}
        </div>
      )}

      {loading && (
        <div className="text-sm text-vscode-text-dim">
          Reading chip info... (device will reconnect)
        </div>
      )}
    </div>
  )
}
