import sys
import time
import getpass

sys.path.append('./gen-py')

from _queue import _Queue

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

_user = 'admin'
_pwd = 'cisco'
received_ip_list = [
    '192.168.1.1',
    '10.0.0.1',
    'zhejian.com',
    '1.1.1.1',
    '172.31.1.1'
]
receiver_list = ['zhejian@example.com']


if __name__ == '__main__':
    try:
        _user = raw_input('Username: ')
        _pwd = getpass.getpass('Password: ')

        #testing start
        t = time.time()
        #testing end

        transport = TSocket.TSocket('localhost', 23456)
        transport = TTransport.TBufferedTransport(transport)
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        client = _Queue.Client(protocol)
        transport.open()

        print client.put_queue(_user, _pwd,
            received_ip_list, receiver_list)
    
        transport.close()
    
    except Thrift.TException, ex:
        print "%s" % (ex.message)

    #testing start
    print time.time() - t
    #testing end
