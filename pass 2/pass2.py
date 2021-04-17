#♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪#
#                                   SIC Assembler - Pass 1                                      #
#                                         4/20/2020                                             #
#                              By: Aseel Arafeh && Shaima Wazwaz                                #
#♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪#

from appendix import FORMAT3
from Pass1_Output import SYMBTAB, LITTAB, PROGLEN, PROGNAME, startAddress
import sys
import math
import os

intermediateFile = open(sys.argv[1], "r")
objectFile = open(sys.argv[2], "w")
# intermediateFile = open(
#     "c:/users/wazwaz/documents/sys prog/sic/pass2/int.mdt", "r")
# objectFile = open("./objfile.obj", "w")
os.system("cls")
listingFile = open("listingfile.lst", "w")
lineNumber = 0
LOCCTR = "0"
objCode = []
endAddress = ""


def errorOutput(error, type, lineNumber):
    if type == "withLine":
        errorMessage = "At line " + \
            str(lineNumber) + " : " + error
    else:
        errorMessage = error
    print(errorMessage)
    exit()


for line in intermediateFile:
    isRESB = 0
    isRESW = 0
    isBYTE = 0
    isWORD = 0
    isStart = 0
    isLITRAL = 0
    isEND = 0
    isINDEXED = 0
    instructionSize = "3"
    lineNumber = lineNumber + 1
    currentObjCode = ""

    if line.strip() == "":
        continue

    # 1-8 Label
    label = line[0:8]
    label = label.strip()

    # 10-15 Operation code (or Assembler directive)
    opCode = line[9:15]
    opCode = opCode.strip()

    if opCode == "START":
        isStart = 1
    elif opCode == "RESW":
        isRESW = 1
    elif opCode == "RESB":
        isRESB = 1
    elif opCode == "BYTE":
        isBYTE = 1
    elif opCode == "WORD":
        isWORD = 1
    elif opCode == "END":
        isEND = 1
    elif label == "*":
        isLITRAL = 1
    elif FORMAT3.get(opCode) == None:
        error = "opCode " + \
            str(opCode) + " doesn't exists!\n"
        errorOutput(error, "withLine", lineNumber)

    # 17-35 Operand
    operand = line[16:35]
    operand = operand.strip()

    if isRESW == 1:
        currentObjCode = "??????"
        instructionSize = hex(int(operand)*3).lstrip("0x")
    elif isRESB == 1:
        currentObjCode = "??????"
        instructionSize = hex(int(operand)).lstrip("0x")
    elif isStart:
        LOCCTR = startAddress
        isStart = 0
        LOCCTR = ("0"*(4-len(LOCCTR))) + LOCCTR
        line = line.replace("\n", "")
        listingFile.write(LOCCTR + "\t" + line[0:35] + "\t"+"\n")
        continue
    elif isEND:
        if operand != "":
            if SYMBTAB.get(operand) != None:
                endAddress = SYMBTAB[operand]
            else:
                error = "End Address " + \
                    str(operand) + " doesn't exists!\n"
                errorOutput(error, "withLine", lineNumber)
        else:
            endAddress = startAddress
        LOCCTR = ("0"*(4-len(LOCCTR))) + LOCCTR
        line = line.replace("\n", "")
        listingFile.write("    \t" + line[0:35] + "\t"+"\n")
        continue
    elif isBYTE:
        value = operand[2:len(operand) - 1]
        conv = ""
        if operand[0] == 'C':
            for ch in value:
                conv += hex(ord(ch)).lstrip("0x")
        elif operand[0] == 'X':
            conv = value
        else:
            conv = hex(int(operand)).lstrip("0x")
        currentObjCode = conv
        instructionSize = hex(math.ceil(len(conv) / 2)).lstrip("0x")
    elif isWORD:
        value = operand[2:len(operand) - 1]
        conv = ""
        if operand[0] == 'C':
            for ch in value:
                conv += hex(ord(ch)).lstrip("0x")
        elif operand[0] == 'X':
            conv = value
        else:
            conv = hex(int(operand)).lstrip("0x")
        currentObjCode = conv
        instructionSize = "3"
    elif isLITRAL:
        value = line[12:len(line) - 2]
        conv = ""
        if line[10] == 'C':
            for ch in value:
                conv += hex(ord(ch)).lstrip("0x")
        elif line[10] == 'X':
            conv = value
        else:
            conv = hex(int(value, 16)).lstrip("0x")
        length = math.ceil(len(conv) / 2)
        currentObjCode = conv
        instructionSize = hex(length).lstrip("0x")
    else:
        if operand == "":
            currentObjCode = FORMAT3[opCode]+"0000"
            objCode.append([currentObjCode, instructionSize, LOCCTR])
            LOCCTR = ("0"*(4-len(LOCCTR))) + LOCCTR
            line = line.replace("\n", "")
            line = line[0:36] + (" "*(36-len(line)))
            listingFile.write(LOCCTR + "\t" + line + currentObjCode+"\n")
            LOCCTR = hex(int(LOCCTR, 16) +
                         int(instructionSize, 16)).lstrip("0x")
            continue
        elif operand.find(", X") != -1:
            operand = operand.replace(", X", "")
            isINDEXED = 1
        if(SYMBTAB.get(operand) == None and LITTAB.get(operand) == None):
            error = "operand " + \
                str(operand) + " is not defined\n"
            errorOutput(error, "withLine", lineNumber)
        if SYMBTAB.get(operand) != None:
            currentObjCode = str(FORMAT3[opCode]) + str(SYMBTAB[operand])
        elif LITTAB.get(operand) != None:
            currentObjCode = str(LITTAB[operand][2])
        if isINDEXED:
            currentObjCode = hex(int(currentObjCode, 16) |
                                 int("008000", 16)).lstrip("0x")
    if isLITRAL == 1:
        objCode.append([currentObjCode, instructionSize, LOCCTR])
    else:
        if not isBYTE:
            currentObjCode = ("0"*(6-len(currentObjCode))) + currentObjCode
            objCode.append([currentObjCode, instructionSize, LOCCTR])
        else:
            objCode.append([currentObjCode, instructionSize, LOCCTR])

    LOCCTR = ("0"*(4-len(LOCCTR))) + LOCCTR
    line = line.replace("\n", "")
    line = line + (" "*(35-len(line)))
    # write to the listing file
    if isLITRAL:
        line = line.strip()
        listingFile.write(
            LOCCTR + "\t" + line[0:len(line)] + (" "*(23-len(value)))+currentObjCode+"\n")
    elif currentObjCode != "??????":
        listingFile.write(
            LOCCTR + "\t" + line[0:35] + "\t"+currentObjCode+"\n")
    else:
        listingFile.write(LOCCTR + "\t" + line[0:35] + "\t"+"\n")

    LOCCTR = hex(int(LOCCTR, 16) + int(instructionSize, 16)).lstrip("0x")
maxCapacity = int("1e", 16)
textRecordLen = "0"
currCapacity = 0
startRec = 0
PROGNAME = PROGNAME+(" "*(6-len(PROGNAME)))
currText = ""
startAddress = ("0"*(6-len(startAddress))) + str(startAddress)
PROGLEN = ("0"*(6-len(PROGLEN))) + str(PROGLEN)
prevRec = startAddress
whiteBold = "\033[1;37m"
whiteLight = "\033[0;37m"
yellow = "\033[1;33m"
purple = "\033[1;36m"
blue = "\033[1;35m"
print(whiteBold+"H^" + yellow+PROGNAME+whiteBold+"^"+purple +
      startAddress+whiteBold+"^"+blue+PROGLEN+whiteBold)
objectFile.write("H^"+PROGNAME+"^" + startAddress+"^"+PROGLEN+"\n")
for obj in objCode:
    if int(currCapacity) + int(obj[1], 16) <= maxCapacity and obj[0] != "??????":
        if currCapacity == 0:
            startRec = (obj[2]).upper()
        currCapacity = int(currCapacity) + int(obj[1], 16)
        currText = currText+"^" + obj[0].upper()
        textRecordLen = (hex(int(textRecordLen, 16) +
                             int(obj[1], 16)).lstrip("0x")).upper()
    elif currText != "":
        startRec = (("0"*(6-len(startRec))) + str(startRec)).upper()
        textRecordLen = ("0"*(2-len(textRecordLen))) + str(textRecordLen)
        print("T^"+purple + startRec + whiteBold+"^"+blue +
              str(textRecordLen)+whiteBold + str(currText))
        objectFile.write("T^" + startRec + "^" +
                         str(textRecordLen) + str(currText)+"\n")
        prevRec = hex(int(obj[1], 16) + int(startRec, 16)).lstrip("0x")
        if int(currCapacity) + int(obj[1], 16) >= maxCapacity and obj[0] != "??????":
            currText = "^"+obj[0]
            textRecordLen = obj[1]
            currCapacity = obj[1]
            startRec = obj[2]
        else:
            currText = ""
            textRecordLen = "0"
            currCapacity = 0
    elif obj[0] == "??????":
        startRec = hex(int(obj[1], 16) + int(prevRec, 16)).lstrip("0x")

if currText != "":
    startRec = ("0"*(6-len(startRec))) + str(startRec)
    textRecordLen = ("0"*(2-len(textRecordLen))) + str(textRecordLen)
    print("T^" + purple + startRec + whiteBold+"^"+blue +
          str(textRecordLen)+whiteBold + str(currText))
    objectFile.write("T^" + startRec + "^" +
                     str(textRecordLen) + str(currText)+"\n")

print("E^"+yellow+("0"*(6-len(endAddress))) + endAddress+whiteLight)
objectFile.write("E^"+("0"*(6-len(endAddress))) + endAddress+"\n")
objectFile.close()
listingFile.close()
