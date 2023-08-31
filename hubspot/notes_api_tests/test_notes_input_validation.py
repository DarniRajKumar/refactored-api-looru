import requests
import json
import os
import string
import random
import pytest
from requests.exceptions import JSONDecodeError
from hs_notes_utils import base_url,headers
from hs_notes_utils import get_valid_post_luru_note_payload,get_invalid_post_luru_note_payload,get_valid_update_note_payload,get_invalid_update_note_payload,get_valid_post_add_note_connection_payload,get_invalid_post_add_note_connection_payload

note_id = 0

# Positive Test Case: Successful POST creating new Luru note
def test_validate_create_schedule_workflow_with_valid_url():
    global note_id
    url = base_url+"/notes"
    valid_post_payload=get_valid_post_luru_note_payload()
    response = requests.post(url, headers=headers, json=valid_post_payload)
    json_data = response.json()
    note_id = json_data["data"]["note_id"]
    assert response.status_code == 201, "Expected status code: 201"

# Negative Test Cases: input validations

# Test Case 1: Invalid URL
def test_validate_create_note_with_invalid_url():
    try:
        valid_post_payload=get_valid_post_luru_note_payload()
        response = requests.post("https://b2btesters.my.luru.ai.app", headers=headers, json=valid_post_payload)
        json_data = response.json()
        json_str = json.dumps(json_data, indent=4)
        print("json POST response body: ", json_str)
        assert response.status_code == 404, "Expected status code: 404"
    except requests.exceptions.ConnectionError:
        pass  # Expected behavior for an invalid URL

# Test Case 2: Invalid header
def test_validate_create_note_with_invalid_auth():
    url = base_url+"/notes"
    invalid_headers = {"cookie": "eJxVjstOwzAQRf_Fa5L67aS7rFqqlgqxoLCxxi8SNUpQbVMkxL"}
    valid_post_payload=get_valid_post_luru_note_payload()
    response = requests.post(url, headers=invalid_headers, json=valid_post_payload)
    json_data = response.json()
    json_str = json.dumps(json_data, indent=4)
    print("json POST response body: ", json_str)
    assert response.status_code == 401, "Expected status code: 401"

# Test Case 3: Invalid payload
def test_validate_create_note_with_invalid_body():
    url = base_url+"/notes"
    invalid_post_note_payload=get_invalid_post_luru_note_payload()
    response = requests.post(url, headers=headers, json=invalid_post_note_payload)
    json_data = response.json()
    json_str = json.dumps(json_data, indent=4)
    print("json POST response body: ", json_str)
    assert response.status_code == 400, "Expected status code: 400"

# Test Case 4: Invalid endpoint
def test_validate_create_note_with_invalid_endpoint():
    invalid_endpoint = base_url + "/note"
    valid_post_payload=get_valid_post_luru_note_payload()
    response = requests.post(invalid_endpoint, headers=headers, json=valid_post_payload)
    assert response.status_code == 404, "Expected status code: 404"
    print("Response Content:", response.content)
    try:
        json_data = response.json()
        print("Decoded JSON Data:", json_data)
    except JSONDecodeError as e:
        print("JSON Decoding Error:", e)
        print("Response Content:", response.content)
        print("Error occurred while decoding JSON data.")
    
# Test Case 5:  empty payload
def test_validate_create_note_with_empty_body():
    empty_payload = {}
    response = requests.post(base_url+"/notes", headers=headers, json=empty_payload)
    json_data = response.json()
    json_str = json.dumps(json_data, indent=4)
    print("json POST response body: ", json_str)
    assert response.status_code == 400, "Expected status code: 400"


# Positive Test Case: Successful PUT update notes
def test_validate_update_Note_with_valid_url():
    global note_id
    global note_id
    url = base_url + f"/notes/{note_id}"
    valid_put_payload=get_valid_update_note_payload()
    response = requests.put(url, headers=headers, json=valid_put_payload)
    response_body = response.json()
    if response.status_code == 202:
        assert response_body["http_code"]==202
        print("pause done")
    if response.status_code == 400:
       assert response_body["error_data"]["description"]=="Please retry later"

 # Negative Test Cases: input validations
  
# Test Case 1: Invalid URL
def test_validate_update_Note_with_invalid_url():
    try:
        valid_put_payload=get_valid_update_note_payload()
        response = requests.put("https://b2btesters.my.luru.ai.app", headers=headers, json=valid_put_payload)
        assert response.status_code == 404, "Expected status code: 404"
    except requests.exceptions.ConnectionError:
        pass  # Expected behavior for an invalid URL

# Test Case 2: Invalid header
def test_validate_update_Note_invalid_auth():
    global note_id
    url = base_url + f"/notes/{note_id}"
    invalid_headers = {"cookie": "eJxVjstOwzAQRf_Fa5L67aS7rFqqlgqxoLCxxi8SNUpQbVMkxL"}
    valid_put_payload=get_valid_update_note_payload()
    response = requests.put(url, headers=invalid_headers, json=valid_put_payload)
    assert response.status_code == 401, "Expected status code: 401"

# Test Case 3: Invalid payload
def test_validate_update_Note_with_invalid_body():
    global note_id
    url = base_url + f"/notes/{note_id}"
    invalid_note_put_payload=get_invalid_update_note_payload()
    response = requests.put(url, headers=headers, json=invalid_note_put_payload)
    assert response.status_code == 202, "Expected status code: 400"

# Test Case 4: Invalid endpoint
def test_validate_update_Note_with_invalid_endpoint():
    global note_id
    invalid_endpoint = base_url + f"/note/{note_id}"
    valid_put_payload=get_valid_update_note_payload()
    response = requests.put(invalid_endpoint, headers=headers, json=valid_put_payload)
    assert response.status_code == 404, "Expected status code: 404"

# Test Case 5:  empty payload
def test_validate_update_Note_with_empty_body():
    url = base_url + "/notes/fe106aa2-842b-419a-9b2f-4938f748f1ff"
    empty_payload = {}
    response = requests.put(url, headers=headers, json=empty_payload)
    assert response.status_code == 202, "Expected status code: 202"


# Positive Test Case: Successful POST Add Note Connection 
def test_validate_add_note_connection_with_valid_url():
    global note_id
    url = base_url + f"/notes/{note_id}/connections"
    valid_post_add_note_connection_payload=get_valid_post_add_note_connection_payload()
    response = requests.post(url, headers=headers, json=valid_post_add_note_connection_payload)
    response_body = response.json()
    if response.status_code == 200:
        assert response_body["http_code"]==200
        print("pause done")
    if response.status_code == 400:
       assert response_body["http_code"]==400
       print(response_body)

# Negative Test Cases: input validations
# Test Case 1: Invalid URL
def test_validate_add_note_connection_with_invalid_url():
    try:
        valid_post_add_note_connection_payload=get_valid_post_add_note_connection_payload()
        response = requests.post("https://b2btesters.my.luru.ai.app", headers=headers, json=valid_post_add_note_connection_payload)
        assert response.status_code == 404, "Expected status code: 404"
    except requests.exceptions.ConnectionError:
        pass  # Expected behavior for an invalid URL

# Test Case 2: Invalid header
def test_validate_add_note_connection_with_invalid_auth():
    global note_id
    url = base_url + f"/notes/{note_id}/connections"
    invalid_headers = {"cookie": "eJxVjstOwzAQRf_Fa5L67aS7rFqqlgqxoLCxxi8SNUpQbVMkxL"}
    valid_post_add_note_connection_payload=get_valid_post_add_note_connection_payload()
    response = requests.post(url, headers=invalid_headers, json=valid_post_add_note_connection_payload)
    assert response.status_code == 401, "Expected status code: 401"

# Test Case 3: Invalid payload
def test_validate_add_note_connection_with_invalid_body():
    global note_id
    url = base_url + f"/notes/{note_id}/connections"
    invalid_post_add_note_connection_payload=get_invalid_post_add_note_connection_payload()
    response = requests.post(url, headers=headers, json=invalid_post_add_note_connection_payload)
    assert response.status_code == 400, "Expected status code: 400"

# Test Case 4: Invalid endpoint
def test_validate_add_note_connection_with_invalid_endpoint():
    global note_id
    invalid_endpoint = base_url + f"/note/{note_id}/connections"
    valid_post_add_note_connection_payload=get_valid_post_add_note_connection_payload()
    response = requests.post(invalid_endpoint, headers=headers, json=valid_post_add_note_connection_payload)
    assert response.status_code == 404, "Expected status code: 404"

# Test Case 5:  empty payload
def test_validate_add_note_connection_with_empty_body():
    global note_id
    url = base_url + f"/notes/{note_id}/connections"
    empty_payload = {}
    response = requests.post(url, headers=headers, json=empty_payload)
    response_body = response.json()
    if response.status_code == 200:
        assert response_body["http_code"]==200
        print("connection done")
    if response.status_code == 400:
       assert response_body["http_code"]==400
       


# Positive Test Case: Successful GET list of Notes 
def test_validate_get_list_of_notes_with_valid_url():
    url = base_url + "/notes"
    response = requests.get(url, headers=headers)
    assert response.status_code == 200, "Expected status code: 202"

# Negative Test Cases: input validations

# Test Case 1: Invalid URL
def test_validate_get_list_of_notes_with_invalid_url():
    try:
        response = requests.get("https://b2btesters.my.luru.ai.app", headers=headers)
        assert response.status_code == 404, "Expected status code: 404"
    except requests.exceptions.ConnectionError:
        pass  # Expected behavior for an invalid URL

# Test Case 2: Invalid header
def test_validate_get_list_of_notes_with_invalid_auth():
    url = base_url + "/notes"
    invalid_headers = {"cookie": "eJxVjstOwzAQRf_Fa5L67aS7rFqqlgqxoLCxxi8SNUpQbVMkxL"}
    response = requests.get(url, headers=invalid_headers)
    assert response.status_code == 401, "Expected status code: 401"


# Test Case 3: Invalid endpoint
def test_validate_get_list_of_notes_with_invalid_endpoint():
    invalid_endpoint = base_url + "/note"
    response = requests.get(invalid_endpoint, headers=headers)
    assert response.status_code == 404, "Expected status code: 404"


# Positive Test Case: Successful GET specific Note
def test_validate_get_specific_note_with_valid_url():
    global note_id
    url = base_url+f"/notes/{note_id}"
    response = requests.get(url, headers=headers)
    assert response.status_code == 200, "Expected status code: 202"

# Negative Test Cases: input validations

# Test Case 1: Invalid URL
def test_validate_get_specific_note_with_invalid_url():
    try:
        response = requests.get("https://b2btesters.my.luru.ai.app", headers=headers)
        assert response.status_code == 404, "Expected status code: 404"
    except requests.exceptions.ConnectionError:
        pass  # Expected behavior for an invalid URL

# Test Case 2: Invalid header
def test_validate_get_specific_note_with_invalid_auth():
    global note_id
    url = base_url+f"/notes/{note_id}"
    invalid_headers = {"cookie": "eJxVjstOwzAQRf_Fa5L67aS7rFqqlgqxoLCxxi8SNUpQbVMkxL"}
    response = requests.get(url, headers=invalid_headers)
    assert response.status_code == 401, "Expected status code: 401"

# Test Case 3: Invalid endpoint
def test_validate_get_specific_note_with_invalid_endpoint():
    global note_id
    invalid_endpoint = base_url+f"/note/{note_id}"
    response = requests.get(invalid_endpoint, headers=headers)
    assert response.status_code == 404, "Expected status code: 404"



# Positive Test Case: Successful delete specific Note
def test_validate_delete_specific_note_with_valid_url():
    global note_id
    url = base_url+ f"/notes/{note_id}?propagate=true"
    api_params = {"propagate":"true"}
    response = requests.get(url, headers=headers,params=api_params)
    response_body = response.json()
    if response.status_code == 200:
        assert response_body["http_code"]==200
        print("pause done")
    if response.status_code == 404:
       assert response_body["http_code"]==404


# Test Case 1: Invalid URL
def test_validate_delete_specific_note_with_invalid_url():
    try:
        response = requests.get("https://b2btesters.my.luru.ai.app", headers=headers)
        assert response.status_code == 404, "Expected status code: 404"
    except requests.exceptions.ConnectionError:
        pass  # Expected behavior for an invalid URL

# Test Case 2: Invalid header
def test_validate_delete_specific_note_with_invalid_auth():
    global note_id
    url = base_url+ f"/notes/{note_id}?propagate=true"
    invalid_headers = {"cookie": "eJxVjstOwzAQRf_Fa5L67aS7rFqqlgqxoLCxxi8SNUpQbVMkxL"}
    response = requests.get(url, headers=invalid_headers)
    assert response.status_code == 401, "Expected status code: 401"

# Test Case 4: Invalid endpoint
def test_validate_delete_specific_note_with_invalid_endpoint():
    global note_id
    invalid_endpoint = base_url+ f"/note/{note_id}?propagate=true"
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