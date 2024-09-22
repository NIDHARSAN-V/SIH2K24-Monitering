@echo off

REM Run Python scripts
start "" python ..\eval.py
start "" python ..\gemini.py
start "" python ..\eval2.py
start "" python ..\res_an.py

REM Start Node.js server
nodemon server.js
