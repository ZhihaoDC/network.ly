from io import BytesIO


def test_visualize_network(client):
    """
    GIVEN backend listens in route: "community-detection/network-visualization"
    WHEN a POST request with file is sent to the same route "community-detection/network-visualization"
    THEN backend must respond with a json that contains the graph
        AND contains graph's edges
        AND contains graph's nodes
    """
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

    rv = client.post('/graph-visualization',
                    data= data,
                    content_type='multipart/form-data')

    response = rv.json
    assert 'network_json' in response
    assert 'nodes' in response['network_json']['elements']
    assert 'edges' in response['network_json']['elements']
    assert all(['name' in node['data'] for node in response['network_json']['elements']['nodes']])
    assert all(['degree' in node['data'] for node in response['network_json']['elements']['nodes']])