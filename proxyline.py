import asyncio

from aioproxyline import ProxyLine


async def get_balance(api_token: str) -> None:
    async with ProxyLine(api_token=api_token) as client:
        result = await client.get_balance()  # Balance(balance=0.0, partner_balance=0.0)


asyncio.run(get_balance(api_token='10S4hhFr2CARCBjyYIJMu2QmoLGuprebMFlAI3A6'))