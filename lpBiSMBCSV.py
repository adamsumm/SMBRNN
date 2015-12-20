import cv2
import json
import numpy as np
import json
import math

def clamp(val,minimum,maximum):
    return max(min(val, maximum), minimum)

def findSubImageLocations(image,subImages,confidence):
    allLocations = [ np.array([]) , np.array([])];
    for subImage in subImages:
        
        result = cv2.matchTemplate(image,subImage,cv2.TM_CCOEFF_NORMED)
        
        match_indices = np.arange(result.size)[(result>confidence).flatten()]
        locations =  np.unravel_index(match_indices,result.shape)
        
       # print locations
        allLocations[0] = np.concatenate((allLocations[0],locations[0]+(subImage.shape[0]-16)))
        allLocations[1] = np.concatenate((allLocations[1],locations[1]))
    return allLocations     

def tileToString(t):
    tToStr = ['empty','solid','breakable','pickup','goodBlock','enemy','pipe','coin','bullet']
    return tToStr[int(t)]

def parseLevel(levelname,tiles,nums):
    level = cv2.imread(levelname) 
    
    # plt.imshow(level);
    # plt.show()
    tilemap = {}
    
    prefix =  'Tiles/SMBTiles/tileset_tile'
    postfix = '.png'
    tile = 'X'
    for t in ['LLground','LLground2','LLground3','LLground4','LLground5',
                    'LLground6','LLground7','LLground8','LLground9',
                    'LLground10','LL1','LL2','LL3',                    
                    '00','10','33','66','99','269','270','271','434','435','436','437','438','439','450','girder','CR','C','CL']:
        tilemap['{}{}{}'.format(prefix,t,postfix)] = tile

    
    prefix =  'Tiles/SMBTiles/tileset_tile'
    postfix = '.png'
    tile = '?'
    for t in ['Mushroom','MushroomLL','MushroomLL2','MushroomLL3','MushroomLL4',
                    'MushroomLL5','MushroomLL6','MushroomLL7','MushroomLL8','MushroomHidden']:
        tilemap['{}{}{}'.format(prefix,t,postfix)] = tile
    
    prefix =  'Tiles/SMBTiles/tileset_tile'
    postfix = '.png'
    tile = 'S'
    for t in ['LLbreak','LLbreak2','01','03','67','68','69']:
        tilemap['{}{}{}'.format(prefix,t,postfix)] = tile
    
    prefix =  'Tiles/SMBTiles/tileset_tile'
    postfix = '.png'
    tile = 'Q'
    for t in ['24','90']:
        tilemap['{}{}{}'.format(prefix,t,postfix)] = tile
        
    prefix =  'Tiles/SMBTiles/'
    postfix = '.png'
    tile = 'E'
    for t in ['hammerbro','turtle1','turtle2','fly1','fly2','fly3','fly4','turtle1D','turtle2D','fly1D','fly2D','fly3D','fly4D','pirannha','turtle1b','turtle2b','fly1b','fly2b','fly3b','fly4b','pirannha2','turtle1bD','turtle2bD','fly1bD','fly2bD','fly3bD','fly4bD','pirannha2D','goomba','goomba2','goomba2D','PPR','PPRud']:
        tilemap['{}{}{}'.format(prefix,t,postfix)] = tile
   

    prefix =  'Tiles/SMBTiles/tileset_tile'
    postfix = '.png'
    tile = 'B'
    for t in ['09','75']:
        tilemap['{}{}{}'.format(prefix,t,postfix)] = tile

    prefix =  'Tiles/SMBTiles/tileset_tile'
    postfix = '.png'
    tile = 'b'
    for t in ['108','42']:
        tilemap['{}{}{}'.format(prefix,t,postfix)] = tile

    prefix =  'Tiles/SMBTiles/tileset_tile'
    postfix = '.png'
    tile = 'o'
    for t in  ['57','58','123']:
        tilemap['{}{}{}'.format(prefix,t,postfix)] = tile

    prefix =  'Tiles/SMBTiles/'
    postfix = '.png'
    tile = '['
    for t in  ['pipe','pipeD','Lg']:
        tilemap['{}{}{}'.format(prefix,t,postfix)] = tile

    prefix =  'Tiles/SMBTiles/'
    postfix = '.png'
    tile = '>'
    for t in  ['pipe_ur','URg']:
        tilemap['{}{}{}'.format(prefix,t,postfix)] = tile
    prefix =  'Tiles/SMBTiles/'
    postfix = '.png'
    tile = '<'
    for t in  ['pipe_ul','ULg']:
        tilemap['{}{}{}'.format(prefix,t,postfix)] = tile
    prefix =  'Tiles/SMBTiles/'
    postfix = '.png'
    tile = ']'
    for t in  ['pipe_r','pipe_rD','Rg']:
        tilemap['{}{}{}'.format(prefix,t,postfix)] = tile
    levelMap = {}

    tileToCertainty = {'X':.78,'?':.75,'S':.85,'Q':.85,'E':.6,'o':.7,'B':.8,'b':.8,'<':.85,'>':.85,'[':.95,']':.85}
    
    maxX = -1
    maxY = -1
    
    tm = {}
    for tileImage,tile in tilemap.items():
        if tile not in tm:
            tm[tile] = []
        tm[tile].append(tileImage)
    
    tiles = ['o','X','E','Q','S','?','B','b','[',']','<','>']
    for tile in tiles:
        images = tm[tile]
        #print images
        locs = findSubImageLocations(level,map(cv2.imread,images),tileToCertainty[tile])
        for yy,xx in zip(locs[0],locs[1]):
            xx = int(math.ceil(xx/16))
            yy = int(math.ceil(yy/16))
            levelMap[(xx,yy)] = tile
            maxX = max(maxX,xx)
            maxY = max(maxY,yy)
        
    
    levelStr = [['-' for xx in range(maxX+1)] for yy in range(maxY+1)] 

    for loc,tile in levelMap.items():
        levelStr[loc[1]][loc[0]] = tile
    curX = 2
    curY = -1
    
    def isSolid(tile):
        return tile in ['X','Q','S','?','B','b','[',']','<','>']
    for yy in range(maxY-1,-1,-1):
        if levelStr[yy][curX] == '-' and isSolid(levelStr[yy+1][curX]) :
             curY = yy
             break
    import pathfinding
    jumps  = [[( 0,-1),
               ( 0,-2),
               ( 1,-3),
               (1,-4),
               ( 0,-4)]
              , [( 0,-1),
                 ( 0,-2),
                 ( 0,-3),
                 (0,-4),
                 ( 1,-4)]
              ,[( 1,-1),
                ( 1,-2),
                ( 1,-3),
                (1,-4),
                ( 2,-4)]
              ,[( 1,-1),
                ( 1,-2),
                ( 2,-2),
                ( 2,-3),
                ( 3,-3),
                ( 3,-4),
                ( 4,-4),
                ( 5,-3),
                ( 6,-3),
                ( 7,-3),
                ( 8,-2),
                ( 8,-1)]
              ,[( 1,-1),
                ( 1,-2),
                ( 2,-2),
                ( 2,-3),
                ( 3,-3),
                ( 3,-4),
                ( 4,-4),
                ( 5,-4),
                ( 6,-3),
                ( 7,-3),
                ( 8,-2),
                ( 8,-1)]]
    jumpDiffs = []
    for jump in jumps:
        jumpDiff = [jump[0]]
        for ii in range(1,len(jump)):
            jumpDiff.append((jump[ii][0]-jump[ii-1][0],jump[ii][1]-jump[ii-1][1]))
        jumpDiffs.append(jumpDiff)
    jumps = jumpDiffs
    visited = set()
    def getNeighbors(pos):
        dist = pos[0]
        pos = pos[1]
        #print pos
        visited.add((pos[0],pos[1]))
        below = (pos[0],pos[1]+1)
        neighbors = []
        if below[1] > maxY:
            return []
        if pos[2] != -1:
            ii = pos[3] +1
            jump = pos[2]
            if ii < len(jumps[jump]):
                if  not (pos[0]+pos[4]*jumps[jump][ii][0] > maxX or pos[0]+pos[4]*jumps[jump][ii][0] < 0 or pos[1]+jumps[jump][ii][1] < 0) and not isSolid(levelStr[pos[1]+jumps[jump][ii][1]][pos[0]+pos[4]*jumps[jump][ii][0]]):
                    #print jump, jumps[jump], ii, (pos[0],pos[1]), (pos[0]+pos[4]*jumps[jump][ii][0],pos[1]+jumps[jump][ii][1])
                    neighbors.append([dist+1,(pos[0]+pos[4]*jumps[jump][ii][0],pos[1]+jumps[jump][ii][1],jump,ii,pos[4])])
                if pos[1]+jumps[jump][ii][1] < 0 and not isSolid(levelStr[pos[1]+jumps[jump][ii][1]][pos[0]+pos[4]*jumps[jump][ii][0]]):
                    neighbors.append([dist+1,(pos[0]+pos[4]*jumps[jump][ii][0],0,jump,ii,pos[4])])
                
        if isSolid(levelStr[below[1]][below[0]]):
            if pos[0]+1 <= maxX and not isSolid(levelStr[pos[1]][pos[0]+1]):
                neighbors.append([dist+1,(pos[0]+1,pos[1],-1)])
            if pos[0]-1 >= 0 and not isSolid(levelStr[pos[1]][pos[0]-1]):
                neighbors.append([dist+1,(pos[0]-1,pos[1],-1)])

            for jump in range(len(jumps)):
                ii = 0
                if not (pos[0]+jumps[jump][ii][0] > maxX or pos[1] < 0) and not isSolid(levelStr[pos[1]+jumps[jump][ii][1]][pos[0]+jumps[jump][ii][0]]):
                    neighbors.append([dist+ii+1,(pos[0]+jumps[jump][ii][0],pos[1]+jumps[jump][ii][1],jump,ii,1)])

                if not (pos[0]-jumps[jump][ii][0] < 0 or pos[1] < 0) and not isSolid(levelStr[pos[1]+jumps[jump][ii][1]][pos[0]-jumps[jump][ii][0]]):
                    neighbors.append([dist+ii+1,(pos[0]-jumps[jump][ii][0],pos[1]+jumps[jump][ii][1],jump,ii,-1)])

        else:
            neighbors.append([dist+1,(pos[0],pos[1]+1,-1)])
            if pos[1]+1 <= maxY:
                if not isSolid(levelStr[pos[1]+1][pos[0]+1]):
                    neighbors.append([dist+1.4,(pos[0]+1,pos[1]+1,-1)])
                if not isSolid(levelStr[pos[1]+1][pos[0]-1]):
                    neighbors.append([dist+1.4,(pos[0]-1,pos[1]+1,-1)])
            if pos[1]+2 <= maxY:
                if not isSolid(levelStr[pos[1]+2][pos[0]+1]):
                    neighbors.append([dist+2,(pos[0]+1,pos[1]+2,-1)])
                if not isSolid(levelStr[pos[1]+2][pos[0]-1]):
                    neighbors.append([dist+2,(pos[0]-1,pos[1]+2,-1)])
        return neighbors
    subOptimal = 10
    paths = pathfinding.dijkstras_shortest_path( (curX,curY,-1), lambda pos: pos[0] == maxX, getNeighbors, subOptimal)
    paths = [[ (p[0],p[1]) for p in path] for path in paths]
    print levelname, len(paths)
    for yy in range(maxY+1):
        s = ''
        for xx in range(maxX+1):
            if (xx,yy) in visited:# paths[0]:
                s+= '*'
            else:
                s += levelStr[yy][xx]
        print s
    if len(paths) == 0:
        exit()
        
    strs = []
    for path in paths:
        str = ''
        if True:
        #with open('input.txt','a') as outputFile:
            #outputFile.write('\n')
            #str += ';'
            #for ii in range(nums[0]):
            #    outputFile.write('W')
            #for ii in range(nums[1]):
            #    outputFile.write('L')

            direction  = 1
            offset = 0
            div = 10
            for xx in range(maxX):
                
                if direction == 1:
                    line = '('
                elif direction == -1:
                    line = ')'
                for dy in range(16):
                    yy = offset+direction*dy
                    if (xx,yy) in path and levelStr[yy][xx] == '-' :
                        line += '*'
                    else:
                        if yy <= maxY:
                            line += levelStr[yy][xx]
                        else :
                            line += levelStr[maxY][xx]

                if direction == 1:
                    direction = -1
                    offset = 15
                elif direction == -1:
                    direction = 1
                    offset = 0
                #line += ':'
                str += line
                #outputFile.write(line)
            #outputFile.write('\n')
            strs.append(str)
            str = ''
            direction  = -1
            offset = 15
            for xx in range(maxX):
                if direction == 1:
                    line = '('
                elif direction == -1:
                    line = ')'
                for dy in range(16):
                    yy = offset+direction*dy
                    if (xx,yy) in path and levelStr[yy][xx] == '-' :
                        line += '*'
                    else:
                        if yy <= maxY:
                            line += levelStr[yy][xx]
                        else :
                            line += levelStr[maxY][xx]

                if direction == 1:
                    direction = -1
                    offset = 15
                elif direction == -1:
                    direction = 1
                    offset = 0
                #line += ':'
                #outputFile.write(line)
                str += line
            strs.append(str)
            #outputFile.write('\n')
    return strs
        #    levelMap['{},{}'.format(round(locs[0][ii]/16),round(locs[1][ii]/16))] = tile
levels = [  'levels/mario-1-1.png','levels/mario-1-2.png','levels/mario-1-3.png','levels/mario-2-1.png',
            'levels/mario-3-1.png','levels/mario-3-2.png','levels/mario-3-3.png','levels/mario-4-1.png',
            'levels/mario-4-2.png','levels/mario-4-3.png','levels/mario-5-1.png','levels/mario-5-2.png',
            'levels/mario-5-3.png','levels/mario-6-1.png','levels/mario-6-2.png','levels/mario-6-3.png',
            'levels/mario-7-1.png','levels/mario-8-1.png','levels/mario-8-2.png','levels/SuperMarioBros2(J)-World1-1.png','levels/SuperMarioBros2(J)-World1-2.png','levels/SuperMarioBros2(J)-World1-3.png',
 'levels/SuperMarioBros2(J)-World2-1.png','levels/SuperMarioBros2(J)-World2-2.png',
 'levels/SuperMarioBros2(J)-World2-3.png','levels/SuperMarioBros2(J)-World3-1.png',
 'levels/SuperMarioBros2(J)-World3-3.png','levels/SuperMarioBros2(J)-World4-1.png',
 'levels/SuperMarioBros2(J)-World4-2.png',
 'levels/SuperMarioBros2(J)-World4-3.png','levels/SuperMarioBros2(J)-World5-1.png',
 'levels/SuperMarioBros2(J)-World5-2.png','levels/SuperMarioBros2(J)-World6-1.png',
 'levels/SuperMarioBros2(J)-World6-3.png',
 'levels/SuperMarioBros2(J)-World8-1.png','levels/SuperMarioBros2(J)-WorldA-1.png','levels/SuperMarioBros2(J)-WorldA-3.png',
 'levels/SuperMarioBros2(J)-WorldB-1.png','levels/SuperMarioBros2(J)-WorldB-3.png','levels/SuperMarioBros2(J)-WorldC-2.png',
 'levels/SuperMarioBros2(J)-WorldD-1.png','levels/SuperMarioBros2(J)-WorldD-2.png',]
#levels = ['levels/mario-1-1.png']
levelNums = [  (1,1),(1,2),(1,3),(2,1),
            (3,1),(3,2),(3,3),(4,1),
            (4,2),(4,3),(5,1),(5,2),
            (5,3),(6,1),(6,2),(6,3),
            (7,1),(8,1),(8,2),(1,1),(1,2),(1,3),
 (2,1),(2,2),
 (2,3),(3,1),
 (3,3),(4,1),
 (4,2),
 (4,3),(5,1),
 (5,2),(6,1),
 (6,3),
 (8,1),(10,1),(10,3),
 (11,1),(11,3),(12,2),
 (13,1),(13,2),]
#levels = ['levels/mario-1-1.png','levels/mario-6-3.png']
tiles = []
levelstrs = []
stats = {'E':[0,0],'o':[0,0],'[':[0,0],'?':[0,0],'Q':[0,0]}
statToChar = {'E':'E','o':'o','[':'p','?':'q','Q':'Q'}

for levelFile,nums in zip(levels,levelNums):
    for level in parseLevel(levelFile,tiles,nums):
        levelstrs.append(level)

for level in levelstrs:
    for stat in stats:
        c = level.count(stat)
        if c > stats[stat][1]:
            stats[stat][1] = c
        if c < stats[stat][0]:
            stats[stat][0] = c

#with open('input.txt','w') as openfile:
#    for stat in stats:
#        openfile.write(statToChar[stat]+',')
#    openfile.write('c\n')
count = 0
chars = set()
for level in levelstrs:
    for c in level:
        count += 1
        chars.add(c)
charToI = { c:i for c,i in zip(chars,range(len(chars)))}
print charToI
print [count,len(stats)+len(chars)]
input = np.zeros([count,len(stats)+len(chars)])
count = 0

for level in levelstrs:
    actualStats = {}
    for stat in stats:
        c = level.count(stat)
        actualStats[stat] = 1# (float(c - stats[stat][0])/float(stats[stat][1]-stats[stat][0]))*2-1
    for c in level:
        ind = 0
        for stat in stats:
            input[count][ind] = actualStats[stat]
            ind += 1
        input[count][ind+charToI[c]] = 1
        count += 1

import h5py
h5f = h5py.File('smb.h5', 'w')
h5f.create_dataset('dat', data=input)
h5f.close()
            #openfile.write('{},'.format(actualStats[stat]))            
        #openfile.write(c)
        #openfile.write('\n')

        
        
    # get count for each of the stats
    # then go from 0-5 for min to max

