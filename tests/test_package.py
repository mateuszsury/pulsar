"""Packaging checks that do not require a GUI or connected board."""
import ast
from pathlib import Path
import tomllib

ROOT = Path(__file__).resolve().parents[1]

def test_entry_points_resolve_to_packaged_callables():
    config = tomllib.loads((ROOT / 'pyproject.toml').read_text())
    entries = list(config['project']['scripts'].values()) + list(config['project']['entry-points']['mcp.servers'].values())
    for entry in entries:
        module, function = entry.split(':')
        path = ROOT / 'src' / (module.replace('.', '/') + '.py')
        tree = ast.parse(path.read_text())
        assert any(isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == function for node in tree.body), entry

def test_internal_absolute_imports_use_package_namespace():
    internal = {'core', 'server', 'serial_comm', 'mcp_impl', 'tools', 'ui', 'lsp'}
    for path in (ROOT / 'src/pulsar').rglob('*.py'):
        for node in ast.walk(ast.parse(path.read_text())):
            if isinstance(node, ast.ImportFrom) and not node.level and node.module:
                assert node.module.split('.')[0] not in internal, (path, node.module)
