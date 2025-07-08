from flask import request, Blueprint
from flask.json import jsonify
import sys
from os.path import dirname, join, realpath
#import custom modules
from src.community_detection import louvain_algorithm as louvain
import src.api.__network_formatter__ as nw_formatter
from src.api.__input_manager__ import InputManager
from src.models.DatasetModel import Dataset
from src.services import DatasetService
from src.api.__token_handler__ import token_required
from networkx.algorithms.community.quality import modularity as nx_modularity
from networkx import from_pandas_edgelist
from pandas import read_csv


LouvainController = Blueprint('LouvainController', __name__)


#Main method
@LouvainController.route('/community-detection/louvain', methods=['POST'])
def apply_louvain():
    try: 
        input = InputManager(request.files)
        file, file_name, file_hash, columns = input.file, input.file_name, input.file_hash, input.csv_columns       

        graph = nw_formatter.file_to_network(file, columns)

        #Apply louvain method
        supergraph, communities = louvain.Louvain(graph)
        last_community = louvain.last_community(graph, communities)
        modularity = nx_modularity(graph, louvain.dendrogram(last_community))

        graph_json = nw_formatter.network_to_json(graph, last_community)

        default_visualization_params = {'nodeSeparation': 500, 'communitySeparation': 800, 'gravity': 0.1}
        
        return jsonify({ 
                        'experiment_name': file_name, #default value
                        'network_json': graph_json,
                        'communities': last_community,
                        'metrics' : {'modularity': modularity},
                        'visualization_params': default_visualization_params,
                        'category': 'Louvain',
                        'dataset_name': file_name,
                        'dataset_id': file_hash
                    }), 200
    
    except Exception as e:
        print(f"{type(e).__name__}: {e}", file=sys.stderr)
        return jsonify({"errorMessage": "Invalid .csv format"}), 500


@LouvainController.route("/community-detection/louvain/<dataset_id>", methods=['GET'])
@token_required
def apply_louvain_to_dataset(user, dataset_id):
    try:
        dataset = DatasetService.get_by_id(Dataset, user['id'], dataset_id)
        graph = nw_formatter.json_to_network(dataset['json']) 

        #Apply louvain method
        supergraph, communities = louvain.Louvain(graph)
        last_community = louvain.last_community(graph, communities)
        modularity = nx_modularity(graph, louvain.dendrogram(last_community))
        graph_json = nw_formatter.network_to_json(graph, last_community)

        default_visualization_params = {'nodeSeparation': 500, 'communitySeparation': 800, 'gravity': 0.1}

        return jsonify({
                        'experiment_name': dataset['name'], #default value
                        'network_json': graph_json,
                        'communities': last_community,
                        'metrics' : {'modularity': modularity},
                        'visualization_params': default_visualization_params,
                        'category': 'Louvain',
                        'dataset_name': dataset['name'],
                        'dataset_id': dataset['id']
                    }), 200
    except Exception as e:
        print(e, file=sys.stderr)
        return jsonify({"errorMessage": "Error interno del servidor"}), 500
    


@LouvainController.route('/community-detection/louvain/example', methods=['GET'])
def get_example():
        example_dataset = 'book1'
        dir_path = dirname(dirname(dirname(realpath(__file__)))) #server directory
        edge_list = read_csv(join(dir_path, "static", 'game-of-thrones-books', f"{example_dataset}.csv"))  

        graph = from_pandas_edgelist(edge_list, 
                                    source='Source', 
                                    target='Target',
                                    edge_attr='weight')
        
        #Apply louvain method
        supergraph, communities = louvain.Louvain(graph)
        last_community = louvain.last_community(graph, communities)
        modularity = nx_modularity(graph, louvain.dendrogram(last_community))

        graph_json = nw_formatter.network_to_json(graph, last_community)

        default_visualization_params = {'nodeSeparation': 500, 'communitySeparation': 800, 'gravity': 0.1}
        
        return jsonify({ 
                        'experiment_name': 'Ejemplo de experimento', #default value
                        'network_json': graph_json,
                        'communities': last_community,
                        'metrics' : {'modularity': modularity},
                        'visualization_params': default_visualization_params,
                        'category': 'Louvain',
                        'dataset_name': 'book1',
                        'dataset_id': None
                    }), 200