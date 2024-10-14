import requests
import os

AUTH_TOKEN = os.getenv('AUTH_TOKEN')

if not AUTH_TOKEN:
    raise ValueError("AUTH_TOKEN environment variable must be set")

def get_sales(date, page):
   
    response = requests.get(
        url='https://fake-api-vycpfa6oca-uc.a.run.app/sales',
        params={'date': date, 'page': page},
        headers={'Authorization': AUTH_TOKEN},
    )
    if response.status_code != 200:
        print(f"Error getting data: {response.status_code}")
        return None
    return response.json()