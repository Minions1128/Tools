from b_cls import TDevice
from errors import AuthenticationError


def backup_conf(_user, file_system):
    total_count = 0
    succ_count = 0
    fail_count = 0
    fail_info = {}
    succ_ip = []

    file_system.create_log()    

    for ip in open(file_system._ip_list_path).readlines():

        total_count += 1
        ip = ip.strip()

        file_system.note("Device %s is the %s devices." % (ip, total_count))

        if _user._name != "":
            switch = TDevice(ip, _user._password, _user._name, _user._enable_pwd)
        else:
            switch = TDevice(ip, _user._password, enable_password=_user._enable_pwd)
        try:
            switch.t_connect(timeout=_user._timeout)
            switch.enable(_user._enable_pwd)
            file_system.note("Logged into %s successfully." % ip)
        except AuthenticationError as e:
            file_system.note("Couldn't connect to %s: %s" % (ip, e.value))
            fail_count += 1
            fail_info.setdefault(e.value, [])
            fail_info[e.value].append(ip)
            continue
        except Exception as e:
            file_system.note("Couldn't connect to %s: %s$" % (ip, str(e)))
            fail_count += 1
            fail_info.setdefault(str(e), [])
            fail_info[str(e)].append(ip)
            continue
        
        backup_file_path = file_system.conf_path(switch.hostname)
        f_bak_conf = open(backup_file_path, 'w+')
        f_bak_conf.write(switch.cmd("sh run"))
        f_bak_conf.close()
        switch.disconnect()
        succ_count += 1
        succ_ip.append(ip)
        file_system.note(ip + ' backup success')

    temp_log = ('\n\n==================================================\n' +
        '==================================================\n' +
        'SUB TOTAL'.center(50) +
        '\n==================================================' +
        '\n==================================================')
    file_system.note(temp_log)

    file_system.note('TOTAL BACKUP %s' % str(total_count))
    file_system.note('SUCCESS BACKUP ' + str(succ_count))
    file_system.note('FAIL BACKUP ' + str(fail_count))

    temp_log = ('\n' +
        '--------------------------------------------------\n' +
        'SUCCESS IP ADDRESS'.center(50) +
        '\n--------------------------------------------------\n')
    file_system.note(temp_log)

    for _ip in succ_ip:
        file_system.note(str(_ip))

    temp_log = ('\n' +
        '--------------------------------------------------\n' +
        'FAIL DETAILS'.center(50) +
        '\n--------------------------------------------------\n')
    file_system.note(temp_log)
    file_system.note(str(fail_info))

    for _err in fail_info:
        file_system.note('====================')
        file_system.note(_err)
        file_system.note('--------------------')
        for err_ip in fail_info[_err]:
            file_system.note(err_ip)

    f_post_login = open('post-login.txt', 'w+')

    f_post_login.write('Change timeout to 10 or longer.....\n' +
        'Change the file name into post-login.txt')

    fail_info.setdefault('Unexpected text post-login', [])


    for i in fail_info['Unexpected text post-login']:
        f_post_login.write('\n'+i)

    file_system.close_log()