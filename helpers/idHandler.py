import shutil
import json
from helpers import paths

"""
    Please notice that ID inheritance takes only one argument, which is the next one to be inherited.
    The full ID will be fetched by each ID subtype calling recursively its parent ID.
"""
"""
    In order to request and create new ID of a certain type, just create a new ID object somewhere
"""
"""
    Format helper:

    "a": that character can take any lower case value, starting from the specified letter, except in case of carries
    "A": that character can take any upper case value, starting from the specified letter, except in case of carries
    "0": that character can take any numerical digit value, starting from the specified one, except in case of carries
    "[t]": that character is fixed and will not change regardless of any ID scrolling
    "": empty ID record. The next ID will be its format
    Other characters cannot be part of an ID
    

    The IDs are scrolled from right to left, as regular numbers do. Check the code below for better understanding.
"""


class IDConfigError(Exception):
    pass


class IDTypeError(Exception):
    pass


class IDFormatError(Exception):
    pass


class IDOverflowError(Exception):
    pass


def getCharType(s):
    if type(s) is not str or len(s) > 1: return 'notChar'
    if s.isdigit(): return 'digit'
    if s.isalpha():
        if s.lower() == s:
            return 'lowerAlpha'
        else:
            return 'upperAlpha'
    return 'symbol'


def checkFormatIntegrity(format):
    openSquareBracket = False
    if type(format) is not str: return False
    for c in format:
        if c == ']':
            if openSquareBracket:
                openSquareBracket = False
            else:
                return False
        elif c == '[':
            openSquareBracket = True
        elif getCharType(c) not in ['digit', 'lowerAlpha', 'upperAlpha']:
            return False
    return True


def checkIDFormatIntegrity(idString, format):
    if not checkFormatIntegrity(format): return False
    if type(idString) is not str: return False
    lf = len(format)
    ls = len(idString)
    if ls == 0: return True
    elif ls != lf : return False
    openSquareBracket = False
    for i in range(0, lf):
        if format[i] == '[': openSquareBracket = True
        if openSquareBracket and idString[i] != format[i]: return False
        if getCharType(idString[i]) != getCharType(format[i]): return False
        if format[i] == ']': openSquareBracket = False
    return True


def nextID(idString, fixedCharacter=False, carry=False):
    if idString == '':
        if not carry:
            return ''
        else:
            raise IDOverflowError("Max partial ID reached for this type.")
    c = idString[-1]
    s = idString[:-1]
    if c == '[': return nextID(s, False, carry) + c
    if fixedCharacter: return nextID(s, fixedCharacter, carry) + c
    if c == ']': return nextID(s, True, carry) + c
    nextc = chr(ord(c) + 1)
    ct = getCharType(c)
    if ct != getCharType(nextc):
        carry = True
        if ct == 'digit':
            return nextID(s, fixedCharacter, carry) + '0'
        elif ct == 'lowerAlpha':
            return nextID(s, fixedCharacter, carry) + 'a'
        elif ct == 'upperAlpha':
            return nextID(s, fixedCharacter, carry) + 'A'
        else:
            raise IDFormatError("Unexpected behavior calling nextID function")
    carry = False
    return s + nextc


class ID():

    def __init__(self, type, getNew=True, reset=False):
        #try:
        with open(paths.idConfig, 'r') as f:
            jsonVar = json.load(f)
        #except:
        #    raise ("A problem occurred while trying to fetch data from ID configuration json file")
        try:
            idData = jsonVar["idTypes"][type]
        except:
            raise IDConfigError("A problem occurred while trying to interpret the ID configuration json file.")
        self.type = type
        try:
            self.format = idData["format"]
            self.parentType = idData["parentType"]
            partialID = "" if reset else idData["lastRecord"]
        except:
            raise IDConfigError(f"Corrupted or missing data for '{type}' ID type.")
        if self.parentType not in jsonVar["idTypes"] and self.parentType != "":
            raise IDConfigError("ParentType not found in ID configuration json file.")
        if not checkFormatIntegrity(self.format):
            raise IDFormatError(f"Illegal format inside '{type}' ID type.")
        if not checkIDFormatIntegrity(partialID, self.format):
            raise IDFormatError(f"Illegal 'lastRecord' format inside '{type}' ID type.")
        if getNew:
            if partialID == "":
                partialID = self.format
            else:
                partialID = nextID(partialID)
        if self.parentType == "":
            parentID = ""
        else:
            parentID = ID(self.parentType, False, False).fullID
        self.partialID = partialID
        self.fullID = parentID + partialID
        if reset or getNew:
            shutil.copyfile(paths.idConfig, paths.idConfig.parent / "idConfid.json.bak.old")
            jsonVar["idTypes"][type]["lastRecord"] = partialID
            with open(paths.idConfig, "w+") as f:
                json.dump(jsonVar, f, indent=4)


"""
    def getFullJson(self):
        with open(projectPath.idConfig, "r") as f:
            jsonVar = json.load(f)
        return jsonVar

    def getIDInfo(self, type, fullJson=None):
        if fullJson == None:
            jsonVar = self.getFullJson()
        return jsonVar[type]
        #ERROR


    def getCurrentPartialID(self, type, fullJson=None):
        return self.getIDInfo(type, fullJson)["lastRecord"]


    def getCurrentFullID(self, type, fullJson=None):
        if type == "": return ""
        idInfo = self.getIDInfo(type, fullJson)
        return self.getCurrentFullID(idInfo["parentType"], fullJson) + self.getCurrentPartialID(type, fullJson)
"""

"""
def getNewID(type, partial = True):
    with open("../config/idConfig.json", "r") as f:
        idJson = json.load(f)
    idJson["idTypes"]["session"]["format"] = "aaaa"
    with open("../config/idConfig.json", "w+") as f:
        json.dump(idJson, f, indent=4)
    if type in idJson.get("idTypes"):
        if partial: return 0
        else: return 1
    else: return -1

print(getNewID("status"))


#lastIdRecordsFilePointer = open("", "w+")
#lastIdRecordsString = lastIdRecordsFilePointer.read()
#lastIdRecords = json.loads(lastIdRecordsString)

def getNextPartialId(ofWhat):
    pass



def getNextFullId(ofWhat):
    pass

idFormatConfig.update(message2 = "it works")
print(idFormatConfig)

"""
