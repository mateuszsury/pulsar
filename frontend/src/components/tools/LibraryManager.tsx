import { useState, useEffect } from 'react'
import { Package, Search, Download, Trash2, RefreshCw, Check } from 'lucide-react'
import { Button } from '../common/Button'
import { Modal } from '../common/Modal'
import { useDeviceStore, selectSelectedDevice } from '../../stores/deviceStore'
import { useSettingsStore } from '../../stores/settingsStore'

interface PackageInfo {
  name: string
  version: string
  description: string
  author: string
  license: string
  url: string
  dependencies: string[]
  installed: boolean
  available_versions: string[]
}

interface InstallProgress {
  status: string
  package: string
  progress: number
  message: string
  error: string
}

const API_BASE = '/api'

export function LibraryManager() {
  const selectedDevice = useDeviceStore(selectSelectedDevice)
  const { activeToolPanel, setActiveToolPanel } = useSettingsStore()

  const [availablePackages, setAvailablePackages] = useState<PackageInfo[]>([])
  const [installedPackages, setInstalledPackages] = useState<PackageInfo[]>([])
  const [searchResults, setSearchResults] = useState<PackageInfo[]>([])
  const [searchQuery, setSearchQuery] = useState('')
  const [loading, setLoading] = useState(false)
  const [installing, setInstalling] = useState<string | null>(null)
  const [progress, setProgress] = useState<InstallProgress | null>(null)
  const [activeTab, setActiveTab] = useState<'available' | 'installed'>('available')

  const isOpen = activeToolPanel === 'library'
  const port = selectedDevice?.port

  useEffect(() => {
    if (isOpen) {
      loadAvailablePackages()
      if (port) {
        loadInstalledPackages()
      }
    }
  }, [isOpen, port])

  useEffect(() => {
    let interval: ReturnType<typeof setInterval>
    if (installing) {
      interval = setInterval(async () => {
        const res = await fetch(`${API_BASE}/packages/progress`)
        const data = await res.json()
        setProgress(data)

        if (data.status === 'complete' || data.status === 'error') {
          setInstalling(null)
          if (data.status === 'complete' && port) {
            loadInstalledPackages()
          }
        }
      }, 500)
    }
    return () => clearInterval(interval)
  }, [installing, port])

  const loadAvailablePackages = async () => {
    setLoading(true)
    try {
      const res = await fetch(`${API_BASE}/packages`)
      const data = await res.json()
      setAvailablePackages(data.packages || [])
    } catch (e) {
      console.error('Failed to load packages:', e)
    }
    setLoading(false)
  }

  const loadInstalledPackages = async () => {
    if (!port) return
    try {
      const res = await fetch(`${API_BASE}/devices/${encodeURIComponent(port)}/packages`)
      const data = await res.json()
      setInstalledPackages(data.packages || [])
    } catch (e) {
      console.error('Failed to load installed packages:', e)
    }
  }

  const searchPackages = async () => {
    if (!searchQuery.trim()) {
      setSearchResults([])
      return
    }
    setLoading(true)
    try {
      const res = await fetch(`${API_BASE}/packages/search?q=${encodeURIComponent(searchQuery)}`)
      const data = await res.json()
      setSearchResults(data.packages || [])
    } catch (e) {
      console.error('Search failed:', e)
    }
    setLoading(false)
  }

  const installPackage = async (name: string) => {
    if (!port) return

    setInstalling(name)
    setProgress({
      status: 'starting',
      package: name,
      progress: 0,
      message: 'Starting installation...',
      error: '',
    })

    try {
      await fetch(`${API_BASE}/devices/${encodeURIComponent(port)}/packages/install`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ package: name }),
      })
    } catch (e) {
      console.error('Install failed:', e)
      setInstalling(null)
    }
  }

  const uninstallPackage = async (name: string) => {
    if (!port) return
    if (!confirm(`Uninstall ${name}?`)) return

    try {
      await fetch(`${API_BASE}/devices/${encodeURIComponent(port)}/packages/${encodeURIComponent(name)}`, {
        method: 'DELETE',
      })
      loadInstalledPackages()
    } catch (e) {
      console.error('Uninstall failed:', e)
    }
  }

  const handleClose = () => {
    setActiveToolPanel(null)
    setSearchQuery('')
    setSearchResults([])
  }

  const isInstalled = (name: string) => {
    return installedPackages.some(p => p.name === name || p.name === name.replace('.', '/'))
  }

  const displayPackages = searchQuery ? searchResults : availablePackages

  if (!port) {
    return (
      <Modal isOpen={isOpen} onClose={handleClose} title="Library Manager">
        <div className="p-4 text-center text-vscode-text-dim">
          <Package size={48} className="mx-auto mb-4 opacity-50" />
          <p>Connect to a device to manage libraries</p>
        </div>
      </Modal>
    )
  }

  return (
    <Modal isOpen={isOpen} onClose={handleClose} title="MicroPython Library Manager">
      <div className="flex flex-col h-[500px]">
        {/* Search */}
        <div className="p-3 border-b border-vscode-border">
          <div className="flex gap-2">
            <div className="flex-1 relative">
              <Search size={16} className="absolute left-2 top-1/2 -translate-y-1/2 text-vscode-text-dim" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && searchPackages()}
                placeholder="Search packages..."
                className="w-full pl-8 pr-3 py-1.5 bg-vscode-input border border-vscode-border rounded text-sm"
              />
            </div>
            <Button onClick={searchPackages} disabled={loading}>
              <Search size={14} />
            </Button>
            <Button onClick={loadAvailablePackages} disabled={loading}>
              <RefreshCw size={14} className={loading ? 'animate-spin' : ''} />
            </Button>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex border-b border-vscode-border">
          <button
            onClick={() => setActiveTab('available')}
            className={`px-4 py-2 text-sm ${activeTab === 'available' ? 'text-vscode-accent border-b-2 border-vscode-accent' : 'text-vscode-text-dim'}`}
          >
            Available ({displayPackages.length})
          </button>
          <button
            onClick={() => setActiveTab('installed')}
            className={`px-4 py-2 text-sm ${activeTab === 'installed' ? 'text-vscode-accent border-b-2 border-vscode-accent' : 'text-vscode-text-dim'}`}
          >
            Installed ({installedPackages.length})
          </button>
        </div>

        {/* Progress bar */}
        {installing && progress && (
          <div className="p-3 bg-vscode-sidebar border-b border-vscode-border">
            <div className="flex items-center justify-between mb-1">
              <span className="text-sm">
                {progress.status === 'error' ? (
                  <span className="text-vscode-error">{progress.error}</span>
                ) : (
                  progress.message
                )}
              </span>
              <span className="text-xs text-vscode-text-dim">
                {Math.round(progress.progress * 100)}%
              </span>
            </div>
            <div className="h-1 bg-vscode-border rounded overflow-hidden">
              <div
                className={`h-full transition-all ${progress.status === 'error' ? 'bg-vscode-error' : 'bg-vscode-accent'}`}
                style={{ width: `${progress.progress * 100}%` }}
              />
            </div>
          </div>
        )}

        {/* Package list */}
        <div className="flex-1 overflow-auto p-2">
          {activeTab === 'available' ? (
            <div className="space-y-2">
              {displayPackages.map((pkg) => (
                <div
                  key={pkg.name}
                  className="p-3 bg-vscode-sidebar border border-vscode-border rounded hover:border-vscode-accent/50 transition-colors"
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2">
                        <Package size={16} className="text-vscode-accent flex-shrink-0" />
                        <span className="font-medium truncate">{pkg.name}</span>
                        {pkg.version && (
                          <span className="text-xs text-vscode-text-dim">{pkg.version}</span>
                        )}
                        {isInstalled(pkg.name) && (
                          <span className="text-xs px-1.5 py-0.5 bg-green-500/20 text-green-400 rounded">
                            Installed
                          </span>
                        )}
                      </div>
                      <p className="text-xs text-vscode-text-dim mt-1 line-clamp-2">
                        {pkg.description}
                      </p>
                      {pkg.dependencies.length > 0 && (
                        <p className="text-xs text-vscode-text-dim mt-1">
                          Requires: {pkg.dependencies.join(', ')}
                        </p>
                      )}
                    </div>
                    <div className="flex items-center gap-1 ml-2">
                      <Button
                        size="sm"
                        variant={isInstalled(pkg.name) ? 'ghost' : 'primary'}
                        onClick={() => installPackage(pkg.name)}
                        disabled={!!installing || isInstalled(pkg.name)}
                      >
                        {installing === pkg.name ? (
                          <RefreshCw size={14} className="animate-spin" />
                        ) : isInstalled(pkg.name) ? (
                          <Check size={14} />
                        ) : (
                          <Download size={14} />
                        )}
                      </Button>
                    </div>
                  </div>
                </div>
              ))}
              {displayPackages.length === 0 && !loading && (
                <div className="text-center text-vscode-text-dim py-8">
                  {searchQuery ? 'No packages found' : 'No packages available'}
                </div>
              )}
            </div>
          ) : (
            <div className="space-y-2">
              {installedPackages.map((pkg) => (
                <div
                  key={pkg.name}
                  className="p-3 bg-vscode-sidebar border border-vscode-border rounded"
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Package size={16} className="text-green-400" />
                      <span className="font-medium">{pkg.name}</span>
                    </div>
                    <Button
                      size="sm"
                      variant="danger"
                      onClick={() => uninstallPackage(pkg.name)}
                    >
                      <Trash2 size={14} />
                    </Button>
                  </div>
                </div>
              ))}
              {installedPackages.length === 0 && (
                <div className="text-center text-vscode-text-dim py-8">
                  No packages installed in /lib
                </div>
              )}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="p-3 border-t border-vscode-border bg-vscode-sidebar text-xs text-vscode-text-dim">
          <p>
            Packages are installed to <code>/lib</code> on the device.
            Use <code>import {'{name}'}</code> in your code.
          </p>
        </div>
      </div>
    </Modal>
  )
}
