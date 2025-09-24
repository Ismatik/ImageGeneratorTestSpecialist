import json
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Load data from JS.Json
with open("JS.Json", encoding="utf-8") as f:
    data = json.load(f)

def get_categories(data):
    return sorted(set(item["ВГруппе"] for item in data))

def get_nomenclature(data, category):
    return [item["Номенклатура"] for item in data if item["ВГруппе"] == category]

def build_category_menu():
    categories = get_categories(data)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=cat, callback_data=f"cat_{cat}")]
            for cat in categories
        ]
    )
    return keyboard

def build_nomenclature_menu(category):
    nomenclatures = get_nomenclature(data, category)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=nom, callback_data=f"nom_{nom}")]
            for nom in nomenclatures
        ]
    )
    return keyboard