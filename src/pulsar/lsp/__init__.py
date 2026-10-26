"""LSP (Language Server Protocol) integration for MicroPython development.

This module provides Pyright language server integration for intelligent
code completion, diagnostics, hover information, and go-to-definition
support for MicroPython development.
"""

from pulsar.lsp.manager import LSPManager
from pulsar.lsp.protocol import JSONRPCProtocol

__all__ = ["LSPManager", "JSONRPCProtocol"]
