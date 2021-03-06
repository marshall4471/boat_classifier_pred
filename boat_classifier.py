# -*- coding: utf-8 -*-
"""boat_classifier.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1DlTm-P33WMtP8d6LtHB6-FKrc1_zJtqO
"""

from sklearn.model_selection import train_test_split

import numpy as np

import tensorflow as tf
from keras import backend as K
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

from keras.layers import Dropout, Flatten, Activation
from keras.layers import Conv2D, MaxPooling2D

from tqdm import tqdm

import zipfile
zip_ref = zipfile.ZipFile("/content/boats.zip", 'r')
zip_ref.extractall("/content/")
zip_ref.close()

from keras.utils import to_categorical

import os

import cv2

from google.colab import drive

drive.mount("/content/Mydrive")

from keras import models

from sklearn.preprocessing import LabelEncoder

from keras.preprocessing.image import ImageDataGenerator

X=[]
Z=[]
IMG_SIZE=286
BOATS_DIR = '/content/boats'
BUOY_DIR='/content/buoy'
CRUISE_SHIP_DIR='/content/cruise ship'
FERRY_BOAT_DIR='/content/ferry boat'
FREIGHT_BOAT_DIR='/content/gondola'
GONDOLA_DIR='/content/gondola'
INFLATABLE_BOAT_DIR='/content/inflatable boat'
KAYAK_DIR='/content/kayak'
PAPER_BOAT_DIR='/content/paper boat'
SAILBOAT_DIR='/content/sailboat'

def is_correct_file(file_name):
    filename, file_extension = os.path.splitext(file_name)
    is_file = os.path.isfile(file_name)
    is_image = file_extension.lower() == ".jpg"
    return is_file and is_image

def assign_label(img,boat_type):
    return boat_type

def make_train_data(boat_type,DIR):
    for img in tqdm(os.listdir(DIR)):
        label=assign_label(img,boat_type)
        path = os.path.join(DIR,img)
        if is_correct_file(path):
            img = cv2.imread(path,cv2.IMREAD_COLOR)
            img = cv2.resize(img, (IMG_SIZE,IMG_SIZE))

            X.append(np.array(img))
            Z.append(str(label))
        
make_train_data('Buoy',BUOY_DIR)

make_train_data('Cruise ship',CRUISE_SHIP_DIR)

make_train_data('Ferry boat',FERRY_BOAT_DIR)

make_train_data('Freight boat',FREIGHT_BOAT_DIR)

make_train_data('Gondola',GONDOLA_DIR)

make_train_data('Inflatable boat',INFLATABLE_BOAT_DIR)

make_train_data('Kayak',KAYAK_DIR)

make_train_data('Paper boat',PAPER_BOAT_DIR)

make_train_data('Sailboat',SAILBOAT_DIR)

le=LabelEncoder()
Y=le.fit_transform(Z)
Y=to_categorical(Y)
X=np.array(X)

x_train,x_test,y_train,y_test=train_test_split(X,Y,test_size=0.30,random_state=42)

datagen = ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.02,
                                   zoom_range = 0.05,
                                   horizontal_flip = True)
datagen.fit(x_train)

cnn = tf.keras.models.Sequential()
cnn.add(tf.keras.layers.Conv2D(filters=16, kernel_size=2, activation='sigmoid', input_shape=[286, 286, 3]))
cnn.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=2))
cnn.add(tf.keras.layers.Conv2D(filters=16, kernel_size=2, activation='sigmoid'))
cnn.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=2))
cnn.add(tf.keras.layers.Flatten())
cnn.add(tf.keras.layers.Dense(9, activation='sigmoid'))
cnn.compile(optimizer = 'adam', loss='binary_crossentropy', metrics=['accuracy'])
cnn.summary()

cnn.fit(datagen.flow(x_train,y_train, batch_size=8),
                    epochs=55, validation_data = (x_test,y_test), verbose = 1)

cnn.save("boat_pred2.h5")

import matplotlib.pyplot as plt

pred=cnn.predict(x_test)
pred_digits=np.argmax(pred,axis=1)

i=0
prop_class=[]
mis_class=[]

for i in range(len(y_test)):
    if(np.argmax(y_test[i])==pred_digits[i]):
        prop_class.append(i)
    if(len(prop_class)==8):
        break

i=0
for i in range(len(y_test)):
    if(not np.argmax(y_test[i])==pred_digits[i]):
        mis_class.append(i)
    if(len(mis_class)==8):
        break

count=0
fig,ax=plt.subplots(4,2)
fig.set_size_inches(8,8)
for i in range (4):
    for j in range (2):
        ax[i,j].imshow(x_test[prop_class[count]])
        ax[i,j].set_title("Predicted boat : "+str(le.inverse_transform([pred_digits[prop_class[count]]])))
        plt.tight_layout()
        count+=1