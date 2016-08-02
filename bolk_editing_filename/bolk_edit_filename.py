
import os

def main():
	count = 1
	flag_once = True

	for v in os.listdir("./"):
		print v
		flag = raw_input("the file wanna change its file name? (press any key YES, except n or N)\n")
		if flag in ['n', 'N']:
			continue
		else:
			if flag_once:
				name_template = raw_input("input name template, stand for number with\'$$$\'\n")
				flag_once = False
				try:
					a, b = name_template.split("$$$", 2)
				except:
					print "$$$ is not exist in name template\n"
					return
		new_name = a + str(count) + b
		print "if replace \"%s\" with \"%s\" ?" % (v, new_name)
		flag = raw_input("Y(es) or N(o)\n")
		cmd = "cmd.exe /k ren \"" + v + "\" \"" + new_name + "\""
		#print cmd
		if flag in ['y', 'Y']:
			os.popen(cmd).read()
		count += 1


if __name__ == '__main__':
	global name_template
	global count
	global flag_once
	main()