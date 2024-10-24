import sys
import re


USAGESTRING = """usage: migrate.py [options] inputfile.csv outputfile.csv
options:
    --append": append to output file
    --recoverid": attempt to add missing id when possible
    --invertnegativepurchase": if purchase amount is negative, simply invert it
"""
#PATTERNS/checks - seperated to better provide specific error messages
# base  ^[^,]*,[^,]*,[^,]*,.*$
correctCommaCount   = re.compile(r",")
captureId           = re.compile(r"^(?P<id>\d+),.*,.*,.*$")
checkName           = re.compile(r"^.*,(\w+\.?\s?)+,.*$")
#email starts with one \w then however many \w or ".", an "@", a word, "." and a word
matchEmail        = re.compile(r".*,\w[\w.]*@\w+\.\w+,.*$")
matchPurchaseAmount = re.compile(r",\d+([.,]\d+)?$")
negativePurchase = re.compile(r".*,(?P<amount>-\d+([.,]\d+)?)$")




def readArgs():
    flags = {
        "--append": False,
        "--recoverid": False,
        "--invertnegativepurchase": False,
    }
    inFile = ""
    outFile = ""
    for arg in sys.argv[1:]:
        if flags.get(arg)!=None:
            flags[arg] = True
        elif inFile == "":
            inFile = arg
        else:
            outFile = arg
    return (flags,inFile,outFile)

(flags, inFile, outFile) = readArgs()
if inFile == "" or outFile == "":
    print(USAGESTRING)
else:
    with open(inFile,"r") as INF:
        data = INF.readlines()
        header = data[0]
        data = data[1:]
        correct = [header] #assumed to be correct
        errors = []
        for (i,L) in enumerate(data):
            #perform universally valid fixes
            _L = L
            
            _L = re.sub(r",,+",",",_L)
            _L = re.sub(r"\s\s+"," ",_L)
            _L = re.sub(r"(?<=,)\s|\s(?=,)","",_L)#there should not be a comma next to a space
            
            L = _L
            if re.match("^,+$",L):
                pass#completely empty. throw away the line
            else:
                expId = i + 1
                errorString = ""
                #handle each check
                commaMatch = correctCommaCount.findall(L)
                if len(commaMatch) > 3:
                    L = re.sub(r"^,|,$","",L)
                    commaMatch = correctCommaCount.findall(L)
                idMatch = captureId.match(L)
                nameMatch = checkName.match(L)
                emailMatch = matchEmail.match(L)
                commaMatch = correctCommaCount.findall(L)
                purchaseMatch = matchPurchaseAmount.findall(L)
                if len(commaMatch) != 3:
                    errorString+="\t#Incorrect number of commas\n"
                elif idMatch == None:
                    if flags["--recoverid"]:
                        L = str(expId)+L[L.find(","):]
                    else:
                        errorString+=f"\t#id not found (expected id: {expId})\n"
                else:
                    Lid = idMatch.groupdict()["id"]
                    if(str(expId)!=Lid):
                        if flags["--recoverid"]:
                            L=L.replace(Lid,str(expId))
                        else:
                            errorString+=f"\t#expected/matched id: {expId}/{Lid}\n"
                if(nameMatch == None):
                    errorString+=f"\t#name not matched\n"
                if(emailMatch == None):
                    errorString+=f"\t#malformed email\n"
                if(len(purchaseMatch) != 1):
                    if flags["--invertnegativepurchase"]:
                        negative = negativePurchase.match(L)
                        if negative != None:
                            negative = negative.groupdict()["amount"]
                            L = L.replace(negative,negative[1:])
                    else:
                        errorString+=f"\t#malformed purchase amount\n"
                #end
                if(errorString == ""):
                    correct.append(L)
                else:
                    errors.append(L+errorString)
        writeflag = "w"
        if(flags["--append"]): writeflag = "a"
        with open(outFile,writeflag) as OUTF:
            OUTF.writelines(correct)
        with open(outFile+".error","w") as OUTERR:
            OUTERR.writelines(errors)