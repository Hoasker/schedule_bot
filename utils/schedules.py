import aiohttp
from bs4 import BeautifulSoup
import asyncio

async def get_schedule(date: str, group_name: str) -> dict | None:
    url = "https://mtec.by/wp-admin/admin-ajax.php"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, как Gecko) Chrome/126.0.0.0 Safari/537.36"
    }
    params = {
        "action": "sendSchedule",
        "date": date,
        "value": group_name,
        "rtype": "stds"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=params) as response:
            if response.status == 200:
                text = await response.text()
                soup = BeautifulSoup(text, 'html.parser')
                schedule = {}
                
                for table in soup.find_all('table'):
                    for row in table.find_all('tr'):
                        cols = row.find_all('td')
                        if len(cols) == 3:
                            time = cols[0].text.strip()
                            time = ' '.join(time.split()) 
                            subject = cols[1].text.strip()
                            subject = ' '.join(subject.split())  
                            room = cols[2].text.strip()
                            room = ' '.join(room.split())
                            if time not in schedule:
                                schedule[time] = []
                            schedule[time].append({'subject': subject, 'room': room})
                
                return schedule
            else:
                print(f"Ошибка: {response.status}")
                return None


async def main():
    date = "21.06.2024"
    group_name = "Б201"
    schedule = await get_schedule(date, group_name)
    if schedule:
        for time, lessons in schedule.items():
            print(f"{time}:")
            for lesson in lessons:
                print(f"  {lesson['subject']} - {lesson['room']}")

if __name__ == "__main__":
    asyncio.run(main())
