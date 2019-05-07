#The following program converts the current version of the U.S. government released Patent XML files to a more readable CSV format.
#The important information that is brought the CSV file about the patents is the Patent Number, Patent Title, Country, Kind of Patent, Date Published,
#Description, Classification CPC Text, and the number of cited patents. To test this, use the xml file 25PatentsCurrent.xml.


## Ask the user for the patent file they want to use.
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
final.write('Patent Number,Patent Title,Country,Kind,Date Published,Description,Classification Cpc Text,Number of Cited Patents,Cited Patent Numbers')
final.write('\n')

##Creating and Initializing the Variables that will be Used
#A counter used to count the number of patents
counter = 0
#A variable that represents the number assigned to each patent
patentNumber = 'VOID'
#A variable that represents the country the patent was published in
patentCountry = 'VOID'
#A variable that checks that the patent number is the patent's and not one of the other document's listed within its content
patentNumberCheck = True
#A variable that checks that the patent country is the patent's and not one of the other doucument's listed within its content
patentCountryCheck = True
#A variable that checks that the patent kind is the patent's and not one of the other document's listed within its content
patentKindCheck = True
#A variable that checks the patent number is of a cited patent and not the patent which cites it
citedPatNumberCheck = False
#A counter used to count the number of cited patents a given patent has
patCounter = 0
#A variable that represents the description of the given patent
description = None
#A variable that represents the date of the given patent
date = 'VOID'
#A variable that represents the total number of cited patents
patNumbertot = 'VOID'
#A variable that is a list of the cited patents
citedPatNumbs = list()
#A variable that represents the contents of citedPatNumbs printed out
printedList = ''
#A variable that is a list of the classification cpc texts of the given patent
classTexts = list()
#A variable that represents the contents of the classTexts printed out
printedClassTexts = ''

##A for loop that runs through each line of the xml file given
for line in OpenedDataFile:
    #If the line represents the doc number of the patent, add 1 to the number of patents, assign the number to the proper variable and store the patent number.
    if line.startswith('<doc-number') and patentNumberCheck is True:
        counter = counter + 1
        patentNumberLine = line
        startPatNum = line.find('>')
        endPatNum = line.find('/doc-numb')
        patentNumber = line[startPatNum + 1:startPatNum+2] + line[startPatNum + 3:endPatNum - 1]
        patentNumberCheck = False
    #If the line represents the country of the patent, assign it to the proper variable
    if line.startswith('<country>') and patentCountryCheck is True:
        startPatCountry = line.find('>')
        endPatCountry = line.find('/')
        patentCountry = line[startPatCountry + 1:endPatCountry - 1]
        patentCountryCheck = False
    #If the line represents the kind of the patent, assign it to the proper variable
    if line.startswith('<kind>') and patentKindCheck is True:
        startPatKind = line.find('>')
        endPatKind = line.find('/')
        patentKind = line[startPatKind + 1: endPatKind - 1]
        patentKindCheck = False
    #If the line represents the doc number of a cited patent, add this doc number to the list of cited patents variable
    if line.startswith('<doc-number') and patentNumberCheck is False and line is not patentNumberLine and citedPatNumberCheck is True :
        startCitedPatNum = line.find('>')
        endCitedPatNum = line.find('/doc-numb')
        citedPatNumbs.append(line[startCitedPatNum + 1: endCitedPatNum - 1])
    #If the line represents classification cpc texts, add them to the list of cpc texts.
    if line.startswith('<classification-cpc'):
        startClassText = line.find('>')
        endClassText = line.find('</classification-cpc')
        classTexts.append(line[startClassText + 1:endClassText].replace(' ',''))
    #If the line is a claim text of the patent, add the description given to the proper variable
    if line.startswith('<claim-text'):
        pointa = line.find('>')
        pointb = line.find('/')
        description = line[pointa+1:pointb-2].replace(',','')
    #If the line starts with the tag of a cited pat, add to the counter of cited pats.
    if line.startswith('<patcit'):
        patCounter = patCounter + 1
        citedPatNumberCheck = True
    if line.startswith('</patcit'):
        citedPatNumberCheck = False
    #If the line starts with the invention title tag of the patent, place the title in the proper variable
    if line.startswith('<invention-title'):
        if patCounter != 0:
                patNumbertot = patCounter
        patCounter = 0
        frontPoint = line.find('>')
        endPoint = line.find('/')
        newLine = line[frontPoint+1:endPoint-1]
        title = newLine
    #If the line is the one that starts a new patent, add all of the info of the previous patent to the csv file, and get the date of the next patent and place it in the proper variable.
    #If this is the first patent, ignore adding to the csv and just get the date.
    if line.startswith('<us-patent-grant'):
        patentCountryCheck = True
        patentNumberCheck = True
        patentKindCheck = True
        if counter > 0:
            printedClassTexts = ''
            printedList = ''
            citedCounter = 0
            for citedPats in citedPatNumbs:
                if printedList is '':
                    printedList = printedList + citedPats
                else:
                    printedList = printedList + '-' + citedPats
                citedCounter = citedCounter + 1
            for classes in classTexts:
                if printedClassTexts is '':
                    printedClassTexts = printedClassTexts + classes
                else:
                    printedClassTexts = printedClassTexts + '-' + classes
            citedPatNumbs = list()
            classTexts = list()
            final.write(str(patentNumber) + ',' + title + ',' + str(patentCountry) + ',' + str(patentKind) + ',' +  str(date) + ',' + str(description) + ',' + str(printedClassTexts) + ',' + str(patCounter) + ',' + str(printedList))
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
## The following lines insures that the proper variables are  reset and adds the info gathered about the final patent to the csv file.
printedList = ''
printedClassTexts = ''
citedCounter = 0
for citedPats in citedPatNumbs:
    if printedList is '':
        printedList = printedList + citedPats
    else:
        printedList = printedList + '-' + citedPats
for classes in classTexts:
    if printedClassTexts is '':
        printedClassTexts = printedClassTexts + classes
    else:
        printedClassTexts = printedClassTexts + '-' + classes
    citedPatNumbs = list()
    citedCounter = citedCounter + 1
final.write(str(patentNumber) + ',' + title + ',' + str(patentCountry) + ',' + str(patentKind) + ',' + str(date) + ',' + str(description) + ',' + str(printedClassTexts) + ',' + str(patCounter) + ',' + str(printedList))
final.write('\n')
