# from phone_gen import PhoneNumber
# # or
# phone_number = PhoneNumber("Vietnam")  # Country name
#
# # Get a phone number
# number = phone_number.get_number()
# print(number)  # +442908124840

import pandas as pd
import random as rd
from faker import Faker
from datetime import datetime

fake = Faker(locale="vi_VN")  # Vietnamese locale
# Generate a fake date
fake_date_str = fake.date()

# Define the date to compare against
comparison_date_str = "2002-10-13"

# Convert the strings to datetime objects
fake_date = datetime.strptime(fake_date_str, "%Y-%m-%d").date()
comparison_date = datetime.strptime(comparison_date_str, "%Y-%m-%d").date()

print(fake_date, comparison_date)
# Compare the dates
result = fake_date < comparison_date

print(result)
from faker import Faker
import datetime

fake = Faker()

start_date = datetime.date(2000, 1, 1)  # Convert string '01-01-2000' to a date object
end_date = datetime.date(2024, 6, 6)  # Convert string '2024-06-06' to a date object

result = fake.date_between(start_date=start_date, end_date=end_date)
print(result)
print(type(result))