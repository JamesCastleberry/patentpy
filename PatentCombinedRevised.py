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
final.write('Patent Number,Patent Title,Date Published,Description,Number of Cited Patents')
final.write('\n')

counter = 0
patCounter = None
description = None
date = 'VOID'
patNumbertot = 'VOID'
for line in OpenedDataFile:
    if line.startswith('<claim id='):
        counter = counter + 1
    if line.startswith('<claim-text'):
        pointa = line.find('>')
        pointb = line.find('/')
        description = line[pointa+1:pointb-2].replace(',','')
    if line.startswith('<patcit'):
        patCounter = patCounter + 1
    if line.startswith('<invention-title'):
        if patCounter != None:
                patNumbertot = patCounter
        patCounter = 0
        frontPoint = line.find('>')
        endPoint = line.find('/')
        newLine = line[frontPoint+1:endPoint-1]
        title = newLine
    if line.startswith('<us-patent-grant'):
        if counter > 0:
            final.write(str(counter) + ',' + title + ',' + str(date) + ',' + str(description) + ',' + str(patNumbertot))
            final.write('\n')
        pointa2 = line.find('date-publ')
        pointb2 = line.find('>')
        startYear = pointa2 + 11
        endYear = pointa2 + 15
        startMonth = pointa2 + 15
        endMonth = pointa2 + 17
        startDay = pointa2 + 17
        endDay = pointa2 + 19
        date = line[startMonth:endMonth] + '-' + line[startDay:endDay] + '-' + line[startYear:endYear]
final.write(str(counter) + ',' + title + ',' + str(date) + ',' + str(description) + ',' + str(patNumbertot))
final.write('\n')
