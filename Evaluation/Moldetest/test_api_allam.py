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
# apikey = "62mr_rYX7J3EZffAtnXyOav-Lt7-io_I7M6oq4bYEljL"
# project_id = "231a1b2a-0200-40d4-abcb-6d4c3357d9de"


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
        'project_id': PROJECT_ID
    }

    response = requests.post(url, headers=headers, json=body,timeout=500)

    if response.status_code == 200:
        json_response = response.json()
        generated_text = json_response['results'][0]['generated_text']
        return generated_text
    else:
        print('Status Code:', response.status_code)
        print('Response Body:', response.text)
        raise Exception(f'API Error: {response.text}')

# Paths to your input and output JSONL files
input_file = 'testdata.jsonl'    # Replace with your input JSONL file path
output_file = 'testdata_outputAllm5.jsonl'  # Replace with your desired output JSONL file path

# Open the input and output files

with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
    for line_number, line in enumerate(infile, 1):
        if line.strip():  # Skip empty lines
            try:
                data = json.loads(line.strip())
                input_text = data.get('input', '')
                original_output = data.get('output', '')
                try:
                    # Generate response from the model
                    model_output = generate_text(input_text)
                    
                    # Prepare the output data
                    output_data = {
                        'input': input_text,
                        'original output': original_output,
                        'output of tested model': model_output
                    }
                    # Write the output data as a JSONL line
                    outfile.write(json.dumps(output_data, ensure_ascii=False) + '\n')
                except Exception as e:
                    print(f"Error processing input: {input_text}")
                    print(e)
            except json.JSONDecodeError as e:
                print(f"JSONDecodeError on line {line_number}: {e}")
                print(f"Line content: {line}")
                continue  # Ski





                

        




