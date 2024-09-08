import asyncio


async def run1():
    for i in range(10):
        yield f"haha-{i}"


async def run2():
    async for i in run1():
        print(i)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    loop.run_until_complete(run2())
