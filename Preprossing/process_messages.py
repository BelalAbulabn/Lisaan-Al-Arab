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
            # Check if 'messageslist' exists
            if 'messageslist' not in row:
                print(f"'messageslist' key not found in row with id {row.get('idstring', 'Unknown ID')}")
                continue
            
            messages_list_raw = row['messageslist']
            
            # Remove leading/trailing quotes and fix double quotes
            if messages_list_raw.startswith('"') and messages_list_raw.endswith('"'):
                messages_list_raw = messages_list_raw[1:-1]
            messages_list_raw = messages_list_raw.replace('""', '"')
            
            try:
                messages = json.loads(messages_list_raw)
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON in row {row.get('idstring', 'Unknown ID')}: {e}")
                continue

            # Process messages to handle multiple exchanges
            exchanges = extract_exchanges(messages)
            
            # Write each input-output pair to the output file
            for input_text, output_text in exchanges:
                json_obj = {'input': input_text.strip(), 'output': output_text.strip()}
                outfile.write(json.dumps(json_obj, ensure_ascii=False) + '\n')

def extract_exchanges(messages):
    """
    Extracts all input-output pairs from the messages list.
    Handles multi-turn conversations.
    """
    exchanges = []
    user_messages = []
    assistant_messages = []

    for msg in messages:
        content = msg['content']
        role = msg['role']
        
        # Handle multiple exchanges within a single message content
        if '<|assistant|>' in content or '<|user|>' in content:
            split_msgs = split_multi_turn(content)
            for role_tag, text in split_msgs:
                if role_tag == 'user':
                    user_messages.append(text)
                elif role_tag == 'assistant':
                    assistant_messages.append(text)
        else:
            if role == 'user':
                user_messages.append(content)
            elif role == 'assistant':
                assistant_messages.append(content)
    
    # Pair up the user and assistant messages
    for u_msg, a_msg in zip(user_messages, assistant_messages):
        # Remove the prefix from user messages if present
        input_text = remove_prefix(u_msg, ["ترجم من الدارجة للفصحى: ", "ترجم: "])
        output_text = a_msg.strip()
        exchanges.append((input_text, output_text))

    return exchanges

def split_multi_turn(content):
    """
    Splits multi-turn conversations into individual messages based on role tags.
    """
    pattern = r'(<\|user\|>|<\|assistant\|>)'
    parts = re.split(pattern, content)
    messages = []
    current_role = None

    for part in parts:
        if part == '<|user|>':
            current_role = 'user'
        elif part == '<|assistant|>':
            current_role = 'assistant'
        else:
            if current_role:
                messages.append((current_role, part.strip()))
    
    return messages

def remove_prefix(text, prefixes):
    """
    Removes any of the specified prefixes from the text.
    """
    for prefix in prefixes:
        if text.startswith(prefix):
            return text[len(prefix):].strip()
    return text.strip()

if __name__ == '__main__':
    csv_filename = 'table_data dr_msa.csv'      # Replace with your CSV file path
    output_filename = 'output5.jsonl'  # Replace with your desired output file path
    process_csv(csv_filename, output_filename)
