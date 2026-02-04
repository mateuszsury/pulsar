import { useState, useEffect } from 'react'
import { Upload, Download, Trash2, Plus, RefreshCw } from 'lucide-react'
import { Button } from '../common/Button'
import { Tooltip } from '../common/Tooltip'
import { FileTree } from './FileTree'
import { DropZone } from './DropZone'
import { useDeviceStore, selectSelectedDevice } from '../../stores/deviceStore'
import { api, FileInfo } from '../../services/api'

export function FileBrowser() {
  const selectedDevice = useDeviceStore(selectSelectedDevice)
  const [files, setFiles] = useState<FileInfo[]>([])
  const [currentPath, setCurrentPath] = useState('/')
  const [loading, setLoading] = useState(false)
  const [selectedFile, setSelectedFile] = useState<FileInfo | null>(null)
  const [expandedDirs, setExpandedDirs] = useState<Set<string>>(new Set(['/']))

  const port = selectedDevice?.port

  const loadFiles = async (path: string) => {
    if (!port) return

    setLoading(true)
    const result = await api.listFiles(port, path)
    if (result.data) {
      setFiles(result.data)
    }
    setLoading(false)
  }

  useEffect(() => {
    if (port) {
      loadFiles(currentPath)
    } else {
      setFiles([])
    }
  }, [port, currentPath])

  const handleRefresh = () => {
    loadFiles(currentPath)
  }

  const handleToggleDir = (path: string) => {
    setExpandedDirs(prev => {
      const next = new Set(prev)
      if (next.has(path)) {
        next.delete(path)
      } else {
        next.add(path)
      }
      return next
    })
  }

  const handleNavigate = (path: string) => {
    setCurrentPath(path)
    if (!expandedDirs.has(path)) {
      handleToggleDir(path)
    }
  }

  const handleSelect = (file: FileInfo) => {
    setSelectedFile(file)
  }

  const handleDelete = async () => {
    if (!port || !selectedFile) return

    if (confirm(`Delete ${selectedFile.name}?`)) {
      await api.deleteFile(port, selectedFile.path)
      setSelectedFile(null)
      handleRefresh()
    }
  }

  const handleUpload = async (fileList: FileList) => {
    if (!port) return

    for (const file of Array.from(fileList)) {
      const reader = new FileReader()
      reader.onload = async (e) => {
        const content = e.target?.result as string
        // Remove data URL prefix for base64
        const base64Content = content.split(',')[1] || content
        await api.writeFile(port, `${currentPath}/${file.name}`, base64Content, true)
        handleRefresh()
      }
      reader.readAsDataURL(file)
    }
  }

  const handleDownload = async () => {
    if (!port || !selectedFile || selectedFile.is_dir) return

    const result = await api.readFile(port, selectedFile.path)
    if (result.data) {
      const content = result.data.binary
        ? atob(result.data.content)
        : result.data.content

      const blob = new Blob([content], { type: 'application/octet-stream' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = selectedFile.name
      a.click()
      URL.revokeObjectURL(url)
    }
  }

  const handleCreateDir = async () => {
    if (!port) return

    const name = prompt('Enter directory name:')
    if (name) {
      const path = currentPath === '/' ? `/${name}` : `${currentPath}/${name}`
      await api.mkdir(port, path)
      handleRefresh()
    }
  }

  if (!port) {
    return (
      <div className="flex items-center justify-center h-full text-vscode-text-dim">
        Connect to a device to browse files
      </div>
    )
  }

  return (
    <div className="flex flex-col h-full">
      {/* Toolbar */}
      <div className="flex items-center justify-between px-2 py-1 border-b border-vscode-border">
        <div className="flex items-center gap-1">
          <span className="text-xs text-vscode-text-dim truncate max-w-48">
            {currentPath}
          </span>
        </div>

        <div className="flex items-center gap-1">
          <Tooltip content="Refresh">
            <Button
              icon
              size="sm"
              variant="ghost"
              onClick={handleRefresh}
              disabled={loading}
            >
              <RefreshCw size={14} className={loading ? 'animate-spin' : ''} />
            </Button>
          </Tooltip>

          <Tooltip content="New Folder">
            <Button icon size="sm" variant="ghost" onClick={handleCreateDir}>
              <Plus size={14} />
            </Button>
          </Tooltip>

          <Tooltip content="Upload">
            <label className="cursor-pointer">
              <span className="btn-icon p-1.5 rounded hover:bg-vscode-hover inline-flex">
                <Upload size={14} />
              </span>
              <input
                type="file"
                multiple
                className="hidden"
                onChange={(e) => e.target.files && handleUpload(e.target.files)}
              />
            </label>
          </Tooltip>

          <Tooltip content="Download">
            <Button
              icon
              size="sm"
              variant="ghost"
              onClick={handleDownload}
              disabled={!selectedFile || selectedFile.is_dir}
            >
              <Download size={14} />
            </Button>
          </Tooltip>

          <Tooltip content="Delete">
            <Button
              icon
              size="sm"
              variant="ghost"
              onClick={handleDelete}
              disabled={!selectedFile}
            >
              <Trash2 size={14} />
            </Button>
          </Tooltip>
        </div>
      </div>

      {/* File tree */}
      <div className="flex-1 overflow-auto">
        <DropZone onDrop={handleUpload}>
          <FileTree
            files={files}
            currentPath={currentPath}
            expandedDirs={expandedDirs}
            selectedPath={selectedFile?.path ?? null}
            onToggleDir={handleToggleDir}
            onNavigate={handleNavigate}
            onSelect={handleSelect}
            loading={loading}
          />
        </DropZone>
      </div>
    </div>
  )
}
