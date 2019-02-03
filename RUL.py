
#fhand = open('JanuraryPatents.xml')
fhand = input('The File You Want to Use: ')
myFile = input('Give me a new file name: ')
f = open(myFile,'w+')
for line in fhand:
    if line.startswith('<?xml'):
        continue
    if line.startswith('<!DOCTYPE'):
        continue
    f.write(line)
