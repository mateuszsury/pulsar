import { X, Plus } from 'lucide-react'

interface OpenFile {
  path: string
  name: string
  modified: boolean
}

interface EditorTabsProps {
  files: OpenFile[]
  activeFile: string
  onSelect: (path: string) => void
  onClose: (path: string) => void
  onNew: () => void
}

export function EditorTabs({ files, activeFile, onSelect, onClose, onNew }: EditorTabsProps) {
  return (
    <div className="flex items-center flex-1 overflow-x-auto scrollbar-none">
      {files.map(file => (
        <div
          key={file.path}
          className={`flex items-center gap-1.5 px-3 h-8 text-sm border-r border-vscode-border cursor-pointer group ${
            file.path === activeFile
              ? 'bg-vscode-bg text-vscode-text'
              : 'bg-vscode-sidebar text-vscode-text-dim hover:text-vscode-text'
          }`}
          onClick={() => onSelect(file.path)}
        >
          <span className="flex items-center gap-1 min-w-0">
            {file.modified && (
              <span className="w-2 h-2 rounded-full bg-vscode-accent" />
            )}
            <span className="truncate max-w-32">{file.name}</span>
          </span>

          <button
            className="p-0.5 rounded opacity-0 group-hover:opacity-100 hover:bg-vscode-hover"
            onClick={(e) => {
              e.stopPropagation()
              onClose(file.path)
            }}
          >
            <X size={12} />
          </button>
        </div>
      ))}

      <button
        className="flex items-center justify-center w-8 h-8 text-vscode-text-dim hover:text-vscode-text hover:bg-vscode-hover"
        onClick={onNew}
      >
        <Plus size={14} />
      </button>
    </div>
  )
}
