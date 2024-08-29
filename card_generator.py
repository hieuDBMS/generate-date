import pandas as pd

customer_file_path = 'customer_data.csv'
customer_df = pd.read_csv(customer_file_path, encoding='utf-8')

num_customers = customer_df['CIF Number'].size  # 10.000
card_types = ["Credit Cards",
"Debit Cards",
"Platinum Cards",
]