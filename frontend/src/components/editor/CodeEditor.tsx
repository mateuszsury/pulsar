import { useRef, useState, useCallback, useEffect, useMemo } from 'react'
import Editor, { OnMount, loader, Monaco } from '@monaco-editor/react'
import type { editor } from 'monaco-editor'
import { Play, Save, FileCode, AlertCircle, CheckCircle } from 'lucide-react'
import { Button } from '../common/Button'
import { Tooltip } from '../common/Tooltip'
import { EditorTabs } from './EditorTabs'
import { useDeviceStore, selectSelectedDevice } from '../../stores/deviceStore'
import { useSettingsStore } from '../../stores/settingsStore'
import { useConsoleStore } from '../../stores/consoleStore'
import { api } from '../../services/api'
import { registerMicroPythonCompletions } from './micropython-completions'
import {
  registerLSPProviders,
  initializeLSP,
  documentOpened,
  documentChanged,
  documentClosed,
  onDiagnostics,
  setDiagnostics,
  disposeProviders,
} from './lsp-client'
import type { Diagnostic, LSPStatusResponse } from '../../services/lsp'

// Track initialization state
let basicCompletionsRegistered = false
let lspInitialized = false
let monacoInstance: Monaco | null = null

// Initialize Monaco - first register basic completions, then try LSP
loader.init().then(async (monaco) => {
  monacoInstance = monaco

  // Register basic MicroPython completions as fallback
  if (!basicCompletionsRegistered) {
    registerMicroPythonCompletions(monaco)
    basicCompletionsRegistered = true
  }

  // Try to initialize LSP (enhances completions)
  try {
    const success = await initializeLSP('file:///')
    if (success) {
      registerLSPProviders(monaco)
      lspInitialized = true
      console.log('[Editor] LSP initialized successfully')
    }
  } catch (error) {
    console.warn('[Editor] LSP initialization failed, using basic completions:', error)
  }
})

interface OpenFile {
  path: string
  name: string
  content: string
  modified: boolean
  diagnosticCount?: number
}

// Debounce helper
function debounce<T extends (...args: any[]) => any>(
  fn: T,
  delay: number
): (...args: Parameters<T>) => void {
  let timeoutId: ReturnType<typeof setTimeout>
  return (...args: Parameters<T>) => {
    clearTimeout(timeoutId)
    timeoutId = setTimeout(() => fn(...args), delay)
  }
}

export function CodeEditor() {
  const editorRef = useRef<editor.IStandaloneCodeEditor | null>(null)
  const monacoRef = useRef<Monaco | null>(null)
  const selectedDevice = useDeviceStore(selectSelectedDevice)
  const { fontSize, tabSize, wordWrap, minimap } = useSettingsStore()
  const { execute } = useConsoleStore()

  const [openFiles, setOpenFiles] = useState<OpenFile[]>([
    {
      path: 'untitled.py',
      name: 'untitled.py',
      content: '# Write your MicroPython code here\n\nprint("Hello, ESP32!")\n',
      modified: false,
      diagnosticCount: 0,
    },
  ])
  const [activeFile, setActiveFile] = useState<string>('untitled.py')
  const [lspStatus, setLspStatus] = useState<'loading' | 'connected' | 'disconnected'>('loading')

  const currentFile = openFiles.find((f) => f.path === activeFile)
  const port = selectedDevice?.port

  // Convert file path to LSP URI
  const fileToUri = useCallback((path: string): string => {
    return `file:///${path.replace(/^\//, '')}`
  }, [])

  // Subscribe to LSP diagnostics
  useEffect(() => {
    const unsubscribe = onDiagnostics((uri: string, diagnostics: Diagnostic[]) => {
      // Update diagnostic count for the file
      const path = uri.replace('file:///', '/')
      setOpenFiles((prev) =>
        prev.map((f) =>
          f.path === path || fileToUri(f.path) === uri
            ? { ...f, diagnosticCount: diagnostics.length }
            : f
        )
      )

      // Update Monaco markers if this is the active file
      if (monacoRef.current && editorRef.current) {
        const model = editorRef.current.getModel()
        if (model && model.uri.toString() === uri) {
          setDiagnostics(monacoRef.current, model, diagnostics)
        }
      }
    })

    return () => {
      unsubscribe()
    }
  }, [fileToUri])

  // Check LSP status periodically
  useEffect(() => {
    const checkStatus = async () => {
      try {
        const response = await api.get<LSPStatusResponse>('/api/lsp/status')
        if (response.data?.initialized) {
          setLspStatus('connected')
        } else if (response.data?.running) {
          setLspStatus('loading')
        } else {
          setLspStatus('disconnected')
        }
      } catch {
        setLspStatus('disconnected')
      }
    }

    checkStatus()
    const interval = setInterval(checkStatus, 30000)
    return () => clearInterval(interval)
  }, [])

  // Notify LSP when active file changes
  useEffect(() => {
    if (currentFile && lspInitialized) {
      const uri = fileToUri(currentFile.path)
      documentOpened(uri, currentFile.content)

      return () => {
        documentClosed(uri)
      }
    }
  }, [activeFile, fileToUri])

  // Debounced document change notification
  const debouncedDidChange = useMemo(
    () =>
      debounce((uri: string, content: string) => {
        if (lspInitialized) {
          documentChanged(uri, content)
        }
      }, 300),
    []
  )

  const handleEditorMount: OnMount = (editor, monaco) => {
    editorRef.current = editor
    monacoRef.current = monaco

    // If LSP was initialized before mount, register providers
    if (lspInitialized && !monacoInstance) {
      registerLSPProviders(monaco)
    }

    // Notify LSP of opened document
    if (currentFile && lspInitialized) {
      const uri = fileToUri(currentFile.path)
      documentOpened(uri, currentFile.content)
    }
  }

  const handleChange = (value: string | undefined) => {
    if (!value || !currentFile) return

    setOpenFiles((prev) =>
      prev.map((f) =>
        f.path === activeFile ? { ...f, content: value, modified: true } : f
      )
    )

    // Notify LSP of change
    const uri = fileToUri(currentFile.path)
    debouncedDidChange(uri, value)
  }

  const handleRun = useCallback(async () => {
    if (!port || !currentFile) return

    const code = currentFile.content
    await execute(port, code)
  }, [port, currentFile, execute])

  const handleSave = useCallback(async () => {
    if (!port || !currentFile) return

    // If it's an untitled file, prompt for path
    let savePath = currentFile.path
    if (savePath === 'untitled.py' || savePath.startsWith('untitled-')) {
      const name = prompt('Enter file name:', 'main.py')
      if (!name) return
      savePath = `/${name}`
    }

    const result = await api.writeFile(port, savePath, currentFile.content)
    if (result.data?.success) {
      setOpenFiles((prev) =>
        prev.map((f) =>
          f.path === activeFile
            ? {
                ...f,
                path: savePath,
                name: savePath.split('/').pop() || savePath,
                modified: false,
              }
            : f
        )
      )
    }
  }, [port, currentFile, activeFile])

  const handleCloseTab = (path: string) => {
    const file = openFiles.find((f) => f.path === path)
    if (file?.modified) {
      if (!confirm(`${file.name} has unsaved changes. Close anyway?`)) {
        return
      }
    }

    // Notify LSP of closed document
    if (lspInitialized) {
      documentClosed(fileToUri(path))
    }

    setOpenFiles((prev) => prev.filter((f) => f.path !== path))

    if (activeFile === path && openFiles.length > 1) {
      const remaining = openFiles.filter((f) => f.path !== path)
      setActiveFile(remaining[0]?.path ?? '')
    }
  }

  const handleNewFile = () => {
    const newPath = `untitled-${Date.now()}.py`
    setOpenFiles((prev) => [
      ...prev,
      {
        path: newPath,
        name: 'untitled.py',
        content: '# New file\n',
        modified: false,
        diagnosticCount: 0,
      },
    ])
    setActiveFile(newPath)
  }

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      disposeProviders()
    }
  }, [])

  return (
    <div className="flex flex-col h-full">
      {/* Tabs and toolbar */}
      <div className="flex items-center border-b border-vscode-border">
        <EditorTabs
          files={openFiles}
          activeFile={activeFile}
          onSelect={setActiveFile}
          onClose={handleCloseTab}
          onNew={handleNewFile}
        />

        <div className="flex items-center gap-1 px-2">
          {/* LSP Status indicator */}
          <Tooltip
            content={
              lspStatus === 'connected'
                ? 'Pyright LSP connected'
                : lspStatus === 'loading'
                ? 'LSP initializing...'
                : 'LSP disconnected'
            }
          >
            <div className="flex items-center px-1">
              {lspStatus === 'connected' ? (
                <CheckCircle size={12} className="text-green-500" />
              ) : lspStatus === 'loading' ? (
                <AlertCircle size={12} className="text-yellow-500 animate-pulse" />
              ) : (
                <AlertCircle size={12} className="text-gray-500" />
              )}
            </div>
          </Tooltip>

          <div className="w-px h-4 bg-vscode-border mx-1" />

          <Tooltip content="Run (F5)">
            <Button
              icon
              size="sm"
              variant="ghost"
              onClick={handleRun}
              disabled={!port}
            >
              <Play size={14} className="text-vscode-success" />
            </Button>
          </Tooltip>

          <Tooltip content="Save (Ctrl+S)">
            <Button
              icon
              size="sm"
              variant="ghost"
              onClick={handleSave}
              disabled={!port}
            >
              <Save size={14} />
            </Button>
          </Tooltip>
        </div>
      </div>

      {/* Editor */}
      <div className="flex-1">
        {currentFile ? (
          <Editor
            height="100%"
            language="python"
            theme="vs-dark"
            value={currentFile.content}
            onChange={handleChange}
            onMount={handleEditorMount}
            options={{
              fontSize,
              tabSize,
              wordWrap: wordWrap ? 'on' : 'off',
              minimap: { enabled: minimap },
              lineNumbers: 'on',
              scrollBeyondLastLine: false,
              automaticLayout: true,
              fontFamily: 'Consolas, Menlo, Monaco, "Courier New", monospace',
              fontLigatures: true,
              renderLineHighlight: 'line',
              cursorBlinking: 'smooth',
              smoothScrolling: true,
              padding: { top: 8 },
              quickSuggestions: {
                other: true,
                comments: false,
                strings: true,
              },
              suggestOnTriggerCharacters: true,
              acceptSuggestionOnEnter: 'on',
              tabCompletion: 'on',
              parameterHints: { enabled: true },
            }}
          />
        ) : (
          <div className="flex flex-col items-center justify-center h-full text-vscode-text-dim">
            <FileCode size={48} className="mb-4 opacity-50" />
            <p>No file open</p>
            <Button
              variant="ghost"
              size="sm"
              className="mt-2"
              onClick={handleNewFile}
            >
              Create new file
            </Button>
          </div>
        )}
      </div>
    </div>
  )
}
