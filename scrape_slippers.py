import os.path
import subprocess
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import os
from os import path
import html5lib
import sys
import csv

CHROMEDRIVER_PATH='C:/Users/sarat/OneDrive/Pictures/chromedriver.exe'
link='https://www.maharashtradirectory.com/product/tractor-parts.html'
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,options=options)
driver.get(link)
time.sleep(10)
address_html=BeautifulSoup(driver.page_source, 'html5lib')

address_div=address_html.find_all('div',class_='col-md-12')
source_list=[]
for ss in address_div:
 finder= ss.find('div',class_='pb-5')
 if finder:
     source_list.append(finder)
needed=source_list[0].find_all('div',class_='result_container--right-title')
suppliers=list(filter(None, [ho.get_text().replace('\n', '') for ho in needed]))
with open("C:/Users/sarat/New folder/Desktop/data/supplier_name.csv", "w") as file:
    wr = csv.writer(file, delimiter=',',quoting=csv.QUOTE_ALL)
    wr.writerow(suppliers)
    
print(suppliers[:10])

