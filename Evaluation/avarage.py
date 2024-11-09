import csv

def calculate_average(filename):
    total = 0
    count = 0

    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        
        for row in reader:
            value = float(row[1])
            # Only consider values that are not 0
            if value != 0:
                total += value
                count += 1

    # Calculate the average
    average = total / count if count > 0 else 0
    print(f"The average of the second column (excluding 0 values) is: {average}")

# Specify your CSV file name
filename = 'resultsallamFinetuind2.csv'  # Replace with your actual file path
calculate_average(filename)
