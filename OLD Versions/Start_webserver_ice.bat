@Echo off
title webserver_ice.py
Pushd "%~dp0"
:loop
python webserver_ice.py
goto loop