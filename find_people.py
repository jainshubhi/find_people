import json
import time
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def read_config():
    '''
    Read config.json file. config.json should have companies and jobs keys.
    '''
    with open('config.json') as f:
        config = json.load(f)
    return config['companies'], config['jobs']

def login(driver):
    '''
    Login to linkedin.
    '''
    driver.get('https://www.linkedin.com/')
    elem = driver.find_element_by_id('login-email')
    elem.send_keys(os.environ['EMAIL_USERNAME'])
    elem = driver.find_element_by_id('login-password')
    elem.send_keys(os.environ['EMAIL_PASSWORD'])
    elem.send_keys(Keys.RETURN)

def search_person(driver, company, job):
    '''
    Opens a linkedin page and searches for a specific person with a specific job
    and specific company.
    '''
    driver.get('https://www.linkedin.com/vsearch/f?f_N=F,S,A&openFacets=N,G,CC&rsid=1934857271457685716329&adv=open')
    try:
        # Enter in title
        elem = driver.find_element_by_name('title')
        elem.send_keys(job)
        # Select current in title advanced options
        driver.find_element_by_xpath("//select[@name='titleScope']/option[text()='Current']").click()
        # Enter in company name
        elem = driver.find_element_by_name('company')
        elem.send_keys(company)
        # Select current in company advanced options
        driver.find_element_by_xpath("//select[@name='companyScope']/option[text()='Current']").click()
        # Submit
        elem = driver.find_element_by_name('submit')
        elem.click()
    except:
        print 'Could not find required element'
        driver = webdriver.Chrome()
        login(driver)
        time.sleep(5)
        search_person(driver, company, job)
    # Wait for results to load
    time.sleep(2)
    if 'Sorry, no results containing' in driver.page_source:
        return []
    else:
        # TODO: Return list of names in search results
        try:
            elems = driver.find_elements_by_xpath("//a[@class='title main-headline']")
            return invalid_results([elem.text for elem in elems])
        except:
            return []

def invalid_results(results):
    '''
    This method removes invalid results from returned results
    '''
    # Remove invalid profiles
    results = filter((lambda x: 'LinkedIn' not in x), results)
    # Only have unique elements
    return list(set(results))

if __name__ == '__main__':
    # Login to LinkedIn and set up selenium
    driver = webdriver.Chrome()
    login(driver)
    # Search config
    companies, jobs = read_config()
    # Sleep 5 seconds
    time.sleep(5)
    results = {}
    for company in companies:
        results[company] = []
        for job in jobs:
            results[company] += search_person(driver, company, job)
            time.sleep(3.5)
    time.sleep(3)
    driver.close()
    # Write results of search_person to a json file
    # (key: company, value: [name])
    with open('people.json', 'w') as f:
        json.dump(results, f, sort_keys=True, indent=4)
    print 'Done'
