import logging
from aiogram import Router, F, types, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import pandas as pd
from functions import isAdmin, is_registered_user
from pathlib import Path
from typing import Dict
from buttons.admin_panel import handle_admin_panel
from buttons.user_panel import handle_user_panel

logger = logging.getLogger(__name__)
router = Router()

@router.message(Command("start"))
async def start(message: Message):
    username = message.from_user.username
    # if isAdmin(message.from_user.id):
    #     await handle_admin_panel(message)
    #     return
    if not is_registered_user(username):
        return await message.answer("You are not registered to use this bot.")
    else:
        await handle_user_panel(message)
    return


async def set_default_commands(bot: Bot):
    commands = [
        types.BotCommand(command="/start", description="Start the bot"),
        types.BotCommand(command="/info", description="Register user"),
    ]
    
    await bot.set_my_commands(commands)
    logger.info("Default commands set.")