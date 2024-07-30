API_KEY = "4NuBIBH31XXnMgmyPy3TPdztZfjco3CwtQ3Oiq03"
APOD_ENDPOINT = 'https://api.nasa.gov/planetary/apod'
OUTPUT_IMAGES = './output'

import requests
import os
from datetime import datetime, timedelta
from concurrent.futures import ProcessPoolExecutor

def get_apod_metadata(start_date: str, end_date: str, api_key: str) -> list:

    response = requests.get(APOD_ENDPOINT, params={
        'api_key': api_key,
        'start_date': start_date,
        'end_date': end_date,
    })

    response.raise_for_status()
    data = response.json()
    return data


def download_image(item):
    link_image = item.get('hdurl')
    if item['media_type'] != 'image' or not link_image:
        return f"Skipped {item['date']} - not an image or missing URL"

    try:
        # download the image
        response = requests.get(link_image)
        response.raise_for_status()

        # save the image
        if not os.path.exists(OUTPUT_IMAGES):
            os.makedirs(OUTPUT_IMAGES)

        with open(os.path.join(OUTPUT_IMAGES, f"{item['date']}.jpg"), 'wb') as file:
            file.write(response.content)
        return f"Downloaded {item['date']}.jpg"
    except Exception as e:
        return f"Failed to download {item['date']} - {str(e)}"

def download_apod_images(metadata: list):
    with ProcessPoolExecutor(max_workers=64) as executor:
        results = executor.map(download_image, metadata)

    for result in results:
        print(result)



def main():
    metadata = get_apod_metadata(
        start_date='2024-01-01',
        end_date='2024-07-26',
        api_key=API_KEY,
    )
    # if the output directory does not exist, create it
    if not os.path.exists(OUTPUT_IMAGES):
        os.makedirs(OUTPUT_IMAGES)


    download_apod_images(metadata)


if __name__ == '__main__':
    main()
