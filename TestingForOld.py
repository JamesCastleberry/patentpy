# ## Ask the user for the patent file they want to use.
try:
     dataFile = input('The File You Want to Use: ')
     OpenedDataFile = open(dataFile)

except:
     print('ERROR: File does not exist')
     exit()

## Ask the user what they want the final returned csv file to be called
finalFile = input('What You Want the New csv File To Be Named: ')
final = open(finalFile,'w+')
##Create the top row of the csv
final.write('Patent Number,Patent Title,Date Published,Description,Number of Cited Patents,Cited Patent Numbers')
final.write('\n')

counter = 0
patentNumber = 'VOID'
claimcheck = False
patentNumberCheck = True
citedPatNumberCheck = False
patCounter = 0
description = None
date = 'VOID'
patNumbertot = 'VOID'
citedPatNumbs = list()
printedList = ''

#Temporary Use
title = ''
for line in OpenedDataFile:
    if line.startswith('<B561'):
        citedPatNumberCheck = True
        patCounter = patCounter + 1
    if line.startswith('<B110') and patentNumberCheck is True:
        counter = counter + 1
        patentNumberLine = line
        startPatNum = line.find('T>')
        endPatNum = line.find('/')
        patentNumber = line[startPatNum + 2:startPatNum+3] + line[startPatNum + 4:endPatNum - 1]
        patentNumberCheck = False
    if line.startswith('<DOC') and citedPatNumberCheck is True:
         startCitedPatNum = line.find('PDAT>')
         endCitedPatNum = line.find('</PDAT')
         citedPatNumbs.append(line[startCitedPatNum + 5: endCitedPatNum])
    if line.startswith('<CL'):
         claimcheck = True
    if line.startswith('<PARA') and claimcheck is True:
         pointa = line.find('AT>')
         pointb = line.find('</')
         description = line[pointa+3:pointb].replace(',','')
         claimcheck = False
    if line.startswith('</B561'):
        citedPatNumberCheck = False
    if line.startswith('<B540'):
        if patCounter != 0:
                 patNumbertot = patCounter
        patCounter = 0
        frontPoint = line.find('PDAT>')
        endPoint = line.find('/')
        newLine = line[frontPoint+5:endPoint-1]
        title = newLine
    if line.startswith('<B140'):
        startPoint = line.find('T>')
        year = line[startPoint + 2:startPoint + 6]
        month = line[startPoint + 6:startPoint + 8]
        day = line[startPoint + 8:startPoint + 10]
        date = month + '-' + day + '-' + year
    if line.startswith('<PATDOC'):
         patentNumberCheck = True
         if counter > 0:
             printedList = ''
             citedCounter = 0
             for citedPats in citedPatNumbs:
                 printedList = printedList + '      ' + citedPats
                 citedCounter = citedCounter + 1
             citedPatNumbs = list()
             final.write(str(patentNumber) + ',' + title + ',' + str(date) + ',' + str(description) + ',' + str(patCounter) + ',' + str(printedList))
             final.write('\n')
printedList = ''
citedCounter = 0
for citedPats in citedPatNumbs:
     printedList = printedList + '      ' + citedPats
     citedCounter = citedCounter + 1
final.write(str(patentNumber) + ',' + title + ',' + str(date) + ',' + str(description) + ',' + str(patCounter) + ',' + str(printedList))
final.write('\n')
