"""Plugin base classes and interfaces.

Provides base plugin class and metadata definitions.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import UTC, datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class PluginType(str, Enum):
    """Types of plugins."""

    VERIFIER = "verifier"
    DETECTOR = "detector"
    REPORTER = "reporter"
    CONNECTOR = "connector"
    PROCESSOR = "processor"
    CUSTOM = "custom"


class PluginMetadata(BaseModel):
    """Metadata for a plugin.

    Attributes:
        name: Plugin name.
        version: Plugin version.
        description: Plugin description.
        author: Plugin author.
        plugin_type: Type of plugin.
        dependencies: Required dependencies.
        config_schema: Configuration schema.
        tags: Plugin tags.
    """

    name: str
    version: str = "1.0.0"
    description: str = ""
    author: str = ""
    plugin_type: PluginType = PluginType.CUSTOM
    dependencies: list[str] = Field(default_factory=list)
    config_schema: dict[str, Any] = Field(default_factory=dict)
    tags: list[str] = Field(default_factory=list)


class PluginState(str, Enum):
    """Plugin lifecycle states."""

    UNLOADED = "unloaded"
    LOADED = "loaded"
    INITIALIZED = "initialized"
    RUNNING = "running"
    STOPPED = "stopped"
    ERROR = "error"


class Plugin(ABC):
    """Abstract base class for plugins.

    Plugins must inherit from this class and implement
    the required methods.

    Example:
        ```python
        from ununseptium.plugins import Plugin, PluginMetadata

        class MyPlugin(Plugin):
            @classmethod
            def metadata(cls) -> PluginMetadata:
                return PluginMetadata(
                    name="my_plugin",
                    version="1.0.0",
                    description="My custom plugin"
                )

            def initialize(self, config=None):
                self.config = config or {}

            def execute(self, data):
                return {"processed": True}

            def shutdown(self):
                pass
        ```
    """

    def __init__(self) -> None:
        """Initialize plugin instance."""
        self._state = PluginState.UNLOADED
        self._error: Exception | None = None
        self._initialized_at: datetime | None = None

    @classmethod
    @abstractmethod
    def metadata(cls) -> PluginMetadata:
        """Return plugin metadata.

        Returns:
            PluginMetadata for this plugin.
        """
        ...

    @abstractmethod
    def initialize(self, config: dict[str, Any] | None = None) -> None:
        """Initialize the plugin.

        Args:
            config: Plugin configuration.
        """
        ...

    @abstractmethod
    def execute(self, data: Any) -> Any:
        """Execute the plugin's main function.

        Args:
            data: Input data.

        Returns:
            Plugin output.
        """
        ...

    @abstractmethod
    def shutdown(self) -> None:
        """Shutdown the plugin and cleanup resources."""
        ...

    @property
    def state(self) -> PluginState:
        """Current plugin state."""
        return self._state

    @property
    def name(self) -> str:
        """Plugin name from metadata."""
        return self.metadata().name

    @property
    def version(self) -> str:
        """Plugin version from metadata."""
        return self.metadata().version

    def set_state(self, state: PluginState) -> None:
        """Set plugin state.

        Args:
            state: New state.
        """
        self._state = state
        if state == PluginState.INITIALIZED:
            self._initialized_at = datetime.now(UTC)

    def set_error(self, error: Exception) -> None:
        """Set error state.

        Args:
            error: Exception that occurred.
        """
        self._error = error
        self._state = PluginState.ERROR


class VerifierPlugin(Plugin):
    """Base class for verification plugins.

    Verification plugins check data against specific criteria.
    """

    @classmethod
    def metadata(cls) -> PluginMetadata:
        """Default metadata for verifier plugins."""
        return PluginMetadata(
            name="base_verifier",
            plugin_type=PluginType.VERIFIER,
        )

    @abstractmethod
    def verify(self, data: Any) -> dict[str, Any]:
        """Verify data.

        Args:
            data: Data to verify.

        Returns:
            Verification result.
        """
        ...

    def execute(self, data: Any) -> Any:
        """Execute verification.

        Args:
            data: Data to verify.

        Returns:
            Verification result.
        """
        return self.verify(data)


class DetectorPlugin(Plugin):
    """Base class for detection plugins.

    Detection plugins identify patterns or anomalies.
    """

    @classmethod
    def metadata(cls) -> PluginMetadata:
        """Default metadata for detector plugins."""
        return PluginMetadata(
            name="base_detector",
            plugin_type=PluginType.DETECTOR,
        )

    @abstractmethod
    def detect(self, data: Any) -> list[dict[str, Any]]:
        """Detect patterns or anomalies.

        Args:
            data: Data to analyze.

        Returns:
            List of detections.
        """
        ...

    def execute(self, data: Any) -> Any:
        """Execute detection.

        Args:
            data: Data to analyze.

        Returns:
            Detection results.
        """
        return self.detect(data)


class ReporterPlugin(Plugin):
    """Base class for reporting plugins.

    Reporter plugins generate reports from data.
    """

    @classmethod
    def metadata(cls) -> PluginMetadata:
        """Default metadata for reporter plugins."""
        return PluginMetadata(
            name="base_reporter",
            plugin_type=PluginType.REPORTER,
        )

    @abstractmethod
    def generate_report(
        self,
        data: Any,
        template: str | None = None,
    ) -> str:
        """Generate a report.

        Args:
            data: Report data.
            template: Optional template name.

        Returns:
            Generated report.
        """
        ...

    def execute(self, data: Any) -> Any:
        """Execute report generation.

        Args:
            data: Report data.

        Returns:
            Generated report.
        """
        return self.generate_report(data)
