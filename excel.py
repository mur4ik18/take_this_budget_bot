from openpyxl import Workbook
from openpyxl.styles import Font


class Excel:
    def __init__(self):
        self._create_workbook()
        self.write_header()

    def _create_workbook(self):
        self.workbook = Workbook()
        self.sheet = self.workbook.active

    def write_header(self):
        header = ["#", "Money", "Description", "Category", "Date"]
        self.sheet.append(header)
        list_of_celles = ["A", "B", "C", "D", "E"]
        for i in list_of_celles:
            self._celles_bold(f"{i}1")
        self.sheet.freeze_panes = "A1"

    def _celles_bold(self, celle):
        bold_font = Font(bold=True)
        self.sheet[celle].font = bold_font

    def write_data(self, data):
        self.sheet.append(data)

    def save(self, name_of_file: str = "outut"):
        self.workbook.save(f"{name_of_file}.xlsx")


if __name__ == "__main__":
    e = Excel()
    e.write_data([1, 2, 3, 4, 5])
    e.save()
