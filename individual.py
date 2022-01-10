import datetime

from RPA.Browser.Selenium import Selenium
from RPA.FileSystem import FileSystem
from taskFiles import SaveExcel

import os


class IndividualInvestments:

    URL = "https://itdashboard.gov/drupal/summary/{}"
    filesystem = FileSystem()

    def __init__(self, agency_id):
        self._link = self.URL.format(agency_id)
        self.browser = Selenium()
        self.browser.open_available_browser(self._link)

    def click_select_all(self):
        self.browser.wait_until_element_is_visible(
            '//div[@class="pageSelect"]/div')
        self.browser.click_element('//div[@class="pageSelect"]/div')
        self.browser.wait_until_element_is_visible(
            '//div[@class="pageSelect"]/div/label/select/option[4]')
        self.browser.click_element(
            '//div[@class="pageSelect"]/div/label/select/option[4]')
        self.browser.wait_until_element_is_visible(
            '//a[@class="paginate_button next disabled"]',
            timeout=datetime.timedelta(minutes=1))

    def get_row_value(self, row):
        value = []
        cells = row.find_elements_by_tag_name('td')
        column = 1
        for cell in cells:
            value.append(cell.text)
            column += 1
        return value

    def get_table_headers(self):
        self.browser.wait_until_element_is_visible(
            '//div[@class="dataTables_scrollHead"]//th')
        headers = self.browser.get_webelements(
            '//div[@class="dataTables_scrollHead"]//th')
        data_headers = []
        for header in headers:
            data_headers.append(header.text)
        return data_headers

    def get_table_body(self):
        self.click_select_all()
        self.browser.wait_until_element_is_visible(
            '//div[@class="dataTables_scrollBody"]//tbody/tr')
        rows = self.browser.get_webelements(
            '//div[@class="dataTables_scrollBody"]//tbody/tr')
        full_data = []
        for row in rows:
            full_data.append(self.get_row_value(row))
        return full_data

    def downloadPDF(self, link, path=None):
        filename = f"{link.split('/')[-1]}.pdf"
        load_dir = f'{os.getcwd()}/{path}'
        self.browser.set_download_directory(load_dir, True)
        self.browser.open_available_browser(link)
        self.browser.wait_until_element_is_visible(
            '//div[@id="business-case-pdf"]/a')
        self.browser.click_element('//div[@id="business-case-pdf"]/a')
        self.filesystem.wait_until_created(
            f"{load_dir}/{filename}", timeout=60.0)
        self.browser.close_browser()

    def parse(self, fileExcel, worksheet):
        headers = self.get_table_headers()
        fileExcel.create_headers(headers, worksheet)
        content = self.get_table_body()
        for row in content:
            fileExcel.append_row(row, worksheet)
        anchors = self.browser.get_webelements(
            '//div[@class="dataTables_scrollBody"]//tbody/tr//a')
        for anchor in anchors:
            link = anchor.get_attribute('href')
            self.downloadPDF(link, 'output')
