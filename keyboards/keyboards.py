from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



def get_keyboard(groups: list[str], buttons_per_row: int = 2):
    buttons = []
    for i in range(0, len(groups), buttons_per_row):
        row = [InlineKeyboardButton(text=group, callback_data=f"group_{group}") for group in groups[i:i+buttons_per_row]]
        buttons.append(row)
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard