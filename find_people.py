import json
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def read_config():
    '''
    Read config.json file. config.json should have companies and jobs keys.
    '''
    with open('config.json') as f:
        config = json.load(f)
    return config

def search_person(company, job):
    driver = webdriver.Chrome()
    driver.get("https://www.linkedin.com")
    assert "Python" in driver.title
    elem = driver.find_element_by_name("q")
    elem.send_keys("pycon")
    elem.send_keys(Keys.RETURN)
    assert "No results found." not in driver.page_source
    driver.close()
