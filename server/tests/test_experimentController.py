
import jwt
from datetime import datetime, timedelta
from src import app_config
from src.services import UserService, ExperimentService
from src.models.UserModel import User
from src.models.ExperimentModel import Experiment
from werkzeug.security import generate_password_hash
import json

def test_save_experiment(client, auth):
    """
    GIVEN backend listens in route '/save-experiment'
    WHEN receives POST request with the experiment as payload
        AND the experiment does not exist in the database
        AND user is logged in
    THEN save the experiment in the database
    """
    ENDPOINT = '/save-experiment/'

    user_mock, login_headers = auth

    mock_experiment = {'category': "Louvain",
                       'creation_date': "2024/02/20, 21:59",
                       'dataset_id': "8bc32cde24e792e54c9a62b54a02808f",
                       'dataset_name': "book3",
                       'description': "",
                       'experiment_id': 4,
                       'experiment_name': "book3",
                       'metrics': {"modularity": 0.42},
                       'network_json': {"elements": {"edges": [], "nodes": []}},
                       'thumbnail': "",
                       'user_id': user_mock['id'],
                       'visualization_params': {"communitySeparation": 800,
                                                "gravity": 0.1,
                                                "nodeSeparation": 500}
                       }
    mock_experiment = json.dumps(mock_experiment)
    response = client.post(ENDPOINT, 
                           data= mock_experiment,
                           headers=login_headers,
                           content_type="application/json")
    
    experiment_in_db = ExperimentService.get_all_by_user_id(Experiment, user_id=user_mock['id'])
    
    response_json = response.get_json()
    
    assert experiment_in_db
    assert response.status_code == 200
    assert "experiment" in response_json
    assert "Louvain" == response_json['experiment']["category"]
    assert "nodes" in response_json['experiment']["network_json"]["elements"]
    assert "edges" in response_json['experiment']["network_json"]["elements"]
    assert "modularity" in response_json['experiment']["metrics"]