# Greenatom test assignment
This is an assignment for an apprenticeship at Grinatom. Need to write a robot that keeps a counter and a server that controls the robot. 

### Assignment details

- The program should work and run under Windows.
- Before you start, you need to initialize the git repository so see how the project progressed. 
- Need to write a web service backend on FastAPI that is able to start and stop the robot.
- The robot is a Python script that also needs to be written. It must run separately and independently (not inside a web service on FastAPI). Its job: to output numbers from 0 onwards to the console every second, adding one at a time until the script execution is interrupted. The robot should work asynchronously.
- The robot at startup must accept a command line parameter - from what number to start counting (by default - from zero). The web service on FastAPI should be able to pass this number.

**Additional** task (can be realized if you have enough time and energy):
- The program should store information about the time and duration of each run in a database (SQLite), as well as information about the date from which the countdown was started. FastAPI should have an additional endpoint to output this information.

### Project Description

To ***start*** the robot you need to use the following request: 
>`POST "/start_robot/"`
Description: the start value for start_number is automatically 0.

or 

>`POST "/start_robot/{start value}"`
Description: POST "/start_robot/13" will start from 13.

To ***stop*** robot:
>`POST "/stop_robot/"`

Any other queries will return ***errors***

**Attention:** If you try to start more robots than one, they will queue up and start working only when the process is finished. 
