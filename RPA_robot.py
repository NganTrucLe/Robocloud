import logging

from RPA.Browser.Selenium import Selenium

from taskFiles import saveExcel
from agencies import AgenciesList
from individual import IndividualInvestments


class RPARobot:

    def __init__(self):
        self.browser = Selenium()
        self.output_folder = 'output'
        self.list_parser = AgenciesList()
        self.detail_parser = IndividualInvestments('020')
        logfile = f'{self.output_folder}/log_file.log'
        logging.basicConfig(level=logging.INFO, filename=logfile)

    def run(self):
        agencies_list_parser = self.list_parser.parse()
        excel = saveExcel("output/ITDashBoard.xlsx", "Agencies")
        headers = ['name', 'amount']
        excel.create_headers(headers, "Agencies")
        for agencies_row in agencies_list_parser:
            excel.append_row(agencies_row, "Agencies")
        excel.new_worksheet("IndividualInvestments")
        self.detail_parser.parse(excel, "IndividualInvestments")
        excel.save()
        self.browser.close_all_browsers()
