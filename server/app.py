from fastapi import FastAPI
import platform
import subprocess
import uvicorn
import os

app = FastAPI()


def get_absolute_path(file_name):
    current_directory = os.getcwd()
    parent_directory = os.path.abspath(os.path.join(current_directory, ".."))
    absolute_path = os.path.join(parent_directory, file_name)
    return absolute_path


@app.post('/start_robot/{start_number: int}')
@app.post('/start_robot')
async def start_robot(start_number: int = 0) -> dict:
    if platform.system() == 'Darwin':
        subprocess.run(['python', 'robot/main.py', str(start_number)])
    elif platform.system() == 'Windows':
        subprocess.Popen(['start', 'cmd', '/c', 'python',
                         get_absolute_path("robot/main.py")], shell=True)
    elif platform.system() == 'Linux':
        subprocess.Popen(['x-terminal-emulator', '-e',
                         'python', get_absolute_path("robot/main.py")])

    return {'message': 'Robot started'}


if __name__ == '__main__':
    uvicorn.run(app)
