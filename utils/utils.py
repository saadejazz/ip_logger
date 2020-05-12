# pylint: disable=no-member
from selenium.webdriver.firefox.options import Options
from stem.control import Controller
from ..conf import EXECUTABLE_PATH
from selenium import webdriver
from bs4 import BeautifulSoup
from stem import Signal


def setDriver(executable_path = None, headless = True):
    if executable_path is None:
        executable_path = EXECUTABLE_PATH
    fp = webdriver.FirefoxProfile()
    fp.set_preference("network.proxy.type", 1)
    fp.set_preference("network.proxy.socks","127.0.0.1")
    fp.set_preference("network.proxy.socks_port", 9050)
    fp.update_preferences()
    options = Options()
    options.headless = headless
    return webdriver.Firefox(options=options, firefox_profile=fp)

    # fp = webdriver.FirefoxProfile()
    # fp.set_preference("permissions.default.desktop-notification", 2)
    # options = webdriver.FirefoxOptions()
    # options.add_argument('-headless')
    # options.headless = headless
    # fp.set_preference('network.proxy.type', 1)
    # fp.set_preference('network.proxy.socks', '127.0.0.1')
    # fp.set_preference('network.proxy.socks_port', 9051)
    # fp.update_preferences()
    # driver = webdriver.Firefox(executable_path = executable_path, firefox_options = options, firefox_profile = fp)
    # return driver
    # chrome_options = webdriver.ChromeOptions()
    # prefs = {"profile.default_content_setting_values.notifications" : 2}
    # chrome_options.add_experimental_option("prefs",prefs)
    # if headless:
    #     chrome_options.add_argument('--headless')
    # return webdriver.Chrome(executable_path = executable_path, chrome_options=chrome_options)

def efficientGet(driver, url):
    if driver.current_url != url:
        driver.get(url)

def verifyDateFormat(string):
    if type(string) == str:
        s = string.split("-")
        if len(s) == 3:
            if len(s[0]) == 4 and len(s[1]) == 2 and len(s[2]) == 2:
                return True
    return False

def separateData(so):
    return BeautifulSoup(str(so).replace("<br/>", "\n"), "html.parser").text.split("\n")

def changeIP():
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)
