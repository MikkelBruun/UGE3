originalLen, trimmedLen = 0,0
with open("namelist.txt", "r") as names:
    namesLst = names.readlines()
    originalLen = len(namesLst)
    with open("nameListTrimmed.txt", "w") as newFile:
        for i, name in enumerate(namesLst):
            if(i % 5 == 0):
                trimmedLen += 1
                newFile.write(name)
print("original: ",originalLen, "new length: ", trimmedLen)