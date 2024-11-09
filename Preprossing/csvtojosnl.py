import csv
import json
import re

def process_csv(csv_filename, output_filename):
    with open(csv_filename, 'r', encoding='utf-8-sig') as csvfile, \
         open(output_filename, 'w', encoding='utf-8') as outfile:
        
        reader = csv.DictReader(csvfile)
        # Clean up column names
        reader.fieldnames = [field.replace('\n', ' ').strip('"').strip() for field in reader.fieldnames]
        
        for row in reader:
            # Check if 'messages list' exists
            if 'messages list' not in row:
                print(f"'messages list' key not found in row with id {row.get('id string', 'Unknown ID')}")
                continue
            
            messages_list_raw = row['messages list']
            
            # Remove leading/trailing quotes and fix double quotes
            if messages_list_raw.startswith('"') and messages_list_raw.endswith('"'):
                messages_list_raw = messages_list_raw[1:-1]
            messages_list_raw = messages_list_raw.replace('""', '"')
            
            try:
                messages = json.loads(messages_list_raw)
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON in row {row.get('id string', 'Unknown ID')}: {e}")
                continue

            # Initialize lists to hold user and assistant messages
            user_contents = []
            assistant_contents = []

            # Process messages to handle multiple exchanges
            for msg in messages:
                content = msg['content']
                role = msg['role']

                # Handle multiple exchanges within a single message content
                exchanges = split_exchanges(content)
                for exchange in exchanges:
                    if role == 'user':
                        user_contents.append(exchange)
                    elif role == 'assistant':
                        assistant_contents.append(exchange)

            # Pair up the user and assistant messages
            for u_content, a_content in zip(user_contents, assistant_contents):
                input_text = extract_input_text(u_content)
                output_text = a_content.strip()

                if input_text and output_text:
                    json_obj = {'input': input_text, 'output': output_text}
                    outfile.write(json.dumps(json_obj, ensure_ascii=False) + '\n')
                else:
                    print(f"Could not find input or output in row {row.get('id string', 'Unknown ID')}")

def split_exchanges(content):
    """
    Split the content into individual exchanges using <|user|> and <|assistant|> tags.
    """
    # Define the pattern to split content
    pattern = r'(<\|user\|>|<\|assistant\|>)'
    parts = re.split(pattern, content)
    exchanges = []
    current_role = None
    current_content = ''

    for part in parts:
        if part in ('<|user|>', '<|assistant|>'):
            if current_content:
                exchanges.append(current_content.strip())
                current_content = ''
            current_role = part
        else:
            current_content += part

    if current_content:
        exchanges.append(current_content.strip())

    return exchanges

def extract_input_text(user_message):
    """
    Extract the input text from the user's message content.
    """
    # Remove the prefix if present
    prefix = "ترجم من الفصحى للدارجة: "
    if user_message.startswith(prefix):
        return user_message[len(prefix):].strip()
    else:
        return user_message.strip()

if __name__ == '__main__':
    csv_filename = 'table_data msa_dr.csv'      # Replace with your CSV file path
    output_filename = 'output3.jsonl'  # Replace with your desired output file path
    process_csv(csv_filename, output_filename)
