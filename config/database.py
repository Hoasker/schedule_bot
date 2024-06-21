import aiosqlite
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz

from config.config import config
from posts.post import send_schedule


timezone = pytz.timezone(config.time_zone)


async def initialize_db() -> None:
    async with aiosqlite.connect(config.db) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS schedule (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_id INTEGER,
                group_name TEXT DEFAULT NULL,
                schedule_time TEXT DEFAULT NULL
            )
        ''')
        await db.commit()


async def check_id(group_id: int) -> bool:
    async with aiosqlite.connect(config.db) as db:
        cursor = await db.execute('SELECT * FROM schedule WHERE group_id=?', (group_id,))
        row = await cursor.fetchone()
        if row:
            return True
        return False


async def save_chat_id(group_id: int) -> None:
    async with aiosqlite.connect(config.db) as db:
        await db.execute('''
            INSERT OR REPLACE INTO schedule (group_id)
            VALUES (?)
        ''', (group_id,))
        await db.commit()


async def save_group(group_id: int, group_name: str) -> None:
    async with aiosqlite.connect(config.db) as db:
        await db.execute('''UPDATE schedule SET group_name=? WHERE group_id=?''', (group_name, group_id))
        await db.commit()


async def save_schedule(group_id: int, schedule_time: str) -> None:
    async with aiosqlite.connect(config.db) as db:
        await db.execute('''
            UPDATE schedule SET schedule_time=? WHERE group_id=?)''', 
            (schedule_time, group_id))
        await db.commit()


async def save_schedule_time(group_id: int, schedule_time: str) -> None:
    async with aiosqlite.connect(config.db) as db:
        await db.execute('''
            UPDATE schedule SET schedule_time = ? WHERE group_id = ?
        ''', (schedule_time, group_id))
        await db.commit()


async def setup_scheduler(bot):
    scheduler = AsyncIOScheduler(timezone=timezone)
    async with aiosqlite.connect(config.db) as db:
        async with db.execute('SELECT group_id, group_name, schedule_time FROM schedule') as cursor:
            schedules = await cursor.fetchall()

    for group_id, group_name, schedule_time in schedules:
        hour, minute = map(int, schedule_time.split(':'))
        
        scheduler.add_job(
            send_schedule,
            trigger=CronTrigger(hour=hour, minute=minute),
            args=[bot, group_id, group_name],
            id=f"schedule_{group_id}"
        )

    scheduler.start()
    return scheduler


async def main():
    await initialize_db()


if __name__ == "__main__":
    asyncio.run(main())
