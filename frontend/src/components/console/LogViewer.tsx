import { useEffect, useRef } from 'react'
import { useConsoleStore } from '../../stores/consoleStore'

interface LogViewerProps {
  port: string
}

export function LogViewer({ port }: LogViewerProps) {
  const { outputs } = useConsoleStore()
  const containerRef = useRef<HTMLDivElement>(null)

  // outputs is now a string, split by lines for display
  const outputText = outputs.get(port) ?? ''
  const lines = outputText ? outputText.split('\n') : []

  // Auto-scroll to bottom
  useEffect(() => {
    if (containerRef.current) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight
    }
  }, [lines])

  return (
    <div
      ref={containerRef}
      className="h-full overflow-auto font-mono text-xs p-2 bg-vscode-bg"
    >
      {lines.map((line, index) => (
        <div
          key={index}
          className={`whitespace-pre-wrap ${
            line.includes('Error') || line.includes('Traceback')
              ? 'text-vscode-error'
              : line.includes('Warning')
              ? 'text-vscode-warning'
              : 'text-vscode-text'
          }`}
        >
          {line || '\u00A0'}
        </div>
      ))}
    </div>
  )
}
