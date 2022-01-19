from flask import jsonify, request, Blueprint
import src.blueprints.preprocess as preprocess 

networkVisualizationController = Blueprint('networkVisualizationController', __name__)

@networkVisualizationController.route('/community-detection/network-visualization', methods=['POST'])
def visualize_network():
    file = request.files['file']

    graph = preprocess.preprocess_network(file)

    graph_json = preprocess.preprocess_json(graph)

    return jsonify({'graph': graph_json})
    