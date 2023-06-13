from openpyxl import Workbook
from openpyxl.styles import Font


class Excel:
    def __init__(self):
        self._create_workbook()
        self._write_header()

    def _create_workbook(self):
        self.workbook = Workbook()
        self.sheet = self.workbook.active

    def _write_header(self):
        header = ["#", "Date", "Money", "Name", "Category"]
        self.sheet.append(header)

    def _celles_bold(self, celle):
        bold_font = Font(bold=True)
        self.sheet[celle].font = bold_font

    def save(self):
        self.workbook.save("output.xlsx")


if __name__ == "__main__":
    e = Excel()
    e.save()
