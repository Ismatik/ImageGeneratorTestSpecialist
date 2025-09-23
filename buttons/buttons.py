import logging
from aiogram import Router, F, types, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import pandas as pd
from functions import isAdmin, isUser
from typing import Dict

logger = logging.getLogger(__name__)
router = Router()

ROLE_KEY = 'role'

@router.message(Command("start"))
async def start(message: Message):
    print(message.from_user)
    print(message.from_user.id)
    print(message.from_user.phone_number)
    contact_button = KeyboardButton(
        text="Share Contact",
        request_contact=True,
    )
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[contact_button]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    await message.answer("Welcome!", reply_markup=keyboard)
    
@router.message(F.contact)
async def receive_phone(message: Message):
    contact = message.contact
    phone_number = contact.phone_number
    user_id = message.from_user.id
    logger.info(f"PHONE NUMBER {phone_number} and ID {user_id} of the USER added.")
    kb = [
        [InlineKeyboardButton(text = "Admin Panel", callback_data = "admin_panel")],
        [InlineKeyboardButton(text = "User Panel", callback_data = "user_panel")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    role = None
    if isAdmin(phone=phone_number):
        await message.answer("Welcome back Admin!", reply_markup=keyboard)
        
    elif isUser(phone=phone_number):                                        
        await message.answer("Welcome back User!", reply_markup=keyboard)
    
    else:
        await message.answer("You are not authorized to use this bot.")
        return                                                                                                                                                                                                                                                                          


async def set_default_commands(bot: Bot):
    commands = [
        types.BotCommand(command="/start", description="Start the bot"),
        types.BotCommand(command="/add_user", description="Register user"),
    ]
    
    await bot.set_my_commands(commands)
    logger.info("Default commands set.")