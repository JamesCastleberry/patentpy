#newFile = open('newStart.py')
newFile = input('The File you want to use is :')
for line in newFile:
    if line.startswith('<claim id='):
        pointaa = line.find(' ')
        pointbb = line.find('>')
        print('This is the claim number: ',line[pointaa:pointbb])
    if line.startswith('<claim-text'):
        pointb = line.find('/')
        pointa = line.find('>')
        print('This is the description: ',line[pointa+1:pointb-2])
