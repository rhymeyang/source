#! /bin/python2
# encoding: utf-8

import requests
from lxml import html
# from bs4 import BeautifulSoup
import os

rstfile = 'rst.md'

orgfile = os.readlink("/tmp/ssr/ssr.html")

def get_all_decode():
    with open(orgfile, 'r') as fd:
        content = fd.read()
    selector = html.fromstring(content)
    tds = selector.xpath("//tbody/tr/td/text()")

    while ('\n' in tds):
        tds.remove('\n')

    results = []
    for i in [0, 3, 6]:
        results.append(':'.join(tds[i:i+3]))
    for i in list(range(9, len(tds)))[::4]:
        results.append(':'.join([tds[i], tds[i+1], tds[i+3]]))

    results = [x.encode('utf-8') + os.linesep for x in results]
    with open(rstfile, 'a') as fd:
        fd.writelines(results)


get_all_decode()
