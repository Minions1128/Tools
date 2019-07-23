import time
import socket


def ping_port(host='127.0.0.1', port=22, n=10):
    succ_c, fail_c = 0, 0
    for i in range(n):
        time.sleep(0.5)
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sk.settimeout(3)
        try:
            sk.connect((host, port))
            print('{}:{} ok'.format(host, port))
            succ_c += 1
        except Exception:
            print('{}:{} error'.format(host, port))
            fail_c += 1.0
        sk.close()
    print('\n{} packets transmitted, {} successed, {}% packet loss'.format(n, succ_c, int(fail_c/n*100)))


ping_port('127.0.0.1', port=22, n=10)
