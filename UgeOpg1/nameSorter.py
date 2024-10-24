import matplotlib.pyplot as plt


def KeyFun(a, b):
    return 1

with open("nameListTrimmed.txt","r") as names:
    nameLst = map(lambda str:str[:-1],names.readlines())#trim newline
    
    #Count uccurances
    nameLst = sorted(sorted(nameLst),key=lambda n: len(n))
    letterOccurances = {}
    for n in nameLst:
        for _c in n:
            c = _c.lower()
            current = letterOccurances.get(c, 0)
            letterOccurances[c] = current + 1
    #print occurances
    x = [i for i in letterOccurances]
    y = [letterOccurances[i] for i in letterOccurances]
    fig, ax = plt.subplots()
    ax.bar(x,y)
    plt.savefig("letterCountPlot")
    
    #calculate name length distribution
    nameLenList = [0 for _ in range(20)]
    for name in nameLst:
        nameLenList[len(name)] += 1
    #filter out lengths with 0 words
    nameLenList = list(filter(lambda x:x!=0,nameLenList))
    nameCount = sum(nameLenList)
    m = sum(nameLenList[x]*x for x in range(len(nameLenList)))/sum(nameLenList)
    #print name length distribution
    fig, ax = plt.subplots()
    ax.plot(range(len(nameLenList)),nameLenList)
    
    ax.vlines(m,0,max(nameLenList),"r")
    plt.savefig("nameLengthPlot")