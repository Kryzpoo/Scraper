from typing import List, Tuple

from .base import BaseWriter


class CsvWriter(BaseWriter):
    """
    Writer for recording data into csv format.
    """

    def __init__(self, filename: str):
        self.filename = filename
        self.file = None
        self.delimiter = '|'

    def start(self) -> None:
        # Create file and add headers
        self.file = open(self.filename, 'w')
        self.file.write(
            self.delimiter.join(('Name', 'Price',
                                 'Vehicle Summary',
                                 'Vehicle Options')) + '\n'
        )

    def stop(self) -> None:
        self.file.close()

    def write_many(self, results: List[Tuple[str, str, dict, list]]) -> None:
        # Writing results to file
        for result in results:
            self.file.write(self.delimiter.join([str(s) for s in result]) + '\n')
