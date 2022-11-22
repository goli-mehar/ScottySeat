import glob, copy
#in each image txt file, convert labelings over to coco lobeling

#find all .txt files in folder
file_paths = glob.glob('**/labels/*.txt')

# for each file, get contents
for path in file_paths:
    contents = []
    with open(path) as f:
        c = f.read()
        
        c = c.splitlines()
        new_contents = []
        for i in range(0, len(c)):
            
            #extract first character aka the class
            cl = c[i][0]
            
            line = copy.deepcopy(c[i][1:])

            
            #append correct class at beginning of lines
            if cl == '0':
                line = '24' + line
            elif cl == '1':
                line = '56' + line
            elif cl == '2':
                line = '60' + line
            elif cl == '3':
                line = '0' + line
            
            new_contents.append(line)

        new_contents = '\n'.join(new_contents)

    print(path)
    with open(path, 'w') as f:
        f.write(new_contents)

# for each line, 
