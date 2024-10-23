import os
import json
import shutil
from flask import Flask, request, jsonify
import fastavro
from fastavro.schema import load_schema
app = Flask(__name__)

def clean_dir(directory):
    
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)z

def convert_json_to_avro(json_file, avro_file, schema):
    
    with open(json_file, 'r') as f:
        records = json.load(f)
    with open(avro_file, 'wb') as out:
        fastavro.writer(out, schema, records)
@app.route('/', methods=['POST'])

def process_json_to_avro():
   
    content = request.get_json()
    raw_dir = content.get("raw_dir")
    stg_dir = content.get("stg_dir")
    if not raw_dir or not stg_dir:
        return jsonify({"error": "Missing parameters"}), 400
    print(f"Starting job: Converting JSON from {raw_dir} to Avro in {stg_dir}")
   
    clean_dir(stg_dir)

    schema = {
        "type": "record",
        "name": "SalesRecord",
        "fields": [
            {"name": "field1", "type": "string"},  
            {"name": "field2", "type": "int"}

        ]
    }

    for file_name in os.listdir(raw_dir):
        if file_name.endswith('.json'):
            json_file_path = os.path.join(raw_dir, file_name)
            avro_file_name = file_name.replace('.json', '.avro')
            avro_file_path = os.path.join(stg_dir, avro_file_name)
          
            print(f"Converting {json_file_path} to {avro_file_path}")
            convert_json_to_avro(json_file_path, avro_file_path, schema)
    return jsonify({"message": "Job completed!"}), 201

if __name__ == '__main__':
    app.run(port=8082)