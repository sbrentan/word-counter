docker build -t monitor monitor/
@set /a "p1=%1%"
@set /a "p2=%1%+10"
@set /a "p3=%1%+20"
@set /a "p4=%1%+30"
docker run -d -p 8080:80 -p %p1%:%p1% -p %p2%:%p2% -p %p3%:%p3% -p %p4%:%p4% -e EXP_PORT=%p1% -e ACCEPT_MODE=passive --name=monitor --network=word-counter-net -v %cd%\monitor:/monitor -v %cd%\master:/master monitor