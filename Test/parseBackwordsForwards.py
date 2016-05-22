
import sys

lines = {}
with open(sys.argv[1],'r') as openFile:
    openFile.readline()
    openFile.readline()
    openFile.readline()
    openFile.readline()
    

    for  data in openFile:
        #print data
        ind = data.find(':')
        if ind > 0:
            data = data[ind:]
        
        ind = data.find(';')
        if ind > 0:
            data = data[:ind]
        data = data.replace('\n','')
        data = data.replace('v','')
        data = data.replace(':','')
        data = data.replace(';','')
        world = 0
        level = 0
        for char in data:
            if char == 'W':
                world += 1
            elif char == 'L':
                level += 1
            else :
                break
        data = data.replace('W','')
        data = data.replace('L','')
        direction = 1
        offset = 0
        
        for char in data:
            #print char
            
            if char == '(':
                direction = 1
                offset = 0
            elif char == ')':
                direction = -1
                offset = 15
            else :
                if offset not in lines:
                    lines[offset] = ''
                lines[offset] += char
                    #print offset,char
                offset += direction

maxLen = 0
for yy in range(16):
   if len(lines[yy]) > maxLen:
       maxLen = len(lines[yy]) 

for yy in range(16):
    print lines[yy] + '-'*(maxLen-len(lines[yy]))


            
