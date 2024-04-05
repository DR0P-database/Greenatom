from fastapi import FastAPI
import platform
import subprocess
import uvicorn
import os
import multiprocessing

app = FastAPI()

robot_process = None


def get_absolute_path(file_name):
    current_directory = os.getcwd()
    # parent_directory = os.path.abspath(os.path.join(current_directory, "."))
    absolute_path = os.path.join(current_directory, file_name)
    return absolute_path


def run_robot_process(start_number):
    os.system(
        ' '.join(['start cmd /c', 'python',
                 get_absolute_path("robot/main.py"), start_number])
    )


@app.post('/start_robot/{start_number}')
@app.post('/start_robot')
async def start_robot(start_number: int = 0) -> dict:
    global robot_process
    p = multiprocessing.Process(
        target=run_robot_process, args=(str(start_number), ))
    robot_process = p
    p.start()
    return {'message': 'Robot started'}


@app.post('/stop_robot')
async def stop_robot():
    global robot_process
    robot_process.terminate()
    return {'message': 'Robot stopped'}

if __name__ == '__main__':
    uvicorn.run(app)
