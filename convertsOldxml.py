## This is the program that converts the old (Before 2005) US Government XML patent file format to an easy to read CSV file that pulls important
##information about each patent. (The Patent Number, Patent Title, Date Published, Description, Number of Cited Patents, and Cited Patent Numbers.) To test, 
##use the file 25PatentsOld.xml


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

#A variable that will count the number of patents in the file.
counter = 0
#A variable that will store the patent number.
patentNumber = 'VOID'
#A variable that checks if the claim check tag is present.
claimcheck = False
#A variable that checks if the patent is a new patent and not a cited one.
patentNumberCheck = True
#A variable that checks if the patent is a cited patent.
citedPatNumberCheck = False
#A variable that counts the number of cited patents in the file.
patCounter = 0
#A variable that will be the description of the given patent.
description = None
#A variable that will be the date of the given patent.
date = 'VOID'
#A varialbe that will store the final number of patents.
patNumbertot = 'VOID'
#A variable that will be a list of the cited patents.
citedPatNumbs = list()
#A variable that will be the string of cited patents in the list citedPatNumbs
printedList = ''
#A variable that will store the title of the patent.
title = ''

#A for loop that will step through each line of the file.
for line in OpenedDataFile:
     #The tag <B561 is used for cited patents. If this tag is found, then this patent is indeed a cited patent and 1 is added to the 
     #patent counter.
    if line.startswith('<B561'):
        citedPatNumberCheck = True
        patCounter = patCounter + 1
     #The tag <B110 indicates the patent number. If this tag is found, the patent number is taken from the line.
    if line.startswith('<B110') and patentNumberCheck is True:
        counter = counter + 1
        patentNumberLine = line
        startPatNum = line.find('T>')
        endPatNum = line.find('/')
        patentNumber = line[startPatNum + 2:startPatNum+3] + line[startPatNum + 4:endPatNum - 1]
        patentNumberCheck = False
     #The tag <DOC and citedPatNumberCheck will be true when the line contains the cited patent number.
    if line.startswith('<DOC') and citedPatNumberCheck is True:
         startCitedPatNum = line.find('PDAT>')
         endCitedPatNum = line.find('</PDAT')
         citedPatNumbs.append(line[startCitedPatNum + 5: endCitedPatNum])
    #The claim check will be followed by the description tag.
    if line.startswith('<CL'):
         claimcheck = True
    #When this statement is true, the line will contain the description of the patent, and it will be stored in a variable.
    if line.startswith('<PARA') and claimcheck is True:
         pointa = line.find('AT>')
         pointb = line.find('</')
         description = line[pointa+3:pointb].replace(',','')
         claimcheck = False
    #When this statement is true, the information is no longer referring to the cited patent.
    if line.startswith('</B561'):
        citedPatNumberCheck = False
    #When this statement is true, the title of the patent will be pulled from the line.
    if line.startswith('<B540'):
        if patCounter != 0:
                 patNumbertot = patCounter
        patCounter = 0
        frontPoint = line.find('PDAT>')
        endPoint = line.find('/')
        newLine = line[frontPoint+5:endPoint-1]
        title = newLine
    #The tag <B140 is used for the date the patent was released. This date is stored in a variable.
    if line.startswith('<B140'):
        startPoint = line.find('T>')
        year = line[startPoint + 2:startPoint + 6]
        month = line[startPoint + 6:startPoint + 8]
        day = line[startPoint + 8:startPoint + 10]
        date = month + '-' + day + '-' + year
     #This tag indicates the start of a new patent.
    if line.startswith('<PATDOC'):
         patentNumberCheck = True
         #The following lines store the cited patents of the previous patent in a list.
         if counter > 0:
             printedList = ''
             citedCounter = 0
             for citedPats in citedPatNumbs:
                 printedList = printedList + '      ' + citedPats
                 citedCounter = citedCounter + 1
             citedPatNumbs = list()
             #A line is added to the CSV file consisting of all the information of the previous patent stored in the variables mentioned.
             final.write(str(patentNumber) + ',' + title + ',' + str(date) + ',' + str(description) + ',' + str(patCounter) + ',' + str(printedList))
             final.write('\n')
#Once the for loop is left, the information of the final patent must be added to the CSV file.
printedList = ''
citedCounter = 0
for citedPats in citedPatNumbs:
     printedList = printedList + '      ' + citedPats
     citedCounter = citedCounter + 1
final.write(str(patentNumber) + ',' + title + ',' + str(date) + ',' + str(description) + ',' + str(patCounter) + ',' + str(printedList))
final.write('\n')
