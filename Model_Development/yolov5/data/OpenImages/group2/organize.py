import os, glob, shutil


#get file paths

images = "./images/val" #outer path .
detctions = "./labels/val"

#os.mkdir("./images/train")
#os.mkdir("./labels/train")

#image paths 
imag = glob.glob('./images/val/*.jpg')
lab = glob.glob('./labels/val/*.txt')

print(lab)

for i in range(0, int(0.8*len(imag))):
    im = imag[i]

    #im name
    name = im.split('/')[-1]
    name = name.split('.')[0] 
    path = './labels/val/' + name + '.txt'

    la = lab.index(path)
    la = lab[la]

    new_im = './images/train/' + name + '.jpg'
    new_la = './labels/train/' + name + '.txt'

    shutil.move(im, new_im)
    shutil.move(la, new_la)

    
    pass
