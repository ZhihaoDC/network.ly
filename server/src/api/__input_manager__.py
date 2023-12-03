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
        if (len(files) > 1) and ('columns' in files):
            columns = files['columns'].read().decode('utf8').replace("'",'"')
            columns_json= json.loads(columns)
        else:
            columns_json= None
        return columns_json

    def generate_hash(self, file):
        file.seek(0) #reset file pointer
        md5_hash = hashlib.md5(file.read()).hexdigest()
        return md5_hash
    
    