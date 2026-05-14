"""Application registry - maps apps to their action handlers."""
from typing import Dict, Type, Optional
import logging

logger = logging.getLogger(__name__)


class AppRegistry:
    """Registry of supported applications and their capabilities."""

    # Registry of app -> action handler class mapping
    _registry: Dict[str, str] = {
        "excel": "actions.excel_actions.ExcelActions",
        "spreadsheet": "actions.excel_actions.ExcelActions",
        "whatsapp": "actions.whatsapp_actions.WhatsAppActions",
        "gallery": "actions.photo_actions.PhotoActions",
        "photos": "actions.photo_actions.PhotoActions",
        "chrome": "actions.browser_actions.BrowserActions",
        "browser": "actions.browser_actions.BrowserActions",
        "edge": "actions.browser_actions.BrowserActions",
    }

    # Supported actions per app
    APP_CAPABILITIES = {
        "excel": [
            "open",
            "create_workbook",
            "apply_formula",
            "enter_data",
            "save",
            "format_cells",
            "create_chart",
            "sort",
            "filter",
        ],
        "whatsapp": [
            "open",
            "search_contact",
            "send_message",
            "send_media",
            "read_message",
            "create_group",
        ],
        "gallery": [
            "open",
            "view_photo",
            "crop",
            "rotate",
            "resize",
            "apply_filter",
            "adjust_brightness",
            "save",
        ],
        "chrome": [
            "open",
            "navigate",
            "search",
            "click",
            "scroll",
            "screenshot",
        ],
    }

    @classmethod
    def get_handler_class(cls, app_name: str) -> Optional[str]:
        """Get handler class path for an app."""
        return cls._registry.get(app_name.lower())

    @classmethod
    def is_supported(cls, app_name: str) -> bool:
        """Check if app is supported."""
        return app_name.lower() in cls._registry

    @classmethod
    def get_capabilities(cls, app_name: str) -> list:
        """Get supported actions for an app."""
        # Find matching app
        app_lower = app_name.lower()
        for key, caps in cls.APP_CAPABILITIES.items():
            if key in app_lower or app_lower in key:
                return caps
        return []

    @classmethod
    def list_supported_apps(cls) -> list:
        """List all supported app names."""
        return list(set(cls._registry.keys()))

    @classmethod
    def suggest_app(cls, keyword: str) -> Optional[str]:
        """Suggest app based on keyword."""
        keyword_lower = keyword.lower()
        for app in cls._registry.keys():
            if keyword_lower in app or app in keyword_lower:
                return app
        return None
