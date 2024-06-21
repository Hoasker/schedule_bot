import aiohttp
from bs4 import BeautifulSoup
import asyncio


async def get_values(div_id: str) -> list[tuple[str, str]] | None:
    url = "https://mtec.by/wp-admin/admin-ajax.php"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    }
    params = {
        "action": "getSearchParameters",
        "rtype": "stds",
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=params) as response:
            if response.status == 200:
                soup = BeautifulSoup(await response.text(), 'html.parser')
                div = soup.find('div', {'id': div_id})
                if div:
                    values = [(div['value'], div.text) for div in div.find_all('div', class_='select-body__value')]
                    return values
                else:
                    print(f"Div с id {div_id} не найден.")
                    return None
            else:
                print(f"Ошибка: {response.status}")
                return None


async def get_dates() -> list[str] | None:
    dates = await get_values('s-opt')
    if dates:
        return [date[1] for date in dates]


async def get_groups() -> list[str] | None:
    groups = await get_values('s-opt')
    if groups:
        return [group[1] for group in groups]



async def main():
    a = await get_groups()
    print(a)


if __name__ == "__main__":
    asyncio.run(main())