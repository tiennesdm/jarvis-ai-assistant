"""Application manager - open, close, focus applications."""
import os
import logging
import subprocess
import time
from typing import List, Optional

import psutil
from utils.helpers import get_os

logger = logging.getLogger(__name__)


class AppManager:
    """Manages opening, closing, and focusing applications."""

    # Common app executables by OS
    APP_COMMANDS = {
        "windows": {
            "excel": "excel",
            "winword": "winword",
            "powerpoint": "powerpnt",
            "notepad": "notepad",
            "calculator": "calc",
            "paint": "mspaint",
            "chrome": "chrome",
            "edge": "msedge",
            "firefox": "firefox",
            "vscode": "code",
            "spotify": "spotify",
            "whatsapp": "whatsapp",  # Desktop app if installed
            "settings": "ms-settings:",
            "explorer": "explorer",
            "cmd": "cmd",
            "powershell": "powershell",
            "taskmanager": "taskmgr",
            "control panel": "control",
        },
        "macos": {
            "excel": "/Applications/Microsoft Excel.app",
            "chrome": "/Applications/Google Chrome.app",
            "safari": "/Applications/Safari.app",
            "vscode": "/Applications/Visual Studio Code.app",
            "spotify": "/Applications/Spotify.app",
            "terminal": "/Applications/Utilities/Terminal.app",
        },
        "linux": {
            "chrome": "google-chrome",
            "firefox": "firefox",
            "vscode": "code",
            "gedit": "gedit",
            "calculator": "gnome-calculator",
            "terminal": "gnome-terminal",
            "files": "nautilus",
        }
    }

    def __init__(self, desktop_controller=None):
        self.os = get_os()
        self.desktop = desktop_controller
        self.apps_commands = self.APP_COMMANDS.get(self.os, self.APP_COMMANDS["linux"])
        logger.info(f"AppManager initialized for {self.os}")

    def open_app(self, app_name: str) -> bool:
        """Open an application by name."""
        app_name_lower = app_name.lower().strip()

        # Direct command mapping
        command = self.apps_commands.get(app_name_lower)

        if not command:
            # Try variations
            for key, cmd in self.apps_commands.items():
                if app_name_lower in key or key in app_name_lower:
                    command = cmd
                    break

        if not command:
            # Try to open as-is (might be in PATH)
            command = app_name_lower

        try:
            if self.os == "windows":
                if command.startswith("ms-"):
                    subprocess.Popen(f"start {command}", shell=True)
                else:
                    subprocess.Popen(f"start {command}", shell=True)
            elif self.os == "macos":
                if command.endswith(".app"):
                    subprocess.Popen(["open", command])
                else:
                    subprocess.Popen(["open", "-a", command])
            else:  # linux
                subprocess.Popen(command, shell=True)

            logger.info(f"Opened app: {app_name}")
            time.sleep(2)  # Wait for app to load
            return True

        except Exception as e:
            logger.error(f"Failed to open {app_name}: {e}")
            return False

    def close_app(self, app_name: str) -> bool:
        """Close an application by name."""
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                if app_name.lower() in proc.info['name'].lower():
                    process = psutil.Process(proc.info['pid'])
                    process.terminate()
                    logger.info(f"Closed app: {app_name}")
                    return True

            logger.warning(f"App not found running: {app_name}")
            return False

        except Exception as e:
            logger.error(f"Failed to close {app_name}: {e}")
            return False

    def is_app_open(self, app_name: str) -> bool:
        """Check if application is running."""
        try:
            for proc in psutil.process_iter(['name']):
                if app_name.lower() in proc.info['name'].lower():
                    return True
            return False
        except Exception:
            return False

    def focus_app(self, app_name: str) -> bool:
        """Bring application to foreground."""
        try:
            if self.os == "windows":
                import pyautogui
                # Use Alt+Tab or taskbar
                # Try using pywinauto if available
                try:
                    from pywinauto import Application
                    app = Application(backend="uia").connect(title_re=f".*{app_name}.*", timeout=5)
                    app.top_window().set_focus()
                    return True
                except Exception:
                    pass

            elif self.os == "macos":
                script = f'tell application "{app_name}" to activate'
                subprocess.Popen(["osascript", "-e", script])
                return True

            else:  # linux
                subprocess.Popen(["wmctrl", "-a", app_name], shell=False)
                return True

        except Exception as e:
            logger.error(f"Failed to focus {app_name}: {e}")
            return False

    def get_installed_apps(self) -> List[str]:
        """Get list of installed applications."""
        return list(self.apps_commands.keys())

    def install_app(self, app_name: str) -> bool:
        """Guide user to install an application."""
        logger.info(f"Installation requested: {app_name}")

        # Open browser with search
        search_url = f"https://www.google.com/search?q=download+{app_name}+official"
        if self.os == "windows":
            subprocess.Popen(f"start {search_url}", shell=True)
        elif self.os == "macos":
            subprocess.Popen(["open", search_url])
        else:
            subprocess.Popen(["xdg-open", search_url])

        return True

    def open_file_with_app(self, filepath: str, app_name: str = None) -> bool:
        """Open a file with specific or default application."""
        try:
            if self.os == "windows":
                if app_name:
                    subprocess.Popen(f"start {app_name} \"{filepath}\"", shell=True)
                else:
                    os.startfile(filepath)
            elif self.os == "macos":
                if app_name:
                    subprocess.Popen(["open", "-a", app_name, filepath])
                else:
                    subprocess.Popen(["open", filepath])
            else:
                if app_name:
                    subprocess.Popen([app_name, filepath])
                else:
                    subprocess.Popen(["xdg-open", filepath])
            return True
        except Exception as e:
            logger.error(f"Failed to open file: {e}")
            return False
