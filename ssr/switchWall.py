#! /bin/env python

import json
import sys
import base64
from os import path

# local setting
local_ip = "192.168.2.22"
local_port = 2080

obfs_param="www.microsoft.com"

# remote setting
# server : server_port : protocol : method : obfs : password
# "ha.us-west-6.walllink.io:15300:auth_aes128_md5:rc4-md5:http_simple:ZHpTcHo1"

# ssr: // d3d3Lmdvb2dsZS5jb206MTphdXRoX2NoYWluX2E6Y2hhY2hhMjA6dGxzMS4yX3RpY2tldF9hdXRoOlluSmxZV3QzWVd4cy8_b2Jmc3BhcmFtPSZwcm90b3BhcmFtPSZyZW1hcmtzPTVZbXA1TDJaNXJXQjZZZVA3N3lhT1RrdU56WWxJREV3TkM0NU5FZEMmZ3JvdXA9VjJGc2JFeHBibXNnZkNEbG9ydnBqNGc ssr: // d3d3Lmdvb2dsZS5jb206MTphdXRoX2NoYWluX2E6Y2hhY2hhMjA6dGxzMS4yX3RpY2tldF9hdXRoOlluSmxZV3QzWVd4cy8_b2Jmc3BhcmFtPSZwcm90b3BhcmFtPSZyZW1hcmtzPTZMLUg1cHlmNXBlMjZaZTA3N3lhTWpBeE9DMHhNaTB3TmlBeE5Eb3hNVG94T1EmZ3JvdXA9VjJGc2JFeHBibXNnZkNEbG9ydnBqNGc ssr: // aGEuY2EtZWFzdC0xLndhbGxsaW5rLmlvOjU4NzphdXRoX2FlczEyOF9tZDU6Y2hhY2hhMjAtaWV0Zjp0bHMxLjJfdGlja2V0X2Zhc3RhdXRoOmQyRnNiR3hwYm1zLz9vYmZzcGFyYW09WkRZM05ERXRNekU1Tnk1aGVuVnlaV1ZrWjJVdWJtVjAmcHJvdG9wYXJhbT1NekU1Tnpwa2VsTndlalUmcmVtYXJrcz00NENRNXF5SzZabVFJREhqZ0pIamdKRG1ySXJwaDQwZ01DNHg0NENSNVlxZzVvdV81YVNuNXAyeDZZT283N3lJNkpLWjU0bTU1WWlwNTRpLTc3eUpNU0F0SURVNE55RGxqWlhucTZfbGo2TSZncm91cD1WMkZzYkV4cGJtc2dmQ0Rsb3J2cGo0Z2dMU0RsalpYbnE2X2xqNk0 ssr: // aGEudXMtd2VzdC0yLndhbGxsaW5rLmlvOjU4NzphdXRoX2FlczEyOF9tZDU6Y2hhY2hhMjAtaWV0Zjp0bHMxLjJfdGlja2V0X2Zhc3RhdXRoOmQyRnNiR3hwYm1zLz9vYmZzcGFyYW09WkRZM05ERXRNekU1Tnk1aGVuVnlaV1ZrWjJVdWJtVjAmcHJvdG9wYXJhbT1NekU1Tnpwa2VsTndlalUmcmVtYXJrcz00NENRNXF5SzZabVFJREhqZ0pIamdKRG1ySXJwaDQwZ01DNDE0NENSNTc2TzVaeUw2S1dfNllPbzc3eUk1ck9pNTRtNTZKaXQ3N3lKTWlBdElEVTROeURsalpYbnE2X2xqNk0mZ3JvdXA9VjJGc2JFeHBibXNnZkNEbG9ydnBqNGdnTFNEbGpaWG5xNl9sajZN ssr: // aGEudXMtd2VzdC0xLndhbGxsaW5rLmlvOjU4NzphdXRoX2FlczEyOF9tZDU6Y2hhY2hhMjAtaWV0Zjp0bHMxLjJfdGlja2V0X2Zhc3RhdXRoOmQyRnNiR3hwYm1zLz9vYmZzcGFyYW09WkRZM05ERXRNekU1Tnk1aGVuVnlaV1ZrWjJVdWJtVjAmcHJvdG9wYXJhbT1NekU1Tnpwa2VsTndlalUmcmVtYXJrcz00NENRNXF5SzZabVFJREhqZ0pIamdKRG1ySXJwaDQwZ01DNDE0NENSNTc2TzVaeUw2S1dfNllPbzc3eUk1clNiNXAySjU2T3Y3N3lKTVNBdElEVTROeURsalpYbnE2X2xqNk0mZ3JvdXA9VjJGc2JFeHBibXNnZkNEbG9ydnBqNGdnTFNEbGpaWG5xNl9sajZN ssr: // aGEudXMtd2VzdC03LndhbGxsaW5rLmlvOjU4NzphdXRoX2FlczEyOF9tZDU6Y2hhY2hhMjAtaWV0Zjp0bHMxLjJfdGlja2V0X2Zhc3RhdXRoOmQyRnNiR3hwYm1zLz9vYmZzcGFyYW09WkRZM05ERXRNekU1Tnk1aGVuVnlaV1ZrWjJVdWJtVjAmcHJvdG9wYXJhbT1NekU1Tnpwa2VsTndlalUmcmVtYXJrcz00NENRNXF5SzZabVFJREhqZ0pIamdKRG1ySXJwaDQwZ01DNDE0NENSNTc2TzVaeUw2S1dfNllPbzc3eUk2SUdXNkkyMzZLV183N3lKTVNBdElEVTROeURsalpYbnE2X2xqNk0mZ3JvdXA9VjJGc2JFeHBibXNnZkNEbG9ydnBqNGdnTFNEbGpaWG5xNl9sajZN ssr: // aGEudXMtd2VzdC0zLndhbGxsaW5rLmlvOjU4NzphdXRoX2FlczEyOF9tZDU6Y2hhY2hhMjAtaWV0Zjp0bHMxLjJfdGlja2V0X2Zhc3RhdXRoOmQyRnNiR3hwYm1zLz9vYmZzcGFyYW09WkRZM05ERXRNekU1Tnk1aGVuVnlaV1ZrWjJVdWJtVjAmcHJvdG9wYXJhbT1NekU1Tnpwa2VsTndlalUmcmVtYXJrcz00NENRNXF5SzZabVFJREhqZ0pIamdKRG1ySXJwaDQwZ01DNDE0NENSNTc2TzVaeUw2S1dfNllPbzc3eUk2TEs3NVlpcDZKS1o3N3lKTXlBdElEVTROeURsalpYbnE2X2xqNk0mZ3JvdXA9VjJGc2JFeHBibXNnZkNEbG9ydnBqNGdnTFNEbGpaWG5xNl9sajZN ssr: // aGEudXMtd2VzdC02LndhbGxsaW5rLmlvOjU4NzphdXRoX2FlczEyOF9tZDU6Y2hhY2hhMjAtaWV0Zjp0bHMxLjJfdGlja2V0X2Zhc3RhdXRoOmQyRnNiR3hwYm1zLz9vYmZzcGFyYW09WkRZM05ERXRNekU1Tnk1aGVuVnlaV1ZrWjJVdWJtVjAmcHJvdG9wYXJhbT1NekU1Tnpwa2VsTndlalUmcmVtYXJrcz00NENRNXF5SzZabVFJREhqZ0pIamdKRG1ySXJwaDQwZ01DNDE0NENSNTc2TzVaeUw2S1dfNllPbzc3eUk2TEs3NVlpcDZKS1o3N3lKTmlBdElEVTROeURsalpYbnE2X2xqNk0mZ3JvdXA9VjJGc2JFeHBibXNnZkNEbG9ydnBqNGdnTFNEbGpaWG5xNl9sajZN ssr: // aGEuZXUtd2VzdC0xLndhbGxsaW5rLmlvOjU4NzphdXRoX2FlczEyOF9tZDU6Y2hhY2hhMjAtaWV0Zjp0bHMxLjJfdGlja2V0X2Zhc3RhdXRoOmQyRnNiR3hwYm1zLz9vYmZzcGFyYW09WkRZM05ERXRNekU1Tnk1aGVuVnlaV1ZrWjJVdWJtVjAmcHJvdG9wYXJhbT1NekU1Tnpwa2VsTndlalUmcmVtYXJrcz00NENRNXF5SzZabVFJREhqZ0pIamdKRG1ySXJwaDQwZ01DNDQ0NENSNXEyUTVyU3k2S1dfNllPbzc3eUk2STIzNkppdDc3eUpNU0F0SURVNE55RGxqWlhucTZfbGo2TSZncm91cD1WMkZzYkV4cGJtc2dmQ0Rsb3J2cGo0Z2dMU0RsalpYbnE2X2xqNk0 ssr: // aGEuYXBhYy1zb3V0aC0yLndhbGxsaW5rLmlvOjU4NzphdXRoX2FlczEyOF9tZDU6Y2hhY2hhMjAtaWV0Zjp0bHMxLjJfdGlja2V0X2Zhc3RhdXRoOmQyRnNiR3hwYm1zLz9vYmZzcGFyYW09WkRZM05ERXRNekU1Tnk1aGVuVnlaV1ZrWjJVdWJtVjAmcHJvdG9wYXJhbT1NekU1Tnpwa2VsTndlalUmcmVtYXJrcz00NENRNXF5SzZabVFJREhqZ0pIamdKRG1ySXJwaDQwZ01lT0FrZVM2bnVhMHN1V05sLW1EcU8tOGlPYVdzT1dLb09XZG9lLThpVElnTFNBMU9EY2c1WTJWNTZ1djVZLWomZ3JvdXA9VjJGc2JFeHBibXNnZkNEbG9ydnBqNGdnTFNEbGpaWG5xNl9sajZN ssr: // aGEucnUtY2VudHJhbC0xLndhbGxsaW5rLmlvOjU4NzphdXRoX2FlczEyOF9tZDU6Y2hhY2hhMjAtaWV0Zjp0bHMxLjJfdGlja2V0X2Zhc3RhdXRoOmQyRnNiR3hwYm1zLz9vYmZzcGFyYW09WkRZM05ERXRNekU1Tnk1aGVuVnlaV1ZrWjJVdWJtVjAmcHJvdG9wYXJhbT1NekU1Tnpwa2VsTndlalUmcmVtYXJrcz00NENRNXF5SzZabVFJREhqZ0pIamdKRG1ySXJwaDQwZ01lT0FrZVNfaE9lLWhlYVdyLVM0cmVtRHFPLThpT2FXc09pbHYtUzhyLVdJcWVTNm51LThpVEVnTFNBMU9EY2c1WTJWNTZ1djVZLWomZ3JvdXA9VjJGc2JFeHBibXNnZkNEbG9ydnBqNGdnTFNEbGpaWG5xNl9sajZN ssr: // aGEucnUtd2VzdC0xLndhbGxsaW5rLmlvOjU4NzphdXRoX2FlczEyOF9tZDU6Y2hhY2hhMjAtaWV0Zjp0bHMxLjJfdGlja2V0X2Zhc3RhdXRoOmQyRnNiR3hwYm1zLz9vYmZzcGFyYW09WkRZM05ERXRNekU1Tnk1aGVuVnlaV1ZrWjJVdWJtVjAmcHJvdG9wYXJhbT1NekU1Tnpwa2VsTndlalUmcmVtYXJrcz00NENRNXF5SzZabVFJREhqZ0pIamdKRG1ySXJwaDQwZ01lT0FrZVNfaE9lLWhlYVdyLWlsdi1tRHFPLThpT2lPcS1hV3ItZW5rZS04aVRFZ0lDMGdOVGczSU9XTmxlZXJyLVdQb3cmZ3JvdXA9VjJGc2JFeHBibXNnZkNEbG9ydnBqNGdnTFNEbGpaWG5xNl9sajZN ssr: // aGEucnUtd2VzdC0yLndhbGxsaW5rLmlvOjU4NzphdXRoX2FlczEyOF9tZDU6Y2hhY2hhMjAtaWV0Zjp0bHMxLjJfdGlja2V0X2Zhc3RhdXRoOmQyRnNiR3hwYm1zLz9vYmZzcGFyYW09WkRZM05ERXRNekU1Tnk1aGVuVnlaV1ZrWjJVdWJtVjAmcHJvdG9wYXJhbT1NekU1Tnpwa2VsTndlalUmcmVtYXJrcz00NENRNXF5SzZabVFJREhqZ0pIamdKRG1ySXJwaDQwZ01lT0FrZVNfaE9lLWhlYVdyLWlsdi1tRHFPLThpT2lPcS1hV3ItZW5rZS04aVRJZ0xTQTFPRGNnNVkyVjU2dXY1WS1qJmdyb3VwPVYyRnNiRXhwYm1zZ2ZDRGxvcnZwajRnZ0xTRGxqWlhucTZfbGo2TQ ssr: // aGEuanAtZWFzdC01LndhbGxsaW5rLmlvOjU4NzphdXRoX2FlczEyOF9tZDU6Y2hhY2hhMjAtaWV0Zjp0bHMxLjJfdGlja2V0X2Zhc3RhdXRoOmQyRnNiR3hwYm1zLz9vYmZzcGFyYW09WkRZM05ERXRNekU1Tnk1aGVuVnlaV1ZrWjJVdWJtVjAmcHJvdG9wYXJhbT1NekU1Tnpwa2VsTndlalUmcmVtYXJrcz00NENRNXF5SzZabVFJREhqZ0pIamdKRG1ySXJwaDQwZ01lT0FrZWFYcGVhY3JPUzRuT21EcU8tOGlPUzRuT1M2ck8tOGlUVWdMU0ExT0RjZzVZMlY1NnV2NVktaiZncm91cD1WMkZzYkV4cGJtc2dmQ0Rsb3J2cGo0Z2dMU0RsalpYbnE2X2xqNk0 ssr: // aGEuanAtZWFzdC0yLndhbGxsaW5rLmlvOjU4NzphdXRoX2FlczEyOF9tZDU6Y2hhY2hhMjAtaWV0Zjp0bHMxLjJfdGlja2V0X2Zhc3RhdXRoOmQyRnNiR3hwYm1zLz9vYmZzcGFyYW09WkRZM05ERXRNekU1Tnk1aGVuVnlaV1ZrWjJVdWJtVjAmcHJvdG9wYXJhbT1NekU1Tnpwa2VsTndlalUmcmVtYXJrcz00NENRNXF5SzZabVFJREhqZ0pIamdKRG1ySXJwaDQwZ01lT0FrZWFYcGVhY3JPYWRzZW1EcU8tOGlPYWRzZVM2ck8tOGlUSWdMU0ExT0RjZzVZMlY1NnV2NVktaiZncm91cD1WMkZzYkV4cGJtc2dmQ0Rsb3J2cGo0Z2dMU0RsalpYbnE2X2xqNk0 ssr: // aGEuanAtZWFzdC00LndhbGxsaW5rLmlvOjU4NzphdXRoX2FlczEyOF9tZDU6Y2hhY2hhMjAtaWV0Zjp0bHMxLjJfdGlja2V0X2Zhc3RhdXRoOmQyRnNiR3hwYm1zLz9vYmZzcGFyYW09WkRZM05ERXRNekU1Tnk1aGVuVnlaV1ZrWjJVdWJtVjAmcHJvdG9wYXJhbT1NekU1Tnpwa2VsTndlalUmcmVtYXJrcz00NENRNXF5SzZabVFJREhqZ0pIamdKRG1ySXJwaDQwZ01lT0FrZWFYcGVhY3JPYWRzZW1EcU8tOGlPYWRzZVM2ck8tOGlUUWdMU0ExT0RjZzVZMlY1NnV2NVktaiZncm91cD1WMkZzYkV4cGJtc2dmQ0Rsb3J2cGo0Z2dMU0RsalpYbnE2X2xqNk0 ssr: // aGEudXMtd2VzdC01LndhbGxsaW5rLmlvOjU4NzphdXRoX2FlczEyOF9tZDU6Y2hhY2hhMjAtaWV0Zjp0bHMxLjJfdGlja2V0X2Zhc3RhdXRoOmQyRnNiR3hwYm1zLz9vYmZzcGFyYW09WkRZM05ERXRNekU1Tnk1aGVuVnlaV1ZrWjJVdWJtVjAmcHJvdG9wYXJhbT1NekU1Tnpwa2VsTndlalUmcmVtYXJrcz00NENRNXF5SzZabVFJREhqZ0pIamdKRG1ySXJwaDQwZ01lT0FrZWUtanVXY2ktaWx2LW1EcU8tOGlPYTBtLWFkaWVlanItLThpVFVnTFNBMU9EY2c1WTJWNTZ1djVZLWomZ3JvdXA9VjJGc2JFeHBibXNnZkNEbG9ydnBqNGdnTFNEbGpaWG5xNl9sajZN ssr: // aGEuanAtZWFzdC0zLndhbGxsaW5rLmlvOjU4NzphdXRoX2FlczEyOF9tZDU6Y2hhY2hhMjAtaWV0Zjp0bHMxLjJfdGlja2V0X2Zhc3RhdXRoOmQyRnNiR3hwYm1zLz9vYmZzcGFyYW09WkRZM05ERXRNekU1Tnk1aGVuVnlaV1ZrWjJVdWJtVjAmcHJvdG9wYXJhbT1NekU1Tnpwa2VsTndlalUmcmVtYXJrcz00NENRNXF5SzZabVFJREhqZ0pIamdKRG1ySXJwaDQwZ011T0FrZWFYcGVhY3JPYWRzZW1EcU8tOGlPYWRzZVM2ck8tOGlUTWdMU0ExT0RjZzVZMlY1NnV2NVktaiZncm91cD1WMkZzYkV4cGJtc2dmQ0Rsb3J2cGo0Z2dMU0RsalpYbnE2X2xqNk0 ssr: // aGEudHctc291dGgtMS53YWxsbGluay5pbzo1ODc6YXV0aF9hZXMxMjhfbWQ1OmNoYWNoYTIwLWlldGY6dGxzMS4yX3RpY2tldF9mYXN0YXV0aDpkMkZzYkd4cGJtcy8_b2Jmc3BhcmFtPVpEWTNOREV0TXpFNU55NWhlblZ5WldWa1oyVXVibVYwJnByb3RvcGFyYW09TXpFNU56cGtlbE53ZWpVJnJlbWFya3M9NDRDUTVxeUs2Wm1RSURMamdKSGpnSkRtcklycGg0MGdPT09Ba2VTNm51YTBzdWFkc2VtRHFPLThpT21ybU9tYmhPLThpVEVnTFNBMU9EY2c1WTJWNTZ1djVZLWomZ3JvdXA9VjJGc2JFeHBibXNnZkNEbG9ydnBqNGdnTFNEbGpaWG5xNl9sajZN
# $("#ssr_json textarea").text()
# https://cp.walllink.net/user/node/18?ismu=587&relay_rule=0

remote_list = [
    {
        "server": "ha.eu-west-1.walllink.io",
        "local_address": "127.0.0.1",
        "local_port": 1080,
        "timeout": 300,
        "workers": 1,
        "server_port": 15300,
        "password": "dzSpz5",
        "method": "rc4-md5",
        "obfs": "http_simple",
        "obfs_param": "www.microsoft.com",
        "protocol": "auth_aes128_md5",
        "protocol_param": ""
    },
    {
        "server": "ha.jp-east-3.walllink.io",
        "timeout": 300,
        "workers": 1,
        "server_port": 15300,
        "password": "dzSpz5",
        "method": "rc4-md5",
        "obfs": "http_simple",
        "obfs_param": "www.microsoft.com",
        "protocol": "auth_aes128_md5",
        "protocol_param": ""
    },
    {
        "server": "ha.ca-east-1.walllink.io",
        "timeout": 300,
        "workers": 1,
        "server_port": 587,
        "password": "walllink",
        "method": "chacha20-ietf",
        "obfs": "tls1.2_ticket_fastauth",
        "obfs_param": "d6741-3197.azureedge.net",
        "protocol": "auth_aes128_md5",
        "protocol_param": "3197:dzSpz5"
    },
    {
        "server": "ha.eu-west-1.walllink.io",
        "timeout": 300,
        "workers": 1,
        "server_port": 587,
        "password": "walllink",
        "method": "chacha20-ietf",
        "obfs": "tls1.2_ticket_fastauth",
        "obfs_param": "d6741-3197.azureedge.net",
        "protocol": "auth_aes128_md5",
        "protocol_param": "3197:dzSpz5"
    }
]


work_dir = path.dirname(path.abspath(sys.argv[0]))
config_file = path.join(work_dir, "shadowsocks.json")

print(config_file)


def decode(stringin):
    stringin = stringin.strip()
    if(stringin and stringin[-1:] != '='):
        if (len(stringin) % 4):
            add_num = 4-(len(stringin)) % 4

            stringin += ('=' * add_num)

    # print(stringin)
    result = base64.urlsafe_b64decode(stringin).decode('utf-8')
    # print(result)
    return result


def update_info(remote_list):
    base64_file = path.join(work_dir, "WallLink", "decode_base64.txt")
    with open(base64_file, "r", encoding="utf-8") as fh:
        lines = fh.readlines()

    lines = [line.strip().strip('ssr://') for line in lines if line.strip()]
    lines = [decode(line) for line in lines]
    lines = [line for line in lines if not line.startswith("www.google.com")]

    ssr_list = [get_ssr_detail(raw_ssr) for raw_ssr in lines]
    # print(ssr_list)
    # nonlocal remote_list
    if len(ssr_list) >0:
        remote_list.clear()
        remote_list = remote_list.extend(ssr_list)


def get_ssr_detail(raw_ssr):
    server, paras = raw_ssr.split('/?')
    # server : server_port : protocol : method : obfs : password
    server, server_port, protocol, method, obfs, password = server.split(':')
    
    password = decode(password)

    paras = paras.replace("obfsparam", "obfs_param")
    paras = paras.replace("protoparam", "protocol_param")
    paras = {rst[:rst.index('=')]: decode(
        rst[rst.index('=')+1:]) for rst in paras.split('&')}

    ssr_info = {
        "server": server,
        "server_ipv6": "::",
        "server_port": server_port,
        "local_address": local_ip,
        "local_port": local_port,
        "password": password,
        "timeout": 300,
        "udp_timeout": 60,
        "method": method,
        "protocol": protocol,
        # "protocol_param": "",
        "obfs": obfs,
        # "obfs_param": "",
        "fast_open": False,
        "workers": 1
    }
    for key in paras.keys():
        ssr_info[key] = paras[key]

    return ssr_info


def get_new_ip_info():
    def set_fix_setting():
        new_ip_info['local_address'] = local_ip
        new_ip_info['local_port'] = local_port


    with open(config_file, 'r') as fd:
        in_config = json.load(fd)

    try:
        server = in_config['server']
        server_index = [index for index in range(len(remote_list)) if remote_list[index]['server'] == server]
        server_index = server_index[0] if server_index else -1
        server_index = (server_index + 1) % len(remote_list)

        print("index : {}".format(server_index))

    except Exception as ex:
        server_index = 0
        print("get_new_ip error: ", ex)

    new_ip_info = remote_list[server_index]
    set_fix_setting()

    return new_ip_info


def main():
    update_info(remote_list)
    out_config = get_new_ip_info()
    
    with open(config_file, 'w', encoding='utf8') as fd:
        json.dump(out_config, fd, indent=4, ensure_ascii=False)

    result_file = path.join(work_dir, "WallLink", "decode_ssr.txt")
    with open(result_file, 'w', encoding='utf8') as fd:
        json.dump(remote_list, fd, indent=4, ensure_ascii=False)
    print(json.dumps(out_config, indent=4, ensure_ascii=False))


main()
