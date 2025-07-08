from dataclasses import dataclass
import json
from pandas import read_csv
from csv import writer, QUOTE_NONNUMERIC
import networkx
import src.api.__network_formatter__ as preprocess


def test_preprocess_network(csv_file):
    """
    GIVEN a .csv file from the body of a http POST request
    WHEN function file_to_network is called
    THEN function file_to_network returns formatted networkx.Graph Object
    """

    result = preprocess.file_to_network(csv_file)

    assert isinstance(result, networkx.Graph)
    assert not networkx.classes.function.is_empty(result)

    #assert that node labels are strings 
    assert all([isinstance(i, str) for i in result.nodes()])

    #assert that weight is an edge attribute
    assert all(['weight' in data for u, v, data in result.edges(data=True)])



def test_preprocess_json(csv_file):
    """
    GIVEN that we have executed one of the community detection algorithms on a networkx.Graph Object
    WHEN we obtain the networkx.Graph Object and a dict() of communities
    THEN we format the Graph to have the desired attribute names
    AND we return a json of the Graph
    """
    graph = preprocess.file_to_network(csv_file)

    communities = {'node_1':1, 'node_2':1, 'node_3':2, 'node_4':1, 'node_5':3} #mock communities

    result = preprocess.network_to_json(graph, communities)

    assert isinstance(result, dict)
    assert all(['name' in node['data'] for node in result['elements']['nodes']])
    assert all(['background_color' in node['data'] for node in result['elements']['nodes']])
    assert all(['community' in node['data'] for node in result['elements']['nodes']])
    assert all(['degree' in node['data'] for node in result['elements']['nodes']])


def test_preprocess_json_visualization(csv_file):
    """
    GIVEN that we have transformed our .csv file to a networkx.Graph Object for plain visualization
    WHEN we obtain the networkx.Graph Object and no communities
    THEN we format the Graph to have the desired attribute names
    AND we return a json of the Graph
    """
    graph = preprocess.file_to_network(csv_file)

    result = preprocess.network_to_json(graph)

    assert isinstance(result, dict)
    assert all(['name' in node['data'] for node in result['elements']['nodes']])
    assert all(['degree' in node['data'] for node in result['elements']['nodes']])