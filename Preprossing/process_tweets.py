import csv
import json
import re

def process_csv(csv_filename, output_filename):
    with open(csv_filename, 'r', encoding='utf-8-sig') as csvfile, \
         open(output_filename, 'w', encoding='utf-8') as outfile:
        
        reader = csv.DictReader(csvfile)
        # Clean up column names
        reader.fieldnames = [field.strip() for field in reader.fieldnames]
        
        for row in reader:
            # Extract fields
            tweet = row.get('uae_tweet_cleaned', '').strip()
            translation = row.get('msa_translation', '').strip()
            
            # Check if either field is empty
            if not tweet or not translation:
                print(f"Skipping incomplete row: {row}")
                continue
            
            # Handle multiple input-output pairs within the fields
            tweet_pairs = split_pairs(tweet)
            translation_pairs = split_pairs(translation)
            
            # Ensure equal number of tweets and translations
            if len(tweet_pairs) != len(translation_pairs):
                print(f"Mismatch in number of pairs in row: {row}")
                continue
            
            # Write each pair to the output file
            for input_text, output_text in zip(tweet_pairs, translation_pairs):
                json_obj = {'input': input_text.strip(), 'output': output_text.strip()}
                outfile.write(json.dumps(json_obj, ensure_ascii=False) + '\n')

def split_pairs(text):
    """
    Splits the text into multiple parts if delimiters are found.
    Delimiters can be custom-defined based on your data.
    """
    # Define possible delimiters
    delimiters = r'[،.;،\n]'  # Comma, semicolon, period, newline
    parts = re.split(delimiters, text)
    # Remove empty strings and strip whitespace
    return [part.strip() for part in parts if part.strip()]

if __name__ == '__main__':
    csv_filename = 'Emi-NADI.csv'      # Replace with your CSV file path
    output_filename = 'output4.jsonl'  # Replace with your desired output file path
    process_csv(csv_filename, output_filename)
