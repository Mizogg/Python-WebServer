@Echo off
title webserver_bonus.py
Pushd "%~dp0"
:loop
python webserver_bonus.py
goto loop