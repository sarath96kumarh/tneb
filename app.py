from flask import Flask,jsonify,request
import requests
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
from fpdf import FPDF 
from os import path
import html5lib
import sys

app = Flask(__name__)

bill_path='/app/tneb_pdf_bills'

tneb_link = 'https://www.tnebnet.org/awp/login'


GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google-chrome'  
CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver' 
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--remote-debugging-port=9222')
chrome_options.binary_location = GOOGLE_CHROME_PATH



@app.route('/PaymentDetail',methods=['POST']) 
def home():
    if request.method == "POST":
        data = request.get_json()
    
        
        if len(data) ==2:
              driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=chrome_options)
              driver.get(tneb_link)
              mail_or_number=driver.find_element_by_xpath('//*[@id="userName"]')
              mail_or_number.send_keys(data['user_id'])
              user_password=driver.find_element_by_xpath('//*[@id="password"]')
              user_password.send_keys(data['tneb_password'])
              driver.find_element_by_xpath('//*[@id="lin"]/table/tbody/tr/td[1]/table/tbody/tr[6]/td/input').click()
              time.sleep(3)
              driver.find_element_by_xpath('//*[@id="header1"]/div/table/tbody/tr[3]/td/label/a[3]').click()
              time.sleep(1)
              address_html=BeautifulSoup(driver.page_source, 'html5lib')
              address_div=address_html.find('div',class_='ui-datatable ui-widget')
              address_span=address_div.find_all('span')
              address_content=list(filter(None, [ho.get_text() for ho in address_span]))
              driver.find_element_by_css_selector('button[class^="ui-button ui-widget ui-state-default ui-corner-all ui-button-icon-only"]').click()
              time.sleep(3)
           
           
              driver.find_element_by_css_selector('button[class^="ui-button ui-widget ui-state-default ui-corner-all ui-button-icon-only"]').click()
              time.sleep(3)
              ebbill= BeautifulSoup(driver.page_source, 'html5lib')
              bill_heading_table=ebbill.find('table',attrs={"width":"100%"})
              bill_heading_row=bill_heading_table.find_all('td')
              bill_info_table=ebbill.find('table',attrs={"cellpadding":"4"})  
              bill_info_row=bill_info_table.find_all('td')
              bill_header=list(filter(None, [ho.get_text() for ho in bill_heading_row]))
           
              def Convert(lst): 
                res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)} 
                return res_dct 
                
              bill_text=Convert(list(filter(None, [ho.get_text() for ho in bill_info_row])))
              bill_dic=dict(bill_text)
              bill_text_pair=[dd+' '+kk for dd,kk in bill_text.items()]
              bill=bill_header+bill_text_pair
              pdf = FPDF()    
              pdf.add_page() 
              pdf.set_font("Arial", size = 15) 
           
              for gg in bill:
                pdf.cell(200, 10, txt = gg,  ln = 1, align = 'C') 
           
              path=os.path.exists(bill_path)
              path_to_file=os.path.exists(bill_path+'/'+data["user_id"])
              if path == False:
                os.mkdir(bill_path)
              if path_to_file ==False:
                os.mkdir(bill_path+'/'+data["user_id"])
            
              pdf.output(bill_path+'/'+data["user_id"]+"/tneb_bill_of_"+bill_dic['Receipt Date:']+".pdf")
              driver.close()
           
              item_to_be_retrieved=['Name:','Bill Amount:','Receipt No','Receipt Date:']
              bill=dict([(key, value) for key,value in bill_text.items() if key in item_to_be_retrieved])
              bill['Address']=address_content[-2]
              return jsonify({'PaymentDetail':bill})
           
           
           
           
       
        else:
            check_list=['tneb_user_id','tneb_password']
            given_list=list(data.keys())
            miss_value=[keys for keys in check_list if keys not in given_list]
            if miss_value:
                return jsonify({'parameter not given':miss_value})
         
        
 
if __name__ == "__main__":
    app.run(debug=True)
    
