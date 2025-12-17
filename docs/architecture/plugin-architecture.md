# Plugin Architecture

## Scope

This document describes the ununseptium plugin system for extending library functionality.

### Non-Goals

- Plugin implementation tutorials (see examples)
- Third-party plugin support policies

## Definitions

| Term | Definition |
|------|------------|
| Plugin | Dynamically loaded extension module |
| Hook | Extension point in the library |
| Entry Point | Python packaging mechanism for discovery |

See [Glossary](../glossary.md) for additional terminology.

## Overview

The plugin system enables extending ununseptium without modifying core code:

```mermaid
graph TB
    subgraph "Core Library"
        HOOKS[Extension Hooks]
        REGISTRY[Plugin Registry]
    end

    subgraph "Discovery"
        ENTRY[Entry Points]
        SCAN[Plugin Scanner]
    end

    subgraph "Plugins"
        P1[Plugin A]
        P2[Plugin B]
        P3[Plugin C]
    end

    ENTRY --> SCAN
    SCAN --> REGISTRY
    REGISTRY --> HOOKS
    P1 --> ENTRY
    P2 --> ENTRY
    P3 --> ENTRY

```text
## Plugin Types

| Type | Purpose | Hook Location |
|------|---------|---------------|
| Screener | Custom watchlist sources | `kyc.screening` |
| Detector | Custom typology detection | `aml.typology` |
| Encryptor | Custom encryption backends | `security.encryption` |
| Model | Custom ML models | `ai.models` |
| Exporter | Custom audit export formats | `security.audit` |

## Entry Point Configuration

Plugins register via `pyproject.toml`:

```toml
[project.entry-points."ununseptium.plugins"]
my_plugin = "my_package.plugin:MyPlugin"

```text
Or `setup.py`:

```python
entry_points={
    "ununseptium.plugins": [
        "my_plugin = my_package.plugin:MyPlugin",
    ],
}

```text
## Plugin Interface

### Base Plugin Class

```python
from abc import ABC, abstractmethod
from typing import Any

class Plugin(ABC):
    """Base class for all plugins."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique plugin identifier."""
        ...

    @property
    @abstractmethod
    def version(self) -> str:
        """Plugin version string."""
        ...

    def initialize(self, config: dict[str, Any]) -> None:
        """Called when plugin is loaded."""
        pass

    def shutdown(self) -> None:
        """Called when plugin is unloaded."""
        pass

```text
### Hook-Specific Interfaces

| Hook | Interface | Required Methods |
|------|-----------|------------------|
| Screener | `ScreenerPlugin` | `screen(name) -> list[Match]` |
| Detector | `DetectorPlugin` | `detect(txns) -> list[Alert]` |
| Encryptor | `EncryptorPlugin` | `encrypt(data)`, `decrypt(data)` |

## Plugin Lifecycle

```mermaid
sequenceDiagram
    participant App
    participant Registry
    participant Plugin

    App->>Registry: discover_plugins()
    Registry->>Plugin: load()
    Registry->>Plugin: validate()
    Registry->>Plugin: initialize(config)

    Note over App,Plugin: Plugin is active

    App->>Plugin: hook_method()
    Plugin-->>App: result

    Note over App,Plugin: Shutdown

    App->>Registry: shutdown_plugins()
    Registry->>Plugin: shutdown()
    Registry->>Plugin: unload()

```text
### Lifecycle Stages

| Stage | Description | Can Fail |
|-------|-------------|----------|
| Discovery | Find entry points | Yes |
| Load | Import module | Yes |
| Validate | Check interface | Yes |
| Initialize | Setup plugin | Yes |
| Active | Ready for use | - |
| Shutdown | Cleanup | No (best effort) |
| Unload | Release resources | No |

## Plugin Discovery

```python
from ununseptium.plugins import PluginRegistry

registry = PluginRegistry()
registry.discover()

for plugin in registry.plugins:
    print(f"{plugin.name} v{plugin.version}")

```text
### Discovery Process

$$\text{Plugins} = \bigcup_{e \in \text{EntryPoints}} \text{Load}(e)$$

## Configuration

Plugins receive configuration during initialization:

```python
# In ununseptium config
plugins:
  my_plugin:
    api_key: "xxx"
    timeout: 30

```text

```python
class MyPlugin(Plugin):
    def initialize(self, config: dict[str, Any]) -> None:
        self.api_key = config.get("api_key")
        self.timeout = config.get("timeout", 60)

```text
## Error Handling

| Error | Handling |
|-------|----------|
| Load failure | Skip plugin, log warning |
| Validation failure | Skip plugin, log error |
| Initialize failure | Skip plugin, log error |
| Runtime error | Catch, log, continue |
| Shutdown error | Log, continue shutdown |

## Security Considerations

| Risk | Mitigation |
|------|------------|
| Malicious plugins | Only use trusted sources |
| Code injection | Sandboxing (future) |
| Resource exhaustion | Timeout enforcement |
| Information leakage | Audit plugin calls |

## Example Plugin

### Custom Screener

```python
from ununseptium.plugins import ScreenerPlugin
from ununseptium.kyc import Match

class CustomWatchlistPlugin(ScreenerPlugin):
    name = "custom_watchlist"
    version = "1.0.0"

    def initialize(self, config: dict) -> None:
        self.watchlist_url = config["watchlist_url"]
        self._load_watchlist()

    def screen(self, name: str) -> list[Match]:
        matches = []
        for entry in self.watchlist:
            score = self._fuzzy_match(name, entry.name)
            if score > self.threshold:
                matches.append(Match(
                    name=entry.name,
                    score=score,
                    source=self.name,
                ))
        return matches

```text
## Plugin Registry API

| Method | Description |
|--------|-------------|
| `discover()` | Find and load plugins |
| `get(name)` | Get plugin by name |
| `plugins` | List all plugins |
| `enable(name)` | Enable a plugin |
| `disable(name)` | Disable a plugin |
| `shutdown()` | Shutdown all plugins |

## Related Documentation

- [Architecture Overview](overview.md)
- [Glossary](../glossary.md)

## References

- [Python Entry Points](https://packaging.python.org/en/latest/specifications/entry-points/)
- [Plugin Architecture Patterns](https://refactoring.guru/design-patterns/plugin)
