

import sys
def parseAll(filename):  
    allLines = []
    with open(filename,'r') as openFile: 
        for  data in openFile:
            #print data
            ind = data.find(':')
            if ind > 0:
                data = data[ind:]
            ind = data.find(';')
            sublevels = data.split(';')
            
            for data in sublevels:
                if len(data) > 0:
                    lines = {}
                    #if ind > 0:
                    #    data = data[:ind]
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
                        lines[yy] =  lines[yy] + '-'*(maxLen-len(lines[yy]))
                    allLines.append(lines)
    return allLines

def parse(filename):
    with open(filename,'r') as openFile:
        lines = {}
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
            sublevels = data.split(';')
            largest = ''
            for l in sublevels:
                if len(l) > len(largest):
                    largest = l
            data = largest
            #if ind > 0:
            #    data = data[:ind]
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
        lines[yy] =  lines[yy] + '-'*(maxLen-len(lines[yy]))
    return lines
