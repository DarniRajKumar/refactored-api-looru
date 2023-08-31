import requests
import pytest
import json
import string
import os
import random
from requests.exceptions import JSONDecodeError
from sf_workflows_utils import base_url,headers
from sf_workflows_utils import get_valid_post_schedule_payload,get_valid_update_workflow_payload,get_valid_post_unpause_workflow_payload,get_valid_post_pause_workflow_payload,get_invalid_post_schedule_payload,get_invalid_update_workflow_payload,get_invalid_post_unpause_workflow_payload,get_invalid_post_pause_workflow_payload

workflow_id = 0

# Positive Test Case: successful POST schedule workflows
def test_validate_create_schedule_workflow_with_valid_url():
    global workflow_id
    url = base_url+"/workflows"
    valid_post_payload =get_valid_post_schedule_payload()
    response = requests.post(url, headers=headers, json=valid_post_payload)
    json_data = response.json()
    workflow_id = json_data["data"]["workflow_id"]
    assert response.status_code == 201, "Expected status code: 201"


# Negative Test Cases: input validations

# Test Case 1: Invalid URL

def test_validate_create_schedule_workflow_with_invalid_url():
    try:
        
        valid_post_payload =get_valid_post_schedule_payload()
        response = requests.post("https://b2btesters.my.luru.ai.app", headers=headers, json=valid_post_payload)
        json_data = response.json()
        json_str = json.dumps(json_data, indent=4)
        print("json POST response body: ", json_str)
        assert response.status_code == 404, "Expected status code: 404"
    except requests.exceptions.ConnectionError:
        pass  # Expected behavior for an invalid URL

# Test Case 2: Invalid header

def test_validate_create_schedule_workflow_with_invalid_auth():
    url = base_url+"/workflows"
    invalid_headers = {"cookie": "eJxVjstOwzAQRf_Fa5L67aS7rFqqlgqxoLCxxi8SNUpQbVMkxL"}
    valid_post_payload =get_valid_post_schedule_payload()
    response = requests.post(url, headers=invalid_headers, json=valid_post_payload)
    json_data = response.json()
    json_str = json.dumps(json_data, indent=4)
    print("json POST response body: ", json_str)
    assert response.status_code == 401, "Expected status code: 401"

# Test Case 3: Invalid payload

def test_validate_create_schedule_workflow_with_invalid_body():
    url = base_url+"/workflows"
    invalid_post_payload =get_invalid_post_schedule_payload()
    response = requests.post(url, headers=headers, json=invalid_post_payload)
    json_data = response.json()
    json_str = json.dumps(json_data, indent=4)
    print("json POST response body: ", json_str)
    assert response.status_code == 400, "Expected status code: 400"
    
    
# Test Case 4: Invalid endpoint

def test_validate_create_schedule_workflow_with_invalid_endpoint():
    invalid_endpoint = base_url + "/workflow"
    valid_post_payload =get_valid_post_schedule_payload()
    response = requests.post(invalid_endpoint, headers=headers, json=valid_post_payload)
     # Assert the response status code
    assert response.status_code == 404, "Expected status code: 404"
    # Print the response content
    print("Response Content:", response.content)
    try:
        json_data = response.json()
        print("Decoded JSON Data:", json_data)
    except JSONDecodeError as e:
        print("JSON Decoding Error:", e)
        print("Response Content:", response.content)
        print("Error occurred while decoding JSON data.")
    
# Test Case 5:  empty payload
 
def test_validate_create_schedule_workflow_with_empty_body():
    empty_payload = {}
    response = requests.post(base_url+"/workflows", headers=headers, json=empty_payload)
    json_data = response.json()
    json_str = json.dumps(json_data, indent=4)
    print("json POST response body: ", json_str)
    assert response.status_code == 400, "Expected status code: 400"






# Positive Test Case: successful PUT workflows
def test_validate_update_workflow_with_valid_url():
    global workflow_id
    url = base_url + f"/workflows/{workflow_id}"
    valid_put_payload =get_valid_update_workflow_payload()
    response = requests.put(url, headers=headers, json=valid_put_payload)
    response_body = response.json()
    if response.status_code == 202:
        assert response_body["http_code"]==202
        print("pause done")
    if response.status_code == 400:
       assert response_body["error_data"]["description"]=="Please retry later"

# Negative Test Cases: input validations

# Test Case 1: Invalid URL   
def test_validate_update_workflow_with_invalid_url():
    try:
        valid_put_payload =get_valid_update_workflow_payload()
        response = requests.put("https://b2btesters.my.luru.ai.app", headers=headers, json=valid_put_payload)
        json_data = response.json()
        json_str = json.dumps(json_data, indent=4)
        print("json PUT response body: ", json_str)
        assert response.status_code == 404, "Expected status code: 404"
    except requests.exceptions.ConnectionError:
        pass  # Expected behavior for an invalid URL

# Test Case 2: Invalid header
def test_validate_update_workflow_with_invalid_auth():
    global workflow_id
    url = base_url + f"/workflows/{workflow_id}"
    invalid_headers = {"cookie": "eJxVjstOwzAQRf_Fa5L67aS7rFqqlgqxoLCxxi8SNUpQbVMkxL"}
    valid_put_payload =get_valid_update_workflow_payload()
    response = requests.put(url, headers=invalid_headers, json=valid_put_payload)
    json_data = response.json()
    json_str = json.dumps(json_data, indent=4)
    print("json PUT response body: ", json_str)
    assert response.status_code == 401, "Expected status code: 401"

# Test Case 3: Invalid payload
def test_validate_update_workflow_with_invalid_body():
    global workflow_id
    url = base_url + f"/workflows/{workflow_id}"
    invalid_put_payload =get_invalid_update_workflow_payload()
    response = requests.put(url, headers=headers, json=invalid_put_payload)
    json_data = response.json()
    json_str = json.dumps(json_data, indent=4)
    print("json PUT response body: ", json_str)
    assert response.status_code == 400, "Expected status code: 400"

# Test Case 4: Invalid endpoint
def test_validate_update_workflow_with_invalid_endpoint():
    global workflow_id
    invalid_endpoint = base_url + f"/workflow/{workflow_id}"
    valid_put_payload =get_valid_update_workflow_payload()
    response = requests.put(invalid_endpoint, headers=headers, json=valid_put_payload)
     # Assert the response status code
    assert response.status_code == 404, "Expected status code: 404"
    # Print the response content
    print("Response Content:", response.content)
    try:
        json_data = response.json()
        print("Decoded JSON Data:", json_data)
    except JSONDecodeError as e:
        print("JSON Decoding Error:", e)
        print("Response Content:", response.content)
        print("Error occurred while decoding JSON data.")

# Test Case 5:  empty payload
def test_validate_update_workflow_with_empty_body():
    global workflow_id
    url = base_url + f"/workflows/{workflow_id}"
    empty_payload = {}
    response = requests.put(url, headers=headers, json=empty_payload)
    json_data = response.json()
    json_str = json.dumps(json_data, indent=4)
    print("json PUT response body: ", json_str)
    assert response.status_code == 202, "Expected status code: 202"





# Positive Test Case: successful POST pause workflows
def test_validate_pause_workflow_with_valid_url():
    global workflow_id
    url = base_url + f"/workflows/{workflow_id}/pause"
    valid_post_pause_payload =get_valid_post_pause_workflow_payload()
    response = requests.post(url, headers=headers, json=valid_post_pause_payload)
    response_body = response.json()
    if response.status_code == 200:
        assert response_body["http_code"]==200
        print("pause done")
    if response.status_code == 400:
       assert response_body["error_data"]["message"]=="Workflow pause failed: Can pause only when it is currently active"

# Negative Test Cases: input validations

# Test Case 1: Invalid URL
def test_validate_pause_workflow_with_invalid_url():
    try:
        valid_post_pause_payload =get_valid_post_pause_workflow_payload()
        response = requests.post("https://b2btesters.my.luru.ai.app", headers=headers, json=valid_post_pause_payload)
        json_data = response.json()
        json_str = json.dumps(json_data, indent=4)
        print("json POST pause response body: ", json_str)
        assert response.status_code == 404, "Expected status code: 404"
    except requests.exceptions.ConnectionError:
        pass  # Expected behavior for an invalid URL

# Test Case 2: Invalid header
def test_validate_pause_workflow_with_invalid_auth():
    global workflow_id
    url = base_url + f"/workflows/{workflow_id}/pause"
    invalid_headers = {"cookie": "eJxVjstOwzAQRf_Fa5L67aS7rFqqlgqxoLCxxi8SNUpQbVMkxL"}
    valid_post_pause_payload =get_valid_post_pause_workflow_payload()
    response = requests.post(url, headers=invalid_headers, json=valid_post_pause_payload)
    json_data = response.json()
    json_str = json.dumps(json_data, indent=4)
    print("json POST pause response body: ", json_str)
    assert response.status_code == 401, "Expected status code: 401"

# Test Case 3: Invalid payload
def test_validate_pause_workflow_with_invalid_body():
    global workflow_id
    url = base_url + f"/workflows/{workflow_id}/pause"
    invalid_post_pause_payload =get_invalid_post_pause_workflow_payload()
    response = requests.post(url, headers=headers, json=invalid_post_pause_payload)
    json_data = response.json()
    json_str = json.dumps(json_data, indent=4)
    print("json POST pause response body: ", json_str)
    assert response.status_code == 400, "Expected status code: 400"


# Test Case 4: Invalid endpoint
def test_validate_pause_workflow_with_invalid_endpoint():
    global workflow_id
    invalid_endpoint = base_url + f"/workflow/{workflow_id}/pause"
    valid_post_pause_payload =get_valid_post_pause_workflow_payload()
    response = requests.post(invalid_endpoint, headers=headers, json=valid_post_pause_payload)
    # Assert the response status code
    assert response.status_code == 404, "Expected status code: 404"
    # Print the response content
    print("Response Content:", response.content)
    try:
        json_data = response.json()
        print("Decoded JSON Data:", json_data)
    except JSONDecodeError as e:
        print("JSON Decoding Error:", e)
        print("Response Content:", response.content)
        print("Error occurred while decoding JSON data.")

# Test Case 5:  empty payload
def test_validate_pause_workflow_with_empty_body():
    global workflow_id
    url = base_url + f"/workflows/{workflow_id}/pause"
    empty_payload = {}
    response = requests.post(url, headers=headers, json=empty_payload)
    response_body = response.json()
    if response.status_code == 200:
        assert response_body["http_code"]==200
        print("pause done")
    if response.status_code == 400:
       assert response_body["error_data"]["message"]=="Workflow pause failed: Can pause only when it is currently active"
       


# Positive Test Case: Successful  POST unpause workflows
def test_validate_unpause_workflow_with_valid_url():
    global workflow_id
    url = base_url + f"/workflows/{workflow_id}/unpause"
    valid_post_unpause_payload =get_valid_post_unpause_workflow_payload()
    response = requests.post(url, headers=headers, json=valid_post_unpause_payload)
    response_body = response.json()
    if response.status_code == 200:
        assert response_body["http_code"]==200
        print("pause done")
    if response.status_code == 400:
       assert response_body["error_data"]["message"]=="Workflow unpause failed: Can unpause only when it is currently paused"

# Negative Test Cases: input validations

# Test Case 1: Invalid URL
def test_validate_unpause_workflow_with_invalid_url():

    try:
        valid_post_unpause_payload =get_valid_post_unpause_workflow_payload()
        response = requests.post("https://b2btesters.my.luru.ai.app", headers=headers, json=valid_post_unpause_payload)
        json_data = response.json()
        json_str = json.dumps(json_data, indent=4)
        print("json POST unpause response body: ", json_str)
        assert response.status_code == 404, "Expected status code: 404"
    except requests.exceptions.ConnectionError:
        pass  # Expected behavior for an invalid URL

# Test Case 2: Invalid header
def test_validate_unpause_workflow_with_invalid_auth():
    global workflow_id
    url = base_url + f"/workflows/{workflow_id}/unpause"
    invalid_headers = {"cookie": "eJxVjstOwzAQRf_Fa5L67aS7rFqqlgqxoLCxxi8SNUpQbVMkxL"}
    valid_post_unpause_payload =get_valid_post_unpause_workflow_payload()
    response = requests.post(url, headers=invalid_headers, json=valid_post_unpause_payload)
    json_data = response.json()
    json_str = json.dumps(json_data, indent=4)
    print("json POST unpause response body: ", json_str)
    assert response.status_code == 401, "Expected status code: 401"

# Test Case 3: Invalid payload
def test_validate_unpause_workflow_with_invalid_body():
    global workflow_id
    url = base_url + f"/workflows/{workflow_id}/unpause"
    invalid_post_unpause_payload =get_invalid_post_unpause_workflow_payload()
    response = requests.post(url, headers=headers, json=invalid_post_unpause_payload)
    json_data = response.json()
    json_str = json.dumps(json_data, indent=4)
    print("json POST unpause response body: ", json_str)
    assert response.status_code == 400, "Expected status code: 400"

# Test Case 4: Invalid endpoint
def test_validate_unpause_workflow_with_invalid_endpoint():
    global workflow_id
    invalid_endpoint = base_url + f"/workflow/{workflow_id}/unpause"
    valid_post_unpause_payload =get_valid_post_unpause_workflow_payload()
    response = requests.post(invalid_endpoint, headers=headers, json=valid_post_unpause_payload)
    # Assert the response status code
    assert response.status_code == 404, "Expected status code: 404"
    # Print the response content
    print("Response Content:", response.content)
    try:
        json_data = response.json()
        print("Decoded JSON Data:", json_data)
    except JSONDecodeError as e:
        print("JSON Decoding Error:", e)
        print("Response Content:", response.content)
        print("Error occurred while decoding JSON data.")

# Test Case 5:  empty payload
def test_validate_unpause_workflow_with_empty_body():
    global workflow_id
    url = base_url + f"/workflows/{workflow_id}/unpause"
    empty_payload = {}
    response = requests.post(url, headers=headers, json=empty_payload)
    response_body = response.json()
    if response.status_code == 200:
        assert response_body["http_code"]==200
        print("pause done")
    if response.status_code == 400:
       assert response_body["error_data"]["message"]=="Workflow unpause failed: Can unpause only when it is currently paused"


# Positive Test Case: Successful GET list workflows
def test_validate_get_list_of_workflows_with_valid_url():
    url = base_url + "/workflows"
    response = requests.get(url, headers=headers)
    assert response.status_code == 200, "Expected status code: 202"

# Negative Test Cases: input validations

# Test Case 1: Invalid URL
def test_validate_get_list_of_workflows_with_invalid_url():
    try:
        response = requests.get("https://b2btesters.my.luru.ai.app", headers=headers)
        assert response.status_code == 404, "Expected status code: 404"
    except requests.exceptions.ConnectionError:
        pass  # Expected behavior for an invalid URL

# Test Case 2: Invalid header
def test_validate_get_list_of_workflows_with_invalid_auth():
    url = base_url + "/workflows"
    invalid_headers = {"cookie": "eJxVjstOwzAQRf_Fa5L67aS7rFqqlgqxoLCxxi8SNUpQbVMkxL"}
    response = requests.get(url, headers=invalid_headers)
    assert response.status_code == 401, "Expected status code: 401"

# Test Case 3: Invalid endpoint
def test_validate_get_list_of_workflows_with_invalid_endpoint():
    invalid_endpoint = base_url + "/workflow"
    response = requests.get(invalid_endpoint, headers=headers)
    assert response.status_code == 404, "Expected status code: 404"


# Positive Test Case: Successful GET specific Workflow
def test_validate_get_specific_workflow_with_valid_url():
    global workflow_id
    url = base_url + f"/workflows/{workflow_id}"
    response = requests.get(url, headers=headers)
    assert response.status_code == 200, "Expected status code: 202"

# Negative Test Cases: input validations

# Test Case 1: Invalid URL
def test_validate_get_specific_workflow_with_invalid_url():
    try:
        response = requests.get("https://b2btesters.my.luru.ai.app", headers=headers)
        assert response.status_code == 404, "Expected status code: 404"
    except requests.exceptions.ConnectionError:
        pass  # Expected behavior for an invalid URL

# Test Case 2: Invalid header
def test_validate_get_specific_workflow_with_invalid_auth():
    global workflow_id
    url = base_url + f"/workflows/{workflow_id}"
    invalid_headers = {"cookie": "eJxVjstOwzAQRf_Fa5L67aS7rFqqlgqxoLCxxi8SNUpQbVMkxL"}
    response = requests.get(url, headers=invalid_headers)
    assert response.status_code == 401, "Expected status code: 401"

# Test Case 3: Invalid endpoint
def test_validate_get_specific_workflow_with_invalid_endpoint():
    global workflow_id
    invalid_endpoint = base_url + f"/workflow/{workflow_id}"
    response = requests.get(invalid_endpoint, headers=headers)
    assert response.status_code == 404, "Expected status code: 404"


# Positive Test Case: Successful delete specific workflow
def test_validate_delete_specific_workflow_with_valid_url():
    global workflow_id
    url = base_url + f"/workflows/{workflow_id}"
    response = requests.get(url, headers=headers)
    response_body = response.json()
    if response.status_code == 200:
        assert response_body["http_code"]==200
        print("pause done")
    if response.status_code == 404:
       assert response_body["error_data"]["message"]=="Given workflow not found"


# Test Case 1: Invalid URL
def test_validate_delete_specific_workflow_with_invalid_url():
    try:
        response = requests.get("https://b2btesters.my.luru.ai.app", headers=headers)
        assert response.status_code == 404, "Expected status code: 404"
    except requests.exceptions.ConnectionError:
        pass  # Expected behavior for an invalid URL

# Test Case 2: Invalid header
def test_validate_delete_specific_workflow_with_invalid_auth():
    global workflow_id
    url = base_url + f"/workflows/{workflow_id}"
    invalid_headers = {"cookie": "eJxVjstOwzAQRf_Fa5L67aS7rFqqlgqxoLCxxi8SNUpQbVMkxL"}
    response = requests.get(url, headers=invalid_headers)
    assert response.status_code == 401, "Expected status code: 401"

# Test Case 4: Invalid endpoint
def test_validate_delete_specific_workflow_with_invalid_endpoint():
    global workflow_id
    invalid_endpoint = base_url + f"/workflow/{workflow_id}"
    response = requests.get(invalid_endpoint, headers=headers)
     # Assert the response status code
    assert response.status_code == 404, "Expected status code: 404"
    # Print the response content
    print("Response Content:", response.content)
    try:
        json_data = response.json()
        print("Decoded JSON Data:", json_data)
    except JSONDecodeError as e:
        print("JSON Decoding Error:", e)
        print("Response Content:", response.content)
        print("Error occurred while decoding JSON data.")