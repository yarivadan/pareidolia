import glob
import os
import random
import shutil
import sys

def main(argv):
    folder = argv[0]#'./img_align_celeba'
    print (folder)

    train_subdir='data/' + folder + '/train'
    validation_subdir='data/' + folder + '/validation'

    if not os.path.exists('data'):
        os.makedirs('data')
       
    if not os.path.exists(train_subdir):
        os.makedirs(train_subdir)
    if not os.path.exists(validation_subdir):
        os.makedirs(validation_subdir)


    mylist = os.listdir(folder)
    random.shuffle(mylist)

    train_counter = 0
    validation_counter = 0
    train_size=len(mylist)*0.8
    print("total: {}, train:{}", len(mylist), train_size)

            # Randomly assign an image to train or validation folder
    for filename in mylist:
                   
        fileparts = filename.split('.')

        if train_counter <= train_size:
            shutil.copyfile(os.path.join(folder, filename), os.path.join(train_subdir, filename))
            #print(os.path.join(train_subdir, filename))
            train_counter += 1
        else:
            shutil.copyfile(os.path.join(folder, filename), os.path.join(validation_subdir, filename))
            #print(os.path.join(validation_subdir,  filename))
            validation_counter += 1
                       
    print('Copied ' + str(train_counter) + ' images to ' + train_subdir)
    print('Copied ' + str(validation_counter) + ' images to ' + validation_subdir)

if __name__ == "__main__":
   main(sys.argv[1:])
