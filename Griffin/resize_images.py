import time
from datetime import timedelta
import math
import random
import numpy as np
import os,glob
from subprocess import call


classes = ['Empty','Occupied']
train_path = './test_data/'
out_path = './test_data_resized/'

for fields in classes:
    index = classes.index(fields)
    for folder in os.listdir(os.path.join(train_path, fields)):
        count = 1
        path = os.path.join(train_path, fields, folder,'*g')
        files = glob.glob(path)
        for fl in files:
            print(fl)
            call(["convert", "-resize" , "!100x!100" , fl , os.path.join(out_path, fields, str(count)+".jpg")])
            count += 1
