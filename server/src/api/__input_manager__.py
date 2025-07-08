from flask import json
from werkzeug.utils import secure_filename
import hashlib


class InputManager():
    """Manages user input from request and verifies file format (must be .csv)"""

    def __init__(self, request_files) -> None:
        self._file = request_files['file']
        self._dataset_name = self.verify_csv_name(self._file)
        self._dataset_hash = self.generate_hash(self._file)
        self._csv_columns = self.columns_as_json(request_files)

    @property
    def file(self):
        self._file.seek(0)
        return self._file
    
    @property
    def file_name(self):
        return self._dataset_name
    
    @property
    def file_hash(self):
        return self._dataset_hash
    
    @property
    def csv_columns(self):
        return self._csv_columns
    
    def verify_csv_name(self, file):
        file_name = file.filename
        file_name_no_ext = file_name.replace(".csv", "") 
        secured_filename = secure_filename(file_name_no_ext)
        return secured_filename

    def columns_as_json(self, files):
        import csv, sys
        if (len(files) > 1) and ('columns' in files):
            try:
                # Convert the CSV data into a JSON object
                json_data = csv.DictReader(files['columns'])
                # Now json_data contains the parsed JSON object
                return json.dumps([row for row in json_data])
            
            except Exception as e:
                # Handle error in CSV parsing or JSON conversion
                print( f'Error processing file: {e}', file=sys.stderr)

    def generate_hash(self, file):
        file.seek(0) #reset file pointer
        md5_hash = hashlib.md5(file.read()).hexdigest()
        return md5_hash
    
    