#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 10:57:30 2017

@author: navid
"""

"""
to load the model
https://keras.io/getting-started/faq/#how-can-i-save-a-keras-model


#code segment

from keras.models import load_model

classifier.save('cat_dog_model.h5')  # creates a HDF5 file 'my_model.h5'
del classifier  # deletes the existing model

# returns a compiled model
# identical to the previous one
classifier = load_model('cat_dog_model.h5')
"""

from keras.models import load_model


classifier = load_model('cat_dog_model.h5')

#making prediction
import numpy as np
from keras.preprocessing import image 
test_image = image.load_img('dataset/single_prediction/cat_or_dog_2.jpg', target_size=(64, 64))
test_image = image.img_to_array(test_image)
test_image = np.expand_dims(test_image , axis = 0)
result = classifier.predict(test_image)
#training_set.class_indices
if result[0][0] == 1 :
    prediction = ' dog'
else:
    prediction = 'cat'
print (prediction)