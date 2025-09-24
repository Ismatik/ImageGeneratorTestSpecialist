import logging

from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


logger = logging.getLogger(__name__)
router = Router()


def build_user_menu() -> Message:
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="View Categories", callback_data="view_cat")],
        ]
    )

async def handle_user_panel(message: Message) -> None:
    """Respond to the user panel button tap."""
    await message.answer(
        "Welcome! You have access to view categories.",
        reply_markup=build_user_menu(),
    )
