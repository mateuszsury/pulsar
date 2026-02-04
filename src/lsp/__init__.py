"""LSP (Language Server Protocol) integration for MicroPython development.

This module provides Pyright language server integration for intelligent
code completion, diagnostics, hover information, and go-to-definition
support for MicroPython development.
"""

from lsp.manager import LSPManager
from lsp.protocol import JSONRPCProtocol

__all__ = ["LSPManager", "JSONRPCProtocol"]
