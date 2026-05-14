"""Desktop automation - mouse, keyboard, screenshots using pyautogui."""
import os
import time
import logging
from typing import Tuple, Optional
from datetime import datetime

import pyautogui
from PIL import Image
import config

logger = logging.getLogger(__name__)

# Configure pyautogui safety
pyautogui.FAILSAFE = True  # Move mouse to corner to abort
pyautogui.PAUSE = 0.1


class DesktopController:
    """Controls desktop via mouse, keyboard, and screenshots."""

    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()
        logger.info(f"Screen size: {self.screen_width}x{self.screen_height}")

    def get_screen_size(self) -> Tuple[int, int]:
        """Get screen dimensions."""
        return pyautogui.size()

    def screenshot(self, filename: str = None) -> str:
        """Capture screenshot and save to file. Returns filepath."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"

        filepath = os.path.join(config.SCREENSHOT_DIR, filename)
        os.makedirs(config.SCREENSHOT_DIR, exist_ok=True)

        try:
            screenshot = pyautogui.screenshot()
            screenshot.save(filepath)
            logger.debug(f"Screenshot saved: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Screenshot failed: {e}")
            raise

    def click(self, x: int, y: int, clicks: int = 1, button: str = 'left'):
        """Click at specified coordinates."""
        try:
            pyautogui.click(x, y, clicks=clicks, button=button)
            logger.debug(f"Clicked at ({x}, {y})")
        except Exception as e:
            logger.error(f"Click failed at ({x}, {y}): {e}")
            raise

    def double_click(self, x: int, y: int):
        """Double click at coordinates."""
        self.click(x, y, clicks=2)

    def right_click(self, x: int, y: int):
        """Right click at coordinates."""
        self.click(x, y, button='right')

    def move_to(self, x: int, y: int, duration: float = 0.5):
        """Move mouse to coordinates."""
        pyautogui.moveTo(x, y, duration=duration)

    def type_text(self, text: str, interval: float = 0.01):
        """Type text at current cursor position."""
        pyautogui.typewrite(text, interval=interval)
        logger.debug(f"Typed: {text[:50]}...")

    def press_key(self, key: str):
        """Press a single key."""
        pyautogui.press(key)
        logger.debug(f"Pressed key: {key}")

    def hotkey(self, *keys: str):
        """Press keyboard shortcut (e.g., ctrl, c)."""
        pyautogui.hotkey(*keys)
        logger.debug(f"Hotkey: {'+'.join(keys)}")

    def scroll(self, amount: int, x: int = None, y: int = None):
        """Scroll up (positive) or down (negative)."""
        if x is not None and y is not None:
            pyautogui.scroll(amount, x, y)
        else:
            pyautogui.scroll(amount)

    def get_mouse_position(self) -> Tuple[int, int]:
        """Get current mouse position."""
        return pyautogui.position()

    def find_on_screen(self, image_path: str, confidence: float = 0.8) -> Optional[Tuple[int, int]]:
        """Find image on screen and return center coordinates."""
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=confidence)
            if location:
                center = pyautogui.center(location)
                logger.debug(f"Found {image_path} at {center}")
                return center
            logger.debug(f"Image not found: {image_path}")
            return None
        except Exception as e:
            logger.error(f"Error finding image: {e}")
            return None

    def wait_and_click(self, image_path: str, confidence: float = 0.8, timeout: int = 10):
        """Wait for image to appear and click it."""
        start = time.time()
        while time.time() - start < timeout:
            pos = self.find_on_screen(image_path, confidence)
            if pos:
                self.click(pos[0], pos[1])
                return True
            time.sleep(0.5)
        logger.warning(f"Timeout waiting for image: {image_path}")
        return False

    def open_run_dialog(self):
        """Open Windows Run dialog."""
        self.hotkey('win', 'r')
        time.sleep(0.5)

    def type_in_run(self, command: str):
        """Type in Run dialog and press Enter."""
        self.open_run_dialog()
        self.type_text(command)
        self.press_key('enter')

    def take_screenshot_region(self, x: int, y: int, width: int, height: int, filename: str = None) -> str:
        """Screenshot of specific region."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"region_{timestamp}.png"

        filepath = os.path.join(config.SCREENSHOT_DIR, filename)
        screenshot = pyautogui.screenshot(region=(x, y, width, height))
        screenshot.save(filepath)
        return filepath

    def open_start_menu(self):
        """Open Windows Start menu."""
        self.press_key('win')
        time.sleep(0.5)

    def search_in_start(self, query: str):
        """Open Start menu and search."""
        self.open_start_menu()
        self.type_text(query)
        time.sleep(0.5)
        self.press_key('enter')
