from random import *
import re

with open("chickenActin.txt","r") as f:
    seq = f.read()
seq = seq.replace(" ","")
seq = seq.replace("\n","")
seq = seq.replace("\r","")

#Generate Random ACTG Sequence
def generateRandomSequence(length):
    sequence = []
    nucleotides = ["A","C","T","G"] #Get it outside as CAPS
    for i in range(length):
        sequence.append(nucleotides[randint(0,3)])
    return "".join(sequence)

#Pack Generated Sequence into 3 Codon Possibilities
def packSequenceIntoCodons(sequence):
    sequenceLength = len(sequence)
    class codonList: #Have a 2D Array, classes are global
        shiftNone = []
        shiftOne = []
        shiftTwo = []
    for i in range(0, sequenceLength, 3):
        #Check Remaining Length
        if i <= sequenceLength-3:
            codonList.shiftNone.append(str(sequence[i:i+3]))
    for i in range(1, sequenceLength, 3):
        if i <= sequenceLength-3:
            codonList.shiftOne.append(str(sequence[i:i+3]))
    for i in range(2, sequenceLength, 3):
        if i <= sequenceLength-3:
            codonList.shiftTwo.append(str(sequence[i:i+3]))
    return codonList

#Sort Lists of Codons for Start and Stop
def sortStartStopCodon(codonList):
    startCodonPositions = []
    stopCodonPositions = []
    stopCodonTypes = []
    for codonIndex, codon in enumerate(codonList):
        #Sort for START
        if codon == "ATG":
            startCodonPositions.append(codonIndex)
        #Sort for STOP
        if codon == "TAA" or codon == "TAG" or codon == "TGA":
            stopCodonPositions.append(codonIndex)
            stopCodonTypes.append(codon)
    return {"start":startCodonPositions, "stop":stopCodonPositions,"stopTypes":stopCodonTypes}

#Find Longest Potential ORF based on Codon List
def findORF(startCodonPositions,stopCodonPositions):
    currentORF = [None]
    ORF_length = 0
    multipleORF = False
    for startIndex in startCodonPositions:
        for stopIndex in stopCodonPositions:
            #Condition 1: START before STOP
            if startIndex < stopIndex:
                #Conditon 2: No Other STOPS between Current START and STOP
                prevStopIndex = stopCodonPositions[stopCodonPositions.index(stopIndex)-1]
                if not(prevStopIndex > startIndex and prevStopIndex < stopIndex):
                    #Condition 3: Length Condition
                    temp_ORF_length = stopIndex - startIndex
                    if temp_ORF_length > ORF_length:
                        ORF_length = temp_ORF_length
                        currentORF[0]=[startIndex, stopIndex]
                    if temp_ORF_length == ORF_length and currentORF[0] != [startIndex,stopIndex]:
                        multipleORF = True
                        currentORF.append([startIndex,stopIndex])
    return {"ORF Coordinates":currentORF,"ORF Length":ORF_length, "Multiple ORFs?":multipleORF}

#Execution
#Generate Sequence
#foundSequence = generateRandomSequence(5000)
print(seq)

#2 Lists of Start and Stop Codons
start_stop_shiftNone = sortStartStopCodon(packSequenceIntoCodons(seq).shiftNone)
start_stop_shiftOne = sortStartStopCodon(packSequenceIntoCodons(seq).shiftOne)
start_stop_shiftTwo = sortStartStopCodon(packSequenceIntoCodons(seq).shiftTwo)
#Longest ORF in Each Reading Frame
ORF_shiftNone = findORF(start_stop_shiftNone['start'],start_stop_shiftNone['stop'])
ORF_shiftOne = findORF(start_stop_shiftOne['start'],start_stop_shiftOne['stop'])
ORF_shiftTwo = findORF(start_stop_shiftTwo['start'],start_stop_shiftTwo['stop'])

#Print Stats
ORF = max(ORF_shiftNone["ORF Length"],ORF_shiftOne["ORF Length"],ORF_shiftTwo["ORF Length"])
print ("ORF = " + str(ORF))
#Detailed Stats
if ORF == ORF_shiftNone["ORF Length"]:
    print("Found from: Shift None\n"+str(ORF_shiftNone))
    print("Frame Shift 0: " + str(start_stop_shiftNone))
elif ORF == ORF_shiftOne["ORF Length"]:
    print("Found from: Shift One\n"+str(ORF_shiftOne))
    print("Frame Shift 1: " + str(start_stop_shiftOne))
else:
    print("Found from: Shift Two\n"+str(ORF_shiftTwo))
    print("Frame Shift 2: " + str(start_stop_shiftTwo))
