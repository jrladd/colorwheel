#!/usr/bin/env python

from bs4 import BeautifulSoup
import sys

input_file = sys.argv[1]

with open(input_file, 'r') as f:
    xml = f.read()
    soup = BeautifulSoup(xml, 'lxml')

for s in soup.find_all('l'):
    line = []
    for x in s.contents:
        if x.name == 'choice':
            line.append(x.find('reg').text)
        elif x.name == 'hi':
            line.append(x.text)
        elif x.name != 'span':
            line.append(x)
    print ''.join(line)

