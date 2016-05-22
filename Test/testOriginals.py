from os import listdir
import parselevel
from testSMB import testLevel

output = []
statNames = None
for level in parselevel.parseAll('originals.txt'):
    stats =  testLevel(level)
    data = []
    if statNames is None:
        statNames = []
        for s in stats:
            statNames.append(s)
    for s in statNames:
        data.append(str(stats[s]))
    output.append(data)


with open('originals.summary','w') as outputfile:
    outputfile.write(','.join(statNames)+'\n')
    for line in output:
        outputfile.write(','.join(line)+'\n')

                
