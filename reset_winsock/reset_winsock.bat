@echo off
netsh winsock reset
echo 10秒钟后自动重启
ping 127.0.0.1 -n 5 >nul
echo 5秒钟后自动重启
ping 127.0.0.1 -n 5 >nul
echo 重启中，请稍等。。。
shutdown -r -t 0