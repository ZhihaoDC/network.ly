import hashlib
from io import BytesIO
from os.path import dirname, join, realpath

from src.services import DatasetService
from src.models.DatasetModel import Dataset


def test_apply_louvain(client):
    """
    GIVEN backend listens in route: "community-detection/louvain"
    WHEN a POST request with file is sent to the same route "community-detection/louvain"
    THEN backend must respond with a json that contains the graph resulting from louvain algorithm
        AND contains graph's edges
        AND contains graph's nodes
        AND contains communities
        AND contains modularity
    """
    #create mock csv for POST request
    mock_csv = BytesIO(b"""\
                from,to,weight
                node_1,node_2,2
                node_1,node_4,1
                node_2,node_3,4
                node_4,node_5,5
                node_4,node_2,3
                    """)
    data = dict()
    data['file'] = (mock_csv, 'edge_list.csv')

    #Mock request
    rv = client.post("/community-detection/louvain",
                    data= data,
                    content_type='multipart/form-data')

    response = rv.json #convert response to json

    assert "network_json" in response
    assert "Louvain" == response["category"]
    assert "nodes" in response["network_json"]["elements"]
    assert "edges" in response["network_json"]["elements"]
    assert "communities" in response
    assert "modularity" in response["metrics"]



def test_apply_louvain_to_dataset(client, auth):
    """
        GIVEN user is authenticated
        WHEN api receives GET request on route '/community-detection/louvain/<dataset_id>'
            AND dataset exists
        THEN return louvain experiment
    """
    ENDPOINT = '/community-detection/louvain'
    user_mock, login_headers = auth

    dir_path = dirname(dirname(realpath(__file__))) #parent directory
    conf_path = join(dir_path, 'static', 'game-of-thrones-books', 'book3.csv')

    with open(conf_path, mode='rb') as file:
        response = client.post("/save-dataset",
                           headers=login_headers,
                           content_type="multipart/form-data",
                           data=({'file': file}))
    
    #check if dataset is present in db
    with open(conf_path, mode='rb') as file:
        file_hash = hashlib.md5(file.read()).hexdigest()
        dataset = DatasetService.get_by_id(Dataset, user_id=user_mock['id'], id=file_hash)

    response = client.get(f'{ENDPOINT}/{dataset["id"]}',
                          headers=login_headers)
    response_json = response.get_json()

    assert response.status_code == 200
    assert response_json['category'] == 'Louvain'
    assert 'network_json' in response_json.keys()
    assert 'communities' in response_json.keys()


def test_get_example(client):
    """
        GIVEN the user is a new user and is not logged in
        WHEN the api receives a GET request on endpoint '/community-detection/louvain/example'
        THEN the api responds with a new experiment
    """
    response = client.get("/community-detection/louvain/example")
    response_json = response.get_json()
    assert 'network_json' in response_json.keys()
    assert 'communities' in response_json.keys()