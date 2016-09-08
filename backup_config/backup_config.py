"""
from 0files\sw.txt backup running configurations to 
0files\ip.txt
"""

import ciscolib
import time
# import getpass

def main():
    _password = "cisco"
    _username = "admin"
    _enable_pwd = ""

    # UserName = raw_input("Pleause input username:")
    # Password = getpass.getpass("Password:")

    total_count, suc_count, fail_count = 0, 0, 0
    fail_info = {}
    succ_ip = []
    _l_time = time.strftime("%y%m%d%H%M%S", time.localtime())

    f_log = open('0files\\'+_l_time+'_log_', 'w+')

    for ip in open('0files\\sw.txt').readlines():
        total_count += 1
        ip = ip.strip()
        f_log.write('\n'+ip)
        if _username != "":
            switch = ciscolib.Device(ip, _password, _username, _enable_pwd)
        else:
            switch = ciscolib.Device(ip, _password, enable_password=_enable_pwd)
        try:
            switch.connect()
            temp_log = "\nLogged into %s successfully." % ip
            f_log.write(temp_log)
            print temp_log

        except ciscolib.AuthenticationError as e:
            temp_log = "\nCouldn't connect to %s: %s" % (ip, e.value)
            print temp_log
            f_log.write(temp_log)
            fail_count += 1
            fail_info[ip] = temp_log
            continue
        except Exception as e:
            temp_log = "\nCouldn't connect to %s: %s$" % (ip, str(e))
            f_log.write(temp_log)
            print temp_log
            fail_count += 1
            fail_info[ip] = temp_log
            continue

        switch.enable(_enable_pwd)
        # print switch.cmd("sh run")
        backup_file_path = "0files\\" + _l_time + '_' + ip + ".txt"
        f_bak_conf = open(backup_file_path, 'w+')
        f_bak_conf.write(switch.cmd("sh run"))
        f_bak_conf.close()
        switch.disconnect()
        suc_count += 1
        succ_ip.append(ip)
        temp_log = '\n' + ip + ' backup success'
        f_log.write(temp_log)

    temp_log = ('\n\n\n' +
        '----------------------------------------------------\n' +
        '**********             SubTotal           **********\n' +
        '----------------------------------------------------')
    f_log.write(temp_log)
    print temp_log

    temp_log = '\nTOTAL BACKUP ' + str(total_count)
    f_log.write(temp_log)
    print temp_log

    temp_log = '\nSUCCESS BACKUP ' + str(suc_count)
    f_log.write(temp_log)
    print temp_log

    temp_log = '\n' + str(succ_ip)
    f_log.write(temp_log)
    print temp_log

    temp_log = '\nFAIL BACKUP ' + str(fail_count)
    f_log.write(temp_log)
    print temp_log

    temp_log = ('\n\n\n' +
        '----------------------------------------------------\n' +
        '**********          FAIL DETAILS          **********\n' +
        '----------------------------------------------------\n')
    f_log.write(temp_log)

    for i in fail_info:        
        f_log.write(str(i))
        f_log.write(str(fail_info[i]))
        f_log.write('\n----------\n')

    f_log.close()


if __name__ == "__main__":
    main()
