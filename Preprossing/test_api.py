import requests
import json
import os

def get_iam_token(api_key):
    iam_url = 'https://iam.cloud.ibm.com/identity/token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'grant_type': 'urn:ibm:params:oauth:grant-type:apikey',
        'apikey': api_key
    }
    response = requests.post(iam_url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise Exception(f'Failed to obtain IAM token: {response.text}')

# Replace with your actual API key, project ID, and model ID
SERVICE_URL = 'https://eu-de.ml.cloud.ibm.com'

API_KEY = 'A7fCX7J8EARR85DLvSAyrMoKNCD13ICvnmHbpvNENZNR'
PROJECT_ID = 'b5976110-fe74-4388-b42f-ec08a9fad675'
MODEL_ID = 'sdaia/allam-1-13b-instruct'
# Replace these with your actual API key and project ID
parameters = {
    "decoding_method": "greedy",
    "max_new_tokens": 900,
    "repetition_penalty": 1.05
}

def generate_text(prompt):
    iam_token = get_iam_token(API_KEY)
    url = f'{SERVICE_URL}/ml/v1-beta/generation/text?version=2023-05-18'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {iam_token}',
        'Accept': 'application/json',
    }

    body = {
        'model_id': MODEL_ID,
        'input': prompt,
        'parameters': parameters,
        'project_id': PROJECT_ID  # Add project_id to the request body
    }

    response = requests.post(url, headers=headers, json=body)

    if response.status_code == 200:
        json_response = response.json()
        generated_text = json_response['results'][0]['generated_text']
        return generated_text
    else:
        print('Status Code:', response.status_code)
        print('Response Body:', response.text)
        raise Exception(f'API Error: {response.text}')

if __name__ == '__main__':
    input_query = "م متوقعتش إني أشوفك هنا"
    try:
        generated_response = generate_text(input_query)
        print(generated_response)
    except Exception as e:
        print('Error:', e)








