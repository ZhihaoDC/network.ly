from flask import request, Blueprint
from flask.json import jsonify
import hashlib
import json
from networkx import cytoscape_graph
from werkzeug.utils import secure_filename


#Import custom modules
from src.community_detection import girvan_newman_algorithm as gn
from src.models.DatasetModel import Dataset
from src.services import DatasetService
import src.api.__network_formatter__ as nw_formatter
from src.api.__input_manager__ import InputManager
from src.api.__token_handler__ import token_required


GirvanNewmanController = Blueprint('GirvanNewmanController', __name__)


#Main method
@GirvanNewmanController.route("/community-detection/girvan-newman", methods=['POST'])
def apply_girvan_newman():
    try:
        input = InputManager(request.files)
        file, file_name, file_hash, columns = input.file, input.file_name, input.file_hash, input.csv_columns        

        #Preprocess network from file
        graph = nw_formatter.file_to_network(file, columns)

        #Apply girvan-newman method
        dendrogram, modularity = gn.Girvan_Newman_2004(graph)
        GN_communities = gn.dendrogram_to_community(dendrogram)

        graph_json = nw_formatter.network_to_json(graph, GN_communities)

        default_visualization_params = {'nodeSeparation': 500, 'communitySeparation': 800, 'gravity': 0.1}

        return jsonify(
                        {'experiment_name': file_name, #default value
                        'network_json': graph_json,
                        'communities': GN_communities,
                        'metrics' : {'modularity': modularity},
                        'visualization_params': default_visualization_params,
                        'category' : 'Girvan-Newman',
                        'dataset_name': file_name,
                        'dataset_id': file_hash
                        }), 200
    except:
        return jsonify({"errorMessage": "Invalid .csv format"}), 400



@GirvanNewmanController.route("/community-detection/girvan-newman/<dataset_id>", methods=['GET'])
@token_required
def apply_girvan_newman_to_dataset(user, dataset_id):
    try:
        dataset = DatasetService.get_by_id(Dataset, user['id'], dataset_id)
        graph = nw_formatter.json_to_network(dataset['json'])

        #Apply girvan-newman method
        dendrogram, modularity = gn.Girvan_Newman_2004(graph)
        GN_communities = gn.dendrogram_to_community(dendrogram)
        graph_json = nw_formatter.network_to_json(graph, GN_communities)
        
        default_visualization_params = {'nodeSeparation': 500, 'communitySeparation': 800, 'gravity': 0.1}

        return jsonify(
                        {'experiment_name': dataset['name'], #default value
                        'network_json': graph_json,
                        'communities': GN_communities,
                        'metrics' : {'modularity': modularity},
                        'visualization_params': default_visualization_params,
                        'category' : 'Girvan-Newman',
                        'dataset_name': dataset['name'],
                        'dataset_id': dataset['id']
                        }), 200
    except Exception as e:
        import sys
        print(e, file=sys.stderr)
        return jsonify({"errorMessage": "Invalid .csv format"}), 400
        

