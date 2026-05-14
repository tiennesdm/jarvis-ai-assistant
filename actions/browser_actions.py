"""Browser automation actions."""
import logging
import time
import webbrowser
import urllib.parse

from automation.desktop import DesktopController
from automation.app_manager import AppManager

logger = logging.getLogger(__name__)


class BrowserActions:
    """Handles browser-based operations."""

    def __init__(
        self,
        desktop: DesktopController = None,
        app_manager: AppManager = None,
    ):
        self.desktop = desktop or DesktopController()
        self.app_manager = app_manager or AppManager()

    def open_browser(self, url: str = None) -> bool:
        """Open browser with optional URL."""
        try:
            if url:
                webbrowser.open(url)
            else:
                webbrowser.open("about:blank")
            time.sleep(3)
            return True
        except Exception as e:
            logger.error(f"Failed to open browser: {e}")
            return False

    def navigate(self, url: str) -> bool:
        """Navigate to URL."""
        try:
            webbrowser.open(url)
            time.sleep(3)
            logger.info(f"Navigated to: {url}")
            return True
        except Exception as e:
            logger.error(f"Failed to navigate: {e}")
            return False

    def search(self, query: str) -> bool:
        """Search on Google."""
        try:
            encoded = urllib.parse.quote(query)
            url = f"https://www.google.com/search?q={encoded}"
            webbrowser.open(url)
            time.sleep(3)
            logger.info(f"Searched: {query}")
            return True
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return False

    def click(self, x: int, y: int) -> bool:
        """Click at screen coordinates."""
        self.desktop.click(x, y)
        return True

    def scroll_down(self, amount: int = 500) -> bool:
        """Scroll down the page."""
        self.desktop.scroll(-amount)
        return True

    def scroll_up(self, amount: int = 500) -> bool:
        """Scroll up the page."""
        self.desktop.scroll(amount)
        return True

    def take_screenshot(self) -> str:
        """Take screenshot of current page."""
        return self.desktop.screenshot()

    def type_in_address_bar(self, text: str) -> bool:
        """Click address bar and type."""
        try:
            # Click address bar (top of browser)
            screen_w, screen_h = self.desktop.get_screen_size()
            self.desktop.click(int(screen_w * 0.5), 60)
            time.sleep(0.3)

            # Select all and type
            self.desktop.hotkey("ctrl", "a")
            time.sleep(0.1)
            self.desktop.type_text(text)
            time.sleep(0.3)
            self.desktop.press_key("enter")

            return True
        except Exception as e:
            logger.error(f"Failed to type in address bar: {e}")
            return False
