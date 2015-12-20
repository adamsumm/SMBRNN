from os import listdir
from os.path import isfile, join
import os

import sys
import re
pattern = re.compile('([\d\.]+)\.t7')
for path in sys.argv[1:]:    
    onlyfiles = [ f for f in listdir(path) if isfile(join(path,f)) ]
    minV = 99999999999;
    minFiles = []
    if len(onlyfiles) == 0:
        os.rmdir(path)
    for file in onlyfiles:
        m = pattern.search(file)

        if m:
            d = float(m.group(1))
            if d < minV:
                minV = d
                minFiles = [file]
            elif d == minV:
                minFiles.append(file)
    for file in onlyfiles:
        if file not in minFiles:
           os.remove(join(path,file))
        else :
            print path,file
       # if m:
        #    print m.group(1)
    #print onlyfiles
