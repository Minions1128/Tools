"""
read the ip in the path _ip_list_path
copy the running configure of these devices to .\config\hostname.txt
"""


from back_lib.backup import backup_conf
from back_lib.b_cls import User
from back_lib.b_cls import FileSystem


_username = "admin"
_password = "cisco"
_enable_pwd = "cisco"

_timeout = 5
_ip_list_path = 'ip_list.txt'
_conf_path = 'config\\hostname.cfg'


def main():

    # _user = User(u=_username, p=_password, ep=_enable_pwd, t=_timeout)
    _user = User(t=_timeout)
    # _user.new_user()

    file_system = FileSystem(ip_list=_ip_list_path, conf_path=_conf_path)
    # file_system = FileSystem()

    backup_conf(_user, file_system)


if __name__ == "__main__":
    main()
