import random


piDecimalsStr = '1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679'

# THE ALGORITHM ONLY WORKS IF THE LEN OF CUSTOM CHAR TABLE IS A PRIME NUMBER !!!!!!!!!!!!!!!


def buildCustomCharTable(charSwappingDigits):
    table = ''
    """
    first var, minimal:
    for i in range (0, 10):
        table += chr(i+48)
    for i in range (0, 26):
        table += chr(i + 65)
        table += chr(i + 97)
    for i in [44, 46, 58, 59, 61]:
        table += chr(i)
    """
    """
    second var, len97: may have problems with quotes symbols
    for i in range(32, 127):
        table += chr(i)
    for i in [224, 225]:
        table += chr(i)
    """
    for i in range(40, 92):
        table += chr(i)
    for i in range(93, 127):
        table += chr(i)
    for i in [33, 35, 38]:
        table += chr(i)
    csdLen = len(charSwappingDigits)
    slen = len(table)
    for i in range(0, csdLen-1):
        j = int(charSwappingDigits[i:i+2])%slen
        tempTable = table[j] + table[:j]
        try: tempTable += table[j+1:]
        except IndexError: pass
        table = tempTable
    return table


customCharTable = buildCustomCharTable(piDecimalsStr)
maxPasswordLen = 11
separatorLen = 7
tLen = len(customCharTable)
possiblePartLen = 73
possiblePartLenFactor = 0.8




def stringAdapter(string, expectedLen):
    string = str(string)
    tempP = ''
    for c in string:
        if c in customCharTable:
            tempP += c
    string = tempP
    if expectedLen == 0: return string
    if len(string) >= expectedLen:
        string = string[:expectedLen]
    while len(string) < expectedLen:
        string = customCharTable[expectedLen - len(string)] + string
    return string


def separatorCreator(charTableStr, tableIndex, ascendingOrder):
    returnValue = ''
    for i in range(0, separatorLen):
        if ascendingOrder == False:
            returnValue = charTableStr[(i + tableIndex) % tLen] + returnValue
        elif ascendingOrder == True:
            returnValue = returnValue + charTableStr[(i + tableIndex) % tLen]
    return returnValue


def finalEncrStep(string, r):
    encrString = ''
    for c in string:
        encrString += customCharTable[(customCharTable.find(c) * r) % tLen]
    return encrString


def finalEncrStepDecr(string, encrTable):
    decrString = ''
    for c in string:
        decrString += customCharTable[encrTable.find(c)]
    return decrString



def decrypt(message, password):
    message = str(message)
    password = str(password)
    password = stringAdapter(password, maxPasswordLen)
    failureCase = 'Decryption failed.'
    defaultMessIndRange = [0, len(message)]
    messIndRange = defaultMessIndRange
    for r in range(0, tLen):
        encrCharTableGuess = finalEncrStep(customCharTable, r)
        decrMessageGuess = finalEncrStepDecr(message, encrCharTableGuess)
        for ti0 in range(0, tLen):
            sep0Guess = separatorCreator(customCharTable, ti0, False)
            if sep0Guess in decrMessageGuess:
                messIndRange[0] = decrMessageGuess.find(sep0Guess) + separatorLen
                for ti1 in range(0, tLen):
                    sep1Guess = separatorCreator(customCharTable, ti1, True)
                    if sep1Guess in decrMessageGuess:
                        messIndRange[1] = decrMessageGuess.find(sep1Guess)
                        if messIndRange[0] == messIndRange[1]: return ''
                        if messIndRange[0] < messIndRange[1]:
                            messCharRateInd = messIndRange[1] + separatorLen
                            try:
                                messCharRate = int(decrMessageGuess[messCharRateInd] + decrMessageGuess[messCharRateInd + 1])
                            except ValueError:
                                return failureCase
                            passDecrMess = ''
                            for mi in range(messIndRange[0], messIndRange[1], messCharRate):
                                charInd = customCharTable.find(decrMessageGuess[mi])
                                charIndShift = customCharTable.find(password[mi % maxPasswordLen])
                                passDecrMess += customCharTable[(charInd + tLen - charIndShift) % tLen]
                            return passDecrMess
                        messIndRange[1] = defaultMessIndRange[1]
                    messIndRange[1] = defaultMessIndRange[1]
            messIndRange = defaultMessIndRange
    return failureCase


def encrypt(message, password):
    message = str(message)
    message = stringAdapter(message, 0)
    messageLen = len(message)
    password = str(password)
    password = stringAdapter(password, maxPasswordLen)
    encrMessParts = ['', '', '']
    encrMessPLengths = [0, 0, 0]
    # Middle part, scratch building
    try:
        middlePartMessageCharRate = int(possiblePartLen / messageLen)
        if middlePartMessageCharRate == 0: middlePartMessageCharRate = 1
        encrMessPLengths[1] = messageLen * middlePartMessageCharRate
        for i in range(0, encrMessPLengths[1]):
            if i % middlePartMessageCharRate == 0:
                encrMessParts[1] += message[int(i / middlePartMessageCharRate)]
            else:
                encrMessParts[1] += customCharTable[int(random.random() * tLen)]
    except ZeroDivisionError:
        encrMessParts[1] = ''
        middlePartMessageCharRate = 1
    # First and last parts, scratches building
    encrMessPLengths[0] = int(random.random() * possiblePartLen + 1)
    encrMessPLengths[2] = possiblePartLen * 2 - encrMessPLengths[0]
    for p in [0, 2]:
        for i in range(0, encrMessPLengths[p]):
            encrMessParts[p] += customCharTable[int(random.random() * tLen)]
    tempSep = separatorCreator(customCharTable, int(random.random() * tLen), False)
    encrMessParts[0] = encrMessParts[0] + tempSep
    encrMessParts[2] = str(middlePartMessageCharRate % 10) + encrMessParts[2]
    encrMessParts[2] = str(int(middlePartMessageCharRate / 10)) + encrMessParts[2]
    tempSep = separatorCreator(customCharTable, int(random.random() * tLen), True)
    encrMessParts[2] = tempSep + encrMessParts[2]
    #if encrMessParts[1] == '': return encrMessParts[0] + encrMessParts [2]
    # Lengths fixing
    for i in range(0, len(encrMessPLengths)):
        encrMessPLengths[i] = len(encrMessParts[i])
    # Temp joining the 3 parts
    encrMessage = ''
    for i in range(0, len(encrMessParts)): encrMessage += encrMessParts[i]
    encrMessageLen = len(encrMessage)
    # Adding password to the middle part (message char rate EXCLUDED)
    tempString = ''
    middlePartRange = [encrMessPLengths[0], encrMessPLengths[0] + encrMessPLengths[1]]
    for i in range(middlePartRange[0], middlePartRange[1]):
        charInd = customCharTable.find(encrMessage[i])
        charIndShift = customCharTable.find(password[i % maxPasswordLen])
        tempString += customCharTable[(charInd + charIndShift) % tLen]
    encrMessParts[1] = tempString
    # Actually joining the 3 parts
    encrMessage = ''
    for i in range(0, len(encrMessParts)): encrMessage += encrMessParts[i]
    encrMessageLen = len(encrMessage)
    # applying the security algorithm
    rn = int(random.random() * (tLen - 1) + 1)
    encrMessage = finalEncrStep(encrMessage, rn)
    for i in range(0, 100):
        if decrypt(encrMessage, password) == stringAdapter(message, 0):
            return encrMessage

"""
m1 = 'string to encrypt'
p1 = 'password'
em1 = encrypt(m1, p1)
dem1 = decrypt(em1, p1)


print(m1)
print(em1)
print(len(em1))
print(dem1)
print(customCharTable)



print(customCharTable)
print(len(customCharTable))
"""