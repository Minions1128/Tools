import time
import getpass
import telnetlib

from device import Device
from errors import AuthenticationError


class TDevice(Device):

    def __init__(self, *args, **kwargs):
        super(TDevice, self).__init__(*args, **kwargs)

    def t_connect(self, host=None, port=23, timeout=5):
        if host is None:
            host = self.host
            
        self._connection = telnetlib.Telnet(host, port, timeout)
        self.t_authenticate(timeout)
        self._get_hostname()
        
        self.cmd("term len 0")
        
        self.connected = True

    def t_authenticate(self, timeout=None):
        idx, match, text = self.expect(['sername:', 'assword:'], timeout)

        if match is None:
            raise AuthenticationError("Unable to get a username or password prompt when trying to authenticate.", text)
        elif match.group().count(b'assword:'):
            self.write(self.password + "\n")
            
            # Another password prompt means a bad password
            idx, match, text = self.expect(['assword', '>', '#'], timeout)
            if match.group() is not None and match.group().count(b'assword'):
                raise AuthenticationError("Incorrect login password")            
        elif match.group().count(b'sername') > 0:
            if self.username is None:
                raise AuthenticationError("A username is required but none is supplied.")
            else:
                self.write(self.username + "\n")
                idx, match, text = self.expect(['assword:'], timeout)
                
                if match is None:
                    raise AuthenticationError("Unexpected text when trying to enter password", text)
                elif match.group().count(b'assword'):
                    self.write(self.password + "\n")
                
                # Check for an valid login
                idx, match, text = self.expect(['#', '>', "Login invalid", "Authentication failed"], timeout-3)
                # idx, match, text = self.expect(['#', '>', "Login invalid", "Authentication failed"])

                if match is None:
                    idx_s, match_s, text_s = self.expect(['#', '>', "Login invalid", "Authentication failed"], 2*timeout)
                    if match_s is None:
                        raise AuthenticationError("Unexpected text post-login", text)
                elif b"invalid" in match.group() or b"failed" in match.group():
                    raise AuthenticationError("Unable to login. Your username or password are incorrect.")
        else:
            raise AuthenticationError("Unable to get a login prompt")


class User(object):
    """docstring for User"""
    def __init__(self, *args, **kwargs):
        super(User, self).__init__()
        self._name = kwargs.get('u', 'admin')
        self._password = kwargs.get('p', 'cisco')
        self._enable_pwd = kwargs.get('ep', 'cisco')
        self._timeout = kwargs.get('t', 5)

    def new_user(self):
        _u = raw_input("Please input your Username: [%s] " % self._username)
        if _u == '':
            print "The user is not changed."
            return
        self._name = _u
        self._password = getpass.getpass("Please input your password: ")
        self._enable_pwd = getpass.getpass("Please input your enable password: ")
        return


class FileSystem(object):
    """docstring for FileSystem"""
    def __init__(self, *args, **kwargs):
        super(FileSystem, self).__init__()
        self._ip_list_path = kwargs.get('ip_list', 'ip_list.txt')
        self._conf_path = None
        self._log_path = 'log\\_log' + time.strftime("_%m%d_%H%M_", time.localtime())

    def conf_path(self, hostname):
        self._conf_path = 'config\\' + hostname + '.cfg'
        return self._conf_path

    def create_log(self):
        self.f_log = open(self._log_path, 'w+')

    def note(self, content):
        content += '\n'
        self.f_log.write(content)
        print content

    def close_log(self):
        self.f_log.close()