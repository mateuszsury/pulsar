import { useState, useCallback } from 'react'
import { FolderSync as FolderSyncIcon, Upload, RefreshCw, Check, X, AlertCircle } from 'lucide-react'
import { Button } from '../common/Button'
import { useDeviceStore, selectSelectedDevice } from '../../stores/deviceStore'
import { api, SyncCompareResult, SyncResult } from '../../services/api'

export function FolderSync() {
  const selectedDevice = useDeviceStore(selectSelectedDevice)
  const [localFolder, setLocalFolder] = useState('')
  const [remoteFolder, setRemoteFolder] = useState('/')
  const [comparing, setComparing] = useState(false)
  const [syncing, setSyncing] = useState(false)
  const [compareResult, setCompareResult] = useState<SyncCompareResult | null>(null)
  const [syncResult, setSyncResult] = useState<SyncResult | null>(null)
  const [error, setError] = useState<string | null>(null)

  const port = selectedDevice?.port

  const handleCompare = useCallback(async () => {
    if (!port || !localFolder) return

    setComparing(true)
    setError(null)
    setCompareResult(null)
    setSyncResult(null)

    try {
      const result = await api.syncCompare(port, localFolder, remoteFolder)
      if (result.data) {
        setCompareResult(result.data)
      } else {
        setError(result.error || 'Comparison failed')
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Error')
    } finally {
      setComparing(false)
    }
  }, [port, localFolder, remoteFolder])

  const handleSync = useCallback(async () => {
    if (!port || !localFolder) return

    setSyncing(true)
    setError(null)
    setSyncResult(null)

    try {
      const result = await api.syncUpload(port, localFolder, remoteFolder)
      if (result.data) {
        setSyncResult(result.data)
        // Refresh comparison after sync
        if (result.data.success) {
          await handleCompare()
        }
      } else {
        setError(result.error || 'Sync failed')
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Error')
    } finally {
      setSyncing(false)
    }
  }, [port, localFolder, remoteFolder, handleCompare])

  if (!selectedDevice || selectedDevice.state !== 'connected') {
    return (
      <div className="p-4 text-vscode-text-dim">
        Connect to a device to sync folders
      </div>
    )
  }

  return (
    <div className="p-4 space-y-4">
      <div className="flex items-center gap-2">
        <FolderSyncIcon size={16} />
        <h3 className="text-sm font-medium">Folder Synchronization</h3>
      </div>

      {/* Folder inputs */}
      <div className="space-y-3">
        <div>
          <label className="block text-xs text-vscode-text-dim mb-1">
            Local Folder (PC)
          </label>
          <input
            type="text"
            value={localFolder}
            onChange={(e) => setLocalFolder(e.target.value)}
            placeholder="C:\path\to\project\src"
            className="w-full px-2 py-1.5 bg-vscode-input border border-vscode-border rounded text-sm font-mono"
          />
        </div>

        <div>
          <label className="block text-xs text-vscode-text-dim mb-1">
            Remote Folder (Device)
          </label>
          <input
            type="text"
            value={remoteFolder}
            onChange={(e) => setRemoteFolder(e.target.value)}
            placeholder="/"
            className="w-full px-2 py-1.5 bg-vscode-input border border-vscode-border rounded text-sm font-mono"
          />
        </div>

        <div className="flex gap-2">
          <Button
            size="sm"
            variant="secondary"
            onClick={handleCompare}
            disabled={comparing || !localFolder}
          >
            <RefreshCw size={14} className={comparing ? 'animate-spin' : ''} />
            Compare
          </Button>

          <Button
            size="sm"
            onClick={handleSync}
            disabled={syncing || !localFolder || !compareResult || compareResult.needs_upload === 0}
          >
            <Upload size={14} className={syncing ? 'animate-pulse' : ''} />
            Sync ({compareResult?.needs_upload || 0} files)
          </Button>
        </div>
      </div>

      {/* Compare result */}
      {compareResult && (
        <div className="space-y-2 pt-2 border-t border-vscode-border">
          <div className="flex items-center justify-between text-sm">
            <span className="text-vscode-text-dim">Total files:</span>
            <span>{compareResult.total}</span>
          </div>
          <div className="flex items-center justify-between text-sm">
            <span className="text-vscode-text-dim">Need upload:</span>
            <span className={compareResult.needs_upload > 0 ? 'text-yellow-400' : 'text-green-400'}>
              {compareResult.needs_upload}
            </span>
          </div>

          {compareResult.to_upload.length > 0 && (
            <div className="mt-2">
              <div className="text-xs text-vscode-text-dim mb-1">Files to upload:</div>
              <div className="max-h-40 overflow-y-auto bg-vscode-input rounded p-2">
                {compareResult.to_upload.map((file) => (
                  <div key={file} className="text-xs font-mono flex items-center gap-1">
                    <Upload size={10} className="text-yellow-400" />
                    {file}
                  </div>
                ))}
              </div>
            </div>
          )}

          {compareResult.needs_upload === 0 && (
            <div className="flex items-center gap-2 text-sm text-green-400">
              <Check size={14} />
              All files are up to date
            </div>
          )}
        </div>
      )}

      {/* Sync result */}
      {syncResult && (
        <div className={`p-3 rounded border ${
          syncResult.success
            ? 'bg-green-900/30 border-green-700'
            : 'bg-red-900/30 border-red-700'
        }`}>
          <div className="flex items-center gap-2 mb-2">
            {syncResult.success ? (
              <Check size={16} className="text-green-400" />
            ) : (
              <X size={16} className="text-red-400" />
            )}
            <span className="font-medium">
              {syncResult.success ? 'Sync Complete' : 'Sync Failed'}
            </span>
          </div>

          <div className="text-sm space-y-1">
            {syncResult.uploaded.length > 0 && (
              <div className="text-green-300">
                Uploaded: {syncResult.uploaded.length} files
              </div>
            )}
            {syncResult.skipped.length > 0 && (
              <div className="text-vscode-text-dim">
                Skipped: {syncResult.skipped.length} files
              </div>
            )}
            {syncResult.failed.length > 0 && (
              <div className="text-red-300">
                Failed: {syncResult.failed.join(', ')}
              </div>
            )}
            {syncResult.errors.length > 0 && (
              <div className="text-red-300 text-xs">
                {syncResult.errors.map((e, i) => (
                  <div key={i}>{e}</div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="flex items-start gap-2 p-2 bg-red-900/30 border border-red-700 rounded text-sm text-red-300">
          <AlertCircle size={14} className="mt-0.5 flex-shrink-0" />
          {error}
        </div>
      )}
    </div>
  )
}
