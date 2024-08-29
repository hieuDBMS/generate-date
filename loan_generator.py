import numpy as np
import pandas as pd
from numpy import random as rd
import uuid
from faker import Faker
import datetime
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

faker = Faker('vi_VN')

customer_file_path = 'customer_data.csv'
customer_df = pd.read_csv(customer_file_path, encoding='utf-8')
num_customers = customer_df['CIF Number'].size  # 10.000
credit_score = customer_df['Credit Score']
job = customer_df['Job']
salary = customer_df['Salary']
num_loans = 20000
rd.seed(360)

sample_customers = rd.randint(0, num_customers, num_loans)
loan_amount = rd.randint(1_000_000, 1_000_000_000, num_loans)
loan_term = rd.randint(4, 61, num_loans)  # in months
monthly_debt = loan_amount // loan_term

interest_rate_dict = {
    'Real Estate': '6.5',
    'Home': '7',
    'Consumer': '6.5',
    'Business': '8.5',
    'Automobile': '7.5',
    'Others': '9'
}
loan_purpose = rd.choice(list(interest_rate_dict.keys()), num_loans)

today = datetime.today().date()

start_dates_floors = [today - relativedelta(months=months) for months in loan_term]
start_date = [start_date_floor + timedelta(days=rd.randint(0, (today - start_date_floor).days)) for start_date_floor in
              start_dates_floors]
due_dates = [start_date[i] + relativedelta(months=loan_term[i]) for i in range(num_loans)]

loans = {
    'Loan ID': [i for i in range(num_loans)],
    'CIF Number': sample_customers,  # 1 loan - 1 id
    # 'Credit Score': [credit_score[cif] for cif in sample_customers],
    # 'Job': [job[cif] for cif in sample_customers],
    'Annual Income': [salary[cif] * 12 for cif in sample_customers],
    # 'Years In Current Job' : rd.randint(1, 21, num_loans),
    'Purpose': loan_purpose,
    'Home Ownership': rd.choice(['Rent', 'Own', 'Mortgage', 'Other'], num_loans),
    'Loan Amount': loan_amount,
    'Loan Date': start_date,
    'Due Date': due_dates,
    'Loan Term': loan_term,
    'Monthly Debt': monthly_debt,
    'Years of Credit History': rd.randint(1, 11, num_loans),
    'Interest Rate': [interest_rate_dict[purpose] for purpose in loan_purpose],
    'Total Paid': rd.randint(monthly_debt, loan_amount + 1, num_loans),
    'Months since last delinquency': [rd.randint(1, term // 2) for term in loan_term]
}

loan_filepath = 'loan_data.csv'
loan_df = pd.DataFrame(loans)
loan_df.to_csv(loan_filepath, index=False, encoding='utf-8')
