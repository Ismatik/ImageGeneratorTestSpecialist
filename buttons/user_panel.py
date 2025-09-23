import logging

from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


logger = logging.getLogger(__name__)
router = Router()

class UserStates(StatesGroup):
    pass

@router.callback_query(F.data == "user_panel")
async def handle_user_panel(callback: CallbackQuery) -> None:
    """Respond to the user panel button tap."""
    await callback.answer()
    await callback.message.answer(
        "User panel preview. Browse categories once 1C integration is ready."
    )
