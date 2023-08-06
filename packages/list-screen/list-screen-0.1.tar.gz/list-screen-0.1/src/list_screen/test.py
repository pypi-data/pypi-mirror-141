from main import Screen
import asyncio

money = 20
screen = Screen(["This is a title", str(money), "", "", "Test"])


async def money_loop():
    global money
    while True:
        await asyncio.sleep(0.00001)
        money *= 1.1
        screen.change(money, 1)


async def main():
    asyncio.create_task(screen.start())
    asyncio.create_task(money_loop())
    while True:
        text = await screen.input(append=False)
        screen.insert([f"ok got a value {text}", 'um'], 2)


asyncio.run(main())
