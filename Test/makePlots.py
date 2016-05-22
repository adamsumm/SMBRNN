import numpy as np
import corner
import matplotlib.pyplot as plt

dirs = ['../Torch/outputbasic',
'../Torch/outputbasicLineNo',
'../Torch/outputbasicLineNoP',
'../Torch/outputbasicP',
'../Torch/outputbi',
'../Torch/outputbiLineNo',
'../Torch/outputbiLineNoP',
'../Torch/outputbiP',]

files = ['ag.summary','ug.summary']


#allData = np.array()
metrics = ['emptyPercentage', 'negativeSpace', 'decorationPercentage', 'pathPercentage', 'leniency', 'linearity', 'jumps', 'meaningfulJumps']
prettyNames =  {'emptyPercentage':r"$e$", 'negativeSpace':'$n$', 'decorationPercentage':'$d$', 'pathPercentage':'$p$', 'leniency':'$l$', 'linearity':'$R^2$', 'jumps':'$j$', 'meaningfulJumps':'$j_i$', 'length':'$s$'}

def formatData(file):
    my_data = np.genfromtxt(file, delimiter=',')
    with open(file,'r') as openfile:
        line = openfile.readline().rstrip()
    items = line.split(',')
    metricToIndex = {items[ii]:ii for ii in range(len(items))}
        
    columns = [metricToIndex[metric] for metric in metrics]
    data = my_data[1:,columns]
    data =data[data[:,3] > -1,:]
    labels = [prettyNames[metric] for metric in metrics]

    return (data,labels)
originals,_ = formatData('originals.summary')
allData = originals
file2dat = {}
for dir in dirs:
    combined = None
    for file in files:
        data,labels = formatData('{}/{}'.format(dir,file))
        if  allData is None:
            allData = data
        else:
            allData = np.concatenate([allData,data])
        if  combined is None:
            combined  = data
        else:
            combined  = np.concatenate([combined,data])
            
        #figure = corner.corner(data,labels=labels,quantiles=[0.16, 0.5, 0.84])
        #figure.savefig('{}{}.png'.format(dir,file))
        file2dat['{}{}'.format(dir,file)] = (data,labels)
        file2dat['{}'.format(dir)] = (combined,labels)
            
range = [[allData[:,ii].min(), allData[:,ii].max()] for ii in range(allData.shape[1])]
for file in file2dat:
    figure = corner.corner(file2dat[file][0],labels=labels,range=range)
    figure.savefig('{}.png'.format(file))
    plt.close()
figure = corner.corner(originals,labels=labels,range=range)
figure.savefig('originals.png'.format(file))
plt.close()
