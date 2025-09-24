import logging
from config import config 

from openpyxl import load_workbook
import pandas as pd 
from config import USERS_PATH

def isAdmin(user_id : int) -> bool:
    admin_numbers = int(config.ADMIN_ID.get_secret_value())

    return user_id == admin_numbers


def is_registered_user(username: str) -> bool:
    username = "@" + username.strip()
    try:
        df = pd.read_excel(USERS_PATH)
        if username in df["User"].tolist():
            return True
        return False
    except Exception:
        return False
    
    