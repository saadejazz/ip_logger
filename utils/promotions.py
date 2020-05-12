from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from time import sleep

def denyPromotions(driver, promotions):
    wait = WebDriverWait(driver, 5)
    try:
        for promo in promotions:
            element = wait.until(EC.presence_of_element_located((By.XPATH, f'//input[@id="{promo}"]')))
            if element.get_attribute("value") == "1":
                element = wait.until(EC.visibility_of_element_located((By.XPATH, f'//label[@for="{promo}"]/span')))
                for _ in range(3):
                    driver.execute_script("arguments[0].click();", element)
                    sleep(0.2)
    except (TimeoutException, ElementNotInteractableException):
        print("No promos or something went wrong")
        pass
