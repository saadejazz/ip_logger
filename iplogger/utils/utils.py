# pylint: disable=no-member
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.firefox.options import Options
from stem.control import Controller
from ...conf import EXECUTABLE_PATH
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
    return webdriver.Firefox(executable_path = executable_path, options=options, firefox_profile=fp)

def efficientGet(driver, url):
    try:
        if driver.current_url != url:
            driver.get(url)
    except WebDriverException:
        print("Something went wrong. Please try again")

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
