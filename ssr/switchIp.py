#! /bin/env python

import json
import sys
from os import path


ip_list = ["64.137.246.61", 
           "64.137.251.141", 
           "45.62.249.213", 
           "64.137.228.35"]

work_dir = path.dirname(path.abspath(sys.argv[0]))
config_file = path.join(work_dir, "shadowsocks.json")

with open(config_file, 'r') as fd:
    in_config = json.load(fd)
    
server_index = ip_list.index(in_config['server'])
server_index = (server_index + 1 )% len(ip_list)

in_config['server'] = ip_list[server_index]

with open(config_file, 'w') as fd:
    json.dump(in_config, fd, indent = 4)
