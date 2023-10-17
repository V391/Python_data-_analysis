# Python_data-_analysis

Given: 
- 120GB of Bureau data of users of a credit repayment app(similar to CRED), across 200 CSV files
- The data is unique at a credit line level
- each credit line has 34 parameters(columns) across which data is captured

Objective:
- Find the month of credit line opened for each credit entry
- How long after the credit line was opened did the user take a personal loan?
- What is the montly adoption rate of personal loans for users with Credit lines

Available Approaches:
1. Push all data to Bigquery & write SQL queries to get answer
2. Write a Python script for data extraction & processing 

We have used (2) here.
