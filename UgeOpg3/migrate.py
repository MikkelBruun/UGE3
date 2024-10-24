import sys
import re


USAGESTRING = "usage: migrate.py inputfile.csv outputfile.csv"
#PATTERNS/checks - seperated to better provide specific error messages
# base  ^[^,]*,[^,]*,[^,]*,.*$
correctCommaCount   = re.compile(r",")
captureId           = re.compile(r"^(?P<id>\d+),.*,.*,.*$")
checkName           = re.compile(r"^.*,\w+(\s\w+)*,.*,.*$")
#email starts with one \w then however many \w or ".", an "@", a word, "." and a word
matchEmail        = re.compile(r"^[^,]*,[^,]*,\w[\w.]*@\w+\.\w+,.*$")
matchPurchaseAmount = re.compile(r",\d+([.,]\d+)?$")



if(len(sys.argv)!=3):
    print(USAGESTRING)
else:
    inFile = sys.argv[1];
    outFile = sys.argv[2];
    with open(inFile,"r") as INF:
        data = INF.readlines()
        header = data[0]
        data = data[1:]
        correct = [header] #assumed to be correct
        errors = []
        for (i,L) in enumerate(data):
            #perform universally valid fixes
            _L = L
            _L = _L.replace(r"^,|,$","") #, should not start or end a line
            _L = _L.replace(",,", ",")
            _L = _L.replace(r"\s\s+"," ")
            #if(_L != L):
            #    print(L+_L)
            L = _L
            if re.match("^,+$",L):
                pass#completely empty. throw away the line
            else:
                expId = i + 1
                errorString = ""
                #handle each check
                commaMatch = correctCommaCount.findall(L)
                idMatch = captureId.match(L)
                nameMatch = checkName.match(L)
                emailMatch = matchEmail.match(L)
                commaMatch = correctCommaCount.findall(L)
                purchaseMatch = matchPurchaseAmount.findall(L)
                if len(commaMatch) != 3:
                    errorString+="\t#Incorrect number of commas\n"
                if idMatch == None:
                    errorString+=f"\t#id not found (expected id: {expId})\n"
                else:
                    Lid = idMatch.groupdict()["id"]
                    if(str(expId)!=Lid):
                        errorString+=f"\t#expected/matched id: {expId}/{Lid}\n"
                if(nameMatch == None):
                    errorString+=f"\t#name not matched\n"
                if(emailMatch == None):
                    errorString+=f"\t#malformed email\n"
                if(len(purchaseMatch) != 1):
                    errorString+=f"\t#malformed purchase amount\n"
                    print(L)
                #end
                if(errorString == ""):
                    correct.append(L)
                else:
                    errors.append(L+errorString)
        with open(outFile,"w") as OUTF:
            OUTF.writelines(correct)
        with open(outFile+"error","w") as OUTERR:
            OUTERR.writelines(errors)