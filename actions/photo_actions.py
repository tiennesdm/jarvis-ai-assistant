"""Photo editing automation actions."""
import logging
import time
import os

from automation.desktop import DesktopController
from automation.app_manager import AppManager

logger = logging.getLogger(__name__)


class PhotoActions:
    """Handles photo editing operations via Gallery/Photos app."""

    def __init__(
        self,
        desktop: DesktopController = None,
        app_manager: AppManager = None,
    ):
        self.desktop = desktop or DesktopController()
        self.app_manager = app_manager or AppManager()
        self.current_photo = None

    def open_gallery(self) -> bool:
        """Open default photo viewer."""
        # Try Windows Photos app first
        if os.name == "nt":
            return self.app_manager.open_app("photos")
        else:
            return self.app_manager.open_app("gallery")

    def open_photo(self, photo_path: str) -> bool:
        """Open specific photo file."""
        try:
            self.current_photo = photo_path
            if os.name == "nt":
                os.startfile(photo_path)
            else:
                import subprocess

                subprocess.Popen(["xdg-open", photo_path])
            time.sleep(2)
            return True
        except Exception as e:
            logger.error(f"Failed to open photo: {e}")
            return False

    def apply_filter(self, filter_type: str) -> bool:
        """Apply filter to current photo."""
        # This requires the Photos app's specific UI
        # General approach: open edit mode and navigate to filters
        try:
            # Open edit mode (usually 'E' or Edit button)
            self.desktop.press_key("e")
            time.sleep(1)

            # Navigate to filters tab
            # Tab to navigate, Enter to select
            for _ in range(3):
                self.desktop.press_key("tab")
                time.sleep(0.2)

            logger.info(f"Filter mode opened: {filter_type}")
            return True
        except Exception as e:
            logger.error(f"Failed to apply filter: {e}")
            return False

    def crop(self) -> bool:
        """Start crop mode."""
        try:
            # Common shortcut for crop in Photos app
            self.desktop.press_key("c")
            time.sleep(0.5)
            logger.info("Crop mode activated")
            return True
        except Exception as e:
            logger.error(f"Failed to activate crop: {e}")
            return False

    def rotate(self, direction: str = "right") -> bool:
        """Rotate photo."""
        try:
            if direction == "right":
                self.desktop.hotkey("ctrl", "r")
            else:
                self.desktop.hotkey("ctrl", "shift", "r")
            time.sleep(0.3)
            logger.info(f"Rotated {direction}")
            return True
        except Exception as e:
            logger.error(f"Failed to rotate: {e}")
            return False

    def adjust_brightness(self, increase: bool = True) -> bool:
        """Adjust brightness."""
        try:
            # Open edit mode
            self.desktop.press_key("e")
            time.sleep(0.5)

            # Navigate to light/adjustments
            # This varies by app - generic approach
            logger.info(
                f"Brightness adjustment: {'increase' if increase else 'decrease'}"
            )
            return True
        except Exception as e:
            logger.error(f"Failed to adjust brightness: {e}")
            return False

    def save_photo(self, filepath: str = None) -> bool:
        """Save edited photo."""
        try:
            self.desktop.hotkey("ctrl", "s")
            time.sleep(0.5)

            if filepath:
                self.desktop.type_text(filepath)
                time.sleep(0.3)
                self.desktop.press_key("enter")

            logger.info("Photo saved")
            return True
        except Exception as e:
            logger.error(f"Failed to save photo: {e}")
            return False
