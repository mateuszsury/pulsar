/**
 * LSP (Language Server Protocol) client service.
 *
 * Communicates with the backend Pyright LSP server via WebSocket
 * for intelligent code completion, diagnostics, hover, and more.
 */

import { api } from './api'

// LSP Types
export interface Position {
  line: number
  character: number
}

export interface Range {
  start: Position
  end: Position
}

export interface Location {
  uri: string
  range: Range
}

export interface Diagnostic {
  range: Range
  message: string
  severity?: DiagnosticSeverity
  code?: string | number
  source?: string
}

export enum DiagnosticSeverity {
  Error = 1,
  Warning = 2,
  Information = 3,
  Hint = 4,
}

export interface CompletionItem {
  label: string
  kind?: CompletionItemKind
  detail?: string
  documentation?: string | { kind: string; value: string }
  insertText?: string
  insertTextFormat?: InsertTextFormat
  textEdit?: TextEdit
  additionalTextEdits?: TextEdit[]
  sortText?: string
  filterText?: string
  preselect?: boolean
}

export enum CompletionItemKind {
  Text = 1,
  Method = 2,
  Function = 3,
  Constructor = 4,
  Field = 5,
  Variable = 6,
  Class = 7,
  Interface = 8,
  Module = 9,
  Property = 10,
  Unit = 11,
  Value = 12,
  Enum = 13,
  Keyword = 14,
  Snippet = 15,
  Color = 16,
  File = 17,
  Reference = 18,
  Folder = 19,
  EnumMember = 20,
  Constant = 21,
  Struct = 22,
  Event = 23,
  Operator = 24,
  TypeParameter = 25,
}

export enum InsertTextFormat {
  PlainText = 1,
  Snippet = 2,
}

export interface TextEdit {
  range: Range
  newText: string
}

export interface HoverMarkupContent {
  kind: string
  value: string
}

export interface HoverMarkedString {
  language: string
  value: string
}

export type HoverContents =
  | string
  | HoverMarkupContent
  | HoverMarkedString
  | (string | HoverMarkedString)[]

export interface Hover {
  contents: HoverContents
  range?: Range
}

export interface SignatureHelp {
  signatures: SignatureInformation[]
  activeSignature?: number
  activeParameter?: number
}

export interface SignatureInformation {
  label: string
  documentation?: string | { kind: string; value: string }
  parameters?: ParameterInformation[]
}

export interface ParameterInformation {
  label: string | [number, number]
  documentation?: string | { kind: string; value: string }
}

type DiagnosticsHandler = (uri: string, diagnostics: Diagnostic[]) => void

// API Response types
interface LSPStatusResponse {
  running: boolean
  initialized: boolean
}

interface LSPInitResponse {
  success: boolean
  capabilities?: Record<string, unknown>
  message?: string
}

interface LSPCompletionResponse {
  items: CompletionItem[]
}

interface LSPHoverResponse {
  hover: Hover | null
}

interface LSPDefinitionResponse {
  locations: Location[]
}

interface LSPSignatureResponse {
  signatureHelp: SignatureHelp | null
}

interface LSPSuccessResponse {
  success: boolean
}

class LSPService {
  private ws: WebSocket | null = null
  private pendingRequests = new Map<number, { resolve: (value: unknown) => void; reject: (error: Error) => void }>()
  private initialized = false
  private diagnosticsHandlers: DiagnosticsHandler[] = []
  private documentVersions = new Map<string, number>()
  private reconnectTimer: ReturnType<typeof setTimeout> | null = null

  /**
   * Initialize LSP service and connect to backend.
   */
  async initialize(rootUri: string): Promise<void> {
    // Initialize via REST API (more reliable than WebSocket for initial setup)
    const response = await api.post<LSPInitResponse>('/api/lsp/initialize', {
      rootUri,
    })

    if (response.error) {
      throw new Error(response.error)
    }

    this.initialized = true
    console.log('[LSP] Initialized with capabilities:', response.data?.capabilities)
  }

  /**
   * Connect to WebSocket for real-time notifications (diagnostics).
   */
  connectWebSocket(wsUrl: string): void {
    if (this.ws) {
      this.ws.close()
    }

    this.ws = new WebSocket(wsUrl)

    this.ws.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data)
        this.handleWebSocketMessage(message)
      } catch (e) {
        console.error('[LSP] WebSocket parse error:', e)
      }
    }

    this.ws.onerror = (error) => {
      console.error('[LSP] WebSocket error:', error)
    }

    this.ws.onclose = () => {
      console.log('[LSP] WebSocket closed')
      // Schedule reconnect
      if (this.reconnectTimer === null) {
        this.reconnectTimer = setTimeout(() => {
          this.reconnectTimer = null
          if (this.initialized) {
            this.connectWebSocket(wsUrl)
          }
        }, 5000)
      }
    }
  }

  private handleWebSocketMessage(message: { type: string; data?: Record<string, unknown> }): void {
    const { type, data } = message

    if (type === 'lsp:diagnostics') {
      // Handle diagnostics notification
      const uri = (data?.uri as string) || ''
      const diagnostics = (data?.diagnostics as Diagnostic[]) || []
      this.diagnosticsHandlers.forEach((handler) => handler(uri, diagnostics))
    } else if (type === 'lsp:response') {
      // Handle response to a request
      const requestId = data?.requestId as number
      const pending = this.pendingRequests.get(requestId)
      if (pending) {
        this.pendingRequests.delete(requestId)
        pending.resolve(data?.result)
      }
    } else if (type === 'lsp:error') {
      // Handle error
      const requestId = data?.requestId as number | undefined
      const pending = requestId !== undefined ? this.pendingRequests.get(requestId) : undefined
      if (pending) {
        this.pendingRequests.delete(requestId!)
        pending.reject(new Error((data?.message as string) || 'LSP error'))
      } else {
        console.error('[LSP] Error:', data?.message)
      }
    }
  }

  /**
   * Get completions at a position.
   */
  async completion(uri: string, line: number, character: number): Promise<CompletionItem[]> {
    if (!this.initialized) {
      return []
    }

    const response = await api.post<LSPCompletionResponse>('/api/lsp/completion', {
      uri,
      line,
      character,
    })

    if (response.error) {
      console.error('[LSP] Completion error:', response.error)
      return []
    }

    return response.data?.items || []
  }

  /**
   * Get hover information at a position.
   */
  async hover(uri: string, line: number, character: number): Promise<Hover | null> {
    if (!this.initialized) {
      return null
    }

    const response = await api.post<LSPHoverResponse>('/api/lsp/hover', {
      uri,
      line,
      character,
    })

    if (response.error) {
      console.error('[LSP] Hover error:', response.error)
      return null
    }

    return response.data?.hover || null
  }

  /**
   * Get definition locations.
   */
  async definition(uri: string, line: number, character: number): Promise<Location[]> {
    if (!this.initialized) {
      return []
    }

    const response = await api.post<LSPDefinitionResponse>('/api/lsp/definition', {
      uri,
      line,
      character,
    })

    if (response.error) {
      console.error('[LSP] Definition error:', response.error)
      return []
    }

    return response.data?.locations || []
  }

  /**
   * Get signature help at a position.
   */
  async signatureHelp(uri: string, line: number, character: number): Promise<SignatureHelp | null> {
    if (!this.initialized) {
      return null
    }

    const response = await api.post<LSPSignatureResponse>('/api/lsp/signature', {
      uri,
      line,
      character,
    })

    if (response.error) {
      console.error('[LSP] Signature error:', response.error)
      return null
    }

    return response.data?.signatureHelp || null
  }

  /**
   * Notify server that a document was opened.
   */
  async didOpen(uri: string, content: string, languageId: string = 'python'): Promise<void> {
    if (!this.initialized) {
      return
    }

    this.documentVersions.set(uri, 1)

    await api.post<LSPSuccessResponse>('/api/lsp/didOpen', {
      uri,
      content,
      languageId,
    })
  }

  /**
   * Notify server that a document changed.
   */
  async didChange(uri: string, content: string): Promise<void> {
    if (!this.initialized) {
      return
    }

    const version = (this.documentVersions.get(uri) || 0) + 1
    this.documentVersions.set(uri, version)

    await api.post<LSPSuccessResponse>('/api/lsp/didChange', {
      uri,
      content,
      version,
    })
  }

  /**
   * Notify server that a document was closed.
   */
  async didClose(uri: string): Promise<void> {
    if (!this.initialized) {
      return
    }

    this.documentVersions.delete(uri)

    await api.post<LSPSuccessResponse>('/api/lsp/didClose', {
      uri,
    })
  }

  /**
   * Subscribe to diagnostics updates.
   */
  onDiagnostics(handler: DiagnosticsHandler): () => void {
    this.diagnosticsHandlers.push(handler)
    return () => {
      const index = this.diagnosticsHandlers.indexOf(handler)
      if (index !== -1) {
        this.diagnosticsHandlers.splice(index, 1)
      }
    }
  }

  /**
   * Check if LSP is initialized.
   */
  get isInitialized(): boolean {
    return this.initialized
  }

  /**
   * Shutdown LSP service.
   */
  async shutdown(): Promise<void> {
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer)
      this.reconnectTimer = null
    }

    if (this.ws) {
      this.ws.close()
      this.ws = null
    }

    this.initialized = false
    this.documentVersions.clear()
    this.pendingRequests.clear()

    await api.post<LSPSuccessResponse>('/api/lsp/shutdown', {})
  }
}

// Export singleton instance
export const lsp = new LSPService()

// Re-export api type for LSP status checks
export { api }
export type { LSPStatusResponse }
