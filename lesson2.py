import os
import requests
import json
import shutil
from flask import Flask, request, jsonify
app = Flask(__name__)

AUTH_TOKEN = os.getenv('AUTH_TOKEN')

if not AUTH_TOKEN:
    print("AUTH_TOKEN environment variable must be set")

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

def save_sales(data, file_path):

    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def clean_raw_dir(raw_dir):

    if os.path.exists(raw_dir):
        shutil.rmtree(raw_dir)
    os.makedirs(raw_dir)
@app.route('/', methods=['POST'])

def main():

    content = request.get_json()
    date = content.get("date")
    raw_dir = content.get("raw_dir")

    if not date or not raw_dir:
        return jsonify({"error": "Missing parameters"}), 400
    print(f"Start job for: {date}")

    clean_raw_dir(raw_dir)
    page = 1
    file_index = 0
    while True:
        print(f"Getting page {page}...")
        sales_data = get_sales(date, page)
        if not sales_data or len(sales_data) == 0:
            break 
        
        file_name = f"sales_{date}_{file_index + 1}.json" if page > 1 else f"sales_{date}.json"
        file_path = os.path.join(raw_dir, file_name)
        save_sales(sales_data, file_path)
        print(f"Saved to {file_path}")
        page += 1
        file_index += 1
    return jsonify({"message": "Job completed!"}), 201

if __name__ == '__main__':
    app.run(port=8081)

