import pandas as pd
import numpy as np
import random as rd
from faker import Faker
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta
import datetime
import csv

fake = Faker(locale="vi_VN")  # Vietnamese locale
customer_file_path = './data/customer_data.csv'
customer_df = pd.read_csv(customer_file_path, encoding='utf-8-sig')

# Define supscription type
SubscriptionType = [
    "Tiết kiệm truyền thống",
    "Tiết kiệm Tích Tài",
    "Tiết kiệm Đại Phát",
    "Tiết kiệm Trung Niên Tích Lộc",
    "Tiền gửi tương lai"
]

period_saving = [
    "6 tháng",
    "12 tháng",
    "18 tháng",
    "24 tháng",
    "36 tháng"
]

# Define the period of dates to random the "OPENDATE" field
start_date_period = datetime.date(2020, 1, 1)
end_date_period = datetime.date(2024, 6, 20)

customers_size = customer_df["CIF Number"].size


def check_adjust_balance(money_w_or_d, current_balance, action):
    if action == 'withdraw':
        if current_balance < money_w_or_d:
            return False
        else:
            return True
    return True


def generate_saving_account(num_records):
    all_customer = []
    count = 0
    for i in range(num_records):
        # All the subscriptions that the customer chose
        subscriptions_of_cust = np.random.choice(SubscriptionType, size=rd.randint(1, len(SubscriptionType)),
                                                 replace=False)
        if np.random.choice([True, False], p=[0.6, 0.4]):
            current_customer = []
            for sub in subscriptions_of_cust:
                number_of_updated = np.random.randint(1, 6)
                balance = np.random.randint(10000000, 10000000000, dtype=np.int64)
                saving_period = rd.choice(period_saving)
                opendate = fake.date_between(start_date=start_date_period, end_date=end_date_period)
                duedate = opendate + relativedelta(months=int(saving_period.split()[0]))
                update_date = opendate
                status = np.random.choice(["ACTIVE", "CLOSE"], p=[0.9, 0.1])
                allow_withdraw = "Y" if status == "ACTIVE" else "N"
                customer_data = {
                    "CIF": i,
                    "BALANCE": balance,
                    "CCYCD": "VND",
                    "SUBSCRIPTIONTYPE": sub,
                    "OPENDATE": opendate,
                    "DUEDATE": duedate,
                    "DURATION": saving_period,
                    "STATUS": status,
                    "ALLOWWITHDRAW": allow_withdraw,
                    "UPDATEDATE": update_date
                }
                current_customer.append(customer_data)
                if status == 'CLOSE': continue
                for _ in range(number_of_updated):
                    # money withdraw or deposit
                    money_w_or_d = rd.randint(10000000, 50000000)
                    action = rd.choice(["withdraw", "deposit"])
                    if check_adjust_balance(money_w_or_d=money_w_or_d, current_balance=balance,
                                            action=action):
                        balance = balance - money_w_or_d if action == "withdraw" else balance + money_w_or_d
                    else:
                        continue  # continue when withdraw do not have enough balance
                    # update date
                    updated_date = fake.date_between(start_date=opendate, end_date=datetime.date.today())
                    customer_data_update = {
                        "CIF": i,
                        "BALANCE": balance,
                        "CCYCD": "VND",
                        "SUBSCRIPTIONTYPE": sub,
                        "OPENDATE": opendate,
                        "DUEDATE": duedate,
                        "DURATION": saving_period,
                        "STATUS": status,
                        "ALLOWWITHDRAW": allow_withdraw,
                        "UPDATEDATE": updated_date
                    }
                    current_customer.append(customer_data_update)
            all_customer.extend(current_customer)
    sorted_all_customer = sorted(all_customer, key=lambda x: x["UPDATEDATE"])
    return sorted_all_customer


def save_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in data:
            writer.writerow(row)


file_name = "data/test_saving.csv"
customer_data = generate_saving_account(customers_size)
save_to_csv(customer_data, file_name)
