# pylint: disable=no-member
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options
from stem.control import Controller
from ...conf import EXECUTABLE_PATH
from selenium import webdriver
from bs4 import BeautifulSoup
from stem import Signal
import requests


def setDriver(executable_path = None, headless = True):
    if executable_path is None:
        executable_path = EXECUTABLE_PATH
    fp = webdriver.FirefoxProfile()
    # fp.set_preference("network.proxy.type", 1)
    # fp.set_preference("network.proxy.socks","127.0.0.1")
    # fp.set_preference("network.proxy.socks_port", 9050)
    caps = DesiredCapabilities().FIREFOX
    # caps["pageLoadStrategy"] = "normal"  #  complete
    caps["pageLoadStrategy"] = "eager"
    fp.update_preferences()
    options = Options()
    options.headless = headless
    return webdriver.Firefox(capabilities = caps, executable_path = executable_path, options=options, firefox_profile=fp)

def efficientGet(driver, url):
    try:
        if driver.current_url != url:
            driver.get(url)
    except WebDriverException:
        print("Something went wrong. Please try again")

def get(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    try:
        r = requests.get(url, headers = headers)
        if r.status_code == 200:
            return r.text
        else:
            print("Response Code: ", r.status_code)
            return ""
    except requests.exceptions.RequestException as err:
        print(err)
        return ""

def beautify(string):
    if string.startswith(" "):
        string = string[1:]
    if string.endswith(" "):
        string = string[:-1]
    return string
