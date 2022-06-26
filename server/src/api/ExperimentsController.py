from flask import Blueprint, request
from flask.json import jsonify
from src.models.models import UserExperiment
from src.services import services

ExperimentsController = Blueprint('ExperimentsController', __name__)

@ExperimentsController.route('/experiment', methods=['POST'])
def save_experiment():
    request_json = request.get_json()
    # if all(keys in request_json for keys in ['user_id', 'dataset_hash']):
    if 'dataset_hash' in request_json:
        services.add_instance(UserExperiment, 
                            user_id=1,
                            experiment_id=request_json['dataset_hash']
                            )
        return jsonify({"successMessage": "File saved", 
                        'Access-Control-Allow-Origin': '*'}), 200
    else:
        return jsonify({"errorMessage": "Invalid .csv format"}), 400

















# @ExperimentsController.route('/save-experiment', methods=['POST'])
# def save_experiment():
#     # try:
#     json = request.get_json()
#     print(json.keys())
#     #pendiente: extraer info del user y comprobar que esta logeado
#     user_id  = 1 #usamos este temporalmente
#     experiment_id = json['dataset_hash']

#     cursor = db.connection.cursor()

#     cursor.execute("""INSERT INTO USER_EXPERIMENTS(user_id, experiment_id) VALUES (%s, %s)""", (user_id, experiment_id))

#     db.connection.commit()

#     return jsonify({"successMessage": "File saved", 
#                     'Access-Control-Allow-Origin': '*'}), 200
#     # except:
#     #     return jsonify({"errorMessage": "Invalid .csv format"}), 400