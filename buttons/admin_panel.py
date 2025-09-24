import logging
from pathlib import Path

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from buttons.view_categories import build_category_menu
import pandas as pd

USERS_PATH = Path("/home/ikki/Desktop/Koinot/ImageGeneratorTestSpecialist/users.xlsx")


logger = logging.getLogger(__name__)
router = Router()


class AdminPanelStates(StatesGroup):
    waiting_for_add_nickname = State()
    waiting_for_remove_nickname = State()
    waiting_for_cat_choose = State()


def build_admin_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Add user", callback_data="add_user"),
                InlineKeyboardButton(text="Remove user", callback_data="remove_user"),
            ],
            [InlineKeyboardButton(text="View Categories", callback_data="view_cat")],
        ]
    )


async def handle_admin_panel(message: Message) -> None:
    """Entry point for the admin panel button."""
    await message.answer(
        "Welcome Admin! Select options from the menu below or use commands.",
        reply_markup=build_admin_menu(),
    )


@router.callback_query(F.data == "add_user")
async def add_user(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await state.set_state(AdminPanelStates.waiting_for_add_nickname)
    await callback.message.answer("Send the user nickname to add him as User. (e.g. @example)")


@router.message(AdminPanelStates.waiting_for_add_nickname)
async def receive_add_nickname(message: Message, state: FSMContext) -> None:
    nickname = message.text.strip()
    if not nickname:
        await message.answer("I need a nickname. Try again.")
        return

    if add_nickname_to_registry(nickname):
        await message.answer(f"User '{nickname}' added successfully.")
    else:
        await message.answer(f"User '{nickname}' is already registered.")

    await state.clear()


@router.callback_query(F.data == "remove_user")
async def remove_user(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await state.set_state(AdminPanelStates.waiting_for_remove_nickname)
    await callback.message.answer("Send the nickname to remove. (e.g. @example)")


@router.message(AdminPanelStates.waiting_for_remove_nickname)
async def receive_remove_nickname(message: Message, state: FSMContext) -> None:
    nickname = message.text.strip()
    if not nickname:
        await message.answer("I need a nickname, not empty text.")
        return

    if remove_nickname_from_registry(nickname):
        await message.answer(f"User '{nickname}' removed successfully.")
        await state.clear()
        return
    else:
        await message.answer(f"User '{nickname}' was not found in the registry.")

@router.callback_query(F.data == "view_cat")
async def view_cats(callback: CallbackQuery, state:FSMContext) -> None:
    await callback.message.answer(
        "Select a category:",
        reply_markup=build_category_menu()
    )



def _load_registry() -> pd.DataFrame:
    try:
        df = pd.read_excel(USERS_PATH)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["User"])

    if "User" not in df.columns:
        # Normalize legacy files without headers.
        df.columns = ["User"] + [f"extra_{idx}" for idx in range(len(df.columns) - 1)]
        df = df[["User"]]

    df["User"] = df["User"].astype(str)
    return df

def add_nickname_to_registry(nickname: str) -> bool:
    df = _load_registry()
    normalized_nickname = nickname.strip()
    if normalized_nickname in df["User"].tolist():
        return False

    df.loc[len(df)] = {"User": normalized_nickname}
    df.to_excel(USERS_PATH, index=False)
    logger.info("User %s added to registry", normalized_nickname)
    return True

def remove_nickname_from_registry(nickname: str) -> bool:
    df = _load_registry()
    normalized_nickname = nickname.strip()
    mask = df["User"] == normalized_nickname
    if not mask.any():
        return False

    df = df.loc[~mask]
    df.to_excel(USERS_PATH, index=False)
    logger.info("User %s removed from registry", normalized_nickname)
    return True
