#♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪#
#                                   SIC Assembler - Pass 1                                      #
#                                         3/20/2020                                             #
#                              By: Aseel Arafeh && Shaima Wazwaz                                #
#♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪#

import sys
import math
import os
sicFile = open(sys.argv[1], "r")
intermediateFile = open(sys.argv[2], "w")
# sicFile = open("c:/users/wazwaz/documents/sys prog/sic/pass1/test1.asm", "r")
# intermediateFile = open("int.mdt", "w")
OutputFile = open("Pass1_Output.py", "w")
os.system("cls")
SYMPTAB = {}
LITTAB = {}
lineNumber = 0
LOCCTR = "0"
isStart = 0
labelMap = {}
startAddress = "0"
isFirstLine = 0
startCnt = 0


def errorOutput(error, type, lineNumber):
    if type == "withLine":
        errorMessage = "At line " + \
            str(lineNumber) + " : " + error
    else:
        errorMessage = error
    print(errorMessage)
    exit()


for line in sicFile:
    isRESB = 0
    isRESW = 0
    isBYTE = 0
    isWORD = 0
    isLTORG = 0
    instructionSize = "3"
    lineNumber = lineNumber + 1

    if line.strip() == "":
        continue

    if line.strip()[0] == '.':
        continue

    else:

        # 1-8 Label
        label = line[0:8]
        label = label.strip()
        if labelMap.get(label) != None:
            error = "Symbol " + \
                str(label) + " already exists!\n"
            errorOutput(error, "withLine", lineNumber)

        # 10-15 Operation code (or Assembler directive)
        opCode = line[9:15]
        opCode = opCode.strip()

        if isFirstLine == 0:
            isFirstLine = 1
            if opCode != "START":
                error = "Your Program Must Begin With START Directive \n"
                errorOutput(error, "withoutLine", lineNumber)

        if opCode == "START":
            isStart = 1
            startCnt = startCnt + 1
        elif opCode == "RESW":
            isRESW = 1
        elif opCode == "RESB":
            isRESB = 1
        elif opCode == "BYTE":
            isBYTE = 1
        elif opCode == "LTORG":
            isLTORG = 1
        elif opCode == "WORD":
            isWORD = 1

        if not isLTORG:
            # write the line on list file
            intermediateFile.write(line)
            if opCode == "END":
                intermediateFile.write("\n")

        # 18-35 Operand
        operand = line[16:35]
        operand = operand.strip()
        if startCnt > 1:
            error = "Your Program Must Have Only One START Directive \n"
            errorOutput(error, "withoutLine", lineNumber)

        if isStart == 1:
            startAddress = operand
            LOCCTR = startAddress
            PROGNAME = label
            isStart = 0
            continue
        elif isRESW == 1:
            if operand == "":
                error = " Directive " + \
                    opCode + " needs an operand\n"
                errorOutput(error, "withLine", lineNumber)
            instructionSize = hex(int(operand)*3).lstrip("0x")
        elif isRESB == 1:
            if operand == "":
                error = " Directive " + \
                    opCode + " needs an operand\n"
                errorOutput(error, "withLine", lineNumber)
            instructionSize = hex(int(operand)).lstrip("0x")
        elif isBYTE:
            value = operand[2:len(operand) - 1]
            conv = ""
            if operand == "":
                error = " Directive " + \
                    opCode + " needs an operand\n"
                errorOutput(error, "withLine", lineNumber)
            elif operand[0] == 'C':
                for ch in value:
                    conv += hex(ord(ch)).lstrip("0x")
            elif operand[0] == 'X':
                conv = value
            else:
                conv = hex(int(operand, 16)).lstrip("0x")
            instructionSize = hex(math.ceil(len(conv) / 2)).lstrip("0x")
        elif isWORD:
            value = operand[2:len(operand) - 1]
            conv = ""
            if operand == "":
                error = " Directive " + \
                    opCode + " needs an operand\n"
                errorOutput(error, "withLine", lineNumber)
            elif operand[0] == 'C':
                for ch in value:
                    conv += hex(ord(ch)).lstrip("0x")
            elif operand[0] == 'X':
                conv = value
            else:
                conv = hex(int(operand)).lstrip("0x")
            length = math.ceil(len(conv) / 2)
            if length > 3:
                error = " Directive " + \
                    opCode + " can only reserve only three bytes (one word)\n"
                errorOutput(error, "withLine", lineNumber)
            instructionSize = "3"
        elif isLTORG or opCode == "END":
            for literal in LITTAB:
                if LITTAB[literal][2] == -1:
                    LITTAB[literal][2] = (
                        "0"*(4-len(LOCCTR))) + hex(int(LOCCTR, 16)).lstrip("0x")
                    LOCCTR = hex(int(LOCCTR, 16) +
                                 int(str(LITTAB[literal][1]), 16)).lstrip("0x")
                    starLine = "*        " + str(literal) + "\n"
                    intermediateFile.write(starLine)
            continue
        elif len(operand) > 1 and operand[0] == '=' and LITTAB.get(operand) == None:
            value = operand[3:len(operand) - 1]
            conv = ""
            address = -1
            if(operand[1] == 'C'):
                for ch in value:
                    conv += hex(ord(ch)).lstrip("0x")
            else:
                conv = operand[3:len(operand) - 1]
            length = math.ceil(len(conv) / 2)
            LITTAB[operand] = [conv, length, address]
        if label != "":
            temp = hex(int(LOCCTR, 16)).lstrip("0x")
            SYMPTAB[label] = ("0"*(4-len(temp))) + temp
            labelMap[label] = 1
        LOCCTR = hex(int(LOCCTR, 16) + int(instructionSize, 16)).lstrip("0x")

intermediateFile.close()


PROGLEN = hex(int(LOCCTR, 16) - int(startAddress, 16)).lstrip("0x")
# PROGLEN = hex(int(PROGLEN)).replace("0x", "")
whiteBold = "\033[1;37m"
whiteLight = "\033[0;37m"
watermelon = "\033[1;38;5;210m"
blueLight = "\033[1;38;5;85m"
tableBorder = watermelon+"||"+ whiteBold
print(watermelon+"\n\n\(╹O╹)/♪♪  \(╹O╹)/♪♪  \(╹O╹)/♪♪  \(╹O╹)/♪♪ \(╹O╹)/♪♪  \(╹O╹)/♪♪ \(╹O╹)/♪♪  \(╹O╹)/♪♪")
print(whiteBold+"\n\tTHE PRGRAM PASSED PASS1 SUCCESSFULLY!! HERE THE OUTPUT OF PASS 1:\n"+watermelon)
print("┌(^_^)┘♪  ┌(^_^)┘♪ ┌(^_^)┘♪  ┌(^_^)┘♪ ┌(^_^)┘♪  ┌(^_^)┘♪ ┌(^_^)┘♪  ┌(^_^)┘♪ ┌(^_^)┘♪\n\n"+whiteBold)

print("\tO Program Name : " + blueLight + PROGNAME + whiteBold)
print("\tO Program Length : " + blueLight + PROGLEN + whiteBold)
print("\tO SYMPOL TABLE : ")
print(watermelon+"\t\t=================================================="+ whiteBold)
sys.stdout.write("\t\t" + "%-2s %-20s %-2s %-20s %-2s\n"
                 % (tableBorder, "SYMPOL", tableBorder, "ADDRESS", tableBorder))
print(watermelon+"\t\t=================================================="+ whiteBold)
for sym in SYMPTAB:
    sys.stdout.write("\t\t" + "%-2s %-20s %-2s %-20s %-2s\n" %
                     (tableBorder, str(sym), tableBorder, str(SYMPTAB[sym]), tableBorder))
print(watermelon+"\t\t=================================================="+ whiteBold)

print("\tO LITERAL TABLE : ")
print(watermelon+"\t\t==================================================================================================")
sys.stdout.write("\t\t" + "%-2s %-20s %-2s %-20s %-2s %-20s %-2s %-20s %-2s\n"
                 % (tableBorder, "NAME", tableBorder, "VALUE", tableBorder, "LENGTH", tableBorder, "ADDRESS", tableBorder))
print(watermelon+"\t\t==================================================================================================")
for lit in LITTAB:
    sys.stdout.write("\t\t" + "%-2s %-20s %-2s %-20s %-2s %-20s %-2s %-20s %-2s\n"
                     % (tableBorder, str(lit), tableBorder, str(LITTAB[lit][0]), tableBorder, str(LITTAB[lit][1]), tableBorder, str(LITTAB[lit][2]), tableBorder))
print(watermelon+"\t\t=================================================================================================="+whiteLight)

OutputFile.write("PROGNAME = \"" + str(PROGNAME) + "\"\n")
OutputFile.write("PROGLEN = \"" + str(PROGLEN) + "\"\n")
OutputFile.write("startAddress = \"" + str(startAddress) + "\"\n")
OutputFile.write("SYMBTAB = " + str(SYMPTAB)+"\n")
OutputFile.write("LITTAB = " + str(LITTAB)+"\n")

