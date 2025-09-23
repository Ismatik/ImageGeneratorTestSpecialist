import logging

from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


logger = logging.getLogger(__name__)
router = Router()

class AdminStates(StatesGroup):
    start_admin = State()
    

@router.callback_query(F.data == "admin_panel")
async def handle_admin_panel(callback: CallbackQuery) -> None:
    """Entry point for the admin panel button."""
    await callback.answer()
    
    await callback.message.answer(
        "Admin panel is under construction. Use upcoming commands to manage users."
    )
