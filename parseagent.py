#!/usr/bin/env python
import sys
import httpagentparser
import re

def det(subj,what):
    if what==3:
        rt= subj.replace('http://','').replace('https://','')
        if 'noquery' in sys.argv: rt=rt.split('?')[0]
        if 'nopath' in sys.argv: rt=rt.split('/')[0]
        rt = rt.strip()
        return rt
    else:
        return httpagentparser.simple_detect(subj)[what]

def detect(what=1):
    for line in sys.stdin:
        if len(sys.argv)>1 and re.compile('^\d+$').search(sys.argv[1]):
            ln = line.split('|')
            try:
                s = ln[int(sys.argv[1])].strip()
            except IndexError:
                continue
            ln[int(sys.argv[1])]=det(s,what)
            ln = [e.strip() for e in ln]
            print '|'.join(ln)
        else:
            s = line
            print det(s,what)

if __name__=='__main__':
    detect()
