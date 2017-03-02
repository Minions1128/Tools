import os
import sys
import time
import socket
import zipfile
import threading

from Queue import Queue

from back_lib.errors import AuthenticationError
from back_lib._s_device import TDevice
from back_lib._s_device import DevInfo
from back_lib.send_mail import SendEmail

sys.path.append('./gen-py')
# from backupdevinfo import BackupDevInfo 
# from backupdevinfo.ttypes import *

from _queue import _Queue
from _queue.ttypes import *

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

RECEIVER_LIST = ['zhejian@leju.com']


class BackupDevInfoHandler(object):

    def __init__(self, ip_list):
        super(BackupDevInfoHandler, self).__init__()
        self.ip_list = ip_list
        self.total_count = len(ip_list)
        self.fail_count = 0
        self.succ_count = 0
        self.logs = {}
        os.system('rm -rf ./_config/*')
        os.system('mkdir ./_config/temp')

    def _login(self, username, password):
        self.username = username
        self.password = password

    def get_all_dev_info(self):
        for ip in self.ip_list:
            self.logs.setdefault(ip, {})
            info = {'ip':ip}
            if self._is_ip_addr(ip):
                dev_info = self.get_one_dev_config(ip)
                if dev_info._is_succ:
                    self.succ_count += 1
                    path = './_config/temp/' + dev_info.hostname \
                        + '.' + ip + '.cfg'
                    with open(path, 'w+') as f_cfg:
                        f_cfg.write(dev_info.config)
                else:
                    self.fail_count += 1
                    succ_flg = False
                info['log'] = dev_info.log
                info['status'] = dev_info._is_succ
            else:
                self.fail_count += 1
                info['log'] = ip, 'is bad ip address'
                info['status'] = False
            self.logs[ip] = info
        summary_info = {
            'total_count':self.total_count,
            'fail_count':self.fail_count,
            'succ_count':self.succ_count
        }
        summary = self.get_total_info(summary_info, self.logs)
        log_path = './_config/temp/_log'
        with open(log_path, 'w+') as f_log:
            f_log.write(summary)

    def get_one_dev_config(self, ip):
        """ get one device configuration.
            return the 'show run' result
            arguments:
            ip: the ip address of this device
            username & password: 
                the username and password can
                telnet to the device."""
        device = TDevice(ip, self.password,
                self.username)

        try:
            device.t_connect()  #arg: timeout=10
            _s_log = "Logged into {} successfully".format(
                device.hostname)
            _is_succ = True
        except AuthenticationError as e:
            _s_log =  "Couldn't connect to {}: {}".format(
                ip, e.value)
            _is_succ = False
        except Exception as e:
            _s_log = "Couldn't connect to {}: {}.".format(
                ip, str(e))
            _is_succ = False
        except:
            _s_log = "Couldn't connect to {}.".format(ip)
            _is_succ = False
        dev_info = DevInfo(_is_succ, ip, _s_log)
        if _is_succ:
            dev_info.set_hostname(device.hostname)
            cfg = device.cmd('show run')
            dev_info.show_run(cfg)
        return dev_info

    @staticmethod
    def _is_ip_addr(ip):
        addr = ip.strip().split(".")
        if len(addr) != 4:
            return False
        for part in addr:
            try:
                part = int(part)
            except:
                return False
            if part > 255 or part < 0:
                return False
        return True

    def get_total_info(self, total_info, details):
        summary = time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())
        summary += '\n\n================================================='
        summary += '\n================= SUMMARY START ================='
        summary += '\n================================================='
        summary += '\n\nTotal: {}, Successful: {}, Fail: {}.'.format(
            total_info['total_count'], total_info['succ_count'],
            total_info['fail_count'])

        summary += '\n\n-------------- SUCCESSFUL --------------\n\n'
        l_succ = []
        for ip in details:
            if details[ip]['status'] == True:
                l_succ.append(ip)
        summary += str(l_succ)

        summary += '\n\n----------------- FAIL -----------------\n\n'
        l_fail = []
        for ip in details:
            if details[ip]['status'] == False:
                l_fail.append(ip)
                summary = summary + str(details[ip]['log']) + '\n'
        summary += '\n\n'
        summary += str(l_fail)
        summary += '\n\n================================================='
        summary += '\n================== SUMMARY END =================='
        summary += '\n=================================================\n'
        return summary

    def add_dirfile(self):
        path = './_config/net_dev_config.zip'
        f = zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED)
        startdir = "./_config/temp"
        for dirpath, dirnames, filenames in os.walk(startdir):
            for filename in filenames:
                cmd = 'cp ' + os.path.join(dirpath,filename) \
                    + ' ./' + filename
                os.system(cmd)
                f.write('./'+filename)
                cmd = 'rm -rf ./' + filename
                os.system(cmd)
        f.close()

    def send_mail(self, receiver_list):
        SendEmail(receivers_list=receiver_list)

    def _close(self):
        os.system('rm -rf ./_config/*')


class _QueueHandler(object):
    def __init__(self):
        self._q = Queue()

    def put_queue(self, u, p, ips, r_s):
        self._q.put((u, p, ips, r_s))
        return 'yes'

    def get_queue(self):
        return self._q.get()


if __name__ == '__main__':
    # handler = BackupDevInfoHandler(ip_list)
    handler = _QueueHandler()

    # processor = BackupDevInfo.Processor(handler)
    processor = _Queue.Processor(handler)
    transport = TSocket.TServerSocket("localhost", 23456)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    server = TServer.TSimpleServer(processor, transport, tfactory, pfactory) 
    print "Starting back_up in python..."

    new_thread = threading.Thread(target=server.serve)
    new_thread.start()

    while True:
        u, p, ips, r_s = handler.get_queue()
        _proc = BackupDevInfoHandler(ips)
        _proc._login(u, p)
        print 'login succ'
        _proc.get_all_dev_info()
        print 'get all dev info'
        _proc.add_dirfile()
        print 'packet zipped'
        _proc.send_mail(r_s)
        print 'send mail'
        _proc._close()
        print 'close...'


    print "done!"
