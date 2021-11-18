from typing import List, Tuple

from xlsxwriter import Workbook

from .base import BaseWriter


class ExcelWriter(BaseWriter):
    """
    Writer for recording data into excel format.
    """

    def __init__(self, filename: str):
        self.filename = filename
        self.workbook = None
        self.worksheet = None
        self.last_row = 1

    def start(self) -> None:
        # Create excel file and add headers
        self.workbook = Workbook(self.filename)
        self.worksheet = self.workbook.add_worksheet()
        for col, header in enumerate(('Name', 'Price', 'Vehicle Summary', 'Vehicle Options')):
            self.worksheet.write(0, col, header)

    def stop(self) -> None:
        self.workbook.close()

    def write_many(self, results: List[Tuple[str, str, dict, list]]) -> None:
        # Writing results to file
        for result in results:
            for col, res in enumerate(result):
                self.worksheet.write(self.last_row, col, str(res))
            self.last_row += 1
