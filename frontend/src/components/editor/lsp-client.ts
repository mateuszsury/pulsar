/**
 * Monaco Editor LSP integration.
 *
 * Registers completion, hover, definition, and signature help providers
 * that connect to the backend Pyright LSP server.
 */

import type { Monaco } from '@monaco-editor/react'
import type { editor, languages, IDisposable, IRange } from 'monaco-editor'
import {
  lsp,
  CompletionItem,
  CompletionItemKind,
  InsertTextFormat,
  Hover,
  Location,
  SignatureHelp,
  Diagnostic,
  DiagnosticSeverity,
} from '../../services/lsp'

// Track disposables for cleanup
let registeredProviders: IDisposable[] = []

/**
 * Convert LSP CompletionItemKind to Monaco CompletionItemKind.
 */
function convertCompletionKind(kind: CompletionItemKind | undefined, monaco: Monaco): languages.CompletionItemKind {
  if (!kind) {
    return monaco.languages.CompletionItemKind.Text
  }

  const kindMap: Record<number, languages.CompletionItemKind> = {
    [CompletionItemKind.Text]: monaco.languages.CompletionItemKind.Text,
    [CompletionItemKind.Method]: monaco.languages.CompletionItemKind.Method,
    [CompletionItemKind.Function]: monaco.languages.CompletionItemKind.Function,
    [CompletionItemKind.Constructor]: monaco.languages.CompletionItemKind.Constructor,
    [CompletionItemKind.Field]: monaco.languages.CompletionItemKind.Field,
    [CompletionItemKind.Variable]: monaco.languages.CompletionItemKind.Variable,
    [CompletionItemKind.Class]: monaco.languages.CompletionItemKind.Class,
    [CompletionItemKind.Interface]: monaco.languages.CompletionItemKind.Interface,
    [CompletionItemKind.Module]: monaco.languages.CompletionItemKind.Module,
    [CompletionItemKind.Property]: monaco.languages.CompletionItemKind.Property,
    [CompletionItemKind.Unit]: monaco.languages.CompletionItemKind.Unit,
    [CompletionItemKind.Value]: monaco.languages.CompletionItemKind.Value,
    [CompletionItemKind.Enum]: monaco.languages.CompletionItemKind.Enum,
    [CompletionItemKind.Keyword]: monaco.languages.CompletionItemKind.Keyword,
    [CompletionItemKind.Snippet]: monaco.languages.CompletionItemKind.Snippet,
    [CompletionItemKind.Color]: monaco.languages.CompletionItemKind.Color,
    [CompletionItemKind.File]: monaco.languages.CompletionItemKind.File,
    [CompletionItemKind.Reference]: monaco.languages.CompletionItemKind.Reference,
    [CompletionItemKind.Folder]: monaco.languages.CompletionItemKind.Folder,
    [CompletionItemKind.EnumMember]: monaco.languages.CompletionItemKind.EnumMember,
    [CompletionItemKind.Constant]: monaco.languages.CompletionItemKind.Constant,
    [CompletionItemKind.Struct]: monaco.languages.CompletionItemKind.Struct,
    [CompletionItemKind.Event]: monaco.languages.CompletionItemKind.Event,
    [CompletionItemKind.Operator]: monaco.languages.CompletionItemKind.Operator,
    [CompletionItemKind.TypeParameter]: monaco.languages.CompletionItemKind.TypeParameter,
  }

  return kindMap[kind] ?? monaco.languages.CompletionItemKind.Text
}

/**
 * Convert LSP DiagnosticSeverity to Monaco MarkerSeverity.
 */
function convertSeverity(severity: DiagnosticSeverity | undefined, monaco: Monaco): number {
  switch (severity) {
    case DiagnosticSeverity.Error:
      return monaco.MarkerSeverity.Error
    case DiagnosticSeverity.Warning:
      return monaco.MarkerSeverity.Warning
    case DiagnosticSeverity.Information:
      return monaco.MarkerSeverity.Info
    case DiagnosticSeverity.Hint:
      return monaco.MarkerSeverity.Hint
    default:
      return monaco.MarkerSeverity.Info
  }
}

/**
 * Convert LSP documentation to string or markdown.
 */
function convertDocumentation(
  doc: string | { kind: string; value: string } | undefined
): string | { value: string } | undefined {
  if (!doc) {
    return undefined
  }

  if (typeof doc === 'string') {
    return doc
  }

  if (doc.kind === 'markdown') {
    return { value: doc.value }
  }

  return doc.value
}

/**
 * Convert LSP CompletionItem to Monaco CompletionItem.
 */
function convertCompletionItem(item: CompletionItem, monaco: Monaco, range: IRange): languages.CompletionItem {
  const result: languages.CompletionItem = {
    label: item.label,
    kind: convertCompletionKind(item.kind, monaco),
    detail: item.detail,
    documentation: convertDocumentation(item.documentation),
    insertText: item.insertText || item.label,
    range,
    sortText: item.sortText,
    filterText: item.filterText,
    preselect: item.preselect,
  }

  // Handle snippet format
  if (item.insertTextFormat === InsertTextFormat.Snippet) {
    result.insertTextRules = monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet
  }

  return result
}

/**
 * Convert LSP Hover to Monaco Hover.
 */
function convertHover(hover: Hover | null): languages.Hover | null {
  if (!hover) {
    return null
  }

  const contents: { value: string }[] = []

  if (typeof hover.contents === 'string') {
    contents.push({ value: hover.contents })
  } else if (Array.isArray(hover.contents)) {
    // Array contains string | HoverMarkedString
    hover.contents.forEach((content) => {
      if (typeof content === 'string') {
        contents.push({ value: content })
      } else {
        // HoverMarkedString has language and value
        contents.push({ value: `\`\`\`${content.language}\n${content.value}\n\`\`\`` })
      }
    })
  } else if ('kind' in hover.contents) {
    // HoverMarkupContent
    contents.push({ value: hover.contents.value })
  } else if ('language' in hover.contents) {
    // HoverMarkedString (non-array)
    contents.push({ value: `\`\`\`${hover.contents.language}\n${hover.contents.value}\n\`\`\`` })
  }

  const result: languages.Hover = { contents }

  if (hover.range) {
    result.range = {
      startLineNumber: hover.range.start.line + 1,
      startColumn: hover.range.start.character + 1,
      endLineNumber: hover.range.end.line + 1,
      endColumn: hover.range.end.character + 1,
    }
  }

  return result
}

/**
 * Convert LSP Location to Monaco Location.
 */
function convertLocation(location: Location, monaco: Monaco): languages.Location {
  return {
    uri: monaco.Uri.parse(location.uri),
    range: {
      startLineNumber: location.range.start.line + 1,
      startColumn: location.range.start.character + 1,
      endLineNumber: location.range.end.line + 1,
      endColumn: location.range.end.character + 1,
    },
  }
}

/**
 * Convert LSP SignatureHelp to Monaco SignatureHelp.
 */
function convertSignatureHelp(help: SignatureHelp | null): languages.SignatureHelpResult | null {
  if (!help || !help.signatures.length) {
    return null
  }

  return {
    value: {
      signatures: help.signatures.map((sig) => ({
        label: sig.label,
        documentation: convertDocumentation(sig.documentation),
        parameters:
          sig.parameters?.map((param) => ({
            label: param.label as string | [number, number],
            documentation: convertDocumentation(param.documentation),
          })) || [],
      })),
      activeSignature: help.activeSignature ?? 0,
      activeParameter: help.activeParameter ?? 0,
    },
    dispose: () => {},
  }
}

/**
 * Register LSP-backed language providers for Monaco.
 *
 * Call this after Monaco is loaded to replace the basic MicroPython
 * completions with full LSP support.
 */
export function registerLSPProviders(monaco: Monaco): void {
  // Clean up any existing registrations
  disposeProviders()

  // Completion provider
  const completionProvider = monaco.languages.registerCompletionItemProvider('python', {
    triggerCharacters: ['.', ' ', '(', ',', '[', '{', "'", '"'],

    async provideCompletionItems(
      model: editor.ITextModel,
      position: { lineNumber: number; column: number }
    ): Promise<languages.CompletionList> {
      if (!lsp.isInitialized) {
        return { suggestions: [] }
      }

      const uri = model.uri.toString()
      const line = position.lineNumber - 1
      const character = position.column - 1

      try {
        const items = await lsp.completion(uri, line, character)

        const word = model.getWordUntilPosition(position)
        const range: IRange = {
          startLineNumber: position.lineNumber,
          startColumn: word.startColumn,
          endLineNumber: position.lineNumber,
          endColumn: word.endColumn,
        }

        return {
          suggestions: items.map((item) => convertCompletionItem(item, monaco, range)),
        }
      } catch (error) {
        console.error('[LSP] Completion error:', error)
        return { suggestions: [] }
      }
    },
  })
  registeredProviders.push(completionProvider)

  // Hover provider
  const hoverProvider = monaco.languages.registerHoverProvider('python', {
    async provideHover(
      model: editor.ITextModel,
      position: { lineNumber: number; column: number }
    ): Promise<languages.Hover | null> {
      if (!lsp.isInitialized) {
        return null
      }

      const uri = model.uri.toString()
      const line = position.lineNumber - 1
      const character = position.column - 1

      try {
        const hover = await lsp.hover(uri, line, character)
        return convertHover(hover)
      } catch (error) {
        console.error('[LSP] Hover error:', error)
        return null
      }
    },
  })
  registeredProviders.push(hoverProvider)

  // Definition provider (Go to Definition, Ctrl+Click)
  const definitionProvider = monaco.languages.registerDefinitionProvider('python', {
    async provideDefinition(
      model: editor.ITextModel,
      position: { lineNumber: number; column: number }
    ): Promise<languages.Location[] | null> {
      if (!lsp.isInitialized) {
        return null
      }

      const uri = model.uri.toString()
      const line = position.lineNumber - 1
      const character = position.column - 1

      try {
        const locations = await lsp.definition(uri, line, character)
        return locations.map((loc) => convertLocation(loc, monaco))
      } catch (error) {
        console.error('[LSP] Definition error:', error)
        return null
      }
    },
  })
  registeredProviders.push(definitionProvider)

  // Signature help provider
  const signatureProvider = monaco.languages.registerSignatureHelpProvider('python', {
    signatureHelpTriggerCharacters: ['(', ','],
    signatureHelpRetriggerCharacters: [','],

    async provideSignatureHelp(
      model: editor.ITextModel,
      position: { lineNumber: number; column: number }
    ): Promise<languages.SignatureHelpResult | null> {
      if (!lsp.isInitialized) {
        return null
      }

      const uri = model.uri.toString()
      const line = position.lineNumber - 1
      const character = position.column - 1

      try {
        const help = await lsp.signatureHelp(uri, line, character)
        return convertSignatureHelp(help)
      } catch (error) {
        console.error('[LSP] Signature error:', error)
        return null
      }
    },
  })
  registeredProviders.push(signatureProvider)

  console.log('[LSP] Monaco providers registered')
}

/**
 * Set diagnostics on a Monaco model.
 */
export function setDiagnostics(monaco: Monaco, model: editor.ITextModel, diagnostics: Diagnostic[]): void {
  const markers = diagnostics.map((d) => ({
    severity: convertSeverity(d.severity, monaco),
    message: d.message,
    startLineNumber: d.range.start.line + 1,
    startColumn: d.range.start.character + 1,
    endLineNumber: d.range.end.line + 1,
    endColumn: d.range.end.character + 1,
    source: d.source || 'pyright',
    code: d.code?.toString(),
  }))

  monaco.editor.setModelMarkers(model, 'pyright', markers)
}

/**
 * Dispose all registered providers.
 */
export function disposeProviders(): void {
  registeredProviders.forEach((provider) => provider.dispose())
  registeredProviders = []
}

/**
 * Initialize LSP for a workspace.
 */
export async function initializeLSP(rootUri: string): Promise<boolean> {
  try {
    await lsp.initialize(rootUri)
    return true
  } catch (error) {
    console.error('[LSP] Initialization failed:', error)
    return false
  }
}

/**
 * Notify LSP that a document was opened.
 */
export async function documentOpened(uri: string, content: string): Promise<void> {
  await lsp.didOpen(uri, content)
}

/**
 * Notify LSP that a document changed.
 */
export async function documentChanged(uri: string, content: string): Promise<void> {
  await lsp.didChange(uri, content)
}

/**
 * Notify LSP that a document was closed.
 */
export async function documentClosed(uri: string): Promise<void> {
  await lsp.didClose(uri)
}

/**
 * Subscribe to diagnostics updates for a handler function.
 */
export function onDiagnostics(handler: (uri: string, diagnostics: Diagnostic[]) => void): () => void {
  return lsp.onDiagnostics(handler)
}
