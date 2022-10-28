import os, sys, math
import re
from os import listdir
from os.path import isfile, join
from PIL import Image

#!==========
# Helper Methods
#!==========

#Need this as Python has no "natural" way to sort; it sorts like 0, 1, 10, 2, 20, etc
def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)


#!==========
# Variables
#!==========

folderPath = sys.argv[1]
finalFileName = join(folderPath, '_merged.png')
imageFiles = [join(folderPath, f) for f in sorted_alphanumeric(listdir(folderPath)) if isfile(join(folderPath, f))]

spriteWidth = 32
spriteHeight = 32
columnsToKeep = 1
spriteGroupsOnEachRow = 10

currentColumn = 0
currentRow = 0

#!==========
# Functions
#!==========

def merge(img1, img2):
    box = (0, 0, spriteWidth * columnsToKeep, spriteHeight)
    
    offsetX = spriteWidth * columnsToKeep * (currentColumn % spriteGroupsOnEachRow)
    offsetY = spriteHeight * currentRow
    
    img1.paste(img2.crop(box), (offsetX, offsetY))
    
    return img1


#!==========
# MAIN
#!==========

if __name__ == "__main__":
    listToPop = []

    #Check that all images can be opened; if not remove them
    for fileIndex in range(0,len(imageFiles)):
        #Check to see if merged file is in. If so, ignore items
        if imageFiles[fileIndex] == finalFileName:
            listToPop.append(fileIndex)
            os.remove(finalFileName)
            continue
            
        #Try to open the file and see if it's an image; if not remove it from the list
        try:
            Image.open(imageFiles[fileIndex])
        except OSError as error : 
            listToPop.append(fileIndex)
    
    #Get rid of all incorrect indices
    for index in listToPop:
        imageFiles.pop(index)
      
    #Create the initial merged image that we will paste images in
    totalWidth = spriteWidth * columnsToKeep * spriteGroupsOnEachRow
    totalHeight = spriteHeight * math.ceil(len(imageFiles) / spriteGroupsOnEachRow)
    img = Image.new(mode="RGBA", size=(totalWidth, totalHeight))

    #Do the cropping and merging
    for fileIndex in range(0,len(imageFiles)):
        img = merge(img, Image.open(imageFiles[fileIndex]))
        currentColumn = currentColumn + 1
        if currentColumn > 0 and (currentColumn % spriteGroupsOnEachRow) == 0:
            currentRow = currentRow + 1

    #Delete the file if exists, then save the merged file
    if os.path.exists(finalFileName):
        os.remove(finalFileName)
    img.save(finalFileName)
