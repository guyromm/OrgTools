#!/usr/bin/env python

import sys
from join import get_table_contents,print_table

takeheaders = sys.argv[1:]
headers,data = get_table_contents(sys.stdin)
for h in takeheaders:
    assert h in headers,"%s not in %s"%(h,takeheaders)
    
for d in data:
    for k in d.keys():
        if k not in takeheaders:
            del d[k]
print_table(takeheaders,data)
