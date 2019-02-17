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
patentNumberCheck = True
citedPatNumberCheck = False
patCounter = 0
description = None
date = 'VOID'
patNumbertot = 'VOID'
citedPatNumbs = list()
printedList = ''
for line in OpenedDataFile:
    if line.startswith('<doc-number') and patentNumberCheck is True:
        counter = counter + 1
        patentNumberLine = line
        startPatNum = line.find('>')
        endPatNum = line.find('/')
        patentNumber = line[startPatNum + 1:startPatNum+2] + line[startPatNum + 3:endPatNum - 1]
        patentNumberCheck = False
    if line.startswith('<doc-number') and patentNumberCheck is False and line is not patentNumberLine and citedPatNumberCheck is True :
        startCitedPatNum = line.find('>')
        endCitedPatNum = line.find('/')
        citedPatNumbs.append(line[startCitedPatNum + 1: endCitedPatNum - 1])
    if line.startswith('<claim-text'):
        pointa = line.find('>')
        pointb = line.find('/')
        description = line[pointa+1:pointb-2].replace(',','')
    if line.startswith('<patcit'):
        patCounter = patCounter + 1
        citedPatNumberCheck = True
    if line.startswith('</patcit'):
        citedPatNumberCheck = False
    if line.startswith('<invention-title'):
        if patCounter != 0:
                patNumbertot = patCounter
        patCounter = 0
        frontPoint = line.find('>')
        endPoint = line.find('/')
        newLine = line[frontPoint+1:endPoint-1]
        title = newLine
    if line.startswith('<us-patent-grant'):
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
        pointa2 = line.find('date-publ')
        pointb2 = line.find('>')
        startYear = pointa2 + 11
        endYear = pointa2 + 15
        startMonth = pointa2 + 15
        endMonth = pointa2 + 17
        startDay = pointa2 + 17
        endDay = pointa2 + 19
        date = line[startMonth:endMonth] + '-' + line[startDay:endDay] + '-' + line[startYear:endYear]
printedList = ''
citedCounter = 0
for citedPats in citedPatNumbs:
    printedList = printedList + '      ' + citedPats
    citedCounter = citedCounter + 1
final.write(str(patentNumber) + ',' + title + ',' + str(date) + ',' + str(description) + ',' + str(patCounter) + ',' + str(printedList))
final.write('\n')
