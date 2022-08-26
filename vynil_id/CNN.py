# Ref 1: https://www.youtube.com/watch?v=DksRPZGZ9Tk
# Ref 2: https://www.youtube.com/watch?v=NDyQx6dFx9o

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.layers import Activation, Dropout, Flatten, Dense
from tensorflow.keras import backend as K
import matplotlib.pyplot as plt

import os


# dimensions of our images
# Should we change? The recommendation from the tutorial says 150,150
img_width, img_height = 150, 150

# train data & test data path
train_data_dir = 'data/train'
validation_data_dir = 'data/test'
#count train files
nb_train_samples = len([name for name in os.listdir('./data/train/') for name in os.listdir('./data/train/' + name)])
#count test files
nb_validation_samples = len([name for name in os.listdir('./data/test/') for name in os.listdir('./data/test/' + name)])

# batch size = the number of data we feed per epoch
batch_size = 5
# tensorflow channel last (w, h, c)
input_shape = (img_width, img_height, 3)

#################
### CNN Model ###
#################

model = Sequential()
model.add(Conv2D(32, (3, 3), input_shape=input_shape))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(32, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.5))
#below Dense should equal to class number
model.add(Dense(2))
#Activation function use softmax for multiclass (sigmoid is only 2 classes (0,1))
model.add(Activation('softmax'))

#find loss use categorical_crossentropy for multiclass
model.compile(loss='categorical_crossentropy', # binary_crossentropy or categorical_crossentropy
              optimizer='adam',# rmsprop or adagrad or  #adam
              metrics=['accuracy'])

# This is the augmentation configuration we will use for training
train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True)

train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='categorical') #binary # categorical

# Rescale test data and validate
test_datagen = ImageDataGenerator(rescale=1. / 255)

validation_generator = test_datagen.flow_from_directory(
    validation_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='categorical') #binary # categorical

print(validation_generator.class_indices)


#Train model
epochs = 20
#save in history to use in making graph
history = model.fit(
        train_generator,
        steps_per_epoch=nb_train_samples // batch_size,
        epochs=epochs,
        validation_data=validation_generator,
        validation_steps=nb_validation_samples // batch_size)

model.save('vynil_cnn_model.h5')
