from fastapi import FastAPI, HTTPException
import platform
import subprocess
import uvicorn
import os
from multiprocessing.managers import BaseManager
import multiprocessing

app = FastAPI()
max_concurrent_processes = 1  # Limit count crocesses
semaphore = multiprocessing.Semaphore(max_concurrent_processes)


def get_absolute_path(file_name):
    """Get path to robot exec file"""
    current_directory = os.getcwd()
    parent_path = os.path.abspath(os.path.join(current_directory, os.pardir))
    absolute_path = os.path.join(parent_path, file_name)
    return absolute_path


def run_robot_in_new_process(semathore, start_number):
    """This method should be called from new process"""
    with semathore:
        if platform.system() == 'Windows':
            subprocess.call(r'start /wait python {} {}'.format(
                get_absolute_path(r"robot\main.py"), str(start_number)), shell=True)
        elif platform.system() == 'Darwin':
            # subprocess.call(['open', '-W', '-a', 'Terminal.app', 'python',
            # '--args', get_absolute_path("robot/main.py"), str(start_number)])
            subprocess.run(['python', get_absolute_path(
                "robot/main.py"), str(start_number)])


@app.post('/start_robot/{start_number}')
@app.post('/start_robot')
async def start_robot(start_number: int = 0) -> dict:
    # Start process with robot
    multiprocessing.Process(target=run_robot_in_new_process,
                            args=(semaphore, start_number, )).start()

    return {'message': 'Robot started'}


@app.post('/stop_robot')
async def stop_robot():
    BaseManager.register('kill_process')
    manager = BaseManager(address=('127.0.0.1', 4444), authkey=b'abc')
    try:
        manager.connect()
    except:
        raise HTTPException(
            status_code=404, detail="not found robots to stop")

    try:  # Raises ex to "recv" when robot stops byself
        manager.kill_process()
    except:
        pass
    return {'message': 'success stopped'}


if __name__ == '__main__':
    uvicorn.run(app)
