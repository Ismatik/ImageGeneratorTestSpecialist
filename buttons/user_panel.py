# import logging

# from aiogram import F, Router
# from aiogram.types import CallbackQuery, Message
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import State, StatesGroup


# logger = logging.getLogger(__name__)
# router = Router()


# def build_user_menu() -> Message:
#     from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
#     return InlineKeyboardMarkup(
#         inline_keyboard=[
#             [InlineKeyboardButton(text="View Categories", callback_data="view_cat")],
#         ]
#     )

# async def handle_user_panel(message: Message) -> None:
#     """Respond to the user panel button tap."""
#     await message.answer(
#         "Welcome! You have access to view categories.",
#         reply_markup=build_user_menu(),
#     )


# -*- coding: utf-8 -*-
import io
import json
import re
from pathlib import Path

from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    CallbackQuery, Message, BufferedInputFile
)

from PIL import Image, ImageDraw, ImageFont, ImageOps

router = Router()

# ---------- DATA ----------
DATA_PATH = Path("JS.Json")
with open(DATA_PATH, encoding="utf-8") as f:
    data = json.load(f)

def get_categories(data):
    # unique sorted, ignore empty values
    cats = {str(item.get("ВГруппе", "")).strip() for item in data if item.get("ВГруппе")}
    return sorted(cats)

def get_nomenclature(data, category):
    return [
        str(item.get("Номенклатура", "")).strip()
        for item in data
        if str(item.get("ВГруппе", "")).strip() == str(category).strip()
    ]

def get_item_by_nomenclature(data, name):
    name_norm = str(name).strip().lower()
    for item in data:
        if str(item.get("Номенклатура", "")).strip().lower() == name_norm:
            return item
    return None


# ---------- RENDERING (PIL) ----------
def get_font(size: int):
    # Try good cross-platform fonts; fall back to default.
    for p in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    ]:
        try:
            return ImageFont.truetype(p, size=size)
        except Exception:
            continue
    return ImageFont.load_default()

def safe_hex_to_image(hex_str: str):
    """Decode hex string to PIL.Image or return None if not valid."""
    if not hex_str or not isinstance(hex_str, str):
        return None
    clean = re.sub(r"[^0-9A-Fa-f]", "", hex_str)
    if len(clean) < 8:
        return None
    if len(clean) % 2 == 1:
        clean = clean[:-1]
    try:
        raw = bytes.fromhex(clean)
        bio = io.BytesIO(raw)
        img = Image.open(bio)
        img.load()
        return img
    except Exception:
        return None

def render_product_card(item: dict, size=(1100, 650)) -> Image.Image:
    """
    Renders a neat card:
      - Title: 'Номенклатура'
      - Table with 'ЕдиницаИзмерения' and 'Цена' (TJS)
      - Optional product image decoded from 'ФайлКартинки'
    """
    W, H = size
    bg = Image.new("RGB", (W, H), (245, 245, 245))
    draw = ImageDraw.Draw(bg)

    # Container
    margin = 36
    pad = 28
    container = (margin, margin, W - margin, H - margin)
    draw.rounded_rectangle(container, radius=26, fill=(255, 255, 255))

    # Left image box (square)
    left = margin + pad
    top = margin + pad
    bottom = H - margin - pad
    img_side = bottom - top
    img_box = (left, top, left + img_side, bottom)

    # Product image (or placeholder)
    product_img = safe_hex_to_image(item.get("ФайлКартинки", ""))
    if product_img is None:
        product_img = Image.new("RGB", (800, 800), (232, 236, 240))
        d2 = ImageDraw.Draw(product_img)
        ph_font = get_font(42)
        text = "Нет\nкартинки"
        tw = max(ph_font.getlength(line) for line in text.splitlines())
        th = ph_font.size * len(text.splitlines()) + 10
        d2.multiline_text(((800 - tw) / 2, (800 - th) / 2), text, font=ph_font, fill=(120, 120, 120), align="center")

    product_img = ImageOps.contain(product_img, (img_side, img_side))

    # Rounded mask for the image
    mask = Image.new("L", product_img.size, 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.rounded_rectangle((0, 0, product_img.size[0], product_img.size[1]), 22, fill=255)
    px = img_box[0] + (img_side - product_img.size[0]) // 2
    py = img_box[1] + (img_side - product_img.size[1]) // 2
    bg.paste(product_img, (px, py), mask)

    # Right pane (texts)
    right_x1 = img_box[2] + pad
    right_x2 = W - margin - pad
    y = top

    # Title: Номенклатура
    title = str(item.get("Номенклатура", "")).strip() or "—"
    title_font = get_font(48)
    # Wrap to the width
    def wrap_lines(text: str, font, max_w):
        words = text.split()
        lines, cur = [], []
        for w in words:
            trial = " ".join(cur + [w])
            if font.getlength(trial) <= max_w or not cur:
                cur.append(w)
            else:
                lines.append(" ".join(cur)); cur = [w]
        if cur: lines.append(" ".join(cur))
        return lines

    lines = wrap_lines(title, title_font, right_x2 - right_x1)
    for line in lines[:3]:
        draw.text((right_x1, y), line, font=title_font, fill=(25, 25, 25))
        y += title_font.size + 6
    y += 6

    # Group chip (optional)
    grp = str(item.get("ВГруппе") or "").strip()
    if grp:
        chip_font = get_font(24)
        chip_txt = f"Группа: {grp}"
        chip_pad_x, chip_pad_y = 14, 8
        chip_w = int(chip_font.getlength(chip_txt)) + chip_pad_x * 2
        chip_h = chip_font.size + chip_pad_y * 2
        chip_box = (right_x1, y, right_x1 + chip_w, y + chip_h)
        draw.rounded_rectangle(chip_box, radius=16, fill=(240, 245, 255))
        draw.text((right_x1 + chip_pad_x, y + chip_pad_y), chip_txt, font=chip_font, fill=(40, 70, 120))
        y += chip_h + 20

    # Table: headers
    header_font = get_font(26)
    cell_font = get_font(28)

    # Box for the table
    t_left, t_right = right_x1, right_x2
    row_h = 56
    head_h = 48
    grid = (210, 210, 210)
    head_bg = (245, 249, 255)
    alt_bg = (253, 251, 247)

    # Column split: 50/50
    mid_x = t_left + (t_right - t_left) // 2

    # Header row
    draw.rectangle([t_left, y, t_right, y + head_h], fill=head_bg, outline=grid, width=2)
    draw.line([(mid_x, y), (mid_x, y + head_h)], fill=grid, width=2)
    draw.text((t_left + 12, y + 10), "Единица", font=header_font, fill=(40, 40, 40))
    draw.text((mid_x + 12, y + 10), "Цена (TJS)", font=header_font, fill=(40, 40, 40))
    y += head_h

    # One data row (kept as a table for future extensibility)
    unit = str(item.get("ЕдиницаИзмерения", "")).strip()
    price = item.get("Цена", "")
    try:
        price_str = f"{float(price):g}"
    except Exception:
        price_str = str(price)

    # Row background
    draw.rectangle([t_left, y, t_right, y + row_h], fill=alt_bg, outline=grid, width=1)
    draw.line([(mid_x, y), (mid_x, y + row_h)], fill=grid, width=1)

    draw.text((t_left + 12, y + 12), unit or "—", font=cell_font, fill=(0, 120, 80))
    # right-align the price within right cell
    price_txt = price_str
    p_w = cell_font.getlength(price_txt)
    draw.text((t_right - 12 - p_w, y + 12), price_txt, font=cell_font, fill=(160, 40, 20))
    y += row_h + 16

    # Small footer
    footer_font = get_font(20)
    draw.text((right_x1, H - 36 - footer_font.size), "Автогенерация из JSON • валюта: TJS",
              font=footer_font, fill=(125, 125, 125))

    return bg

# ---------- HANDLERS ----------

# ---------- KEYBOARDS ----------
def build_category_menu():
    categories = get_categories(data)
    # simple grid (one button per row)
    kb = [[InlineKeyboardButton(text=cat, callback_data=f"cat_{cat}")]
          for cat in categories]
    return InlineKeyboardMarkup(inline_keyboard=kb)

def build_nomenclature_menu(category: str):
    noms = get_nomenclature(data, category)
    # keep callback_data short if names are long (64 char limit):
    # here we keep your original style; if you hit the limit, map
    # to indexes instead.
    kb = [[InlineKeyboardButton(text=nom, callback_data=f"nom_{nom}")]
          for nom in noms]
    return InlineKeyboardMarkup(inline_keyboard=kb)

# @router.message(CommandStart() | Command("start"))
async def handle_user_panel(msg: Message):
    await msg.answer("Выберите группу:", reply_markup=build_category_menu())

@router.callback_query(F.data.startswith("cat_"))
async def on_category(cb: CallbackQuery):
    category = cb.data[len("cat_"):]
    await cb.message.edit_text(f"Группа: {category}\nВыберите номенклатуру:",
                               reply_markup=build_nomenclature_menu(category))
    await cb.answer()

@router.callback_query(F.data.startswith("nom_"))
async def on_nomenclature(cb: CallbackQuery):
    nom = cb.data[len("nom_"):]
    item = get_item_by_nomenclature(data, nom)
    if not item:
        await cb.answer("Товар не найден.", show_alert=True)
        return

    # Render card and send as photo (no temp files needed)
    img = render_product_card(item)
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    bio.seek(0)
    await cb.message.answer_photo(
        BufferedInputFile(bio.getvalue(), filename=f"{nom}.png"),
        caption=f"{nom}"
    )
    await cb.answer()
