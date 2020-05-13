from selenium.common.exceptions import ElementNotInteractableException, ElementClickInterceptedException
from .utils.utils import efficientGet, setDriver, verifyDateFormat, separateData, changeIP
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from .utils.promotions import denyPromotions
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from .conf import PROMOTIONS
from time import sleep

class IpLogger():
    def __init__(self, headless = True, timeout = 10):
        self.log_driver = setDriver(headless = headless)
        self.wait = WebDriverWait(self.log_driver, timeout)
        self.URL = "https://iplogger.org/"
        self.DOMAIN = "https://2no.co/"
        self.PROMOTIONS = PROMOTIONS
        self.logs = []
        changeIP()

    def create_payload(self, url):
        '''
        Creates a shortened url that logs IP of any who clicks on it. Service used: "iplogger.org"
        '''
        efficientGet(self.log_driver, self.URL)
        if type(url) == str:
            try:
                smallWait = WebDriverWait(self.log_driver, 3)
                element = self.wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="text"]')))
                element.clear()
                element.send_keys(url)
                element = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@id="fastshort"]/form/button')))
                self.log_driver.execute_script("arguments[0].click();", element)
                try:
                    element = smallWait.until(EC.visibility_of_element_located((By.XPATH, '//label[@for="gdprok1"]/span[1]')))
                    self.log_driver.execute_script("arguments[0].click();", element)
                    element = smallWait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Next" and @type="submit"]')))
                    self.log_driver.execute_script("arguments[0].click();", element)
                except TimeoutException:
                    pass
                element = self.wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@name="imglink"]')))
                self.log_driver.execute_script(f'arguments[0].value="{url}"', element)
                element.send_keys(Keys.ENTER)
                element = self.wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="fromfirst"]')))
                denyPromotions(self.log_driver, self.PROMOTIONS)
                value = element.get_attribute("value")
                if value is not None:
                    value = value.split("/")[-1]
                    value = self.DOMAIN + value
                    payload_url = value
                    if payload_url is not None:
                        element = self.log_driver.find_element_by_xpath('//input[@id="fromlogger2"]')
                        value = element.get_attribute("value")
                        if value is not None:
                            data = {
                                "original_url": url,
                                "payload_url": payload_url,
                                "tracking_code": value,
                                "tracking_url": f'https://www.iplogger.org/logger/{value}',
                                "is_successful": True
                            }
                            self.logs.append(data)
                            if len(self.logs) > 7:
                                changeIP()
                                self.logs = []
                            return data
            except (TimeoutException, ElementNotInteractableException, NoSuchElementException) as err:
                print(f'Something went wrong during url shortening. Check {self.URL}. Error: {err}.')
                changeIP()
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
        if code is None and url is None:
            print("Provide one of tracking code or url to track logger")
            return []
        if code is not None:
            url = f'https://www.iplogger.org/logger/{code}'
        if url.startswith("https://www.iplogger.org/logger/"):
            efficientGet(self.log_driver, url)
            smallWait = WebDriverWait(self.log_driver, 3)
            try:
                element = smallWait.until(EC.visibility_of_element_located((By.XPATH, '//label[@for="gdprok1"]/span[1]')))
                self.log_driver.execute_script("arguments[0].click();", element)
                element = smallWait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Next" and @type="submit"]')))
                self.log_driver.execute_script("arguments[0].click();", element)
            except:
                pass
            try:
                xpaths = [
                    '//label[@for="tab-2"]',
                    '//ul[contains(@class, "cd-pagination")]/li[@value="100"]'
                ]
                for xpath in xpaths:
                    element = self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
                    self.log_driver.execute_script("arguments[0].click();", element)
                ids = ["botsfield", "advancedfield"]
                for i in ids:
                    element = self.log_driver.find_element_by_xpath(f'//input[@id="{i}"]')
                    if element.get_attribute("checked") is None:
                        element = self.log_driver.find_element_by_xpath(f'//label[@for="{i}"]/span[1]')
                        self.log_driver.execute_script("arguments[0].click();", element)
                if verifyDateFormat(start_date):
                    element = self.log_driver.find_element_by_xpath('//input[@id="viewsd"]')
                    self.log_driver.execute_script(f'arguments[0].value="{start_date}"', element)
                if verifyDateFormat(end_date):
                    element = self.log_driver.find_element_by_xpath('//input[@id="viewed"]')
                    self.log_driver.execute_script(f'arguments[0].value="{end_date}"', element)
                sleep(0.5)
                element = self.log_driver.find_element_by_xpath('//div[contains(@class, "refresh")]')
                self.log_driver.execute_script("arguments[0].click();", element)
                sleep(1)
                try:
                    self.log_driver.find_element_by_xpath('//div[text()="On selected period no records found. Try to change filters."]')
                    return []
                except NoSuchElementException:
                    pass
                element = self.wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="statcontent"]')))
                element = element.get_attribute("innerHTML")
                if element is not None:
                    results = []
                    soup = BeautifulSoup(element, "html.parser")
                    for dev in soup.find_all("div", {'class': "statline"}):
                        result = {
                            "timestamp":{
                                "date": "",
                                "time": ""
                            },
                            "network_information":{
                                "ip_address": "",
                                "isp": "",
                            },
                            "location_information": {
                                "country": "",
                                "city": ""
                            },
                            "device_info": {
                                "os": "",
                                "browser": "",
                                "user_agent": ""
                            }
                        }
                        div = dev.find('div')
                        if div:
                            a = separateData(div)
                            if len(a) >= 2:
                                result["timestamp"]["date"] = a[0]
                                result["timestamp"]["time"] = a[1]
                        div = div.findNext("div")
                        if div:
                            a = separateData(div)
                            if len(a) >=2:
                                result["network_information"]["ip_address"] = a[0]
                                result["network_information"]["isp"] = a[1]
                        div = dev.find("div", {"class": "lc-ip"})
                        if div:
                            a = separateData(div)
                            if len(a) >= 2:
                                result["location_information"]["country"] = a[0]
                                result["location_information"]["city"] = a[1]
                        div = dev.find(lambda tag: tag.find("img"))
                        if div:
                            a = div.find_all("img")
                            if len(a) >= 2:
                                result["device_info"]["os"] = a[0].get("title", "")
                                result["device_info"]["browser"] = a[1].get("title", "")
                        div = dev.findNext("div", {"title": "Device identificator"})
                        if div:
                            result["device_info"]["user_agent"] = div.text.partition("Device identificator: ")[2]
                        results.append(result)
                    return results
            except (ElementClickInterceptedException, TimeoutException, NoSuchElementException):
                print("Something went wrong")
        return []

    def __del__(self):
        self.log_driver.close()
