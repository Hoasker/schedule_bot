import re
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from filters.chat_type import ChatTypeFilter
from keyboards.keyboards import get_keyboard
from utils.utils import get_groups
from config import states, database


router = Router()


@router.message(
        ChatTypeFilter(chat_type=["group", "supergroup"]),
        Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    groups = await get_groups()
    if groups:
        keyboard = get_keyboard(groups)
        await database.save_chat_id(message.chat.id)
        await message.answer("Выберите группу:", reply_markup=keyboard)
        await state.set_state(states.GroupSelection.waiting_group)
    else:
        await message.answer("Не удалось получить список групп. Попробуйте позже.")


@router.callback_query(lambda c: c.data.startswith('group_'), states.GroupSelection.waiting_group)
async def process_group_selection(callback: CallbackQuery, state: FSMContext):
    selected_group = callback.data.split('_')[1]
    chat_id = callback.message.chat.id
    
    await database.save_group(chat_id, selected_group)    
    await callback.message.edit_text(f"Группа '{selected_group}' выбрана и сохранена для этого чата.")
    await callback.message.answer("Теперь укажите время для автопостинга расписания в формате ЧЧ:ММ (например, 08:00)")
    
    await state.update_data(selected_group=selected_group)
    await state.set_state(states.GroupSelection.waiting_time)


@router.message(states.GroupSelection.waiting_time)
async def process_time_selection(message: Message, state: FSMContext):
    time = message.text
    
    if not re.match(r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$', time):
        await message.answer("Неверный формат времени. Пожалуйста, используйте формат ЧЧ:ММ (например, 08:00)")
        return

    data = await state.get_data()
    selected_group = data.get('selected_group')
    chat_id = message.chat.id

    await database.save_schedule_time(chat_id, time)

    await message.answer(f"Время автопостинга расписания для группы '{selected_group}' установлено на {time}.")
    await state.clear()