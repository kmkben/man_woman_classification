# -*- coding: utf-8 -*-
"""man_woman_classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1X5aQOBmYJY0HLg0r3yZHRdEMetrKh3tJ

#GROUP 7: Members

###Patrice GADEGBE
###Kemoko KEITA
"""

from google.colab import drive
drive.mount('/content/drive', force_remount=True)

"""# Load datas"""

from keras.preprocessing.image import ImageDataGenerator

shuffle_data = True
batch = 16
# create a new generator
imagegen = ImageDataGenerator()
# load train data
train = imagegen.flow_from_directory("drive/My Drive/images/train/", class_mode="binary", shuffle=shuffle_data, batch_size=batch, target_size=(224, 224))
# load val data
val = imagegen.flow_from_directory("drive/My Drive/images/validation/", class_mode="binary", shuffle=shuffle_data, batch_size=batch, target_size=(224, 224))

"""# Imports"""

from keras.models import Sequential
from keras.layers import Conv2D, MaxPool2D, Flatten, Dense, InputLayer, BatchNormalization, Dropout, Activation
from keras.optimizers import RMSprop
from keras.applications import VGG16
from keras.utils import to_categorical

"""# Network V1"""

optimizer = 'adam'
objective = 'binary_crossentropy'

# build a sequential model
model_v1 = Sequential()
model_v1.add(InputLayer(input_shape=(224, 224, 3)))

# 1st conv block
model_v1.add(Conv2D(25, (5, 5), activation='relu', strides=(1, 1), padding='same'))
model_v1.add(MaxPool2D(pool_size=(2, 2), padding='same'))
model_v1.add(Dropout(0.25))
# 2nd conv block
model_v1.add(Conv2D(50, (5, 5), activation='relu', strides=(2, 2), padding='same'))
model_v1.add(MaxPool2D(pool_size=(2, 2), padding='same'))
model_v1.add(BatchNormalization())
model_v1.add(Dropout(0.25))
# 3rd conv block
model_v1.add(Conv2D(70, (3, 3), activation='relu', strides=(2, 2), padding='same'))
model_v1.add(MaxPool2D(pool_size=(2, 2), padding='valid'))
model_v1.add(BatchNormalization())
model_v1.add(Dropout(0.25))
# ANN block
model_v1.add(Flatten())
model_v1.add(Dense(units=100, activation='relu'))
model_v1.add(Dense(units=100, activation='relu'))
model_v1.add(Dropout(0.25))
# output layer
model_v1.add(Dense(units=1, activation='sigmoid'))

model_v1.summary()

# compile model
model_v1.compile(loss=objective, optimizer=optimizer, metrics=['accuracy'])
# fit on data for 30 epochs
model_v1.fit(train, epochs=30, batch_size=128, validation_data=val)

"""# Network v2
same network but a differente output layer
"""

optimizer = RMSprop(lr=1e-4)
objective = 'binary_crossentropy'
    
# build a sequential model
model_v2 = Sequential()
model_v2.add(InputLayer(input_shape=(224, 224, 3)))

# 1st conv block
model_v2.add(Conv2D(25, (5, 5), activation='relu', strides=(1, 1), padding='same'))
model_v2.add(MaxPool2D(pool_size=(2, 2), padding='same'))
model_v2.add(Dropout(0.25))
# 2nd conv block
model_v2.add(Conv2D(50, (5, 5), activation='relu', strides=(2, 2), padding='same'))
model_v2.add(MaxPool2D(pool_size=(2, 2), padding='same'))
model_v2.add(BatchNormalization())
model_v2.add(Dropout(0.25))
# 3rd conv block
model_v2.add(Conv2D(70, (3, 3), activation='relu', strides=(2, 2), padding='same'))
model_v2.add(MaxPool2D(pool_size=(2, 2), padding='valid'))
model_v2.add(BatchNormalization())
model_v2.add(Dropout(0.25))
# ANN block
model_v2.add(Flatten())
model_v2.add(Dense(units=100, activation='relu'))
model_v2.add(Dense(units=100, activation='relu'))
model_v2.add(Dropout(0.25))
# output layer
model_v2.add(Dense(units=1, activation='sigmoid'))

model_v2.summary()

# compile model
model_v2.compile(loss=objective, optimizer=optimizer, metrics=['accuracy'])
# fit on data for 30 epochs
model_v2.fit(train, epochs=30, validation_data=val)

"""# Network v3"""

optimizer = RMSprop()
objective = 'binary_crossentropy'

model_v3 = Sequential()
#
model_v3.add(Conv2D(32, kernel_size=(3, 3),
                 activation='relu',
                 input_shape=(224, 224, 3)))
model_v3.add(Conv2D(64, (3, 3), activation='relu'))
model_v3.add(MaxPool2D(pool_size=(2, 2)))
model_v3.add(Dropout(0.25))
#
model_v3.add(Conv2D(64, (3, 3), activation='relu'))
model_v3.add(MaxPool2D(pool_size=(2, 2)))
model_v3.add(Dropout(0.25))
#
model_v3.add(Flatten())
model_v3.add(Dense(128, activation='relu'))
model_v3.add(Dropout(0.5))
#
model_v3.add(Dense(1, activation='sigmoid'))

model_v3.summary()

# compile model
model_v3.compile(loss=objective, optimizer=optimizer, metrics=['accuracy'])
# fit on data for 30 epochs
model_v3.fit(train, epochs=30, validation_data=val)

"""**Network V4**

# VGG learning
"""

optimizer = 'adam'
objective = 'binary_crossentropy'

vgg=VGG16(include_top=False, pooling='avg', weights='imagenet',input_shape=(178, 218, 3))

# Freeze the layers except the last 5
for layer in vgg.layers[:-5]:
 layer.trainable = False

# Create the model
model = Sequential()
# Add the VGG16 convolutional base model
model.add(vgg)
 
# Add new layers
model.add(Dense(128, activation='relu'))
model.add(BatchNormalization())
model.add(Dense(1, activation='sigmoid'))

model.compile(optimizer=optimizer, loss=objective, metrics=['accuracy'])
model.fit(train, epochs=30, batch_size=128, validation_data=val)