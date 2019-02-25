import numpy as np
import cv2 as cv
from scipy.spatial import distance

from matplotlib import pyplot as plt
from json import dumps,loads
import pprint as pp
from sys import argv, exit
from os import system

from subprocess import call


def load_spaces(definition_file):
    f = open(definition_file,'r')
    spaces = loads(f.read())

    return spaces

def extract_corners(space):
    points = []
    for i in range(4):
        x = int(space['contour']['point'][i]['x'])
        y = int(space['contour']['point'][i]['y'])
        points.append((x,y))
    return points

def extract_space(img,id,rot_rect,new_size=None):
    """
    This function "extracts" a parking space from a larger image of a parking lot and saves
    the "thumbnail" size space.
    Params:
        img (image): opencv2 image resource
        id (int): integer space id
        rot_rect (json): a dictionary of data representing the space
        new_size (tuple): size of space e.g. (64,64)
    """

    rows,cols,z = img.shape

    # pull values out of dictionary
    x = int(rot_rect['center']['x'])
    y = int(rot_rect['center']['y'])
    w = int(rot_rect['size']['w'])
    h = int(rot_rect['size']['h'])
    d = int(rot_rect['angle']['d'])


    # Use open cv to define a rotation matrix that rotates
    # around x,y by d degrees.
    M = cv.getRotationMatrix2D((x,y),d,1)

    # Apply the rotation and save in dst
    dst = cv.warpAffine(img,M,(cols,rows))
    cv.rectangle(dst, (x-int(w/2),y-int(h/2)), (x+int(w/2),y+int(h/2)), (255,255,0),1, 8,0)
    cv.imshow('space'+str(id),dst)
    # wait for key to be hit before closing
    cv.waitKey(0)

    # Use list slicing to crop the space out of the larger rotated image
    crop_img = dst[y-int(h/2):y+int(h/2), x-int(w/2):x+int(w/2)]
    
    # write that space to our folder
    cv.imwrite('./spaces/'+str(id)+'.png',crop_img)
    cv.imshow('space'+str(id),crop_img)
    # wait for key to be hit before closing
    cv.waitKey(0)

    # if space is wider than high, rotate it so its like the others
    # if we make the image square, then maybe it won't matter?
    if w > h:
        rotate = ' '.join(["convert", "./spaces/"+str(id)+".png -rotate", str(90) ,"./spaces/"+str(id)+".png"])

        # python calling bash to run imagemagick
        system(rotate)

    # if a new_size tuple is passed in, then resize the space 
    if not new_size is None:
        cw,ch = new_size

        resize = ' '.join(["convert", "./spaces/"+str(id)+".png -resize", "!"+str(cw)+"x!"+str(ch) ,"./spaces/"+str(id)+".png"])

        # python calling bash to run imagemagick
        system(resize) 
    

def draw_parking_space(points,img):
    """
    Really just draws a rectangle with four seperate lines
    """
    colors = [(0,0,255),(0,255,0),(255,0,0),(255,255,0)]
    for i in range(4):
        x1 = points[i][0]
        y1 = points[i][1]
        x2 = points[(i+1)%4][0]
        y2 = points[(i+1)%4][1]
        cv.line(img, (x1,y1),(x2,y2),colors[i], 2)

def make_parallelogram(p,type=0):
    """
    Types: 0 = smallest area , 1 = largest area , 2 = avg area
    NOT DONE
    """
    for i in range(4):
        a = p[i]
        b = p[(i+1) % 4]
        dst = distance.euclidean(a,b)
        print(dst)
    print()


def parametric_points(p1,p2,numpoints):
    """
    Generates "numpoints" number of points between point: p1 and point: p2
    Its kinda like interpolation
    """
    # x = x1 + (x2-x1) * t
    # y = y1 + (y2-y1) * t
    points = []
    for i in range(numpoints):
        t = float(i)/float(numpoints)

        x = p1[0] + (p2[0]-p1[0]) * t
        y = p1[1] + (p2[1]-p1[1]) * t
        points.append((round(x),round(y)))

    return points

def new_space_image(pixels,width,height):
    blank_image = np.zeros((height,width,3), np.uint8)

# /p-lot/parking_lot_images/west_virginia

if __name__=='__main__':

    if len(argv) < 3:
        exit()

    

    draw_spaces = False     # If you want the spaces draw on the parking lot image
    test_parametric_points = False 
    show_parking_lot = False
    
    # example python grab_spaces.py definition_file.json pklot_image.png
    definition_file = argv[1]
    image_file = argv[2]

    # Reads in defintion file
    spaces = load_spaces(definition_file)

    # Grabs copy of the image
    img = cv.imread(image_file)

    # Loops through and processes each space
    for space in spaces:
        points = extract_corners(space)
        extract_space(img,space['id'],space['rotatedRect'],(64,64))
        #print(space['rotatedRect'])
        
        if draw_spaces:
            draw_parking_space(points,img)

        if test_parametric_points:
            # Interpolate numpts between two given points
            # probably won't use
            numpts = 100
            pts = parametric_points(points[0],points[1],numpts)
            for p in pts:
                cv.circle(img, p, 2, (0,0,0),1) 
        

    if show_parking_lot:
        # draw parking lot
        cv.imshow('Draw01',img)
        # wait for key to be hit before closing
        cv.waitKey(0)


