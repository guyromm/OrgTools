#!/usr/bin/env python
import sys

#from https://github.com/guyromm/ScratchDocs/blob/journal/docs.py
def get_table_contents(fn):
    if type(fn)==str:
        fp = open(fn,'r') ; 
    else:
        fp = fn
    gothead=False
    def parseline(ln):
        return [f.strip() for f in ln.split('|') if f.strip()!='']
    rt=[]
    while True:
        ln = fp.readline()
        if not ln: break
        if '|' in ln and not gothead:
            headers = parseline(ln)
            gothead=True
            continue
        if ln.startswith('|-'): continue
        row = parseline(ln) 
        row = dict([(headers[i],row[i]) for i in xrange(len(row))])
        if (len(row)==0): continue
        rt.append(row)
        #only active ones:
    fp.close()
    return headers,rt

def join(f1,f2,outer=True,cartesian=False):
    h1,d1 = get_table_contents(f1)
    h2,d2 = get_table_contents(f2)

    commonkey = [k for k in h1 if k in h2]
    assert len(commonkey),"did not find a key to join by"
    destheader = list(set(h1+h2))
    destheader.sort(lambda k1,k2: cmp((h1+h2).index(k1),(h1+h2).index(k2)))
    out=[]
    
    for sr in d1:
        srk = '::'.join([sr[k] for k in commonkey])
        found = False
        for dr in d2:
            try:
                drk = '::'.join([dr[k] for k in commonkey])
            except:
                print 'cannot build a key out of %s'%dr
                raise
            if srk==drk:
                found = True
                out_row={}
                for k in destheader:
                    asgn = sr.get(k)
                    if not asgn: asgn = dr.get(k)
                    elif dr.get(k): assert asgn == dr.get(k)
                    out_row[k]=asgn
                out.append(out_row)
                if not cartesian:
                    #one is enough
                    break
        if not found and outer:
            out_row={}
            for k in destheader:
                asgn = sr.get(k)
                out_row[k]=asgn
            out.append(out_row)
    return destheader,out

def print_table(headers,data):
    print '|'+('|'.join(headers))+'|'
    print '|--'
    for d in data:
        rw='|'
        for h in headers:
            rw+=str(d.get(h,''))+'|'
        print rw
            
            
            

if __name__=='__main__':
    h,d=join(sys.argv[1],
             sys.argv[2],
             outer = ('outer' in sys.argv and True or False), 
             cartesian = ('cartesian' in sys.argv and True or False))
    print_table(h,d)
