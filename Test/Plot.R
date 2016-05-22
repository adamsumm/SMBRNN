directories = c('../Torch/outputbasic',
                '../Torch/outputbasicLineNo',
                '../Torch/outputbasicLineNoP',
                '../Torch/outputbi',
                '../Torch/outputbiLineNo',
                '../Torch/outputbiLineNoP',
                '../Torch/outputbiP',
                '../Torch/outputbasicP')

files = c('ag.summary','ug.summary')

data = read.csv('originals.summary')
data = data[which(data$jumpVariance >=0),]

allData = data
for (dir in directories) {
  combined = NULL
  for (file in files){
    print( paste(dir,file, sep='/'))
    data = read.csv(paste(dir,file, sep='/'))
    data = data[which(data$jumpVariance >=0),]
    allData = rbind(allData,data)
  }
}


yMins = c()
yMaxs = c()

data = read.csv('originals.summary')
data = data[which(data$jumpVariance >=0),]
for (n in names(data)){
  temp = hist(data[[n]],breaks=pretty(allData[[n]],n=10),plot=FALSE)
  yMins[[n]] = min(temp$density)
  yMaxs[[n]] = max(temp$density)
}
for (dir in directories) {
  combined = NULL
  for (file in files){
    data = read.csv(paste(dir,file, sep='/'))
    data = data[which(data$jumpVariance >=0),]
    if (is.null(combined)){
      combined = data
    }
    else {
      combined = rbind(combined,data)
    }
    for (n in names(data)){
      temp =  hist(data[[n]],breaks=pretty(allData[[n]],n=10,plot=FALSE))
      yMins[[n]] = min(yMins[[n]],temp$density)
      yMaxs[[n]] = max(yMaxs[[n]],temp$density)
    }
  }
  for (n in names(combined)){
    temp =  hist(combined[[n]],breaks=pretty(allData[[n]],n=10,plot=FALSE))
    yMins[[n]] = min(yMins[[n]],temp$density)
    yMaxs[[n]] = max(yMaxs[[n]],temp$density)
  }
}

for (dir in directories) {
  combined = NULL
  for (file in files){
    print( paste(dir,file, sep='/'))
    data = read.csv(paste(dir,file, sep='/'))
    data = data[which(data$jumpVariance >=0),]
    if (is.null(combined)){
      combined = data
    }
    else {
      combined = rbind(combined,data)
    }
    for (n in names(data)){
      svg(paste(dir,file,n, 'hist.svg',sep=''))
      hist(data[[n]],breaks=pretty(allData[[n]],n=10),freq=FALSE,ylim=c(yMins[[n]],yMaxs[[n]]))
      dev.off()
    }
  }
  for (n in names(combined)){
    svg(paste(dir,n, 'hist.svg',sep=''))
    hist(combined[[n]],breaks=pretty(allData[[n]],n=10),freq=FALSE,ylim=c(yMins[[n]],yMaxs[[n]]))
    dev.off()
  }
}

data = read.csv('originals.summary')
data = data[which(data$jumpVariance >=0),]
for (n in names(data)){
  svg(paste('originals',n, 'hist.svg',sep=''))
  print(n)
  print(c(min(allData[[n]]),max(allData[[n]]) ))
  print(c(min(data[[n]]),max(data[[n]]) ))
  hist(data[[n]],breaks=pretty(allData[[n]],n=10),freq=FALSE,ylim=c(yMins[[n]],yMaxs[[n]]),col='grey')
  dev.off()
}
