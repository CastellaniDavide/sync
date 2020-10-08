@ECHO OFF
REM sync
	
REM change directory to the current (for the scheduled task)
CD /D "%~dp0"

REM Get init time
ECHO Start_time: "%date% %time%" >> ../log/trace.log

REM Call python code
python.exe ./sync.py --batch

REM Get end time
ECHO End_time: "%date% %time%" >> ../log/trace.log
ECHO. >> ../log/trace.log
