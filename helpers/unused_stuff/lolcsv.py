from ast import literal_eval
from shutil import copy

class LolCsv:

    def __init__(self):
        pass

    def __lineToListOfStrings(self, line, fieldsRequireDoubleQuotes, removeExtraSpaces):
        l=[]
        if fieldsRequireDoubleQuotes:
            s = [-1, -1, -1]
            for i in range(0, len(line)):
                if s[0] == -1:
                    if l[i] == '"':
                        s[0] = i
                elif l[i] == '"':
                    s[1] = i
                if s[0] != -1 and s[1] != -1 and l[i] == ',':
                    s = [-1,-1,-1]
                    l.append(line[s[0]+1, s[1]])
            return l
        s = ''
        for c in line:
            if c == ',':
                if removeExtraSpaces:
                    while s[0] in '\t ':
                        try: s = s[1:]
                        except IndexError: s = ''
                    while s[-1] in '\t ':
                        try: s = s[:-1]
                        except IndexError: s = ''
                l.append(s)
                s=''
            s += c
        return l


    def __fillMissingRecordFields(self, lol):
        lineCount = len(lol)
        colCount = 0
        for record in lol:
            if len(record) > colCount:
                colCount = len(record)
        for i in range(0, lineCount):
            while len(lol[i]) < colCount:
                lol[i].append("")
        return lol


    def __transpLol(self, lol):
        lineCount = len(lol)
        colCount = len(lol[0])
        for record in lol:
            if len(record) != colCount:
                lol = self.__fillMissingRecordFields(lol)
                break
        l = []
        lol_t = []
        for i in range(0, colCount):
            for j in range(0, lineCount):
                l.append(lol_t[j][i])
            lol_t.append(l)
        return lol_t


    def getCsvAsLol(self, fileName, fieldsRequireDoubleQuotes=True, forceValueConversion=True, invertRowCol=False, removeExtraSpaces=True):
        lol = []
        with open(fileName, 'r') as f:
            fileString = f.readlines()
        for line in fileString:
            record = self.__lineToListOfStrings(line, fieldsRequireDoubleQuotes, removeExtraSpaces)
            if forceValueConversion:
                for i in range(0, len(record)):
                    try: record[i] = literal_eval(record[i])
                    except: pass
        lol = self.__fillMissingRecordFields(lol)
        if invertRowCol:
            return self.__transpLol(lol)
        return lol


    def getRecord(self, fileName, recordID=-1, fieldsRequireDoubleQuotes=True, forceValueConversion=True, invertRowCol=False, removeExtraSpaces=True):
        lol = self.getCsvAsLol(fileName, fieldsRequireDoubleQuotes, forceValueConversion, invertRowCol, removeExtraSpaces)
        if type(recordID) is int:
            return lol[recordID]
        if type(recordID) is str:
            for i in range(0, len(lol)):
                if lol[i][0] == recordID:
                    return lol[i]
        raise SyntaxError("The recordID needs to be either an integer or a string identical to the record's first column's field")


    def getField(self, fileName, recordID, columnID, fieldsRequireDoubleQuotes=True, forceValueConversion=True, invertRowCol=False, removeExtraSpaces=True):
        lol = self.getCsvAsLol(fileName, fieldsRequireDoubleQuotes, forceValueConversion, invertRowCol, removeExtraSpaces)
        if type(recordID) is int:
            i = recordID
        if type(columnID):
            j = columnID
        if type(recordID) is str:
            for i in range(0, len(lol)):
                if lol[i][0] == recordID:
                    break
        else:
            raise SyntaxError("The recordID needs to be either an integer or a string identical to the record's first column's field")
        if type(columnID) is str:
            for i in range(0, len(lol[i])):
                if lol[0][j] == columnID:
                    break
        else:
            raise SyntaxError("The columnID needs to be either an integer or a string identical to the column's first line's field")
        return lol[i][j]


    def writeCsvFromLol(self, lol, fileName, backupOld=True, backupNew=False, invertRowCol=False):
        if backupOld: copy(fileName, fileName+'.bak.old')
        with open(fileName, 'w+') as f:
            for i in range(0, len(lol)):
                line = ''
                for j in range(0, len(lol[i]) - 1):
                    line = line + '"' + str(lol[i][j]) + '",'
                line = line + '"' + str(lol[i][-1]) + '"'
                f.writelines(line)
        lol = self.__fillMissingRecordFields(lol)
        if backupNew: copy(fileName, fileName + '.bak')
        if invertRowCol:
            return self.__transpLol(lol)


    def editCsvField(self, lol, fileName, recordID, columnID, value, backupOld=True, backupNew=False, invertRowCol=False):
        if type(recordID) is int:
            i = recordID
        if type(columnID):
            j = columnID
        if type(recordID) is str:
            for i in range(0,len(lol)):
                if lol[i][0] == recordID:
                    break
        else:
            raise SyntaxError("The recordID needs to be either an integer or a string identical to the record's first column's field")
        if type(columnID) is str:
            for i in range(0, len(lol[i])):
                if lol[0][j] == columnID:
                    break
        else:
            raise SyntaxError("The columnID needs to be either an integer or a string identical to the column's first line's field")
        lol[i][j] = value
        self.writeCsvFromLol(lol, fileName, backupOld, backupNew, invertRowCol)


    def editRecord(self, fileName, record, fieldsRequireDoubleQuotes=True, forceValueConversion=True, invertRowCol=False, removeExtraSpaces=True, backupOld=True, backupNew=False):
        lol = self.getCsvAsLol(fileName, fieldsRequireDoubleQuotes, forceValueConversion, invertRowCol, removeExtraSpaces)
        for i in range(0, len(lol)):
            if lol[i][0] == record[0]:
                lol[i] = record
                break
        self.writeCsvFromLol(lol, fileName, backupOld, backupNew, invertRowCol)


    def appendRecord(self, fileName, record, fieldsRequireDoubleQuotes=True, forceValueConversion=True, invertRowCol=False, removeExtraSpaces=True, backupOld=True, backupNew=False):
        lol = self.getCsvAsLol(fileName, fieldsRequireDoubleQuotes, forceValueConversion, invertRowCol, removeExtraSpaces)
        lol.append(record)
        self.writeCsvFromLol(lol, fileName, backupOld, backupNew, invertRowCol)

