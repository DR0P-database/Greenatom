import asyncio
import sys
import multiprocessing
from multiprocessing.managers import BaseManager
import os


def kill_process():
    try:
        print('[INFO] Server stopped with PID', os.getpid())
        os.kill(os.getpid(), 15)
    except Exception as e:
        print(f"Failed to terminate process with PID {os.getpid()}: {e}")


def run_socket():
    BaseManager.register('kill_process', callable=kill_process, )
    manager = BaseManager(address=('127.0.0.1', 4444), authkey=b'abc')
    print('[INFO] Server for connections started with PID',
          multiprocessing.current_process().pid)
    server = manager.get_server()
    server.serve_forever()


async def run_robot(n: int) -> None:
    while multiprocessing.active_children():  # Пока есть зависимые процессы(сервер)
        print(n)
        n += 1
        await asyncio.sleep(1)
    print('[INFO] Robot stopped with PID', os.getpid())


async def main():
    multiprocessing.Process(target=run_socket).start()
    async with asyncio.TaskGroup() as tg:
        print('[INFO] Robot started with PID', os.getpid())
        tg.create_task(run_robot(int(sys.argv[1])))


if __name__ == "__main__":
    asyncio.run(main())
