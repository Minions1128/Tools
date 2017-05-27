
import re
def is_ip(src):
    if not src or not type(src) in [str, unicode]:
        return False
    re_str = ur"^([1-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])(\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])){3}$"    
    ptn = re.compile(re_str, flags=re.S|re.I|re.M)    
    if ptn.findall(src):
        return True    
    return False


print is_ip("233.3.3.3")
