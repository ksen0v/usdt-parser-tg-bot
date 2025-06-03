from datetime import datetime, timezone
import aiohttp
async def convert_utc_time(unix_time):
    return datetime.fromtimestamp(unix_time, timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

async def convert_usdt_value(usdt_value, token_decimals = 6):
    return usdt_value / (10 ** token_decimals)

async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()