import re


def is_ip(host):
    if not host or not type(host) in [str, unicode]:
        return False
    re_str = ur"^([1-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])(\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])){3}$"    
    ptn = re.compile(re_str, flags=re.S|re.I|re.M)
    return True if ptn.findall(host) else False


def is_mask(host):
    if not host or not type(host) in [str, unicode]:
        return False
    re_str = ur"^(254|252|248|240|224|192|128|0)\.0\.0\.0|255\.(254|252|248|240|224|192|128|0)\.0\.0|255\.255\.(254|252|248|240|224|192|128|0)\.0|255\.255\.255\.(255|254|252|248|240|224|192|128|0)$"
    ptn = re.compile(re_str, flags=re.S|re.I|re.M)
    return True if ptn.findall(host) else False


def is_pre_len(pre_len):
    if not isinstance(pre_len, int):
        pre_len = int(pre_len)
    return False if (pre_len < 0 or pre_len > 32) else True


def pre_len_to_mask(pre_len):
    if not is_pre_len(pre_len):
        print '%Error: [{}] is bad pre_len'.format(pre_len)
        return '-1'
    pre_len = int(pre_len)
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
    if not is_mask(mask):
        print '%Error: [{}] is bad mask'.format(mask)
        return '-1'
    mask_l = mask.split('.')
    wildcard_l = []
    for m in mask_l:
        wildcard_l.append(str(int(''.join(
            ['0' if x == '1' else '1' for x in list(bin(int(m)).lstrip('0b').zfill(8))]), 2)))
    return '.'.join(wildcard_l)


def mask_to_pre_len(mask):
    if not is_mask(mask):
        print '%Error: [{}] is bad mask'.format(mask)
        return '-1'
    mask_l = mask.split('.')
    pre_len = 0
    for e in mask_l:
        for i in bin(int(e)).replace('0b', ''):
            if i == '0':
                return pre_len
            pre_len += 1
    else:
        return 32
    print '%Error: [{}] is bad mask'.format(mask)
    return '-1'


def calc_network_add(ip, mask=None, pre_len=None):
    if not is_ip(ip):
        print '%Error: [{}] is not an ip address.'.format(ip)
        return '-1'
    if pre_len != None and mask != None and \
            mask != pre_len_to_mask(pre_len):
        print '%Error: pre_len [{}] is not match mask [{}].'.format(pre_len, mask),
        return '-1'
    if pre_len != None:
        mask = pre_len_to_mask(pre_len)
    else:
        if not is_mask(mask):
            print '%Error [{}] is bad mask'.format(mask)
            return '-1'
        else:
            pre_len = mask_to_pre_len(mask)
    ip_l = ip.split('.')
    if mask != '-1':
        mask_l = mask.split('.')
    else:
        print '%Error [{}] is bad mask'.format(mask)
        return '-1'
    net_l = []
    for i in range(4):
        net_l.append(str(int(ip_l[i])&int(mask_l[i])))
    return '.'.join(net_l) + '/{}'.format(pre_len)


def calc_broadcast_add(ip, mask=None, pre_len=None):
    network_add = calc_network_add(ip, mask, pre_len)
    try:
        (net, pre_len) = network_add.split('/')
    except ValueError:
        print '%Error ip [{}], mask [{}] or pre_len [{}] may be bad info'.format(ip, mask, pre_len)
        return '-1'
    wildcard = mask_to_wildcard(pre_len_to_mask(int(pre_len)))
    wildcard_l = wildcard.split('.')
    net_l = net.split('.')
    broadcast_l = []
    for i in range(4):
        broadcast_l.append(str(int(net_l[i])|(int(wildcard_l[i]))))
    return '.'.join(broadcast_l) + '/{}'.format(pre_len)


ip = '172.29.3.1'
mask = '255.255.255.0'


print calc_network_add(ip=ip, pre_len=-1)
# print calc_broadcast_add(ip=ip, mask=mask)
