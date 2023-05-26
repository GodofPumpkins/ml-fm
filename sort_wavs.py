import os
from shutil import move
from itertools import groupby
import math

absolute_path = os.path.dirname(__file__)

classes_list = open("algos.txt").readlines()

classes_list = [l.strip('\n\r') for l in classes_list]

def getFileName(patchNumber):
    patch = patchNumber % 32
    if ( patch == 0 ):
        patch = 32
        bank = math.floor(patchNumber / 32)
    else:
        bank = math.floor(patchNumber / 32) + 1
    
    filename = "16bit_synlib" + str(bank).zfill(3) + "_" + str(patch).zfill(2) + ".wav"

    return filename

counter = 0

for algoNumMin1 in range(32):
    algoNum = algoNumMin1 + 1
    print(algoNum)
    relative_path = str(algoNum)
    full_path = os.path.join(absolute_path, relative_path) + "/"
    # print("algo num " + str(algoNum))
    for i, x in enumerate(classes_list):
        # print("i " +  str(i) + " x " + str(x))
        if(int(x) == algoNum):
            # generate the file name for the given patch number
            filename = getFileName(i + 1)
            # move the file into the right folder
            move(absolute_path + "/" + filename, full_path + filename)
            counter = counter + 1
        
print(counter)
