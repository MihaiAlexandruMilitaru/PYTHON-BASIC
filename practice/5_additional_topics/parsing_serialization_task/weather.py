import os
import json
import requests
from datetime import datetime
import xml.etree.ElementTree as ET

source_data_dir = 'source_data'

weather = ET.Element('weather')

# Function to convert Unix timestamp to human-readable date
def unix_to_date(timestamp, offset):
    from datetime import datetime, timedelta
    return (datetime.utcfromtimestamp(timestamp) + timedelta(seconds=offset)).strftime('%Y-%m-%d %H:%M:%S')

mean_temp_all = 0
mean_wind_speed_all = 0

# min temp is -inf, max temp is +inf
min_temp_all = float('inf')
max_temp_all = float('-inf')

max_wind_speed_all = float('-inf')
coldest_place = ''
warmest_place = ''
windiest_place = ''

cities = []

# <weather country="Belarus" date="2021-09-25">
#   <summary mean_temp="11.29" mean_wind_speed="5.21" coldest_place="Vitebsk" warmest_place="Brest" windiest_place="Grodno"/>
#   <cities>
#     <Brest mean_temp="13.46" mean_wind_speed="4.78" min_temp="8.99" min_wind_speed="2.68" max_temp="16.99" max_wind_speed="7.47"/>
#     <Gomel mean_temp="11.86" mean_wind_speed="5.17" min_temp="8.98" min_wind_speed="3" max_temp="14.87" max_wind_speed="6"/>
#     <Grodno mean_temp="12.49" mean_wind_speed="6.18" min_temp="8.57" min_wind_speed="3.41" max_temp="16.72" max_wind_speed="10"/>
#     <Minsk mean_temp="10.97" mean_wind_speed="5.92" min_temp="8.85" min_wind_speed="4.12" max_temp="13.85" max_wind_speed="7.74"/>
#     <Mogilev mean_temp="9.71" mean_wind_speed="4.93" min_temp="6.04" min_wind_speed="3" max_temp="12.38" max_wind_speed="7.21"/>
#     <Vitebsk mean_temp="9.22" mean_wind_speed="4.26" min_temp="5.81" min_wind_speed="2" max_temp="12.08" max_wind_speed="6"/>
#   </cities>
# </weather>

# Create country and date attributes
weather.set('country', 'Spain')
date = datetime.now().strftime('%Y-%m-%d')
weather.set('date', date)


for city_folder in os.listdir(source_data_dir):
    city_folder_path = os.path.join(source_data_dir, city_folder)
    path = city_folder_path.split('/')
    city = path[1].replace(' ', '_')


    mean_city_temp = 0
    mean_city_wind_speed = 0

    if os.path.isdir(city_folder_path):
        for filename in os.listdir(city_folder_path):
            if filename.endswith('.json'):
                filepath = os.path.join(city_folder_path, filename)

                with open(filepath, 'r') as file:
                    data = json.load(file)

                city_name = city
                mean_city_temp = sum(hourly['temp'] for hourly in data['hourly']) / len(data['hourly'])
                mean_city_wind_speed = sum(hourly['wind_speed'] for hourly in data['hourly']) / len(data['hourly'])
                min_temp = min(hourly['temp'] for hourly in data['hourly'])
                max_temp = max(hourly['temp'] for hourly in data['hourly'])
                min_wind_speed = min(hourly['wind_speed'] for hourly in data['hourly'])
                max_wind_speed = max(hourly['wind_speed'] for hourly in data['hourly'])

                mean_temp_all += mean_city_temp
                mean_wind_speed_all += mean_city_wind_speed

                if min_temp < min_temp_all:
                    min_temp_all = min_temp
                    coldest_place = city_name

                if max_temp > max_temp_all:
                    max_temp_all = max_temp
                    warmest_place = city_name

                if max_wind_speed > max_wind_speed_all:
                    max_wind_speed_all = max_wind_speed
                    windiest_place = city_name

                city_dict = {
                    'name': city_name,
                    'mean_temp': mean_city_temp,
                    'mean_wind_speed': mean_city_wind_speed,
                    'min_temp': min_temp,
                    'max_temp': max_temp,
                    'min_wind_speed': min_wind_speed,
                    'max_wind_speed': max_wind_speed
                }

                cities.append(city_dict)


mean_temp_all /= len(cities)
mean_wind_speed_all /= len(cities)

# Create summary element
summary = ET.SubElement(weather, 'summary')
summary.set('mean_temp', f"{mean_temp_all:.2f}")
summary.set('mean_wind_speed', f"{mean_wind_speed_all:.2f}")
summary.set('coldest_place', coldest_place)
summary.set('warmest_place', warmest_place)
summary.set('windiest_place', windiest_place)

# Create cities element
cities_element = ET.SubElement(weather, 'cities')

for city in cities:
    city_element = ET.SubElement(cities_element, city['name'])
    city_element.set('mean_temp', f"{city['mean_temp']:.2f}")
    city_element.set('mean_wind_speed', f"{city['mean_wind_speed']:.2f}")
    city_element.set('min_temp', f"{city['min_temp']:.2f}")
    city_element.set('max_temp', f"{city['max_temp']:.2f}")
    city_element.set('min_wind_speed', f"{city['min_wind_speed']:.2f}")
    city_element.set('max_wind_speed', f"{city['max_wind_speed']:.2f}")

# Create XML file
tree = ET.ElementTree(weather)
ET.indent(tree, '  ')
tree.write('weather.xml')


