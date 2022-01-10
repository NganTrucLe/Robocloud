from RPA.Browser.Selenium import Selenium


class AgenciesList:
    URL = "https://itdashboard.gov"

    def __init__(self):
        self.browser = Selenium()
        self.browser.open_available_browser(self.URL)
        
    def agencies_list(self):
        self.browser.wait_until_element_is_visible('//*[@href="#home-dive-in"]')
        self.browser.click_element('//*[@href="#home-dive-in"]')
        # Medium: please don't use generic styling tag like noUnderline to select element. Style can change. Please change it to a structure query
        self.browser.wait_until_element_is_visible(locator=['css:div.noUnderline'])
        agencies = self.browser.get_webelements('css:div.noUnderline')
        return agencies

    def agency_name(self, agency_element):
        self.browser.wait_until_element_is_visible(locator=[agency_element,
            'css:span:nth-of-type(1)'])
        return self.browser.get_webelement(locator=[agency_element,
            'css:span:nth-of-type(1)']).text
    
    def agency_amount(self, agency_element):
        self.browser.wait_until_element_is_visible(locator=[agency_element,
            'css:span:nth-of-type(2)'])
        return self.browser.get_webelement(locator=[agency_element,
            'css:span:nth-of-type(2)']).text

    def parse(self):
        agencies_elements = self.agencies_list()
        agencies = []
        for agency_element in agencies_elements:
            agency = [self.agency_name(agency_element),
                self.agency_amount(agency_element)]
            agencies.append(agency)
        return agencies
