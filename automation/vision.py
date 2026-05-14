"""Computer vision module for screen understanding."""
import os
import logging
from typing import Optional, List, Tuple
from PIL import Image
import numpy as np

logger = logging.getLogger(__name__)


class VisionAnalyzer:
    """Analyzes screenshots to understand UI state."""

    def __init__(self, desktop_controller=None):
        self.desktop = desktop_controller
        self.ocr_reader = None
        self._init_ocr()

    def _init_ocr(self):
        """Initialize OCR engine."""
        try:
            import easyocr
            self.ocr_reader = easyocr.Reader(['en', 'hi'])
            logger.info("OCR initialized (English + Hindi)")
        except ImportError:
            logger.warning("easyocr not installed. OCR features limited.")
            self.ocr_reader = None
        except Exception as e:
            logger.warning(f"OCR init failed: {e}")
            self.ocr_reader = None

    def capture_screen(self) -> str:
        """Capture and return screenshot path."""
        if self.desktop:
            return self.desktop.screenshot()

        # Fallback to direct pyautogui
        import pyautogui
        import config
        from datetime import datetime

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join(config.SCREENSHOT_DIR, f"vision_{timestamp}.png")
        os.makedirs(config.SCREENSHOT_DIR, exist_ok=True)

        screenshot = pyautogui.screenshot()
        screenshot.save(filepath)
        return filepath

    def read_text_from_screen(self, region: Tuple[int, int, int, int] = None) -> str:
        """Extract text from screen using OCR."""
        if not self.ocr_reader:
            return "OCR not available. Install easyocr."

        try:
            # Capture region or full screen
            if region:
                x, y, w, h = region
                screenshot = self.desktop.take_screenshot_region(x, y, w, h) if self.desktop else None
                img = np.array(Image.open(screenshot))
            else:
                screenshot_path = self.capture_screen()
                img = np.array(Image.open(screenshot_path))

            # Run OCR
            results = self.ocr_reader.readtext(img)
            texts = [result[1] for result in results]

            return "\n".join(texts)

        except Exception as e:
            logger.error(f"OCR failed: {e}")
            return f"OCR Error: {e}"

    def find_text_on_screen(self, target_text: str) -> Optional[Tuple[int, int]]:
        """Find specific text on screen and return coordinates."""
        if not self.ocr_reader:
            return None

        try:
            screenshot_path = self.capture_screen()
            img = np.array(Image.open(screenshot_path))
            results = self.ocr_reader.readtext(img)

            for bbox, text, conf in results:
                if target_text.lower() in text.lower():
                    # Calculate center of bounding box
                    pts = np.array(bbox)
                    center_x = int(np.mean(pts[:, 0]))
                    center_y = int(np.mean(pts[:, 1]))
                    return (center_x, center_y)

            return None

        except Exception as e:
            logger.error(f"Text search failed: {e}")
            return None

    def find_element(self, element_description: str) -> Optional[Tuple[int, int]]:
        """Find UI element by description."""
        # Try text-based search first
        result = self.find_text_on_screen(element_description)
        if result:
            return result

        # Could add template matching here for icons
        logger.info(f"Element not found: {element_description}")
        return None

    def get_screen_summary(self) -> str:
        """Get a summary of what's on screen."""
        text = self.read_text_from_screen()
        lines = text.split("\n")

        # Get first 20 lines as summary
        summary = "\n".join(lines[:20])
        return f"Screen content:\n{summary}"
