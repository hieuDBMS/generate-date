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

fake = Faker(locale="vi_VN")  # Vietnamese locale


def get_birthday(ex):
    while True:
        # Generate a fake date of birth between 18 and 70 years ago
        birth_date = fake.date_of_birth(minimum_age=18, maximum_age=70)

        # Extract birth year
        birth_year = birth_date.year

        # Calculate age
        age = 2024 - birth_year

        # Simulate work experience (you need to define or generate this value)
        # Check if (2024 - birth_year) - work_experience > 20
        if (2024 - birth_year) - ex >= 18:
            print(f"Valid birth date: {birth_date}")
            break
        else:
            continue

    return birth_date


def generate_customer_data(num_records):
    customers = []
    id = 0
    for _ in range(num_records):
        experience = random.choice(experiences)
        job_title = random.choice(IT_JOB_title)
        salary = calculate_salary(experience, job_title)
        district = random.choice(list(HCM.keys()))
        street = random.choice(district_hcm_mapping[district])
        address = f"{street}, {district}, TP.HCM"

        cust_type = "Individual"
        org = "N/A"
        if random.random() < 0.5:  # 10% chance of being an organization
            cust_type = "Organization"
            org = random.choice(companies)

        birthday = get_birthday(experience)
        existing_time = np.random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        sex = random.choice(["Male", "Female"])
        MartialStatus = random.choice(["Single", "Married"])
        Dependents = "Yes" if MartialStatus == "Married" else random.choice(["Yes", "No"])
        incom_freq = 0
        outcom_freq = 0
        customer = {
            "CIF Number": id,
            "CustName": generator.generate(1 if sex == "Male" else 0),
            "Address": address,
            "Mobile": PhoneNumber("Vietnam").get_number(),
            "MartialStatus": MartialStatus,
            "Dependents": Dependents,
            "CustType": cust_type,
            "BirthDay": birthday.strftime("%Y-%m-%d"),
            "Sex": sex,
            "Organization": org,
            "Job": job_title,
            "Experience": experience,
            "Salary": salary,
            "Existing time": existing_time,
            "Credit Score": random.randint(300, 850),
            # "Current Saving Balance": round(random.randint(0, 500000000), 2),
            # "Current Checking Balance": round(random.randint(0, 100000000), 2),
            # "Housing Loan": 0,
            # "Loan": 0,
            # "Transaction Frequency Incoming": incom_freq,
            # "Transaction Frequency Outgoing": outcom_freq,
            # "Balance Update Frequency": 0
        }
        customers.append(customer)
        id += 1
    return customers


def calculate_salary(experience, job_title):
    base_salary = random.randint(HCM["Quận 1"][0], HCM["Quận 1"][1])
    if experience > 8:
        return round(random.randint(40000000, 75000000), -3)
    elif 5 <= experience <= 8:
        return round(random.randint(30000000, 70000000), -3)
    elif 3 <= experience <= 4 or "Manager" in job_title or "Architect" in job_title:
        return round(random.randint(20000000, 40000000), -3)
    elif experience == 2:
        return round(random.randint(15000000, 20000000), -3)
    elif experience == 1:
        return round(random.randint(10000000, 15000000), -3)
    else:
        return round(random.randint(3000000, 5000000), -3)


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

# Print the first few records to verify
for customer in customer_data[:5]:
    print(customer)

# Save to CSV
csv_filename = 'customer_data.csv'
save_to_csv(customer_data, csv_filename)
print(f"Generated {num_records} customer records and saved to {csv_filename}")
