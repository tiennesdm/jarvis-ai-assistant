"""Safety guard for Jarvis AI - confirms destructive actions."""
import logging
from typing import Dict, List

import config

logger = logging.getLogger(__name__)

class SafetyGuard:
    """Ensures safety by confirming potentially destructive actions."""

    # Actions that always need confirmation
    DESTRUCTIVE_ACTIONS = [
        "delete", "format", "uninstall", "remove",
        "overwrite", "reset", "clear", "erase",
        "install", "modify_system"
    ]

    # System-sensitive apps
    SYSTEM_APPS = ["settings", "system", "registry", "terminal", "control_panel", "cmd"]

    # Suspicious keywords
    DANGEROUS_KEYWORDS = [
        "rm -rf", "format c:", "del /f /s", "registry delete",
        "sudo rm", "drop table", "delete from",
        "rd /s /q", "erase all"
    ]

    def needs_confirmation(self, action: Dict) -> bool:
        """Check if action needs user confirmation."""
        if not config.REQUIRE_CONFIRMATION:
            return False

        intent_action = action.get("action", "")
        app = action.get("app_needed", "")
        params = action.get("parameters", {})

        # Destructive actions always need confirmation
        if intent_action in self.DESTRUCTIVE_ACTIONS:
            return True

        # Check for file deletion
        if intent_action == "delete_file" or params.get("delete"):
            return True

        # Check for app uninstall
        if intent_action == "uninstall":
            return True

        # Check for sensitive apps
        if app in self.SYSTEM_APPS:
            return True

        # Check for system-level operations
        system_actions = ["install", "uninstall", "modify_system", "change_settings"]
        if intent_action in system_actions:
            return True

        return False

    def confirm_action(self, action: Dict) -> bool:
        """Ask user to confirm a destructive action."""
        app = action.get("app_needed", "Unknown")
        action_name = action.get("action", "Unknown")
        params = action.get("parameters", {})

        # Build confirmation message
        msg = f"⚠️  Savdhaan: "

        if action_name == "install":
            app_name = params.get("app_name", "app")
            msg += f"Kya aap '{app_name}' install karna chahte hain?"
        elif action_name in ["delete", "remove", "uninstall"]:
            target = params.get("app_name", params.get("file", "ye item"))
            msg += f"Kya aap '{target}' ko hamesha ke liye hataana chahte hain?"
        elif action_name == "format":
            msg += "Kya aap sach mein format karna chahte hain? Sari data delete ho jayegi!"
        else:
            msg += f"Kya aap '{action_name}' karna chahte hain {app} mein?"

        # Print in red color
        print(f"\n{'='*50}")
        print(f"\033[91m{msg}\033[0m")
        print(f"{'='*50}\n")

        try:
            response = input("Type 'haan' to confirm, 'nahi' to cancel: ").lower().strip()
            confirmed = response in ['haan', 'han', 'yes', 'y', 'h', 'ha']

            if confirmed:
                logger.info(f"Action confirmed: {action_name}")
            else:
                logger.info(f"Action cancelled: {action_name}")

            return confirmed

        except (EOFError, KeyboardInterrupt):
            logger.info("Confirmation cancelled by user")
            return False

    def is_safe_command(self, command: str) -> bool:
        """Check if command contains dangerous patterns."""
        command_lower = command.lower()

        for keyword in self.DANGEROUS_KEYWORDS:
            if keyword.lower() in command_lower:
                logger.warning(f"Dangerous command detected: {keyword}")
                return False

        return True

    def get_warning_message(self, action: Dict) -> str:
        """Get warning message for a destructive action."""
        action_name = action.get("action", "")

        warnings = {
            "install": "⚠️  App install hoga. Internet connection chahiye.",
            "uninstall": "⚠️  App uninstall ho jayega. Iska data delete ho sakta hai.",
            "delete": "⚠️  File/Folder delete ho jayega. Recycle Bin mein jayega.",
            "format": "⚠️  FORMAT: SARA DATA DELETE HO JAYEGA!",
        }

        return warnings.get(action_name, "⚠️  Ye action system ko affect kar sakta hai.")
