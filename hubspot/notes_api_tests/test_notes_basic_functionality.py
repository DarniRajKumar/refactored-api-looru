import requests
import pytest
import json
import string
from hs_notes_utils import base_url,headers
from hs_notes_utils import get_expected_data_payload,get_valid_post_luru_note_payload,get_valid_update_note_payload,get_valid_post_add_note_connection_payload

note_id = 0

#API Test for creating new Looru Note
def test_create_note():
    global note_id
    url = base_url+"/notes"
    valid_post_payload=get_valid_post_luru_note_payload()
    expected_data_payload=get_expected_data_payload()
    response=requests.post(url,json=valid_post_payload,headers=headers)
    print("print URL" + url)
    # check for response status code
    assert response.status_code==expected_data_payload["post_http_code"]
    json_data = response.json()
    json_str = json.dumps(json_data, indent=4)
    print("json POST response body: ", json_str)
    note_id = json_data["data"]["note_id"]
    print("note_id ===>", note_id)
    # Assertions for each key and value
    assert json_data["http_code"] == expected_data_payload["post_http_code"]
    assert json_data["metadata"] == None
    assert json_data["method"] == expected_data_payload["post_method"]
    assert json_data["request_id"] is not None
    assert json_data["data"]["note_id"]==note_id
    assert json_data["data"]["sync_state"] == "private"
    assert json_data["data"]["title"] == valid_post_payload["title"]
    assert json_data["data"]["template_id"] == None
    assert json_data["data"]["created_by"]["id"] == expected_data_payload["owner_id"]
    assert json_data["data"]["created_by"]["sor_id"] == None
    assert json_data["data"]["created_by"]["email"] == expected_data_payload["owner_email"]
    assert json_data["data"]["created_by"]["name"] == expected_data_payload["owner_name"]
    assert json_data["data"]["updated_by"]["id"] == expected_data_payload["owner_id"]
    assert json_data["data"]["updated_by"]["sor_id"] == None
    assert json_data["data"]["updated_by"]["email"] == expected_data_payload["owner_email"]
    assert json_data["data"]["updated_by"]["name"] == expected_data_payload["owner_name"]
    assert json_data["data"]["connections"] == []
    assert json_data["error_data"] == None   
    return note_id


#API Test for update Note
def test_update_Note():
    global note_id
    url = base_url + f"/notes/{note_id}"
    valid_put_payload=get_valid_update_note_payload()
    expected_data_payload=get_expected_data_payload()
    response = requests.put(url, json=valid_put_payload, headers=headers)
    print("print URL" + url) 
    # check for response status code
    assert response.status_code == expected_data_payload["put_http_code"] 
    data = response.json()
    json_str = json.dumps(data, indent=4)
    print("json PUT response body: ", json_str)
    note_id = data["data"]["note_id"]
    print("note_id ===>", note_id)
    # Assertions for each key and value
    assert data["http_code"] == expected_data_payload["put_http_code"]
    assert data["metadata"] == None
    assert data["method"] == expected_data_payload["put_method"]
    assert data["request_id"] is not None
    assert data["data"]["note_id"]==note_id
    assert data["data"]["sync_state"] == "private"
    assert data["data"]["title"] == valid_put_payload["title"]
    assert data["data"]["template_id"] == None
    assert data["data"]["created_by"]["id"] == expected_data_payload["owner_id"]
    assert data["data"]["created_by"]["sor_id"] == None
    assert data["data"]["created_by"]["email"] == expected_data_payload["owner_email"]
    assert data["data"]["created_by"]["name"] == expected_data_payload["owner_name"]
    assert data["data"]["updated_by"]["id"] == expected_data_payload["owner_id"]
    assert data["data"]["updated_by"]["sor_id"] == None
    assert data["data"]["updated_by"]["email"] == expected_data_payload["owner_email"]
    assert data["data"]["updated_by"]["name"] == expected_data_payload["owner_name"]
    assert data["data"]["connections"] == []
    assert data["error_data"] == None  
    return note_id



#API Test for Add Note Connection
def test_add_note_connection():
    global note_id
    url = base_url + f"/notes/{note_id}/connections"
    valid_post_add_note_connection_payload=get_valid_post_add_note_connection_payload()
    expected_data_payload=get_expected_data_payload()
    response = requests.post(url, json=valid_post_add_note_connection_payload,headers=headers)
    print("print URL:" + url) 
    assert response.status_code == expected_data_payload["success_http_code"]
    json_data = response.json()
    json_str = json.dumps(json_data, indent=4)
    print("json POST response body: ", json_str)   
    # Assertions for keys
    assert "http_code" in json_data
    assert "metadata" in json_data
    assert "method" in json_data
    assert "request_id" in json_data
    assert "data" in json_data
    assert "error_data" in json_data
    # Assertions for values
    assert json_data["http_code"] == expected_data_payload["success_http_code"]
    assert json_data["metadata"] is None
    assert json_data["method"] == expected_data_payload["post_method"]
    assert json_data["request_id"] is not None
    # assertions for values within the "data" dictionary and its nested dictionaries/lists
    data = json_data["data"]
    assert "note_id" in data
    assert "sync_state" in data
    # Assertions for the nested "created_by" and "updated_by" dictionaries
    created_by = data["created_by"]
    assert "id" in created_by
    assert "sor_id" in created_by
    assert "email" in created_by
    assert "name" in created_by
    updated_by = data["updated_by"]
    assert "id" in updated_by
    assert "sor_id" in updated_by
    assert "email" in updated_by
    assert "name" in updated_by
   # Assertions for the nested "connections" list
    connections = data["connections"]
    assert isinstance(connections, list)
    assert len(connections) > 0  
    # Assertions for the "error_data" key
    assert json_data["error_data"] is None



# API Test for single note
def test_get_specific_note():
    global note_id
    url = base_url+f"/notes/{note_id}"
    api_params = {"type":"luru"}
    response = requests.get(url,params=api_params,headers=headers)  
    print("Print URL "+url)
    # check for response status code
    assert response.status_code == 200  
    # check if no errors from the response data
    if(response.json()['error_data'] == None):
        assert response.json() is not None 
        # Check for notes in the reponse
        if (response.json()['data'] is not None):
            #get the note_id for checking the correct values in the response
            api_note_id = response.json()['data']['note_id']
            assert api_note_id == note_id    
            #assert response.json()['data'][0]['note_id'] is not None



#API Test for getting all notes
def test_get_notes():
    global note_id
    url = base_url+"/notes?type=luru"
    api_params = {"type":"luru"}
    response = requests.get(url,params=api_params,headers=headers)  
    print("Print URL "+url)
    # check for response status code
    assert response.status_code == 200 
    # check if no errors from the response data
    if(response.json()['error_data'] == None):
        assert response.json() is not None
        # Check for notes in the reponse
        if (len(response.json()['data']) > 0):
            #get the note_id for checking the correct values in the response
            note_id = response.json()['data'][0]['note_id']           
            assert response.json()['data'][0]['note_id'] is not None



#API Test for delete Note
def test_delete_note():
    global note_id
    url = base_url+ f"/notes/{note_id}?propagate=true"
    api_params = {"propagate":"true"}
    expected_data_payload=get_expected_data_payload()
    response = requests.delete(url,params=api_params,headers=headers)
    print("print URL" + url)
    # print response body
    data = response.json()
    json_str = json.dumps(data, indent=4)
    print("json delete response body: ", json_str)
    assert response.status_code == expected_data_payload["success_http_code"]
    # Assertion for each key and value 
    assert data["http_code"] == expected_data_payload["success_http_code"]
    assert data["metadata"] is None
    assert data["method"] == expected_data_payload["delete_method"] 
    assert data["request_id"] is not None
    assert data["error_data"] is None