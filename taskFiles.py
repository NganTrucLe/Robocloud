from RPA.Excel.Files import Files
from RPA.Browser.Selenium import Selenium
from RPA.FileSystem import FileSystem


class SaveExcel:
    def __init__(self, path, worksheet):
        excel = Files()
        self.workbook = excel.create_workbook(path)
        self.path = path
        self.workbook.create_worksheet(worksheet)

    def new_worksheet(self, worksheet):
        self.workbook.create_worksheet(worksheet)

    def append_row(self, row, worksheet):
        row_number = self.workbook.find_empty_row(worksheet)
        column = 'A'
        for cell in row:
            self.workbook.set_cell_value(row_number, column, cell, worksheet)
            column = chr(ord(column) + 1)

    def create_headers(self, headers, worksheet):
        column = 'A'
        for item in headers:
            self.workbook.set_cell_value(1, column, item, worksheet)
            column = chr(ord(column) + 1)

    def append_data_agencies(self, agencies):
        row = 2
        for agency in agencies:
            self.workbook.set_cell_value(row, 'A', agency['name'])
            self.workbook.set_cell_value(row, 'B', agency['amount'])
            row += 1

    def save(self):
        self.workbook.save(self.path)
