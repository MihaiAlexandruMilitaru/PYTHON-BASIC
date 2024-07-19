import re

import requests
from bs4 import BeautifulSoup
import webbrowser


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time

# Setup Selenium WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Open the Yahoo Finance most active stocks page

count = 100
offsets = [0, 100, 200]
companies = []

for offset in offsets:

    base_url = 'https://finance.yahoo.com/most-active'
    params = {
        'count': count,
        'offset': offset,
    }
    response = requests.get(base_url, params=params)
    driver.get(response.url)
    time.sleep(10)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    try:
        table = soup.find('table')
        rows = table.find_all('tr')
    except AttributeError:
        print('No table found')
        continue
    for row in rows[1:]:
        try:
            cells = row.find_all('td')
        except AttributeError:
            print('No cells found')
            continue

        # extract the CEO
        # pattern can  be ceo, CEO, Chief Executive Officer, Chief executive officer, chief executive officer
        ceo_pattern = 'CEO|Chief Executive Officer|Chief executive officer|chief executive officer'
        ceo_array = []

        company_symbol = cells[0].text
        print(company_symbol)
        company_url = f'https://finance.yahoo.com/quote/{company_symbol}/profile'
        company_response = requests.get(company_url)
        driver.get(company_response.url)
        time.sleep(5)
        company_soup = BeautifulSoup(driver.page_source, 'lxml')

        try:
            ceo_table = company_soup.find('table')
            ceo_rows = ceo_table.find_all('tr')
        except AttributeError:
            print('No CEO table found')
            continue

        try:
            div_company_address = company_soup.find('div', {'class': 'address yf-wxp4ja'})
            company_location = div_company_address.find_all('div')
            company_country = company_location[len(company_location)-1].text
            company_address = ' '.join([div.text for div in company_location[:-1]])
        except AttributeError:
            print('No company address found')
            continue

        main_company_url = f'https://finance.yahoo.com/quote/{company_symbol}'
        main_company_response = requests.get(main_company_url)
        driver.get(main_company_response.url)
        main_company_soup = BeautifulSoup(driver.page_source, 'lxml')

        try:
            company_employee = main_company_soup.find('div', {'class': 'infoSection yf-1xu2f9r'})
            company_employee = company_employee.find_all('p')[0].text
            company_employee = int(company_employee.replace(',', '')) if company_employee != '--' else company_employee
        except AttributeError:
            print('No company employee found')
            continue