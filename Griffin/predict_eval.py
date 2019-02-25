import tensorflow as tf
import numpy as np
import os,glob,cv2
import sys,argparse
import fnmatch
import random 

def find_files(directory, pattern):
    results = []
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                results.append(os.path.join(root, basename))
    return results

# First, pass the path of the image
dir_path = os.path.dirname(os.path.realpath(__file__))
# if len(sys.argv) < 2:
#     print("Usage: python predict.py path/to/parking_space/image")
#     sys.exit()
# image_path=sys.argv[1] 
# filename = dir_path +'/' +image_path
# filename = image_path
image_size=100
num_channels=3
images = []

empty_count = 0
empty_pred = 0
occupied_count = 0
occupied_pred = 0


#filenames = find_files('./test_data_resized', '*.jpg')  
filenames = find_files('/code/pkLot/PKLotSegmented/test_data_big', '*.jpg')  
random.shuffle(filenames)


## Let us restore the saved model
sess = tf.Session()
# Step-1: Recreate the network graph. At this step only graph is created.
saver = tf.train.import_meta_graph('empty_occupied_model.meta')
# Step-2: Now let's load the weights saved using the restore method.
saver.restore(sess, tf.train.latest_checkpoint('./'))

# Accessing the default graph which we have restored
graph = tf.get_default_graph()

for filename in filenames:
    
    images = []
    # Reading the image using OpenCV
    image = cv2.imread(filename)
    # Resizing the image to our desired size and preprocessing will be done exactly as done during training
    image = cv2.resize(image, (image_size, image_size), cv2.INTER_LINEAR)
    images.append(image)


    images = np.array(images, dtype=np.uint8)
    images = images.astype('float32')
    images = np.multiply(images, 1.0/255.0) 

    #The input to the network is of shape [None image_size image_size num_channels]. Hence we reshape.
    x_batch = images.reshape(1, image_size,image_size,num_channels)

    # Now, let's get hold of the op that we can be processed to get the output.
    # In the original network y_pred is the tensor that is the prediction of the network
    y_pred = graph.get_tensor_by_name("y_pred:0")

    ## Let's feed the images to the input placeholders
    x = graph.get_tensor_by_name("x:0")
    y_true = graph.get_tensor_by_name("y_true:0")
    y_test_images = np.zeros((1, 2))


    ### Creating the feed_dict that is required to be fed to calculate y_pred 
    feed_dict_testing = {x: x_batch, y_true: y_test_images}
    result=sess.run(y_pred, feed_dict=feed_dict_testing)

    # result is of this format [probabiliy_of_rose probability_of_sunflower]
    #print("%.2f,%.2f" % result[0],result[1])
    if "Empty" in filename:
        empty_count += 1
        if result[0][0] > .5:
            empty_pred += 1
        print("Empty counts: %d %d" % (empty_count,empty_pred))
    elif "Occupied" in filename:
        occupied_count += 1
        if result[0][1] > .5:
            occupied_pred += 1
        print("Occupied counts: %d %d" % (occupied_count,occupied_pred))
