@echo off
netsh winsock reset
echo 10���Ӻ��Զ�����
ping 127.0.0.1 -n 5 >nul
echo 5���Ӻ��Զ�����
ping 127.0.0.1 -n 5 >nul
echo �����У����Եȡ�����
shutdown -r -t 0