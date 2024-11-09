from flask import Flask, request, jsonify
from ibm_watson_machine_learning import APIClient
from flask_cors import CORS
import requests
import json
import ssl


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Replace these with your actual IBM Watson credentials and URL
access_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im5WZTRrVnZkc25JUUdrOWs0YzFRMlhrNjBmekhKSW1GUW5NWUJjN3A4ZkkifQ.eyJ1aWQiOiIxMDAwMzMxMDgxIiwidXNlcm5hbWUiOiI4ZmJlMjRmMC1iZGVjLTQyM2MtYWFjNC03ZjBiNzRiMGRiNmEiLCJyb2xlIjoiVXNlciIsInBlcm1pc3Npb25zIjpbInNpZ25faW5fb25seSJdLCJncm91cHMiOlsxMDAzNywxMDAwMF0sInN1YiI6IjhmYmUyNGYwLWJkZWMtNDIzYy1hYWM0LTdmMGI3NGIwZGI2YSIsImlzcyI6IktOT1hTU08iLCJhdWQiOiJEU1giLCJhcGlfcmVxdWVzdCI6dHJ1ZSwiaWF0IjoxNzMwODgwMjAzLCJleHAiOjUzMzA4NzY2MDN9.z1yaeflpF45bnwVbr_eDpV-D7MEPBuebyPDPADmdhLoUmdsDZQCdm2iB12B5xhSYQSoLFjQtjrDqI7cRIlauxKUpq9MGRwPxPMLUCKYt8XrFQXlSUFt1stjLmoPcx2w_yvyZEyL6bspy60c0brpBuKMRqmMoBRbh9pEQhpli80MBG4X6MBuxdlw5uD3xbgaZQXjw7XDpElrISqpj17ukeG_1n29p7H7rz9MqMKtIUSaiEYvalGkPz88bYY1n8e7grzJzvfOnpwu8xh-vHVn3Cv7JYKA3NSDYiTZSCuj0HX5OOypmSKN1yBUPwn7hFRGqmkNlxChhtTsQHGU7wx1wFQ'
deployment_url = "https://ai.deem.sa/ml/v1/deployments/cb7a4cb2-9580-4467-9caa-21bb501fba26/text/generation?version=2021-05-01"
deployment_id = "cb7a4cb2-9580-4467-9caa-21bb501fba26"  # Replace with your deployment ID
project_id = '730eddd7-7cb1-417c-9b09-8930edd15163'  # Replace with your actual project ID

system_prompt = """
Your name is always "المعتز بالله". You are a multilingual conversational model specialized in handling different Arabic dialects: Egyptian, Levantine, Moroccan, and Gulf. You can identify dialects, translate between Modern Standard Arabic (MSA) and dialects, and generate poetry, novels, and sarcasm. Your responses must strictly adhere to the following instructions and examples for each task type to maintain high quality and ensure consistency with the dataset training.

Key Instructions for System Behavior:

Dialect Identification: from user's input you try to identify the input's dialect, provide the answer in same dialect based on the input, if identifying dialect was requested then you define which dialect.
Poetry Generation: When generating poems, focus on cultural references and idioms pertinent to the requested dialect. Ensure the poem captures the emotions expressed in the prompt, such as affection, frustration, or reconciliation.
Novel Writing: When writing a story, emphasize realistic social settings and dialect nuances. Keep the storyline reflective of struggles, societal challenges, or humor, as requested.
Sarcasm Generation: When creating sarcastic responses, ensure they convey humor while reflecting the given dialect's informal tone.
Dialect Translation: For translations, accurately convert MSA to the requested dialect, ensuring that idiomatic expressions retain their original meanings.

General Guidelines:
Always adhere to the given prompt format and dialect.
When in doubt, prioritize context relevance and cultural idioms of the dialect.
Keep responses concise, contextual, and true to the request's emotional or factual tone.

Example Interaction:
User: "وش سويت اليوم في المدرسة/الجامعة؟"
Response: " ما سويت شي كثير، بس درسنا الدرس الجديد"

Expected Output Quality:
The responses should be contextually relevant, showing cultural familiarity with idioms, slang, and dialect-specific references. Here are examples of expected results for various tasks:
Identifying Dialect: Given mixed dialectal content, clearly recognize and identify the correct dialect and use it in your answers.
Poetry: Accurately capture the cultural nuances, emotional depth, and unique expressions of the requested dialect.
Novels and Stories: Provide relatable narratives set in the context of the dialect, reflecting societal norms, challenges, and humor.
Sarcasm: Ensure humor is nuanced, capturing the casual, informal nature of the dialect used.
Translations: Maintain the meaning, tone, and idiomatic accuracy during translations between MSA and the specified dialect.

Note:
Follow these instructions strictly to ensure optimal output quality and maintain consistency with the model's capabilities.
"""

# IBM Watson setup
wml_credentials = {
    "url": "https://ai.deem.sa/",
    "token": access_token,
    "instance_id": "openshift",
    "version": "5.0"
}

client = APIClient(wml_credentials)
#client.set.default_project(project_id)

def generate_text(user_input):
    # Combine system prompt and user input
    full_input = f"{system_prompt}\nUser: {user_input}\nالمعتز بالله: "
    
    scoring_payload = {
        "input": full_input,
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 2047,
            "min_new_tokens": 0,
            "repetition_penalty": 1
        }
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    # Send POST request to IBM Watson model endpoint
    response = requests.post(deployment_url, json=scoring_payload, headers=headers, verify=False)
    
    # Check for successful response and parse generated text
    if response.status_code == 200:
        generated_text = response.json()['results'][0]['generated_text']
        return generated_text
    else:
        print('Error:', response.status_code, response.text)
        raise Exception(f"Error from IBM Watson API: {response.status_code} {response.text}")

@app.route('/generate-text', methods=['POST'])
def generate_text_endpoint():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Empty JSON body"}), 400
        user_input = data.get("input", "")
        if not user_input:
            return jsonify({"error": "Missing 'input' field"}), 400

        # Generate response from model
        generated_text = generate_text(user_input)
        
        # Use json.dumps with ensure_ascii=False to prevent Unicode escaping
        response_json = json.dumps({"response": generated_text}, ensure_ascii=False)
        
        # Return the response with mimetype set to application/json
        return app.response_class(response=response_json, mimetype="application/json; charset=utf-8")
    except Exception as e:
        print("Error in generate_text_endpoint:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3021, debug=True)