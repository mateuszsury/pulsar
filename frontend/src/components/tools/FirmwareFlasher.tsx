import { useState, useEffect } from 'react'
import { Zap, AlertCircle, CheckCircle, Trash2, FileInput } from 'lucide-react'
import { Button } from '../common/Button'
import { Modal } from '../common/Modal'
import { api, FirmwareInfo, FlashProgress } from '../../services/api'
import { useDeviceStore } from '../../stores/deviceStore'
import { useSettingsStore } from '../../stores/settingsStore'

export function FirmwareFlasher() {
  const { ports } = useDeviceStore()
  const { activeToolPanel, setActiveToolPanel } = useSettingsStore()

  const [firmware, setFirmware] = useState<FirmwareInfo[]>([])
  const [selectedPort, setSelectedPort] = useState<string>('')
  const [selectedFirmware, setSelectedFirmware] = useState<string>('')
  const [customPath, setCustomPath] = useState<string>('')
  const [useCustomPath, setUseCustomPath] = useState(false)
  const [progress, setProgress] = useState<FlashProgress | null>(null)
  const [loading, setLoading] = useState(false)

  const isOpen = activeToolPanel === 'flasher'

  useEffect(() => {
    if (isOpen) {
      loadFirmware()
    }
  }, [isOpen])

  useEffect(() => {
    if (ports.length > 0 && !selectedPort) {
      setSelectedPort(ports[0].port)
    }
  }, [ports, selectedPort])

  const loadFirmware = async () => {
    const result = await api.listFirmware()
    if (result.data) {
      setFirmware(result.data)
      if (result.data.length > 0 && !selectedFirmware) {
        const local = result.data.find(f => f.local)
        setSelectedFirmware(local?.path || result.data[0].path || result.data[0].url || '')
      }
    }
  }

  const handleFlash = async () => {
    const firmwarePath = useCustomPath ? customPath : selectedFirmware
    if (!selectedPort || !firmwarePath) return

    setLoading(true)
    setProgress({ status: 'starting', progress: 0, message: 'Starting...', error: '' })

    await api.flashFirmware(selectedPort, firmwarePath)

    // Poll for progress
    const pollProgress = setInterval(async () => {
      const result = await api.getFirmwareProgress()
      if (result.data) {
        setProgress(result.data)

        if (result.data.status === 'complete' || result.data.status === 'error') {
          clearInterval(pollProgress)
          setLoading(false)
        }
      }
    }, 500)
  }

  const handleErase = async () => {
    if (!selectedPort) return

    setLoading(true)
    setProgress({ status: 'erasing', progress: 0, message: 'Erasing flash...', error: '' })

    await api.eraseFirmware(selectedPort)

    // Poll for progress
    const pollProgress = setInterval(async () => {
      const result = await api.getFirmwareProgress()
      if (result.data) {
        setProgress(result.data)

        if (result.data.status === 'complete' || result.data.status === 'erased' || result.data.status === 'error') {
          clearInterval(pollProgress)
          setLoading(false)

          if (result.data.status === 'erased') {
            setProgress({
              status: 'complete',
              progress: 1,
              message: 'Flash erased successfully!',
              error: ''
            })
          }
        }
      }
    }, 500)
  }

  const handleClose = () => {
    if (!loading) {
      setActiveToolPanel(null)
      setProgress(null)
    }
  }

  const getActiveFirmwarePath = () => useCustomPath ? customPath : selectedFirmware

  return (
    <Modal
      isOpen={isOpen}
      onClose={handleClose}
      title="Firmware Flasher"
      size="lg"
      footer={
        <>
          <Button variant="ghost" onClick={handleClose} disabled={loading}>
            {progress?.status === 'complete' ? 'Done' : 'Cancel'}
          </Button>
          {progress?.status !== 'complete' && (
            <>
              <Button
                variant="ghost"
                onClick={handleErase}
                disabled={loading || !selectedPort}
                className="text-red-400 hover:text-red-300"
              >
                <Trash2 size={14} className="mr-1" />
                Erase Only
              </Button>
              <Button
                variant="primary"
                onClick={handleFlash}
                disabled={loading || !selectedPort || !getActiveFirmwarePath()}
              >
                <Zap size={14} className="mr-1" />
                {loading ? 'Flashing...' : 'Flash Firmware'}
              </Button>
            </>
          )}
        </>
      }
    >
      <div className="space-y-4">
        {/* Port selection */}
        <div>
          <label className="block text-sm font-medium text-vscode-text mb-1">
            Port
          </label>
          <select
            className="select"
            value={selectedPort}
            onChange={e => setSelectedPort(e.target.value)}
            disabled={loading}
          >
            {ports.map(port => (
              <option key={port.port} value={port.port}>
                {port.port} - {port.description}
              </option>
            ))}
          </select>
        </div>

        {/* Firmware selection mode */}
        <div className="flex items-center gap-4">
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="radio"
              checked={!useCustomPath}
              onChange={() => setUseCustomPath(false)}
              disabled={loading}
              className="accent-vscode-accent"
            />
            <span className="text-sm">Select from list</span>
          </label>
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="radio"
              checked={useCustomPath}
              onChange={() => setUseCustomPath(true)}
              disabled={loading}
              className="accent-vscode-accent"
            />
            <span className="text-sm">Custom path</span>
          </label>
        </div>

        {/* Firmware selection or custom path */}
        {useCustomPath ? (
          <div>
            <label className="block text-sm font-medium text-vscode-text mb-1">
              Firmware Path (.bin file)
            </label>
            <div className="flex gap-2">
              <input
                type="text"
                value={customPath}
                onChange={e => setCustomPath(e.target.value)}
                placeholder="C:\path\to\firmware.bin"
                disabled={loading}
                className="flex-1 px-2 py-1.5 bg-vscode-input border border-vscode-border rounded text-sm font-mono"
              />
              <Button
                variant="ghost"
                size="sm"
                disabled={loading}
                title="Enter full path to .bin file"
              >
                <FileInput size={14} />
              </Button>
            </div>
            <p className="text-xs text-vscode-text-dim mt-1">
              Enter the full path to your MicroPython firmware .bin file
            </p>
          </div>
        ) : (
          <div>
            <label className="block text-sm font-medium text-vscode-text mb-1">
              Firmware
            </label>
            <select
              className="select"
              value={selectedFirmware}
              onChange={e => setSelectedFirmware(e.target.value)}
              disabled={loading}
            >
              <optgroup label="Local Files">
                {firmware.filter(f => f.local).length === 0 && (
                  <option disabled>No local firmware found</option>
                )}
                {firmware.filter(f => f.local).map(fw => (
                  <option key={fw.path} value={fw.path}>
                    {fw.name} {fw.size ? `(${(fw.size / 1024 / 1024).toFixed(1)}MB)` : ''}
                  </option>
                ))}
              </optgroup>
              <optgroup label="Download from micropython.org">
                {firmware.filter(f => !f.local).map(fw => (
                  <option key={fw.url} value={fw.url}>
                    {fw.name}
                  </option>
                ))}
              </optgroup>
            </select>
          </div>
        )}

        {/* Progress */}
        {progress && (
          <div className="space-y-2">
            <div className="flex items-center gap-2">
              {progress.status === 'complete' && (
                <CheckCircle size={16} className="text-green-400" />
              )}
              {progress.status === 'error' && (
                <AlertCircle size={16} className="text-red-400" />
              )}
              <span className="text-sm">
                {progress.status === 'starting' && 'Starting...'}
                {progress.status === 'erasing' && 'Erasing flash...'}
                {progress.status === 'erased' && 'Flash erased!'}
                {progress.status === 'flashing' && 'Writing firmware...'}
                {progress.status === 'downloading' && 'Downloading firmware...'}
                {progress.status === 'complete' && 'Complete!'}
                {progress.status === 'error' && 'Failed'}
              </span>
            </div>

            {['flashing', 'erasing', 'downloading'].includes(progress.status) && (
              <div className="w-full h-2 bg-vscode-input rounded overflow-hidden">
                <div
                  className="h-full bg-vscode-accent transition-all duration-300"
                  style={{ width: `${progress.progress * 100}%` }}
                />
              </div>
            )}

            {progress.message && (
              <p className="text-xs text-vscode-text-dim font-mono">{progress.message}</p>
            )}

            {progress.error && (
              <p className="text-xs text-red-400">{progress.error}</p>
            )}
          </div>
        )}

        {/* Warning */}
        <div className="flex items-start gap-2 p-3 rounded bg-yellow-900/20 border border-yellow-700/50">
          <AlertCircle size={16} className="flex-shrink-0 mt-0.5 text-yellow-400" />
          <div className="text-xs text-yellow-200">
            <p className="font-medium">Important</p>
            <p className="mt-1">
              • Put device in bootloader mode (hold BOOT, press RESET, release BOOT)
            </p>
            <p>
              • Flashing will erase all data on the device
            </p>
            <p>
              • Disconnect from serial monitor before flashing
            </p>
          </div>
        </div>
      </div>
    </Modal>
  )
}
