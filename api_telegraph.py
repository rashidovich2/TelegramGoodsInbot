import asyncio

from aiograph import Telegraph

loop = asyncio.get_event_loop()
telegraph = Telegraph()


async def main():
    await telegraph.create_account('aiograph-demo0009')
    page = await telegraph.create_page('Demo07', '<p><strong>Hello, world!</strong></p>')
    print('Created page:', page.url)


if __name__ == '__main__':
    try:
        loop.run_until_complete(main())
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        loop.run_until_complete(telegraph.close())  # Close the aiohttp.ClientSession