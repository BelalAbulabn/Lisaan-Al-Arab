import pandas as pd
import openai
import time

# Set your OpenAI API key
openai.api_key = 'sk-proj-ETFsJX268RMex0DnMBXLT3BlbkFJte8z9HsVVPtrYCLYsxja'

# Load the CSV file
df = pd.read_csv('imagenet_b_darija.csv')

# Ensure the 'english' column exists
if 'english' not in df.columns:
    raise ValueError("The CSV file does not contain an 'english' column.")

# Function to translate text using GPT-4
def translate_text(text):
    prompt = f"Translate the following English word to Modern Standard Arabic:\n\n{text}"
    try:
        response = openai.ChatCompletion.create(
            model='gpt-4',
            messages=[
                {"role": "system", "content": "You are a helpful assistant that translates English to Modern Standard Arabic."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=60,
            n=1,
            stop=None
        )
        translation = response.choices[0].message['content'].strip()
        return translation
    except Exception as e:
        print(f"Error translating '{text}': {e}")
        return ''

# List to store translations
translations = []

# Iterate over each row and translate the 'english' column
for index, row in df.iterrows():
    english_text = row['english']
    if pd.notnull(english_text):
        print(f"Translating '{english_text}'...")
        translation = translate_text(english_text)
        translations.append(translation)
        time.sleep(1)  # To respect API rate limits
    else:
        translations.append('')

# Add the new column to the DataFrame
df['main_arabic'] = translations

# Save the updated DataFrame to a new CSV file
df.to_csv('translated_file.csv', index=False)

print("Translation complete. The updated file is saved as 'translated_file.csv'.")

