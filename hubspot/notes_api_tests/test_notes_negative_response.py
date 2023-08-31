import requests
from hs_notes_utils import base_url,headers
from hs_notes_utils import get_valid_post_luru_note_payload,get_invalid_post_luru_note_payload,get_invalid_update_note_payload


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




# Negative Test Case: POST creating new Luru note
def test_post_luru_note_with_negative_response():
    invalid_post_note_payload=get_invalid_post_luru_note_payload()
    response = requests.post(base_url+"/notes", headers=headers, json=invalid_post_note_payload)
    assert response.status_code == 400, "Expected status code: 400"

# Negative Test Case: PUT update notes
def test_put_note_with_negative_response():
    global note_id
    url = base_url + f"/notes/{note_id}"
    # url = base_url+"/workflows/87f05ba7-f2e0-42f5-8bc3-fc0934ebc3c0"
    try:
        invalid_note_put_payload=get_invalid_update_note_payload()
        response =requests.put(url, headers=headers, json=invalid_note_put_payload)
        response.raise_for_status() 
        print("Response:", response.status_code, response.json())
    except requests.exceptions.HTTPError as e:
        print("HTTP Error:", str(e))
    except requests.exceptions.RequestException as e:
        print("Request error:", str(e))


# Negative Test Case:POST Add Note Connection
def test_post_add_note_connections_with_negative_response():
    global note_id
    url = base_url + f"/notes/{note_id}/connections"
    # url = base_url + "/workflows/0a3f65a3-b3ee-4dfe-9f9f-2c7b3fed546f/pause"
    try:
        invalid_note_put_payload=get_invalid_update_note_payload()
        response = requests.post(url, headers=headers, json=invalid_note_put_payload)
        response.raise_for_status()  # Raise an exception if the response status is not 2xx
        return response.json()
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)
        return None



# Negative Test Case: delete specific Note
def test_delete_specific_note_with_negative_response():
    global note_id
    url = base_url+ f"/notes/{note_id}?propagate=true"
    api_params = {"propagate":"true"}
    # url = base_url + "/notes/0a3f65a3-b3ee-4dfe-9f9f-2c7b3fed546"
    try:
        response = requests.delete(url, headers=headers,params=api_params)
        response.raise_for_status()  # Raise an error if the status code is not 2xx
        print("Request successful!")
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)