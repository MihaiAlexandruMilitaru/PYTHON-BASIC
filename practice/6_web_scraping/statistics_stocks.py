import json
json_file = 'companies.json'

from tabulate import tabulate

def task1():
    with open(json_file, 'r') as file:
        companies = json.load(file)

    ceo_array = []

    for company in companies:
        for ceo in company['ceo']:
            try:
                ceo['born'] = int(ceo['born'])
            except ValueError:
                ceo['born'] = None
            ceo_entity = {
                'name': ceo['name'],
                'birth_year': int(ceo['born']) if ceo['born'] else 0,
                'company_name': company['name'],
                'company_code': company['symbol'],
                'employees': company['employees'],
                'country': company['country']
            }
            ceo_array.append(ceo_entity)

    # sort the companies by youngest CEO
    ceo_array = sorted(ceo_array, key=lambda x: -x['birth_year'])
    sheet = [['Name', 'Code', 'Country', 'Employees', 'CEO Name', 'CEO Year Born']]
    for c in ceo_array[:5]:
        sheet.append([c['company_name'], c['company_code'], c['country'], c['employees'], c['name'], c['birth_year']])

    # Format the data
    formatted_table = tabulate(sheet, headers='firstrow', tablefmt='grid')

    # Write the formatted table to a text file
    with open('ceo_table.txt', 'w') as f:
        f.write(formatted_table)

    print("Formatted table has been written to ceo_table.txt")

def task2():
    with open(json_file, 'r') as file:
        companies = json.load(file)

    stocks = []

    for company in companies:
        stock = {
            'name': company['name'],
            'code': company['symbol'],
            '52_week_change': company['52_week_range'],
            'total_cash': company['total_cash']
        }
        stocks.append(stock)

    sorted_stocks = sorted(stocks, key=lambda x: -float(x['52_week_change'][:-1]))
    sheet = [['Name', 'Code', '52-Week Change', 'Total Cash']]

    for s in sorted_stocks[:10]:
        sheet.append([s['name'], s['code'], s['52_week_change'], s['total_cash']])

    formatted_table = tabulate(sheet, headers='firstrow', tablefmt='grid')

    with open('stocks_table.txt', 'w') as f:
        f.write(formatted_table)

    print("Formatted table has been written to stocks_table.txt")


if __name__ == '__main__':
    task1()
    task2()