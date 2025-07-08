from flask import Blueprint, request
from flask import json, jsonify
import sys 

import src.api.__network_formatter__ as nw_formatter
from src.api.__input_manager__ import InputManager
from src.api.__token_handler__ import token_required

from src.models.DatasetModel import Dataset
from src.services import DatasetService


DatasetController = Blueprint('DatasetController', __name__)


@DatasetController.route('/get-datasets', methods=['GET'])
@token_required
def get_datasets(user):
    data = DatasetService.get_all_by_user_id(
        Dataset,
        user_id=user['id']
    )
    return json.jsonify({'status': 'success',
                        'datasets': data}), 200


@DatasetController.route('/save-dataset', methods=['POST'])
@token_required
def save_dataset(user):
    try:
        input = InputManager(request.files)
        file, file_name, file_hash, columns = input.file, input.file_name, input.file_hash, input.csv_columns       

        graph = nw_formatter.file_to_network(file, columns)
        network_json = nw_formatter.network_to_json(graph)


        added_dataset = DatasetService.add_instance(Dataset,
            id=file_hash,
            name=file_name[:50],
            json=network_json,
            user_id=user['id']
        )
        
        return jsonify(added_dataset), 200
    
    except Exception as e:
        print(e, file=sys.stderr)
        return jsonify({"errorMessage": "Invalid .csv format"}), 400
    

@DatasetController.route('/delete-dataset/<dataset_id>', methods=['DELETE'])
@token_required
def delete_dataset(user, dataset_id):
    try:
        deleted_dataset = DatasetService.delete_by_id(Dataset, user_id=user['id'], id=dataset_id)
        return json.jsonify({'status': 'success', 'deleted_dataset': deleted_dataset}), 200
    
    except Exception as e:
        import sys
        print(e, file=sys.stderr)
        return jsonify({"errorMessage": "Error deleting dataset"}), 400
