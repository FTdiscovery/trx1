#importing required libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
#from selenium_move_cursor.MouseActions import move_to_element_chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import js
import json
import numpy as np
import time
import pandas as pd         #to save CSV file
from bs4 import BeautifulSoup
import ctypes         #to create text popup
import os

# Remove all extra spaces
def remove_spaces(string):
    return remove_unicode(" ".join(string.split()))


def remove_unicode(string):
 return (string.replace("\u2013", "-")
         .replace("\u2014", "-")
         .replace("\u2015", "-")
         .replace("\u2017", "_")
         .replace("\u2018", "\'")
         .replace("\u2019", "\'")
         .replace("\u201a", ",")
         .replace("\u201b", "\'")
         .replace("\u201c", "\"")
         .replace("\u201d", "\"")
         .replace("\u201e", "\"")
         .replace("\u2026", "...")
         .replace("\u2032", "\'")
         .replace("\u2033", "\""))

unique_div = []

while True:
    previous_length = len(unique_div)
    time.sleep(3)
    soup = bs.BeautifulSoup(browser.page_source, 'html.parser')
    for i in soup.find_all('div'):
        if i.text not in unique_div:
            unique_div.append(i.text)
            #print(i.text)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    after_scraped = len(unique_div)
    if previous_length == after_scraped:
        print("Scraped Everything")
        break
#defining browser and adding the “ — headless” argument
opts = Options()
opts.add_argument(' —-headless')
driver = webdriver.Chrome(os.getcwd()+"/chromedriver106",options=opts)
url = 'https://www.wsj.com/articles/fedex-sues-ground-contractor-that-has-agitated-for-change-11661541479'
driver.maximize_window() #maximize the window
driver.get(url)          #open the URL
result = driver.page_source
soup = BeautifulSoup(result, 'html.parser')
article = soup.select_one('article')

# iterate through all elements with class "article-breadCrumb"
if article is None:
    print("{}")

return_obj = {}
if article.h2 is not None and article.p is not None:
    return_obj["summary"] = remove_spaces(article.h2.text) + ". " + remove_spaces(article.p.text)

print(return_obj)
driver.close()

