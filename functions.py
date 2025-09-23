import logging
from config import config

from openpyxl import load_workbook
import pandas as pd 

def isAdmin(phone : str) -> bool:
    admin_numbers = config.ADMIN_PHONE_NUMBERS.get_secret_value()

    return phone in admin_numbers


def isUser(phone : str) -> bool:
    df = pd.read_excel("users.xlsx")
    print(df["Phone Number"].tolist())
    if "+992" in phone:
        phone = int(phone.replace("+992",""))

    return phone in df["Phone Number"].tolist()
