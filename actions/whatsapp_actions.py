"""WhatsApp automation via WhatsApp Web."""
import logging
import time
import urllib.parse
import webbrowser
import os

from automation.desktop import DesktopController
from automation.app_manager import AppManager

logger = logging.getLogger(__name__)


class WhatsAppActions:
    """Handles WhatsApp messaging via WhatsApp Web."""

    WHATSAPP_WEB_URL = "https://web.whatsapp.com"

    def __init__(
        self,
        desktop: DesktopController = None,
        app_manager: AppManager = None,
    ):
        self.desktop = desktop or DesktopController()
        self.app_manager = app_manager or AppManager()
        self.is_logged_in = False

    def open_whatsapp(self) -> bool:
        """Open WhatsApp Web in browser."""
        try:
            webbrowser.open(self.WHATSAPP_WEB_URL)
            time.sleep(5)  # Wait for page to load
            logger.info("WhatsApp Web opened")
            return True
        except Exception as e:
            logger.error(f"Failed to open WhatsApp: {e}")
            return False

    def search_contact(self, name: str) -> bool:
        """Search for a contact in WhatsApp."""
        try:
            # Click on search box (top-left area)
            # This is approximate - WhatsApp Web UI specific
            self.desktop.click(200, 150)
            time.sleep(0.5)

            # Type contact name
            self.desktop.type_text(name)
            time.sleep(1.5)  # Wait for search results

            # Click first result
            self.desktop.click(200, 250)
            time.sleep(1)

            logger.info(f"Searched contact: {name}")
            return True
        except Exception as e:
            logger.error(f"Failed to search contact: {e}")
            return False

    def send_message(self, contact: str, message: str) -> bool:
        """Send message to a contact via WhatsApp Web."""
        try:
            # Method 1: Direct URL (faster, no need to search)
            encoded_message = urllib.parse.quote(message)
            url = f"https://wa.me/?text={encoded_message}"

            # Better method: Use WhatsApp Web with phone
            # Format: https://web.whatsapp.com/send?phone=<number>&text=<message>
            # For now, open WhatsApp Web and search

            self.open_whatsapp()
            time.sleep(5)

            # Search for contact
            self.search_contact(contact)

            # Type message in message box (bottom area)
            screen_w, screen_h = self.desktop.get_screen_size()
            self.desktop.click(int(screen_w * 0.5), int(screen_h * 0.9))
            time.sleep(0.5)

            # Type the message
            self.desktop.type_text(message)
            time.sleep(0.5)

            # Send (press Enter)
            self.desktop.press_key("enter")
            time.sleep(1)

            logger.info(f"Message sent to {contact}")
            return True

        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            return False

    def send_direct_message(self, phone_number: str, message: str) -> bool:
        """Send message using wa.me direct link (no need to save contact)."""
        try:
            # Clean phone number
            phone = phone_number.replace(" ", "").replace("-", "")
            if not phone.startswith("+"):
                phone = "+" + phone

            encoded_msg = urllib.parse.quote(message)
            url = f"https://wa.me/{phone}?text={encoded_msg}"

            webbrowser.open(url)
            time.sleep(5)

            # Click "Continue to Chat" button
            # Then click "use WhatsApp Web"

            logger.info(f"WhatsApp direct link opened for {phone}")
            return True

        except Exception as e:
            logger.error(f"Failed to send direct message: {e}")
            return False

    def send_media(self, contact: str, media_path: str) -> bool:
        """Send media file to contact."""
        try:
            self.search_contact(contact)
            time.sleep(1)

            # Click attachment button (paperclip icon)
            screen_w, screen_h = self.desktop.get_screen_size()
            self.desktop.click(int(screen_w * 0.02), int(screen_h * 0.88))
            time.sleep(0.5)

            # Select gallery/document option
            self.desktop.click(int(screen_w * 0.02), int(screen_h * 0.7))
            time.sleep(1)

            # Type file path in file dialog
            self.desktop.type_text(os.path.abspath(media_path))
            time.sleep(0.3)
            self.desktop.press_key("enter")
            time.sleep(1)

            # Send button
            self.desktop.press_key("enter")

            logger.info(f"Media sent to {contact}")
            return True

        except Exception as e:
            logger.error(f"Failed to send media: {e}")
            return False

    def read_recent_message(self) -> str:
        """Read most recent message."""
        # This would require OCR on the chat area
        logger.info("Reading recent messages")
        return "Message reading requires OCR integration"
