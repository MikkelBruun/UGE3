##Først antog jeg opgaven var at lave et script som forsøgte at validere __alle__
##slags csv filer og ikke bare den specifikke. 
class CsvLine:

    def __init__(self,header,line):
        self.error = ""
        #dict holding the values
        self.csvFields = {}
        self.header = header
        self.line = line
        for f in self.header.split(","):
            self.csvFields[f] = None
        
        self.__validate()
        
    def __validate(self):
        lineFields = self.line.split(",")
        fieldNames = list(self.csvFields.keys())
        expectedLen = len(fieldNames)
        if(len(lineFields) != expectedLen):
            self.error += f"Expected {expectedLen} fields, but line has {len(lineFields)}"
        else:
            for i in range(expectedLen):
                value = lineFields[i]
                key = fieldNames[i]
                self.csvFields[key] = value
                
    def __str__(self):
        S = ""
        for key in self.csvFields:
            match self.csvFields[key]:
                case None:
                    ","
                case any:
                    S += any+","
        return S[:-1] #remove final ,