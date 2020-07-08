# -*- coding: utf-8 -*-
"""Speech_recog.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1p30XhWbv-cUYjeJcxF_kvvw5AMGMbVjo
"""

import os
import librosa
import IPython.display as ipd
import matplotlib.pyplot as plt
from scipy.io import wavfile
import warnings
import numpy as np
import tensorflow as tf
#LibROSA and SciPy py libs for processing audio.
warnings.filterwarnings("ignore")

#uploaded folder through zip and extracted it.
# from zipfile import ZipFile
# file_name = "/content/trainf.zip"

# with ZipFile(file_name, 'r') as zip:
#   zip.extractall()
#   print('Done')

!wget http://download.tensorflow.org/data/speech_commands_v0.01.tar.gz

#uploaded folder through zip and extracted it.
# from zipfile import ZipFile
# file_name = "/content/trainf.zip"

# with ZipFile(file_name, 'r') as zip:
#   zip.extractall()
#   print('Done')
#unzip file
import os
os.mkdir("/tmp/data/")
!tar -xf speech_commands_v0.01.tar.gz -C /tmp/data/

os.listdir('/tmp/data/')

!rm -rf /tmp/data/stop/ /tmp/data/on/ /tmp/data/off/ /tmp/data/three/ /tmp/data/two/ /tmp/data/four/ /tmp/data/no/ /tmp/data/bird/ /tmp/data/down/ /tmp/data/up /tmp/data/cat/ /tmp/data/bed/ /tmp/data/five/ /tmp/data/marvin/ /tmp/data/six/ /tmp/data/tree/ /tmp/data/seven/ /tmp/data/house/ /tmp/data/eight/ /tmp/data/go /tmp/data/README.md /tmp/data/testing_list.txt /tmp/data/validation_list.txt /tmp/data/LICENSE /tmp/data/_background_noise_/

os.listdir('/tmp/data/')

#obtaining file path and checking out an example
train_audio_path = '/tmp/data/'
samples, sample_rate = librosa.load(train_audio_path+'yes/0a7c2a8d_nohash_0.wav', sr = 16000)
fig = plt.figure(figsize=(14, 8))
ax1 = fig.add_subplot(211)
ax1.set_title('Raw wave of ' + '../input/train/audio/yes/0a7c2a8d_nohash_0.wav')
ax1.set_xlabel('time')
ax1.set_ylabel('Amplitude')
ax1.plot(np.linspace(0, sample_rate/len(samples), sample_rate), samples)

#sampling rate
ipd.Audio(samples, rate=sample_rate)
print(sample_rate)

#sample rate is 16000hz , resampling to 8000Hz
samples = librosa.resample(samples, sample_rate, 8000)
ipd.Audio(samples, rate=8000)

labels=os.listdir(train_audio_path)

#find count of each label and plot bar graph
no_of_recordings=[]
for label in labels:
    waves = [f for f in os.listdir(train_audio_path + '/'+ label) if f.endswith('.wav')]
    no_of_recordings.append(len(waves))
    
#plot
plt.figure(figsize=(30,5))
index = np.arange(len(labels))
plt.bar(index, no_of_recordings)
plt.xlabel('Commands', fontsize=12)
plt.ylabel('No of recordings', fontsize=12)
plt.xticks(index, labels, fontsize=15, rotation=60)
plt.title('No. of recordings for each command')
plt.show()

labels=['sheila',
 'right',
 'one',
 'nine',
 'wow',
 'yes',
 'happy',
 'zero',
 'left',
 'dog']
#list of label words

#distribution of duration of recordings.
duration_of_recordings=[]
for label in labels:
    waves = [f for f in os.listdir(train_audio_path + '/'+ label) if f.endswith('.wav')]
    for wav in waves:
        sample_rate, samples = wavfile.read(train_audio_path + '/' + label + '/' + wav)
        duration_of_recordings.append(float(len(samples)/sample_rate))
    
plt.hist(np.array(duration_of_recordings))

#resampling into labels
train_audio_path = '/tmp/data/'

all_wave = []
all_label = []
for label in labels:
    print(label)
    waves = [f for f in os.listdir(train_audio_path + '/'+ label) if f.endswith('.wav')]
    for wav in waves:
        samples, sample_rate = librosa.load(train_audio_path + '/' + label + '/' + wav, sr = 16000)
        samples = librosa.resample(samples, sample_rate, 8000)
        if(len(samples)== 8000) : 
            all_wave.append(samples)
            all_label.append(label)

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
y=le.fit_transform(all_label)
classes= list(le.classes_)

from keras.utils import np_utils
y=np_utils.to_categorical(y, num_classes=len(labels))

#conversion to one hot veecs.
all_wave = np.array(all_wave).reshape(-1,8000,1)

#train 80% and validate rest
from sklearn.model_selection import train_test_split
x_tr, x_val, y_tr, y_val = train_test_split(np.array(all_wave),np.array(y),stratify=y,test_size = 0.2,random_state=777,shuffle=True)

#used conv1d layers since it has convolution only in one direction.
from keras.layers import Dense, Dropout, Flatten, Conv1D, Input, MaxPooling1D
from keras.models import Model
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras import backend as K
K.clear_session()

inputs = Input(shape=(8000,1))

#First Conv1D layer
conv = Conv1D(8,13, padding='valid', activation='relu', strides=1)(inputs)
conv = MaxPooling1D(3)(conv)
conv = Dropout(0.3)(conv)

#Second Conv1D layer
conv = Conv1D(16, 11, padding='valid', activation='relu', strides=1)(conv)
conv = MaxPooling1D(3)(conv)
conv = Dropout(0.3)(conv)

#Third Conv1D layer
conv = Conv1D(32, 9, padding='valid', activation='relu', strides=1)(conv)
conv = MaxPooling1D(3)(conv)
conv = Dropout(0.3)(conv)

#Fourth Conv1D layer
conv = Conv1D(64, 7, padding='valid', activation='relu', strides=1)(conv)
conv = MaxPooling1D(3)(conv)
conv = Dropout(0.3)(conv)

#Flatten layer
conv = Flatten()(conv)

#Dense Layer 1
conv = Dense(256, activation='relu')(conv)
conv = Dropout(0.3)(conv)

#Dense Layer 2
conv = Dense(128, activation='relu')(conv)
conv = Dropout(0.3)(conv)

outputs = Dense(len(labels), activation='softmax')(conv)

model = Model(inputs, outputs)

model.summary()

model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])

es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=10, min_delta=0.0001) 
mc = ModelCheckpoint('best_model.hdf5', monitor='val_acc', verbose=1, save_best_only=True, mode='max')

history=model.fit(x_tr, y_tr ,epochs=100, callbacks=[es,mc], batch_size=32, validation_data=(x_val,y_val))

from matplotlib import pyplot
pyplot.plot(history.history['loss'], label='train')
pyplot.plot(history.history['val_loss'], label='test')
pyplot.legend()
pyplot.show()

#function to predict new audio
def predict(audio):
    prob=model.predict(audio.reshape(1,8000,1))
    index=np.argmax(prob[0])
    return classes[index]

#making predictions on validtion data
import random
index=random.randint(0,len(x_val)-1)
samples=x_val[index].ravel()
print("Audio:",classes[np.argmax(y_val[index])])
ipd.Audio(samples, rate=8000)

print("Text:",predict(samples))

#zip did not accomadate all (first attempt zip scattered all files in one common folder)
# used !wget unzip works.