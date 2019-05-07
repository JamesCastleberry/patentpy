#This program will print the total number of patents cited by a given patent.

#Asks the user what file they want to use.
newFile = input('What file you want to use: ')

#A counter that will be used for the cited patents
counter = None

#A for loop that steps through the lines of the file and counts the number of cited patents. If a new patent tag is found, the previous
#number of cited patents is printed and then the counter is reset.
for line in newFile:
    if line.startswith('<patcit'):
        counter = counter + 1
    if line.startswith('<invention-title'):
        if counter != None:
            print('The total number of cited patents was ',counter,'\n')
        counter = 0
        frontPoint = line.find('>')
        endPoint = line.find('/')
        newLine = line[frontPoint+1:endPoint-1]
        print(newLine)
print('The total number of cited patents was ',counter)
