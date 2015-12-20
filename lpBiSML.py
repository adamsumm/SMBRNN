import cv2
import json
import numpy as np
import json
tileSize = 8

def clamp(val,minimum,maximum):
    return max(min(val, maximum), minimum)

def findSubImageLocations(image,subImages,confidence):
    allLocations = [ np.array([]) , np.array([])];
    for subImage in subImages:
        
        result = cv2.matchTemplate(image,subImage,cv2.TM_CCOEFF_NORMED)
        match_indices = np.arange(result.size)[(result>confidence).flatten()]
        locations =  np.unravel_index(match_indices,result.shape)
        allLocations[0] = np.concatenate((allLocations[0],locations[0]+(subImage.shape[0]-tileSize)))
        allLocations[1] = np.concatenate((allLocations[1],locations[1]))
    return allLocations     

def tileToString(t):
    tToStr = ['empty','solid','breakable','pickup','goodBlock','enemy','pipe','coin','bullet']
    return tToStr[int(t)]

def parseLevel(levelname,tiles):
    level = cv2.imread(levelname) 
    
    # plt.imshow(level);

    # plt.show()
    tilemap = {}
    
    prefix =  'SMLTiles/'
    postfix = '.png'
    tile = 'X'
    for t in ['ground1','ground2','ground3','ground4','solid1','solid2','solid3','solid4','solid5','solid6','solid7','solid8','solid9','solid10','solid11','solid12','solid13','solid14','solid15','solid16','solid17','solid18','solid19','solid20','solid21','solid22','solid23','solid24','solid25','solid26','solid27','solid28','solid29','solid30','solid31','solid32','solid33','solid34','solid35','solid36','solid37','solid38','solid39','solid40','solid41','solid42','solid43','solid45','solid46','solid47']:
        tilemap['{}{}{}'.format(prefix,t,postfix)] = tile

    
    prefix =  'SMLTiles/'
    postfix = '.png'
    tile = '?'
    for t in ['MBlock','MBlock2']:
        tilemap['{}{}{}'.format(prefix,t,postfix)] = tile
    
    prefix =  'SMLTiles/Bblock'
    postfix = '.png'
    tile = 'S'
    for t in ['1','2','3','4','']:
        tilemap['{}{}{}'.format(prefix,t,postfix)] = tile
    
    prefix =  'SMLTiles/'
    postfix = '.png'
    tile = 'Q'
    for t in ['QBlock']:
        tilemap['{}{}{}'.format(prefix,t,postfix)] = tile
        
    prefix =  'SMLTiles/'
    postfix = '.png'
    tile = 'E'
    for t in ['enemy','enemy2','enemy3','enemy4','enemy5','enemy6','enemy7','enemy8','enemy9','enemy10','enemy11','fish','goomba','koopa','sphinx1','sphinx2','spike','seahorse','koopa1','fly1','fly2']:
        tilemap['{}{}{}'.format(prefix,t,postfix)] = tile
   

    prefix =  'SMLTiles/'
    postfix = '.png'
    tile = 'B'
    for t in ['BL']:
        tilemap['{}{}{}'.format(prefix,t,postfix)] = tile

    prefix =  'SMLTiles/'
    postfix = '.png'
    tile = 'b'
    for t in ['Bbase']:
        tilemap['{}{}{}'.format(prefix,t,postfix)] = tile

    prefix =  'SMLTiles/'
    postfix = '.png'
    tile = 'o'
    for t in  ['coin1']:
        tilemap['{}{}{}'.format(prefix,t,postfix)] = tile

    prefix =  'SMLTiles/'
    postfix = '.png'
    tile = '['
    for t in  ['pipeL']:
        tilemap['{}{}{}'.format(prefix,t,postfix)] = tile

    prefix =  'SMLTiles/'
    postfix = '.png'
    tile = '>'
    for t in  ['pipeUR']:
        tilemap['{}{}{}'.format(prefix,t,postfix)] = tile
    prefix =  'SMLTiles/'
    postfix = '.png'
    tile = '<'
    for t in  ['pipeUL']:
        tilemap['{}{}{}'.format(prefix,t,postfix)] = tile
    prefix =  'SMLTiles/'
    postfix = '.png'
    tile = ']'
    for t in  ['pipeR']:
        tilemap['{}{}{}'.format(prefix,t,postfix)] = tile
    levelMap = {}

    tileToCertainty = {'X':.75,'?':.75,'S':.85,'Q':.85,'E':.6,'o':.7,'B':.8,'b':.8,'<':.85,'>':.85,'[':.95,']':.85}
    
    maxX = -1
    maxY = -1
    
    tm = {}
    for tileImage,tile in tilemap.items():
        if tile not in tm:
            tm[tile] = []
        tm[tile].append(tileImage)
    
    tiles = ['X','E','Q','S','?','o','B','b','[',']','<','>']
    for tile in tiles:
        images = tm[tile]
        locs = findSubImageLocations(level,map(cv2.imread,images),tileToCertainty[tile])
        for yy,xx in zip(locs[0],locs[1]):
            xx = int(round(xx/tileSize))
            yy = int(round(yy/tileSize))
            levelMap[(xx,yy)] = tile
            maxX = max(maxX,xx)
            maxY = max(maxY,yy)
        
    
    levelStr = [['-' for xx in range(maxX+1)] for yy in range(maxY+1)] 

    for loc,tile in levelMap.items():
        levelStr[loc[1]][loc[0]] = tile

    
    with open('input.txt','a') as outputFile:
        direction  = 1
        offset = 0
        for xx in range(maxX):
            if direction == 1:
                line = '('
            elif direction == -1:
                line = ')'
            for dy in range(16):
                yy = offset+direction*dy
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
            outputFile.write(line)
        outputFile.write('\n')

        direction  = -1
        offset = 15
        for xx in range(maxX):
            if direction == 1:
                line = '('
            elif direction == -1:
                line = ')'
            for dy in range(16):
                yy = offset+direction*dy
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
            outputFile.write(line)


        outputFile.write('\n')
levels = [ 
'SML/super_mario_land_11.png',
'SML/super_mario_land_12.png',
'SML/super_mario_land_13.png',
'SML/super_mario_land_21.png',
'SML/super_mario_land_22.png',
'SML/super_mario_land_31.png',
'SML/super_mario_land_32.png',
'SML/super_mario_land_33.png',
'SML/super_mario_land_41.png',
'SML/super_mario_land_42.png',
]

tiles = []
for levelFile in levels:
    parseLevel(levelFile,tiles)
