"""Plugin declaration for the Device LifeCycle Management."""
try:
    from importlib import metadata
except ImportError:
    # Python version < 3.8
    import importlib_metadata as metadata

__version__ = metadata.version(__name__)

from packaging import version

from django.conf import settings
from django.db.models.signals import post_migrate

from nautobot.extras.plugins import PluginConfig


current_nautobot_version = version.parse(settings.VERSION)
NAUTOBOT_GRAPHQL_FIX = version.parse("1.2.0b1")


class DeviceLifeCycleConfig(PluginConfig):
    """Plugin configuration for the Device Lifecycle Management plugin."""

    name = "nautobot_device_lifecycle_mgmt"
    verbose_name = "Nautobot Device Lifecycle Management"
    version = __version__
    author = "Network to Code"
    author_email = "opensource@networktocode.com"
    description = "Manages device lifecycle of Nautobot Devices and Components."
    base_url = "nautobot-device-lifecycle-mgmt"
    required_settings = []
    min_version = "1.0.0"
    max_version = "1.9999"
    default_settings = {"expired_field": "end_of_support"}
    caching_config = {}

    def ready(self):
        """Register custom signals."""
        import nautobot_device_lifecycle_mgmt.signals  # pylint: disable=C0415,W0611 # noqa: F401
        from .signals import (  # pylint: disable=import-outside-toplevel
            post_migrate_create_relationships,
        )

        # Workaround for https://github.com/nautobot/nautobot/issues/567 for Nautobot < 1.2.0b1
        if current_nautobot_version < NAUTOBOT_GRAPHQL_FIX:
            import nautobot.extras.graphql.types  # pylint: disable=import-outside-toplevel, unused-import # noqa: F401

        post_migrate.connect(post_migrate_create_relationships, sender=self)

        super().ready()


config = DeviceLifeCycleConfig  # pylint:disable=invalid-name
