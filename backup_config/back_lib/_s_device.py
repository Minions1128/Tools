
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

class DevInfo(object):
    def __init__(self, state, ip, log):
        self._is_succ = state
        self.ip = ip
        self.log = log

    def set_hostname(self, hostname):
        self.hostname = hostname

    def show_run(self, cfg):
        self.config = cfg
