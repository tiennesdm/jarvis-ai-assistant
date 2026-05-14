"""Excel-specific automation actions."""
import logging
import time
from typing import Optional

from automation.desktop import DesktopController
from automation.app_manager import AppManager

logger = logging.getLogger(__name__)


class ExcelActions:
    """Handles all Excel-related operations."""

    def __init__(
        self,
        desktop: DesktopController = None,
        app_manager: AppManager = None,
    ):
        self.desktop = desktop or DesktopController()
        self.app_manager = app_manager or AppManager()

    def open_excel(self) -> bool:
        """Open Excel application."""
        return self.app_manager.open_app("excel")

    def create_workbook(self) -> bool:
        """Create new blank workbook (Ctrl+N after Excel opens)."""
        try:
            self.desktop.hotkey("ctrl", "n")
            time.sleep(1)
            logger.info("New workbook created")
            return True
        except Exception as e:
            logger.error(f"Failed to create workbook: {e}")
            return False

    def apply_formula(self, cell: str, formula: str) -> bool:
        """Apply formula to a cell."""
        try:
            # Navigate to cell
            self.click_cell(cell)
            time.sleep(0.3)

            # Type formula
            self.desktop.type_text(f"={formula}")
            time.sleep(0.2)

            # Press Enter
            self.desktop.press_key("enter")
            time.sleep(0.3)

            logger.info(f"Applied formula ={formula} to cell {cell}")
            return True

        except Exception as e:
            logger.error(f"Failed to apply formula: {e}")
            return False

    def click_cell(self, cell: str):
        """Click on a specific cell (uses Name Box)."""
        # Use Ctrl+G to go to cell
        self.desktop.hotkey("ctrl", "g")
        time.sleep(0.3)
        self.desktop.type_text(cell)
        time.sleep(0.2)
        self.desktop.press_key("enter")
        time.sleep(0.3)

    def enter_data(self, cell: str, data: str) -> bool:
        """Enter data into a cell."""
        try:
            self.click_cell(cell)
            time.sleep(0.3)
            self.desktop.type_text(str(data))
            time.sleep(0.2)
            self.desktop.press_key("enter")
            logger.info(f"Entered data in {cell}: {data}")
            return True
        except Exception as e:
            logger.error(f"Failed to enter data: {e}")
            return False

    def save_workbook(self, filepath: str = None) -> bool:
        """Save the workbook."""
        try:
            self.desktop.hotkey("ctrl", "s")
            time.sleep(1)

            if filepath:
                self.desktop.type_text(filepath)
                time.sleep(0.3)
                self.desktop.press_key("enter")

            logger.info("Workbook saved")
            return True
        except Exception as e:
            logger.error(f"Failed to save: {e}")
            return False

    def format_cells(self, range_str: str, format_type: str = "number") -> bool:
        """Format cells (number, currency, percentage, date)."""
        try:
            # Select range
            self.click_cell(range_str.split(":")[0])
            self.desktop.hotkey("ctrl", "shift", "end")
            time.sleep(0.3)

            # Open format dialog
            self.desktop.hotkey("ctrl", "1")
            time.sleep(0.5)

            # TODO: Navigate format dialog based on format_type
            logger.info(f"Format dialog opened for {format_type}")
            return True
        except Exception as e:
            logger.error(f"Failed to format cells: {e}")
            return False

    def apply_common_formula(
        self, formula_type: str, cell: str, range_str: str
    ) -> bool:
        """Apply common formulas easily."""
        formulas = {
            "sum": f"SUM({range_str})",
            "average": f"AVERAGE({range_str})",
            "count": f"COUNT({range_str})",
            "max": f"MAX({range_str})",
            "min": f"MIN({range_str})",
            "counta": f"COUNTA({range_str})",
        }

        formula = formulas.get(formula_type.lower())
        if formula:
            return self.apply_formula(cell, formula)

        logger.warning(f"Unknown formula type: {formula_type}")
        return False
