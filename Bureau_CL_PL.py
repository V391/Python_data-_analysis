import pandas as pd
import numpy as np
import os

# Specify the directory where your CSV files are located
directory = r'C:\Users\user\Desktop\Analytics\August 2023\ranga t1'

# Function to handle mixed date formats
def parse_dates(date):
    try:
        return pd.to_datetime(date, format='%d-%m-%Y', errors='raise')
    except ValueError:
        return np.nan

def process_csv(file):
    # Read the data from the file
    df = pd.read_csv(file, low_memory=False)

    # Apply the function to the 'openDate' column
    df['openDate'] = df['openDate'].apply(parse_dates)

    # Exclude rows with NaT in 'openDate' column
    df = df[df['openDate'].notna()]

    # Prepare the output DataFrame
    output = df.groupby('cheqUserId')['openDate'].min().to_frame()

    # Generate the required columns
    months = pd.date_range(start="2021-08-01", end="2023-07-01", freq='MS')

    for month in months:
        next_month = month + pd.offsets.MonthBegin(1)

        credit_line_col = f"Credit Line opened before {month.strftime('%B %Y')}"
        personal_loan_col = f"Personal Loan Opened in {month.strftime('%B %Y')}"

        output[credit_line_col] = (output['openDate'] < month).astype(int)

        mask = (df['accountTypeName'].str.contains('PERSONAL')) & (df['openDate'].dt.month == month.month) & (df['openDate'].dt.year == month.year)
        personal_loans = df.loc[mask].groupby('cheqUserId').size()
        output[personal_loan_col] = personal_loans
        output[personal_loan_col].fillna(0, inplace=True)

    # Format the 'openDate' in the output DataFrame
    output['openDate'] = output['openDate'].dt.strftime('%d-%m-%Y')

    # Extract the file number from the input file name
    file_number = os.path.basename(file).split('-')[1].split('.')[0]

    # Define the output file name
    output_file = os.path.join(directory, f'output-{file_number}.csv')

    # Write the output DataFrame to a CSV file
    output.to_csv(output_file)

# Loop through all data files from data-1.csv to data-200.csv
for i in range(1, 201):
    input_file = os.path.join(directory, f'data-{i}.csv')
    if os.path.exists(input_file):
        process_csv(input_file)
    else:
        print(f"File {input_file} does not exist.")
