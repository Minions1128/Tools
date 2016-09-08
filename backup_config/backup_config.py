"""
v1.0
from 0files\sw.txt backup running configurations to 
0files\ip.txt
"""

import ciscolib
import getpass

def main():
	Password = "cisco"
	UserName = "admin"
	Enable_PWD = ""

	UserName = raw_input("Pleause input username:")
	Password = getpass.getpass("Password:")

	fail_device = []
	total_count = 0
	suc_count = 0
	fail_count = 0

	for ip in open('0files\\sw.txt').readlines():
		total_count += 1
		ip = ip.strip()
		if UserName != "":
			switch = ciscolib.Device( ip, Password, UserName, Enable_PWD )
		else:
			switch = ciscolib.Device( ip, Password, enable_password=Enable_PWD )
		try:
			switch.connect()
			print ( "Logged into %s successfully." % ip )

		except ciscolib.AuthenticationError as e:
			print ( "Couldn't connect to %s: %s" % ( ip, e.value ) )
			fail_device.append(ip)
			fail_count += 1
			continue
		except Exception as e:
			print ( "Couldn't connect to %s: %s$" % ( ip, str(e) ) )
			fail_device.append(ip)
			fail_count += 1
			continue

		switch.enable( Enable_PWD )
#		print switch.cmd( "sh run" )
		backup_file_path = "0files\\" + ip + ".txt"
		f = open( backup_file_path, 'w+' )
		f.write( switch.cmd( "sh run" ) )
		f.close()
		switch.disconnect()
		suc_count += 1
	print "ToTal: ", total_count
	print "Success: ", suc_count
	print "Fail: ", fail_count
	print fail_device
	raw_input("Press Enter to continue..")

if __name__ == "__main__":
	main()
