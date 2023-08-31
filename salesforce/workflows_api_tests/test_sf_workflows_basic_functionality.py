import requests
import pytest
import json
import string
import random
import os
from sf_workflows_utils import base_url,headers
from sf_workflows_utils import get_valid_post_schedule_payload,get_valid_update_workflow_payload,get_valid_post_pause_workflow_payload,get_valid_post_unpause_workflow_payload,get_expected_data_payload
workflow_id = 0

# API Test for create schedule workflow of HubSpot
def test_sf_create_workflow():
    global workflow_id
    url = base_url+"/workflows"
    print("print URL" + url)
    valid_post_payload =get_valid_post_schedule_payload()
    expected_data_payload=get_expected_data_payload()
    response = requests.post(url, json=valid_post_payload, headers=headers)
    json_data = response.json()
    json_str = json.dumps(json_data, indent=4)
    print("json POST response body: ", json_str)
    workflow_id = json_data["data"]["workflow_id"]
    print("workflow_id ===>", workflow_id)
    assert response.status_code == expected_data_payload["post_http_code"]
    # Asserting the presence of keys and their values
    assert json_data["http_code"] == expected_data_payload["post_http_code"]
    assert json_data["method"] ==expected_data_payload["post_method"] 
    assert json_data["data"]["name"]==valid_post_payload["name"]
    assert json_data["data"]["sor"] == valid_post_payload["sor"]
    assert json_data["data"]["sor_object_name"] == valid_post_payload["filter"]["data"]["and"][0]["and"][0]["object_name"]
    assert json_data["data"]["state"] == expected_data_payload["workflow_state"]
    assert json_data["data"]["evaluation"]["type"] ==valid_post_payload["evaluation"]["type"]
    assert json_data["data"]["actions"][0]["type"] ==valid_post_payload["actions"][0]["type"]
    return workflow_id


# API Test for update WorkFlow
def test_sf_update_workflow():
    global workflow_id
    url = base_url + f"/workflows/{workflow_id}"
    valid_put_payload =get_valid_update_workflow_payload()
    expected_data_payload=get_expected_data_payload()
    print("print URL" + url)
    response = requests.put(url, json=valid_put_payload, headers=headers)
    print("print URL" + url)
    # check for response status code
    assert response.status_code == expected_data_payload["put_http_code"]
    response_body = response.json()
    json_str = json.dumps(response_body, indent=4)
    print("json POST response body: ", json_str)
    #Asserting the presence of keys and their values
    assert response_body["http_code"] == expected_data_payload["put_http_code"]
    assert response_body["method"] ==expected_data_payload["put_method"] 
    assert response_body["data"]["name"]==valid_put_payload["name"]
    assert response_body["data"]["sor"] == valid_put_payload["sor"]
    assert response_body["data"]["sor_object_name"] == valid_put_payload["filter"]["data"]["and"][0]["and"][0]["object_name"]
    assert response_body["data"]["state"] == expected_data_payload["workflow_state"]
    assert response_body["data"]["evaluation"]["type"] ==valid_put_payload["evaluation"]["type"]
    assert response_body["data"]["actions"][0]["type"] ==valid_put_payload["actions"][0]["type"]


# API Test for pause WorkFlow
def test_pause_workflow():
    global workflow_id
    url = base_url + f"/workflows/{workflow_id}/pause"
    valid_post_pause_payload =get_valid_post_pause_workflow_payload()
    expected_data_payload=get_expected_data_payload()
    response = requests.post(url, json=valid_post_pause_payload, headers=headers)
    print("print URL" + url)
    # check for response status code
    assert response.status_code == expected_data_payload["success_http_code"]
    response_body = response.json()
    json_str = json.dumps(response_body, indent=4)
    print("json response body: ", json_str)
   # Asserting the presence of keys and their values
    assert response_body["http_code"] ==expected_data_payload["success_http_code"]
    assert response_body["method"] ==expected_data_payload["post_method"] 
    assert response_body["data"]["workflow_id"] ==workflow_id
    assert response_body["data"]["evaluation"]["type"] == expected_data_payload["data_evaluation_type"]
    assert response_body["data"]["actions"][0]["type"] ==expected_data_payload["data_actions_type"]
 


# API Test for unpause WorkFlow
def test_unpause_workflow():
    global workflow_id
    url = base_url + f"/workflows/{workflow_id}/unpause"
    valid_post_unpause_payload =get_valid_post_unpause_workflow_payload()
    expected_data_payload=get_expected_data_payload()
    response = requests.post(url, json=valid_post_unpause_payload, headers=headers)
    print("print URL" + url)
    # check for response status code
    assert response.status_code == expected_data_payload["success_http_code"]
    response_body = response.json()
    json_str = json.dumps(response_body, indent=4)
    print("json response body: ", json_str)
    # Asserting the presence of keys and their values
    assert response_body["http_code"] ==expected_data_payload["success_http_code"]
    assert response_body["method"] ==expected_data_payload["post_method"] 
    assert response_body["data"]["workflow_id"] ==workflow_id
    assert response_body["data"]["evaluation"]["type"] == expected_data_payload["data_evaluation_type"]
    assert response_body["data"]["actions"][0]["type"] ==expected_data_payload["data_actions_type"]
 

# API Test for single Workflow
def test_sf_get_specific_workflow():
    global workflow_id
    url = base_url+ f"/workflows/{workflow_id}"
    response = requests.get(url, headers=headers)
    expected_data_payload=get_expected_data_payload()
    print("Print URL "+url)
    response_json = response.json()
    json_str = json.dumps(response_json, indent=4)
    print("json GET response body: ", json_str)
    # check for response status code
    assert response.status_code == expected_data_payload["success_http_code"]
    # Assertions to validate specific values within the JSON structure
    assert response_json["http_code"] ==expected_data_payload["success_http_code"]
    assert response_json["method"] ==expected_data_payload["get_method"] 
    assert response_json["data"]["workflow_id"] ==workflow_id


# API Test for List Workflows
def test_sf_get_workflows():
    url = base_url+"/workflows"
    response = requests.get(url, headers=headers)
    expected_data_payload=get_expected_data_payload()
    print("Print URL "+url)
    response_body = response.json()
    json_str = json.dumps(response_body, indent=4)
    print("json GET response body: ", json_str)
    # check for response status code
    assert response.status_code == expected_data_payload["success_http_code"]
    # Key-level assertions
    assert "http_code" in response_body
    assert "metadata" in response_body
    assert "method" in response_body
    assert "request_id" in response_body
    assert "data" in response_body
    # Assertion for http_code
    assert response_body["http_code"] ==expected_data_payload["success_http_code"]
    # Assertion for method
    assert response_body["method"] ==expected_data_payload["get_method"] 
    # Assertion for workflow_id
    assert response_body["data"][0]["workflow_id"] ==workflow_id
    # Assertion for name
    assert response_body["data"][0]["name"] is not None



# API Test for delete Note
def test_delete_workflow():
    global workflow_id
    url = base_url + f"/workflows/{workflow_id}"
    response = requests.delete(url, headers=headers)
    expected_data_payload=get_expected_data_payload()
    print("print URL" + url)
    # print response body
    data = response.json()
    json_str = json.dumps(data, indent=4)
    print("json delete response body: ", json_str)
    assert response.status_code == expected_data_payload["success_http_code"]
    # Assertion for each key and value 
    assert data["http_code"] ==expected_data_payload["success_http_code"]
    assert data["method"] ==expected_data_payload["delete_method"] 
    assert data["error_data"] is None