import json
import csv
import openai
import os
import time

# Set your OpenAI API key securely
openai.api_key = "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" # Make sure this environment variable is set

def evaluate_output(input_text, original_output, fine_tuned_output, retries=3, delay=5):
    messages = [
        {"role": "system", "content": "You are an AI assistant tasked with evaluating the similarity between outputs from a fine-tuned model and an original output, given an input. Your evaluation should consider word similarity and dialect matching."},
        {"role": "user", "content": f'''
Instructions:
- Provide a similarity score between **0** and **1**.
  - **0** means no similarity.
  - **1** means identical similarity in word choice and dialect.
  - Intermediate values reflect partial similarity based on word matching and dialect consistency.
- Do not provide any additional text or explanation, only the score.

Here are the details:

Input:
"{input_text}"

Original Output:
"{original_output}"

Fine-tuned Output:
"{fine_tuned_output}"

Your evaluation (0 to 1):'''}
    ]
    
    for attempt in range(retries):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=messages,
                temperature=0
            )
            evaluation = response['choices'][0]['message']['content'].strip()
            return evaluation
        except openai.error.RateLimitError:
            if attempt < retries - 1:
                print(f"Rate limit hit. Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print("Exceeded retry limit due to rate limit error.")
                return None

def main():
    input_file = 'modified_finedtunedv3.jsonl'     # Replace with your JSONL file path
    output_file = 'result_outputgpt4.csv'   # Output CSV file

    with open(input_file, 'r', encoding='utf-8') as jsonl_file, \
         open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
        
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['sample_number', 'evaluation'])
        
        for idx, line in enumerate(jsonl_file):
            data = json.loads(line)
            input_text = data.get('input', '')
            original_output = data.get('original output', '')
            fine_tuned_output = data.get('output of tested model', '')  # Updated key here
            
            if input_text and original_output and fine_tuned_output:
                evaluation = evaluate_output(input_text, original_output, fine_tuned_output)
                if evaluation is not None:
                    csv_writer.writerow([idx + 1, evaluation])
                    print(f"Processed sample {idx + 1}: Evaluation {evaluation}")
                else:
                    print(f"Skipping sample {idx + 1}: Rate limit exceeded after retries")
            else:
                print(f"Skipping sample {idx + 1}: Missing data")

if __name__ == '__main__':
    main()
