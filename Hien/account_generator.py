from time import strftime
from datetime import datetime, timedelta
from faker import Faker
import random
from phone_gen import PhoneNumber
import csv
import numpy as np
from vn_fullname_generator import generator
from datetime import datetime, timedelta
from resources.salary_district_HCM import experiences, IT_JOB_title, HCM
from resources.district_street import district_hcm_mapping
from resources.company_names import companies
import string

fake = Faker(locale="vi_VN")  # Vietnamese locale

start_date = datetime(2024, 7, 1)
end_date = datetime(2024, 8, 28)


def generate_customer_data(num_records=10000):
    customers = []
    code_exist = []
    id = 0
    for _ in range(num_records):
        start = False
        code = str(random.randint(10 ** 5, 10 ** 6 - 1))
        if code not in code_exist:
            start = True
            code_exist.append(code)
        while code in code_exist and start == False:
            code = str(random.randint(10 ** 5, 10 ** 6 - 1))

        code_user = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        creator = code_user
        create_date = (start_date + timedelta(days=random.randint(0, (end_date - start_date).days))).strftime(
            '%Y-%m-%d')
        code_account_type = str(random.randint(10 ** 6, 10 ** 7 - 1))
        cccd = random.randint(10 ** 12, 10 ** 13 - 1)

        account = {
            "code": code,
            "code_user": code_user,
            "code_account_type": code_account_type,
            "number_account": None,
            "code_usage_limit": None,
            "code_currency": None,
            "phone": None,
            "cccd": cccd,
            "image_front": None,
            "image_back": None,
            "creator": creator,
            "create_date": create_date,
            "editor": None,
            "edit_date": None,
            "status": random.choice(["success", "draft"])
        }
        customers.append(account)
        id += 1
    return customers


def save_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        print(data[0])
        print(data[0].keys())
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in data:
            writer.writerow(row)


num_records = 10000  # Change this to the number of records you want
customer_data = generate_customer_data(num_records)

# Save to CSV
csv_filename = 'hien_account.csv'
save_to_csv(customer_data, csv_filename)
print(f"Generated {num_records} customer records and saved to {csv_filename}")
