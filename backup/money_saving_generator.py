import pandas as pd
import random as rd
from faker import Faker
from datetime import datetime as dt
import datetime
import csv

fake = Faker(locale="vi_VN")  # Vietnamese locale
customer_file_path = 'customer_data.csv'
customer_df = pd.read_csv(customer_file_path, encoding='utf-8')
SavingProductSubcribed = [
    "Tiết kiệm truyền thống",
    "Tiết kiệm Tích Tài",
    "Tiết kiệm Đại Phát",
    "Tiết kiệm Trung Niên Tích Lộc",
    "Tiền gửi tương lai"
]
period_saving = [
    "12 tháng",
    "18 tháng",
]

start_date = datetime.date(2010, 1, 1)  # Convert string '01-01-2000' to a date object
end_date = datetime.date(2024, 6, 6)


num_customers = customer_df['CIF Number'].size  # 10.000


def check_adjust_balance(fluctuated_balance, current_balance, action):
    if action == 'withdraw':
        if current_balance < fluctuated_balance:
            return False
        else:
            return True
    return True


def generate_current_saving(num_records):
    all_saving = []
    count = 0
    for i in range(num_records):
        if rd.choice([True, False]):
            Existed_date = []
            number_of_updated = rd.randint(1, 20)
            current_saving_balance = rd.randint(10000000, 10000000000)
            application_date = fake.date_between(start_date=start_date, end_date=end_date)

            customer_saving = []
            for _ in range(number_of_updated):
                saving_type = rd.choice(SavingProductSubcribed)
                fluctuated_balance = rd.randint(10000000, 50000000)
                withdraw_deposit_action = rd.choice(["withdraw", "deposit"])
                if check_adjust_balance(fluctuated_balance=fluctuated_balance, current_balance=current_saving_balance,
                                        action=withdraw_deposit_action):
                    current_saving_balance = current_saving_balance - fluctuated_balance if withdraw_deposit_action == "withdraw" else current_saving_balance + fluctuated_balance
                # Update date
                updated_date = fake.date_between(start_date=start_date, end_date=end_date)
                while updated_date not in Existed_date and updated_date < application_date:
                    updated_date = fake.date_between(start_date=start_date, end_date=end_date)
                Existed_date.append(updated_date)
                # print(count)
                customer_data = {
                    "Saving_id": count,
                    "CIF": i,
                    "CurrentSavingBalance": current_saving_balance,
                    "SavingProductSubcribed": saving_type,
                    "ApplicationDate": application_date,
                    "UpdateDate": updated_date
                }
                count += 1
                print(customer_data)
                customer_saving.append(customer_data)
            sorted_customer_saving = sorted(customer_saving, key=lambda x: x["UpdateDate"])
            all_saving.extend(sorted_customer_saving)
    return all_saving


def save_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in data:
            writer.writerow(row)


file_name = "saving_money_data.csv"
customer_data = generate_current_saving(num_customers)
save_to_csv(customer_data, file_name)
