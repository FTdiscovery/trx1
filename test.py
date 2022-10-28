"""
Trying to scrape from newsfilter.io

1. It will login for you
2. Once it logins, we want it to move to the "FDA Drug Approval" subpage (currently, you have 10 seconds to set it there)
3. starts parsing, rn it parses around 3 months of data. the parsed data is VERY UNCLEAN we will need to fix it
"""

from newsapi import NewsApiClient
from datetime import date, timedelta, datetime, time
from alpaca_trade_api import REST, Stream
import bs4 as bs
import urllib.request
from urllib.request import Request, urlopen
from selenium import webdriver
import time
import os
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from undetected_chromedriver import Chrome

if __name__ == '__main__':
    driver: Chrome = uc.Chrome()
    # driver.get('https://accounts.google.com/')
    YOUR_EMAIL = ''
    YOUR_PASSWORD = ''
    #
    # # add email
    # driver.find_element(By.XPATH, '//*[@id="identifierId"]').send_keys(YOUR_EMAIL)
    # driver.find_element(By.XPATH, '//*[@id="identifierNext"]/div/button/span').click()
    # time.sleep(3)
    # driver.find_element(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input').send_keys(YOUR_PASSWORD)
    # driver.find_element(By.XPATH, '//*[@id="passwordNext"]/div/button/span').click()
    # time.sleep(2)

    driver.get('https://newsfilter.io/latest-news/us-food-and-drug-administration-drug-approvals')
    unique_div = []
    articles = []

    # LOG IN
    driver.find_element(By.XPATH, '//*[@class="sc-VigVT eWHfRB"]').click()
    # add email
    driver.find_element(By.XPATH, '//*[@id="identifierId"]').send_keys(YOUR_EMAIL)
    driver.find_element(By.XPATH, '//*[@id="identifierNext"]/div/button/span').click()
    time.sleep(2)
    driver.find_element(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input').send_keys(YOUR_PASSWORD)
    driver.find_element(By.XPATH, '//*[@id="passwordNext"]/div/button/span').click()
    time.sleep(4)

    driver.find_element(By.XPATH, '//*[@class="sc-clNaTc gVIbPZ"]').click()
    time.sleep(10)
    # driver.find_element(By.XPATH, '//a[contains(@href,"latest-news/us-food-and-drug-administration-drug-approvals")]').click()
    # time.sleep(3)

    while len(unique_div) < 5000:
        previous_length = len(unique_div)
        time.sleep(3)
        soup = bs.BeautifulSoup(driver.page_source, 'html.parser')

        for i in soup.find_all('div'):

            if i.text not in unique_div:
                unique_div.append(i.text)
                if "Sign up with Google" in i.text:
                    print(i)
                    print("---")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        after_scraped = len(unique_div)
        if previous_length == after_scraped:
            print("Scraped Everything")
            break

    print(unique_div)
#
#
# opts = Options()
# opts.add_argument(' —-headless')
#
# url = 'https://newsfilter.io/latest-news/us-food-and-drug-administration-drug-approvals'
# browser = webdriver.Chrome(os.getcwd()+"/chromedriver106",options=opts)
# browser.get(url)
#
# unique_div = []
# articles = []
#
# while True:
#     previous_length = len(unique_div)
#     time.sleep(3)
#     soup = bs.BeautifulSoup(browser.page_source, 'html.parser')
#     for i in soup.find_all('div'):
#
#         if i.text not in unique_div:
#             unique_div.append(i.text)
#             if "Log In Required" in i.text:
#                 print(i.text)
#                 print(i)
#     browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     after_scraped = len(unique_div)
#     if previous_length == after_scraped:
#         print("Scraped Everything")
#         break
