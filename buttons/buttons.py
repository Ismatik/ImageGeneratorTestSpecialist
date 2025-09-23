import logging
from aiogram import Router, F, types, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import pandas as pd


logger = logging.getLogger(__name__)
router = Router()

@router.message(Command("start"))
async def start(message: Message):
    


async def set_default_commands(bot: Bot):
    commands = [
        types.BotCommand(command="/start", description="Start the bot"),
        types.BotCommand(command="/add_user", description="Register user"),
    ]
    
    await bot.set_my_commands(commands)
    logger.info("Default commands set.")