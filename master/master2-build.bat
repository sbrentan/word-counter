docker build -t %1 master/
@set /a "p1=%2%"
@set /a "p2=%2%+10"
@set /a "p3=%2%+20"
@set /a "p4=%2%+30"
docker run -d -p %p1%:%p1% -p %p2%:%p2% -p %p3%:%p3% -p %p4%:%p4% -e EXP_PORT=%p1% -e SELF_NAME=%1 -e MASTER_PORT=%3 --network=word-counter-net --name=%1 -v %cd%\node:/node -v %cd%\master:/master %1