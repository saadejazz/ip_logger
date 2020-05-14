from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from .utils.utils import efficientGet, setDriver, get, beautify
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

class IpLogger():
    def __init__(self, headless = True, timeout = 10):
        self.headless = headless
        self.timeout = 10
        self.URL = "https://blasze.com/"

    def create_payload(self, url):
        '''
        Creates a shortened url that logs IP of any who clicks on it. Service used: "https://blasze.com/"
        '''
        self.log_driver = setDriver(headless = self.headless)
        self.wait = WebDriverWait(self.log_driver, self.timeout)
        efficientGet(self.log_driver, self.URL)
        if type(url) == str:
            try:
                element = self.wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="urlorcode"]')))
                element.clear()
                element.send_keys(url)
                element = self.wait.until(EC.presence_of_element_located((By.XPATH, '//button[text()="Submit"]')))
                self.log_driver.execute_script("arguments[0].click();", element)
                self.wait.until(EC.visibility_of_element_located((By.XPATH, '//h3[text()="Share This Link"]')))
                element = self.log_driver.find_element_by_tag_name('body')
                value = element.get_attribute("innerHTML")
                if value is not None:
                    soup = BeautifulSoup(value, "html.parser")
                    a = soup.find("table")
                    if a:
                        data = {
                            "original_url": "",
                            "payload_url": "",
                            "tracking_code": "",
                            "tracking_url": "",
                            "is_successful": True
                        }
                        keys = ["tracking_code", "original_url", "payload_url"]
                        x = ["Access Code", "Original URL", "Tracking Link (give this out)"]
                        for i in range(3):
                            t = a.find("th", text = x[i])
                            if t:
                                data[keys[i]] = t.findNext("td").text
                        data["tracking_url"] = self.URL + "track/" + data["tracking_code"]
                        self.log_driver.close()
                        return data
            except (TimeoutException, NoSuchElementException) as err:
                print(f'Something went wrong during url shortening. Check {self.URL}. Error: {err}.')
        self.log_driver.close()
        return {
            "original_url": url,
            "payload_url": "",
            "tracking_code": "",
            "tracking_url": "",
            "is_successful": False
        }

    def track_code(self, code = None, url = None, start_date = None, end_date = None):
        '''
        Tracks logger corresponding to tracking code or url. This can be obtained from the 'create_payload' method of IpLogger.
        Provide start_date and end_date in the following format: yyyy-mm-dd.
        '''
        response = {
            "code_exists": False,
            "data": []
        }
        if code is None and url is None:
            print("Provide one of tracking code or url to track logger")
            return response
        if code is not None:
            url = f'{self.URL}track/{code}'
        soup = BeautifulSoup(get(url), "html.parser")
        a = soup.find("h3", text = "Access Logs")
        if a:
            results = []
            response["code_exists"] = True
            a = a.findNext('tbody')
            if a:
                for x in a.find_all('tr'):
                    result = {
                        "timestamp": "",
                        "ip": "",
                        "user_agent": "",
                        "hostname": "",
                        "referring_url": ""
                    }
                    td = x.find_all('td')
                    if len(td) == len(result.keys()):
                        for i in range(len(result.keys())):
                            result[list(result.keys())[i]] = beautify(td[i].text)
                    results.append(result)
                response["data"] = results
        return response

