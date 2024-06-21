from datetime import datetime, timedelta
from utils.schedules import get_schedule


async def send_schedule(bot, chat_id: int, group_name: str):
    # Получаем дату на завтра
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%d.%m.%Y')
    
    # Получаем расписание
    schedule = await get_schedule(tomorrow, group_name)
    
    if schedule:
        message = f"Расписание на {tomorrow} для группы {group_name}:\n\n"
        for time, lessons in schedule.items():
            message += f"{time}:\n"
            for lesson in lessons:
                message += f"  {lesson['subject']} ({lesson['room']})\n"
            message += "\n"
        
        await bot.send_message(chat_id, message)    
    else:
        await bot.send_message(chat_id, f"Не удалось получить расписание на {tomorrow} для группы {group_name}")

