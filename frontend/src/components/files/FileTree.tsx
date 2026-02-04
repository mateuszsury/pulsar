import { ChevronRight, ChevronDown, File, Folder, FolderOpen } from 'lucide-react'
import { FileInfo } from '../../services/api'

interface FileTreeProps {
  files: FileInfo[]
  currentPath: string
  expandedDirs: Set<string>
  selectedPath: string | null
  onToggleDir: (path: string) => void
  onNavigate: (path: string) => void
  onSelect: (file: FileInfo) => void
  loading: boolean
}

export function FileTree({
  files,
  currentPath,
  expandedDirs,
  selectedPath,
  onToggleDir,
  onNavigate,
  onSelect,
  loading,
}: FileTreeProps) {
  // Sort files: directories first, then by name
  const sortedFiles = [...files].sort((a, b) => {
    if (a.is_dir !== b.is_dir) {
      return a.is_dir ? -1 : 1
    }
    return a.name.localeCompare(b.name)
  })

  const getFileIcon = (file: FileInfo) => {
    if (file.is_dir) {
      const isExpanded = expandedDirs.has(file.path)
      return isExpanded ? (
        <FolderOpen size={14} className="text-vscode-warning" />
      ) : (
        <Folder size={14} className="text-vscode-warning" />
      )
    }

    // Color based on extension
    const ext = file.name.split('.').pop()?.toLowerCase()
    const iconColors: Record<string, string> = {
      py: 'text-vscode-info',
      json: 'text-vscode-warning',
      txt: 'text-vscode-text-dim',
      md: 'text-vscode-accent',
      html: 'text-vscode-error',
      css: 'text-vscode-info',
      js: 'text-vscode-warning',
    }

    return <File size={14} className={iconColors[ext ?? ''] ?? 'text-vscode-text-dim'} />
  }

  const formatSize = (size: number) => {
    if (size < 1024) return `${size} B`
    if (size < 1024 * 1024) return `${(size / 1024).toFixed(1)} KB`
    return `${(size / (1024 * 1024)).toFixed(1)} MB`
  }

  const handleClick = (file: FileInfo) => {
    onSelect(file)
    if (file.is_dir) {
      onNavigate(file.path)
    }
  }

  const handleDoubleClick = (file: FileInfo) => {
    if (file.is_dir) {
      onToggleDir(file.path)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center py-8 text-vscode-text-dim">
        Loading...
      </div>
    )
  }

  if (files.length === 0) {
    return (
      <div className="flex items-center justify-center py-8 text-vscode-text-dim">
        Empty directory
      </div>
    )
  }

  return (
    <div className="py-1">
      {/* Parent directory link */}
      {currentPath !== '/' && (
        <div
          className="flex items-center gap-1.5 px-2 py-0.5 text-sm cursor-pointer hover:bg-vscode-hover text-vscode-text-dim"
          onClick={() => {
            const parent = currentPath.split('/').slice(0, -1).join('/') || '/'
            onNavigate(parent)
          }}
        >
          <ChevronRight size={14} className="rotate-180" />
          <span>..</span>
        </div>
      )}

      {/* Files */}
      {sortedFiles.map(file => (
        <div
          key={file.path}
          className={`flex items-center gap-1.5 px-2 py-0.5 text-sm cursor-pointer ${
            selectedPath === file.path
              ? 'bg-vscode-selection'
              : 'hover:bg-vscode-hover'
          }`}
          onClick={() => handleClick(file)}
          onDoubleClick={() => handleDoubleClick(file)}
        >
          {file.is_dir && (
            <span className="w-3">
              {expandedDirs.has(file.path) ? (
                <ChevronDown size={12} />
              ) : (
                <ChevronRight size={12} />
              )}
            </span>
          )}

          {!file.is_dir && <span className="w-3" />}

          {getFileIcon(file)}

          <span className="flex-1 truncate">{file.name}</span>

          {!file.is_dir && (
            <span className="text-xs text-vscode-text-dim">
              {formatSize(file.size)}
            </span>
          )}
        </div>
      ))}
    </div>
  )
}
