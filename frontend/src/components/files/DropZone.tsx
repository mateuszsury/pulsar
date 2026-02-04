import { useState, DragEvent, ReactNode } from 'react'
import { Upload } from 'lucide-react'

interface DropZoneProps {
  onDrop: (files: FileList) => void
  children: ReactNode
}

export function DropZone({ onDrop, children }: DropZoneProps) {
  const [isDragging, setIsDragging] = useState(false)

  const handleDragEnter = (e: DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(true)
  }

  const handleDragLeave = (e: DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(false)
  }

  const handleDragOver = (e: DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
  }

  const handleDrop = (e: DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(false)

    if (e.dataTransfer.files?.length) {
      onDrop(e.dataTransfer.files)
    }
  }

  return (
    <div
      className="relative h-full"
      onDragEnter={handleDragEnter}
      onDragLeave={handleDragLeave}
      onDragOver={handleDragOver}
      onDrop={handleDrop}
    >
      {children}

      {isDragging && (
        <div className="absolute inset-0 flex items-center justify-center bg-vscode-accent/10 border-2 border-dashed border-vscode-accent">
          <div className="flex flex-col items-center gap-2 text-vscode-accent">
            <Upload size={32} />
            <span className="text-sm font-medium">Drop files to upload</span>
          </div>
        </div>
      )}
    </div>
  )
}
