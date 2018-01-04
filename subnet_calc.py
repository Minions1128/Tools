import re


ip = '192.168.1.1'
mask = '255.248.0.0'


def is_ip(host):
    if not host or not type(host) in [str, unicode]:
        return False
    re_str = ur"^([1-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])(\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])){3}$"    
    ptn = re.compile(re_str, flags=re.S|re.I|re.M)
    return True if ptn.findall(host) else False


def pre_len_to_mask(pre_len):
    if not isinstance(pre_len, int) or \
            (pre_len <= 0 or pre_len > 32):
        print 'bad pre_len'
        return 'error'
    mask = 0
    while pre_len > 0:
        mask = mask | 1 << (32 - pre_len)
        pre_len -= 1
    a = (mask & 0xff000000) >> 24
    b = (mask & 0xff0000) >> 16
    c = (mask & 0xff00) >> 8
    d = mask & 0xff
    return '{}.{}.{}.{}'.format(a, b, c, d)


def mask_to_wildcard(mask):
    mask_l = mask.split('.')
    wildcard_l = []
    for m in mask_l:
        wildcard_l.append(str(int(''.join(
            ['0' if x == '1' else '1' for x in list(bin(int(m)).lstrip('0b').zfill(8))]), 2)))
    return '.'.join(wildcard_l)


def subnet_calc(ip, mask=-1, pre_len=-1):
    if not is_ip(ip):
        print 'this is not an ip address.'
        return 'error'
    if (mask == -1 and pre_len == -1) or \
            (mask != -1 and pre_len != -1):
        print 'legal mask or pre_len'
        return 'error'
    if mask == -1:
        mask = pre_len_to_mask(pre_len)
    ip_l = ip.split('.')
    mask_l = mask.split('.')
    wildcard = mask_to_wildcard(mask)
    wildcard_l = wildcard.split('.')
    net_l = []
    broadcast_l = []
    for i in range(4):
        net_l.append(str(int(ip_l[i])&int(mask_l[i])))
        broadcast_l.append(str(int(net_l[i])|(int(wildcard_l[i]))))
    print 'IP address\t\t\t{}'.format(ip)
    print 'Sub net mask\t\t{}'.format(mask)
    print 'Network number\t\t{}'.format('.'.join(net_l))
    print 'Broadcast address\t{}'.format('.'.join(broadcast_l))
    start_ip_l = net_l
    start_ip_l[-1] = str(int(net_l[-1]) + 1)
    end_ip_l = broadcast_l
    end_ip_l[-1] = str(int(broadcast_l[-1]) - 1)
    print 'Start host ip\t\t{}'.format('.'.join(start_ip_l))
    print 'End host ip\t\t\t{}'.format('.'.join(end_ip_l))

if __name__ == '__main__':
    subnet_calc(ip, mask=mask)
