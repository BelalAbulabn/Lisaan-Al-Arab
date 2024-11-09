import pandas as pd
import json

# Load the TSV file into a pandas DataFrame
file_path = 'C:/Users/abulabn/Downloads/MADAR_Lexicon_v1.0 (1).tsv'
df = pd.read_csv(file_path, sep='\t')

# Initialize the translator

# Create a dictionary for dialect names mapping
dialect_mapping = {
    'TUN': 'تونيسية',
    'ALX': 'الإسكندرية',
    'AMM': 'العمانية',
    'JED': 'الجداوية',
    'RIY': 'الرياضية',
    'CAI': 'المصرية',
    'BEI': 'اللبنانية',
    'DAM': 'الشامية',
    'RAB': 'الرباطية',
    'BAG': 'البغدادية',
    'SAL': 'الصلالية',
    'FES': 'المغربية',
    'ALG': 'الجزائرية',
    'DOH': 'القطرية',
    'KHA': 'الخبرية',
    'ASW': 'الأسوانية',
    'TRI': 'الطرابلسية',
    'SFA': 'الصفاقسية',
    'SAN': 'الصنعانية',
    'MOS': 'الموصلية',
    'BEN': 'البنغازية',
    'ALE': 'الحلبية',
    'JER': 'القدسية',
    'MUS': 'المسقطية',
    'BAS': 'البصرية'
}

# Open a JSONL file for writing
output_file_path = 'output.jsonl'

with open(output_file_path, 'w', encoding='utf-8') as jsonl_file:
    # Iterate over the rows of the DataFrame
    for _, row in df.iterrows():
        # Translate the dialect to Modern Standard Arabic (MSA)
        
        # Get the full name of the dialect
        dialect_full_name = dialect_mapping.get(row['Dialect'], row['Dialect'])
        
        # Create the desired dictionary format
        json_dict = {
            "input": f"باللهجة {dialect_full_name}، الكلمة '{row['Tokenization']}' تعني في اللغة العربية الفصحى:",
            "output": row['MSA'],
        }
        # Write the JSON dictionary to the JSONL file
        jsonl_file.write(json.dumps(json_dict, ensure_ascii=False) + '\n')

print(f"File converted and saved to {output_file_path}")
