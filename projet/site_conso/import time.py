import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def set_viewport_size(driver, width, height):
    window_size = driver.execute_script("""
        return [window.outerWidth - window.innerWidth + arguments[0],
          window.outerHeight - window.innerHeight + arguments[1]];
        """, width, height)
    driver.set_window_size(window_size)

URL = "https://data.enedis.fr/pages/accueil/?id=dataviz-consommation-et-production-au-pas-12h"
option = Options()
s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(options = option, service = s)
driver.maximize_window()
driver.get(URL)
driver.switch_to.frame(0)
driver.find_element(By.CSS_SELECTOR, ".local-drop-button-title > .ng-binding").click()
driver.find_element(By.CSS_SELECTOR, ".local-drop-frame-content-wrap:nth-child(3) > .ng-binding").click()
driver.find_element(By.CSS_SELECTOR, "td:nth-child(1) > .ng-pristine").click()
a = driver.find_element(By.XPATH, "///div/div/div/div/div/ods-dataset-context/div[1]/div[3]/div/table/tbody/tr/td[1]/select")
b = a.find_element(By.XPATH, "//option[@selected = 'selected']")
driver.execute_script('arguments[0].removeAttribute("selected")', b)
c = a.find_element(By.XPATH, "//option[@value = 'PRO4']")
driver.execute_script('arguments[0].setAttribute("selected", "selected")', c)