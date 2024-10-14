import os
from flask import Flask, request, jsonify
from save_sales import save_sales  
from clean_raw_dir import clean_raw_dir   
from api import get_sales 

app = Flask(__name__)

@app.route('/', methods=['POST'])
def main():

    content = request.get_json()
    date = content.get("date")
    raw_dir = content.get("raw_dir")
    if not date or not raw_dir:
        return jsonify({"error": "Missing parameters"}), 400
    print(f"Starting job for date: {date}")

    clean_raw_dir(raw_dir)
    page = 1
    file_index = 0

    while True:
        print(f"Fetching page {page}...")
        sales_data = get_sales(date, page)
        if not sales_data or len(sales_data) == 0:
            break  

        file_name = f"sales_{date}_{file_index + 1}.json" if page > 1 else f"sales_{date}.json"
        file_path = os.path.join(raw_dir, file_name)

        save_sales(sales_data, file_path)
        print(f"Saved data to {file_path}")
        page += 1
        file_index += 1
    return jsonify({"message": "Job completed!"}), 201
if __name__ == '__main__':
    app.run(port=8081)