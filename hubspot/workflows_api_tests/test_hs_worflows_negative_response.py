import requests
import os
import json
from hs_workflows_utils import base_url,headers
from hs_workflows_utils import get_valid_post_schedule_payload,get_invalid_post_schedule_payload,get_invalid_update_workflow_payload,get_invalid_post_unpause_workflow_payload,get_invalid_post_pause_workflow_payload


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

# Negative Test Case: POST Workflows
def test_post_schedule_workflow_with_negative_response():
    invalid_post_payload =get_invalid_post_schedule_payload()
    response = requests.post(base_url+"/workflows", headers=headers, json=invalid_post_payload)
    assert response.status_code == 400, "Expected status code: 400"


# Negative Test Case: PUT Workflows
def test_put_worklow_with_negative_response():
    global workflow_id
    url = base_url + f"/workflows/{workflow_id}"
    try:
        invalid_put_payload =get_invalid_update_workflow_payload()
        response =requests.put(url, headers=headers, json=invalid_put_payload)
        response.raise_for_status() 
        print("Response:", response.status_code, response.json())
    except requests.exceptions.HTTPError as e:
        print("HTTP Error:", str(e))
    except requests.exceptions.RequestException as e:
        print("Request error:", str(e))



# Negative Test Case:POST pause workflow
def test_post_pause_with_negative_response():
    global workflow_id
    url = base_url + f"/workflows/{workflow_id}/pause"
    try:
        invalid_post_pause_payload=get_invalid_post_pause_workflow_payload()
        response = requests.post(url, headers=headers, json=invalid_post_pause_payload)
        response.raise_for_status()  # Raise an exception if the response status is not 2xx
        return response.json()
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)
        return None



# Negative Test Case:POST unpause workflow
def test_post_unpause_with_negative_response():
    global workflow_id
    url = base_url + f"/workflows/{workflow_id}/unpause"
    try:
        invalid_post_unpause_payload=get_invalid_post_unpause_workflow_payload()      
        response = requests.post(url, headers=headers, json=invalid_post_unpause_payload)
        response.raise_for_status()  # Raise an exception if the response status is not 2xx
        return response.json()
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)
        return None
   
# Negative Test Case: GET list of workflows
def test_get_ls_worklow_with_negative_response():
   url = base_url + "/workflow"
   try:
      response = requests.get(url, headers=headers)
      response.raise_for_status()  # Raise an error if the status code is not 2xx
      print("Request successful!")
   except requests.exceptions.RequestException as e:
         print("An error occurred:", e)



# Negative Test Case: GET specific workflows
def test_get_worklow_with_negative_response():
   global workflow_id
   url = base_url + f"/workflows/{workflow_id}"
   try:
      response = requests.delete(url, headers=headers)
      response.raise_for_status()  # Raise an error if the status code is not 2xx
      print("Request successful!")
   except requests.exceptions.RequestException as e:
         print("An error occurred:", e)


# Negative Test Case: delete workflows
def test_delete_workflow_with_negative_response():
    global workflow_id
    url = base_url + f"/workflows/{workflow_id}"
    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()  # Raise an error if the status code is not 2xx
        print("Request successful!")
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)