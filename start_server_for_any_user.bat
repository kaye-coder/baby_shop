@echo off
cd %USERPROFILE%\PycharmProjects\baby\baby_shop
call %USERPROFILE%\PycharmProjects\baby\env\Scripts\activate.bat
python manage.py makemigrations
python manage.py migrate
start /B python manage.py runserver
timeout /t 3 /nobreak >nul
start http://127.0.0.1:8000
exit
