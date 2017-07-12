import re

def is_mac(mac):
    if not mac or type(mac) not in [str, unicode]:
        return False
    re_str = ur'^([\da-f]{4})(\.([\da-f]){4}){2}$|^([\da-f]{2})([-.:]([\da-f]){2}){5}$'                      
    ptn = re.compile(re_str, re.I)
    return True if ptn.findall(mac) else False

print is_mac('AAaa.dddd.1111')
print is_mac('4G-F0-2F-5C-08-A3')
print is_mac('40-F0-2F-5C-08-A3')
print is_mac('aa:33:dd:ff:DD:22')
print is_mac('AA.aa.dd.dd.11.11')
