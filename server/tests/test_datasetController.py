import sys
from os.path import dirname, join, realpath
from src.api.__input_manager__ import InputManager
from src.services import DatasetService
from src.models.DatasetModel import Dataset
import hashlib

#Note: Dataset validation is done on client side

def test_save_dataset(client, auth):
    """
        GIVEN the user is authenticated
        WHEN the api receives a POST request on route /save-dataset/
            AND the request contains a file 
            AND the file is a valid dataset 
        THEN save the dataset into database
    """

    user_mock, login_headers = auth
    ENDPOINT = "/save-dataset"

    dir_path = dirname(dirname(realpath(__file__))) #parent directory
    conf_path = join(dir_path, 'static', 'game-of-thrones-books', 'book1.csv')

    with open(conf_path, mode='rb') as file:
        response = client.post(ENDPOINT,
                           headers=login_headers,
                           content_type="multipart/form-data",
                           data=({'file': file}))
    
    #check if dataset is present in db
    with open(conf_path, mode='rb') as file:
        file_hash = hashlib.md5(file.read()).hexdigest()
        dataset_in_db = DatasetService.get_by_id(Dataset, user_id=user_mock['id'], id=file_hash)

    assert response.status_code == 200
    assert dataset_in_db
    assert dataset_in_db['user_id'] == user_mock['id']


def test_get_datasets(client, auth):
    """
        GIVEN the user is authenticated
        WHEN the api receibes a GET request on route /get-datasets
        THEN api responds with all the datasets the user has
    """
    user_mock, login_headers = auth
    ENDPOINT = "/get-datasets"

    dir_path = dirname(dirname(realpath(__file__))) #parent directory
    conf_path = join(dir_path, 'static', 'game-of-thrones-books', 'book2.csv')

    #get present dataset ids
    datasets_in_db = DatasetService.get_all_by_user_id(Dataset, user_id=user_mock['id'])
    dataset_hashes = [dataset['id'] for dataset in datasets_in_db]

    #add new dataset (to have multiple datasets)
    with open(conf_path, mode='rb') as file:
        post_response = client.post('/save-dataset',
                           headers=login_headers,
                           content_type="multipart/form-data",
                           data=({'file': file}))
    with open(conf_path, mode='rb') as file:
        file_hash = hashlib.md5(file.read()).hexdigest()

    dataset_hashes.append(file_hash)
    
    #launch request
    response = client.get(ENDPOINT, 
                          headers=login_headers)
    
    dataset_ids_db = [dataset['id'] for dataset in response.get_json()['datasets']]
    dataset_owners = [dataset['user_id'] for dataset in response.get_json()['datasets']]

    assert all(dataset_hash in dataset_ids_db for dataset_hash in dataset_hashes)
    assert all(owner == user_mock['id'] for owner in dataset_owners)




def test_delete_dataset(client, auth):
    """
        GIVEN the user is authenticated
        WHEN the api receives a DELETE request on route /delete-dataset/
            AND the request contains the dataset_id
            AND the dataset is present in the databse
        THEN delete the dataset from database
    """
    user_mock, login_headers = auth
    ENDPOINT = "/delete-dataset"

    dir_path = dirname(dirname(realpath(__file__))) #parent directory
    conf_path = join(dir_path, 'static', 'game-of-thrones-books', 'book1.csv')


    with open(conf_path, mode='rb') as file:
        file_hash = hashlib.md5(file.read()).hexdigest()
        # dataset_to_delete = DatasetService.get_by_id(Dataset, user_id=user_mock['id'], id=file_hash)

    response = client.delete(f"{ENDPOINT}/{file_hash}",
                             headers=login_headers
                             )

    dataset_in_db = DatasetService.get_by_id(Dataset, user_id=user_mock['id'], id=file_hash)

    assert response.status_code == 200
    assert not dataset_in_db
    

