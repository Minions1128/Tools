import re

def is_ip(host):
    if not host or not type(host) in [str, unicode]:
        return False
    re_str = ur"^([1-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])(\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])){3}$"    
    ptn = re.compile(re_str, flags=re.S|re.I|re.M)
    return True if ptn.findall(host) else False

print is_ip("233.3.3.3")
print is_ip('1.1.1.1')
print is_ip('10.0.0.0')
print is_ip('a')
print is_ip('shen.zhejian.baidu.com')