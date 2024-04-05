from fastapi import FastAPI
import platform
import subprocess
import uvicorn
import os
import psutil
import multiprocessing

app = FastAPI()


def find_pid_by_script_name(script_name):
    for proc in psutil.process_iter():
        try:
            if ("Python" in proc.name() or "python" in proc.name()) and script_name in proc.cmdline():
                return proc.pid
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return None


def kill_process_by_pid(pid):
    try:
        if platform.system() == 'Windows':
            os.system(f"taskkill /F /PID {pid}")
        elif platform.system() == 'Darwin':
            os.kill(pid, 9)
    except Exception as e:
        print(f"Failed to terminate process with PID {pid}: {e}")


def get_absolute_path(file_name):
    current_directory = os.getcwd()
    # parent_directory = os.path.abspath(os.path.join(current_directory, "."))
    absolute_path = os.path.join(current_directory, file_name)
    return absolute_path


def run_subprocess(start_number):
    if platform.system() == 'Windows':
        subprocess.run(['start cmd /c', 'python',
                        get_absolute_path("robot/main.py"), str(start_number)])
    elif platform.system() == 'Darwin':
        subprocess.run(['python', get_absolute_path(
            "robot/main.py"), str(start_number)])


@app.post('/start_robot/{start_number}')
@app.post('/start_robot')
async def start_robot(start_number: int = 0) -> dict:

    multiprocessing.Process(target=run_subprocess,
                            args=(start_number, )).start()
    return {'message': 'Robot started'}


@app.post('/stop_robot')
async def stop_robot():
    script_name = get_absolute_path("robot/main.py")
    pid = find_pid_by_script_name(script_name)
    if pid:
        kill_process_by_pid(pid)
        return {'message': 'Robot stopped'}

    return {'message': 'Robot NOT found'}


if __name__ == '__main__':
    uvicorn.run(app)
