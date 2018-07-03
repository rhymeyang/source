#! /usr/bin/python

import base64
import re

result = []


def decode_ssr(ssrString, groupname='ABC'):
    decode_ssr = ''
    try:
        decode_ssr = base64.b64decode(ssrString)
        decode_ssr += '&group=' + groupname
        decode_ssr = 'ssr://' + base64.b64encode(decode_ssr)
    except Exception as e:
#         print("decode ssr error")
#         print(e)
        pass
    return decode_ssr

def decode_ss(ssString, groupname='ABC'):
    decode_ss = ''
    try:
        decode_ss = re.split(r'[:|@]', base64.b64decode(ssString))
        if len(decode_ss) == 4:
            decode_ss = decode_ss[2] + \
                     ':' + decode_ss[3] + \
                     ':origin:' + decode_ss[0] + ':plain:' + \
                     base64.b64encode(decode_ss[1]) + '/?obfsparam=&group=' + groupname
            decode_ss = 'ssr://' + base64.b64encode(decode_ss)
        else:
            decode_ss = ''
    except Exception as e:
#         print("decode ss error")
#         print(e)
        pass
    return decode_ss
        
with open('./ssr.md', 'r') as fd:
    lines = fd.readlines()
    

#     print(lines)
pieces = []

for line in lines:
    pieces += line.split(' ')

for piece in pieces:
    rst = piece.strip()
    decode_rst = ''
    
    if re.search('^ssr://', rst):
        rst = rst[len('ssr://'):]
#         print(rst)
        decode_rst = decode_ssr(rst)
#         print('ssr')
        
       
    elif re.search('^ss://', rst):
        rst = rst[len('ss://'):]
        decode_rst = decode_ss(rst)
#         print('ss')
        
    if decode_rst:
        result.append(decode_rst)
        
        
with open('groupSsr.md', 'w') as fd:
    fd.write('\r\n'.join(result))
