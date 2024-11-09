import openai
import json
import os

# Set up your OpenAI API key
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Function to generate text using OpenAI's GPT model
def generate_text(prompt):
    try:
        # Use the OpenAI ChatCompletion API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if you have access
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=900,
            n=1,
            stop=None,
            temperature=0.7,
        )
        generated_text = response['choices'][0]['message']['content'].strip()
        return generated_text
    except Exception as e:
        raise Exception(f'API Error: {e}')

# Paths to your input and output JSONL files
input_file = 'testdata.jsonl'    # Replace with your input JSONL file path
output_file = 'testdata_outputgpt3.jsonl'  # Replace with your desired output JSONL file path

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
                continue  # Skip this line and proceed to the next
