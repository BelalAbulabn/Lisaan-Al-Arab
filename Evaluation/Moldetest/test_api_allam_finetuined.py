import json
from ibm_watson_machine_learning import APIClient
import requests
# IBM Watson setup

# # Replace these with your actual IBM Watson credentials and URL
access_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im5WZTRrVnZkc25JUUdrOWs0YzFRMlhrNjBmekhKSW1GUW5NWUJjN3A4ZkkifQ.eyJ1aWQiOiIxMDAwMzMxMDgxIiwidXNlcm5hbWUiOiI4ZmJlMjRmMC1iZGVjLTQyM2MtYWFjNC03ZjBiNzRiMGRiNmEiLCJyb2xlIjoiVXNlciIsInBlcm1pc3Npb25zIjpbInNpZ25faW5fb25seSJdLCJncm91cHMiOlsxMDAzNywxMDAwMF0sInN1YiI6IjhmYmUyNGYwLWJkZWMtNDIzYy1hYWM0LTdmMGI3NGIwZGI2YSIsImlzcyI6IktOT1hTU08iLCJhdWQiOiJEU1giLCJhcGlfcmVxdWVzdCI6dHJ1ZSwiaWF0IjoxNzMwODgwMjAzLCJleHAiOjUzMzA4NzY2MDN9.z1yaeflpF45bnwVbr_eDpV-D7MEPBuebyPDPADmdhLoUmdsDZQCdm2iB12B5xhSYQSoLFjQtjrDqI7cRIlauxKUpq9MGRwPxPMLUCKYt8XrFQXlSUFt1stjLmoPcx2w_yvyZEyL6bspy60c0brpBuKMRqmMoBRbh9pEQhpli80MBG4X6MBuxdlw5uD3xbgaZQXjw7XDpElrISqpj17ukeG_1n29p7H7rz9MqMKtIUSaiEYvalGkPz88bYY1n8e7grzJzvfOnpwu8xh-vHVn3Cv7JYKA3NSDYiTZSCuj0HX5OOypmSKN1yBUPwn7hFRGqmkNlxChhtTsQHGU7wx1wFQ'
deployment_url = "https://ai.deem.sa/ml/v1/deployments/aa75d2a5-03e8-4e1a-bb08-7eb17eaf7e21/text/generation?version=2021-05-01"
deployment_id = "aa75d2a5-03e8-4e1a-bb08-7eb17eaf7e21"  # Replace with your deployment ID
project_id = '730eddd7-7cb1-417c-9b09-8930edd15163'  # Replace with your actual project ID


wml_credentials = {
    "url": "https://ai.deem.sa/",
    "token": access_token,
    "instance_id": "openshift",
    "version": "5.0"
}

client = APIClient(wml_credentials)
# Uncomment the line below if you need to set the default project
# client.set.default_project(project_id)

def generate_text(user_input):
    # Prepare the payload with user input only
    
    full_input = f": {user_input} "

    scoring_payload = {
        "input": full_input,
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 900,
            "min_new_tokens": 0,
            "repetition_penalty": 1
        }
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    # Send POST request to IBM Watson model endpoint
    response = requests.post(deployment_url, json=scoring_payload, headers=headers, verify=False, timeout=600)
     # Check for successful response and parse generated text
    if response.status_code == 200:
        generated_text = response.json()['results'][0]['generated_text']
        return generated_text
    else:
        print('Error:', response.status_code, response.text)
        raise Exception(f"Error from IBM Watson API: {response.status_code} {response.text}")


# Paths to your input and output JSONL files
input_file = 'testdata.jsonl'    # Replace with your input JSONL file path
output_file = 'testdata_outputAllm3.jsonl'  # Replace with your desired output JSONL file path

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
                continue  # Skip the line if it's not valid JSON
