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
            company_symbol = cells[0].text
            print(company_symbol)
        except AttributeError:
            print('No cells found')
            continue

        # extract the CEO
        # pattern can  be ceo, CEO, Chief Executive Officer, Chief executive officer, chief executive officer
        ceo_pattern = 'CEO|Chief Executive Officer|Chief executive officer|chief executive officer'
        ceo_array = []

        company_symbol = cells[0].text
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

        statistics_url = f'https://finance.yahoo.com/quote/{company_symbol}/key-statistics'
        statistics_response = requests.get(statistics_url)
        driver.get(statistics_response.url)
        statistics_soup = BeautifulSoup(driver.page_source, 'lxml')

        try:
            statistics_table = statistics_soup.find_all('table')[7]
            week_range = statistics_table.find_all('tr')[1].find_all('td')[1].text
            section = statistics_soup.find_all('section', {'class': 'card small tw-p-0 yf-13ievhf sticky'})[4]
            table = section.find_all('table')[0]
            row = table.find_all('tr')[0]

            total_cash = row.find_all('td')[1].text
        except AttributeError:
            print('No statistics found')
            continue

        holders_url = f'https://finance.yahoo.com/quote/{company_symbol}/holders'
        holders_response = requests.get(holders_url)
        driver.get(holders_response.url)
        holders_soup = BeautifulSoup(driver.page_source, 'lxml')

        # table with class 'svelte-1s2g2lo'

        vanguard_value = 0
        shares = ''
        date_reported = ''
        out = ''

        try:
            holders_table = holders_soup.find_all('table', {'class': 'yf-1s2g2l0'})[0]
            rows = holders_table.find_all('tr')
            for r in rows:
                content = r.find_all('td')
                content_array = [c.text for c in content]
                # strip the content
                content_array = [c.strip() for c in content_array]
                if 'Blackrock Inc.' in content_array:
                    vanguard_value_str = content_array[4]
                    vanguard_value = int(vanguard_value_str.replace(',', '')) if vanguard_value_str != '--' else 0
                    shares_str = content_array[1]
                    date_reported = content_array[2]
                    out_str = content_array[3]

                    shares = shares_str
                    out = out_str
                    
        except AttributeError:
            print('No holders table found')
            continue
        except IndexError:
            print('No holders table found')
            continue

        for ceo_row in ceo_rows:
            ceo_pattern = 'CEO'

            # check if the row contains CEO with regex pattern
            found = re.search(ceo_pattern, ceo_row.text)
            if not found:
                continue

            ceo_name = ceo_row.find_all('td')[0].text.strip()
            ceo_title = ceo_row.find_all('td')[1].text.strip()
            ceo_pay = ceo_row.find_all('td')[2].text.strip()
            ceo_exercised = ceo_row.find_all('td')[3].text.strip()
            ceo_born = ceo_row.find_all('td')[4].text.strip()

            ceo = {
                'name': ceo_name,
                'title': ceo_title,
                'pay': ceo_pay,
                'exercised': ceo_exercised,
                'born': ceo_born,
            }

            print(ceo_name, ceo_title, ceo_pay, ceo_exercised, ceo_born)
            ceo_array.append(ceo)

        company = {
            'symbol': cells[0].text,
            'name': cells[1].text,
            'price': cells[2].text,
            'change': cells[3].text,
            'change_percentage': cells[4].text,
            'volume': cells[5].text,
            'avg_volume': cells[6].text,
            'market_cap': cells[7].text,
            'pe_ratio': cells[8].text,
            'address': company_address,
            'country': company_country,
            'employees': company_employee,
            '52_week_range': week_range,
            'total_cash': total_cash,
            'vanguard_value': vanguard_value,
            'shares': shares,
            'date_reported': date_reported,
            'out': out,
            'ceo': ceo_array,
        }
        companies.append(company)

        print(company, '\n')
        time.sleep(10)


for company in companies:
    print(company['name'])

# Close the WebDriver

driver.quit()

# print the companies in a json format

import json

with open('companies.json', 'w') as f:
    json.dump(companies, f, indent=4)


