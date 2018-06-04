from os import listdir
import parselevel
from testSMB import testLevel

dirs = ['../Torch/outputbasic',
'../Torch/outputbasicLineNo',
'../Torch/outputbasicLineNoP',
'../Torch/outputbi',
'../Torch/outputbiLineNo',
'../Torch/outputbiLineNoP',
'../Torch/outputbiP',
'../Torch/outputbasicP',]

dirs = ['../Torch/outputbiLineNoP_128_0',
'../Torch/outputbiLineNoP_256_0',
'../Torch/outputbiLineNoP_256_0.8',
'../Torch/outputbiLineNoP_256_3_0.6',
'../Torch/outputbiLineNoP_512_0.2',
'../Torch/outputbiLineNoP_512_3_0.8',
'../Torch/outputbiLineNoP_64_0']

statNames = None
for d in dirs:
    outputAG = []
    outputUG = []
    
    for f in sorted(listdir(d)):
        print "Statting ", d, f
        if 'AG' in f or 'UG' in f:
            dataAG = []
            dataUG = []
            stats =  testLevel(parselevel.parse(d + '/' + f))
            if statNames is None:
                statNames = []
                for s in stats:
                    statNames.append(s)
            if 'AG' in f:
                for s in statNames:
                    dataAG.append(str(stats[s]))
                outputAG.append(dataAG)
            elif 'UG' in f:
                for s in statNames:
                    dataUG.append(str(stats[s]))
                outputUG.append(dataUG)
    with open('{}/ag.summary'.format(d),'w') as outputfile:
        outputfile.write(','.join(statNames)+'\n')
        for line in outputAG:
            outputfile.write(','.join(line)+'\n')
    with open('{}/ug.summary'.format(d),'w') as outputfile:
        outputfile.write(','.join(statNames)+'\n')
        for line in outputUG:
            outputfile.write(','.join(line)+'\n')
            
    
                
