import sys
import asyncio


async def run_robot(n: int) -> None:
    while True:
        print(n)
        n += 1
        await asyncio.sleep(1)


async def main():
    async with asyncio.TaskGroup() as tg:
        tg.create_task(run_robot(int(sys.argv[1])))


if __name__ == "__main__":
    print('[INFO] Robot started from', sys.argv[1])
    asyncio.run(main())
