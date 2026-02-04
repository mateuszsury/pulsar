import { useState, useEffect } from 'react'
import { Wifi, WifiOff, RefreshCw, Lock, Signal, CheckCircle } from 'lucide-react'
import { Button } from '../common/Button'
import { Modal } from '../common/Modal'
import { api, WifiNetwork, WifiStatus } from '../../services/api'
import { useDeviceStore, selectSelectedDevice } from '../../stores/deviceStore'
import { useSettingsStore } from '../../stores/settingsStore'

export function WiFiManager() {
  const selectedDevice = useDeviceStore(selectSelectedDevice)
  const { activeToolPanel, setActiveToolPanel } = useSettingsStore()

  const [networks, setNetworks] = useState<WifiNetwork[]>([])
  const [status, setStatus] = useState<WifiStatus | null>(null)
  const [selectedNetwork, setSelectedNetwork] = useState<string | null>(null)
  const [password, setPassword] = useState('')
  const [scanning, setScanning] = useState(false)
  const [connecting, setConnecting] = useState(false)

  const isOpen = activeToolPanel === 'wifi'
  const port = selectedDevice?.port

  useEffect(() => {
    if (isOpen && port) {
      loadStatus()
      scanNetworks()
    }
  }, [isOpen, port])

  const loadStatus = async () => {
    if (!port) return
    const result = await api.getWifiStatus(port)
    if (result.data) {
      setStatus(result.data)
    }
  }

  const scanNetworks = async () => {
    if (!port) return

    setScanning(true)
    const result = await api.scanWifi(port)
    if (result.data) {
      setNetworks(result.data)
    }
    setScanning(false)
  }

  const handleConnect = async () => {
    if (!port || !selectedNetwork) return

    setConnecting(true)
    const result = await api.configureWifi(port, selectedNetwork, password)
    setConnecting(false)

    if (result.data?.success) {
      setPassword('')
      setSelectedNetwork(null)
      await loadStatus()
    }
  }

  const handleClose = () => {
    setActiveToolPanel(null)
    setSelectedNetwork(null)
    setPassword('')
  }

  const getSignalIcon = (signal: string) => {
    const opacity = {
      excellent: 'opacity-100',
      good: 'opacity-75',
      fair: 'opacity-50',
      weak: 'opacity-25',
    }
    return opacity[signal as keyof typeof opacity] || 'opacity-50'
  }

  if (!port) {
    return (
      <Modal isOpen={isOpen} onClose={handleClose} title="WiFi Manager">
        <div className="text-center py-8 text-vscode-text-dim">
          Connect to a device first
        </div>
      </Modal>
    )
  }

  return (
    <Modal
      isOpen={isOpen}
      onClose={handleClose}
      title="WiFi Manager"
      size="lg"
      footer={
        selectedNetwork ? (
          <>
            <Button variant="ghost" onClick={() => setSelectedNetwork(null)}>
              Back
            </Button>
            <Button
              variant="primary"
              onClick={handleConnect}
              disabled={connecting}
            >
              <Wifi size={14} className="mr-1" />
              {connecting ? 'Connecting...' : 'Connect'}
            </Button>
          </>
        ) : (
          <Button variant="ghost" onClick={handleClose}>
            Close
          </Button>
        )
      }
    >
      {/* Current status */}
      {status && (
        <div className="mb-4 p-3 rounded bg-vscode-hover">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              {status.connected ? (
                <Wifi size={16} className="text-vscode-success" />
              ) : (
                <WifiOff size={16} className="text-vscode-text-dim" />
              )}
              <span className="font-medium">
                {status.connected ? status.ssid : 'Not connected'}
              </span>
            </div>
            {status.connected && (
              <span className="text-xs text-vscode-text-dim">{status.ip}</span>
            )}
          </div>
        </div>
      )}

      {selectedNetwork ? (
        /* Password input */
        <div className="space-y-4">
          <div className="flex items-center gap-2 text-lg">
            <Wifi size={20} />
            <span>{selectedNetwork}</span>
          </div>

          <div>
            <label className="block text-sm font-medium text-vscode-text mb-1">
              Password
            </label>
            <input
              type="password"
              className="input"
              value={password}
              onChange={e => setPassword(e.target.value)}
              placeholder="Enter WiFi password"
              autoFocus
              onKeyDown={e => e.key === 'Enter' && handleConnect()}
            />
          </div>
        </div>
      ) : (
        /* Network list */
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-vscode-text">
              Available Networks
            </span>
            <Button
              icon
              size="sm"
              variant="ghost"
              onClick={scanNetworks}
              disabled={scanning}
            >
              <RefreshCw size={14} className={scanning ? 'animate-spin' : ''} />
            </Button>
          </div>

          <div className="max-h-64 overflow-auto space-y-1">
            {networks.map(network => (
              <div
                key={`${network.ssid}-${network.bssid}`}
                className={`flex items-center gap-2 px-3 py-2 rounded cursor-pointer hover:bg-vscode-hover ${
                  status?.ssid === network.ssid ? 'bg-vscode-selection' : ''
                }`}
                onClick={() => setSelectedNetwork(network.ssid)}
              >
                <Signal size={14} className={getSignalIcon(network.signal)} />
                <span className="flex-1 truncate">{network.ssid || '(Hidden)'}</span>

                {network.authmode !== 'open' && (
                  <Lock size={12} className="text-vscode-text-dim" />
                )}

                {status?.ssid === network.ssid && (
                  <CheckCircle size={14} className="text-vscode-success" />
                )}

                <span className="text-xs text-vscode-text-dim">
                  {network.rssi} dBm
                </span>
              </div>
            ))}

            {networks.length === 0 && !scanning && (
              <div className="text-center py-4 text-vscode-text-dim">
                No networks found
              </div>
            )}

            {scanning && (
              <div className="text-center py-4 text-vscode-text-dim">
                Scanning...
              </div>
            )}
          </div>
        </div>
      )}
    </Modal>
  )
}
