#! /bin/env python

import json
import sys
from os import path

remote_port = 3431
local_ip = "192.168.2.22"
local_port = 2080

ip_list = ["64.137.246.61",
           "64.137.251.141",
           "64.137.250.136",
           "64.137.228.35"]

use_ssr = False

work_dir = path.dirname(path.abspath(sys.argv[0]))
config_file = path.join(work_dir, "shadowsocks.json")

def get_setting(new_ip):
    ssr_config = {
        "server": new_ip,
        "server_ipv6": "::",
        "server_port": remote_port,
        "local_address": local_ip,
        "local_port": local_port,
        "password": "doub.io/sszhfx/*" + str(remote_port),
        "timeout": 300,
        "udp_timeout": 60,
        "method": "chacha20",
        "protocol": "auth_sha1_v4" if use_ssr else "origin",
        "protocol_param": "",
        "obfs": "tls1.2_ticket_auth" if use_ssr else "plain",
        "obfs_param": "",
        "fast_open": False,
        "workers": 1
    }

    return ssr_config

def get_new_ip():
    with open(config_file, 'r') as fd:
        in_config = json.load(fd)

    try:
        server_index = ip_list.index(in_config['server'])
        server_index = (server_index + 1) % len(ip_list)

    except Exception as ex:
        server_index = 0
        print("get_new_ip error: ", ex)

    return ip_list[server_index]


new_ip = get_new_ip()


out_config = get_setting(new_ip)


with open(config_file, 'w') as fd:
    json.dump(out_config, fd, indent=4)


