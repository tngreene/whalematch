#!/usr/bin/python
# -*- coding: utf-8 -*-

from cv2 import imread
from keras.models import load_model
from PIL import Image
import numpy as np
import vlc

"""
Predict
This script loads a pre-trained CNN model and classifies whale blowholes based
on a single image
Isaac Vandor
"""

def load(trained_model):
    """ Loads a pre-trained model. """

    model = load_model(trained_model)
    return model

def predict(trained_model, test_image):
    """ Loads an image, resizes it to the size model was trained on,
    corrects the color channels to be similar to the model's channels
    and predicts the blowhole """

    img = Image.open('whaleblowhole509.jpg')
    img = img.resize((75,75), resample=0)     # resize to 200x200 px
    img = img.save('Data/OutputData/temp.jpg')
    img = imread('Data/OutputData/temp.jpg')
    img = img.astype(np.float32)/255.0      # convert to float32
    #img = np.array(img).astype(np.float32)

    # turn image into a 1-element batch :
    #img = np.expand_dims(img, axis=0)

    img = img[:,:,::-1]         # convert from RGB to BGR
    # prediction probability vector :
    #result = model.predict(img)
    result = trained_model.predict(np.expand_dims(img, axis=0))[0]
    return result

def find_blowhole(list, dict):
    """ Finds the biggest element in the list and looks for the corresponding
    key in the dictionary

    result: list whose biggest element we're trying to find
    list: dictionary whose key corresponds to the largest element """
    idx = list.argmax(axis=0)    # find the index of the biggest argument

    # most probable item :
    #best_index = np.argmax(result, axis=1)[0]
    # look for the key corresponding to the biggest argument
    decoded = [key for key, value in dict.items() if value == idx]
    return decoded[0]
    #return best_index

if __name__ == "__main__":

    model = load(trained_model='models/model.h5')
    result = predict(trained_model=model, test_image='Data/OutputData/scaledoutput.jpg')

    whale_types = {"A": 0, "B":0, "C": 2, "D":3, "E": 4, "F": 5,
                "G": 6, "H": 7, "I": 8, "J": 9}

    alphabet = find_blowhole(list=result, dict=whale_types)
    print("The blowhole is: ", alphabet)
