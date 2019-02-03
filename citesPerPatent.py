#newFile = open('newStart.py')
newFile = input('What file you want to use: ')
counter = None
for line in newFile:
    if line.startswith('<patcit'):
        counter = counter + 1
        #print(line)
    if line.startswith('<invention-title'):
        if counter != None:
            print('The total number of cited patents was ',counter,'\n')
        counter = 0
        frontPoint = line.find('>')
        endPoint = line.find('/')
        newLine = line[frontPoint+1:endPoint-1]
        print(newLine)
print('The total number of cited patents was ',counter)
