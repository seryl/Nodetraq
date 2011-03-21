def str_to_mac(string):
    if string:
        string = string.replace(':', '')
        return '%s:%s:%s:%s:%s:%s' % (
                string[0:2], string[2:4], string[4:6],
                string [6:8], string[8:10], string[10:12])
    else:
        return None

def rbind(ip):
    address_list = ip.split('.')
    return '.'.join([
            address_list.pop(),
            address_list.pop(),
            address_list.pop()])

