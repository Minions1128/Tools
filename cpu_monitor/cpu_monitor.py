"""
from 0files\sw.txt backup running configurations to 
0files\ip.txt
"""

import ciscolib
import time

def _logging_():
	Password = "cisco"
	UserName = "cisco"
	Enable_PWD = ""
	ip = '1.1.1.1'

	if UserName != "":
		switch = ciscolib.Device( ip, Password, UserName, Enable_PWD )
	else:
		switch = ciscolib.Device( ip, Password, enable_password=Enable_PWD )
	try:
		switch.connect()
		switch.enable( Enable_PWD )
		print ( "Logged into %s successfully." % ip )
	except ciscolib.AuthenticationError as e:
		print ( "Couldn't connect to %s: %s" % ( ip, e.value ) )
		return
	except Exception as e:
		print ( "Couldn't connect to %s: %s$" % ( ip, str(e) ) )
		return
	
	_log_ = switch.cmd("sh proc cpu sort | ex 0.00")
	switch.disconnect()
	return _log_

def main():
	a = 0
	while True:
		s = time.strftime("%b-%d %H.%M.%S", time.localtime())
		file_name = "0files\\" + s + ".txt"
		f = open(file_name, 'w+')
		f.write(_logging_())
		f.close()
		time.sleep(30)
		if a > 3:
			break
		a += 1

if __name__ == "__main__":
	main()