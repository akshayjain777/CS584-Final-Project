import tensorflow as tf
import numpy as np
from tensorflow.keras import layers
import os
from tensorflow.keras.applications.vgg16 import VGG16
from skimage.color import rgb2lab, lab2rgb, rgb2gray, gray2rgb
from skimage.io import imshow

img_path = "images/"
img_list = list()
img_new_list = list()

for i in os.listdir(img_path):
    img = tf.keras.preprocessing.image.load_img(img_path+i,target_size=(150,150))
    img_new = tf.keras.preprocessing.image.load_img(img_path+i,target_size=(224,224))
    img = tf.keras.preprocessing.image.img_to_array(img)
    img_new = tf.keras.preprocessing.image.img_to_array(img_new)
    img_list.append(img/256)
    img_new_list.append(img_new/256)
img_list = np.asarray(img_list)


X=list()
Y=list()
for image in img_new_list:
    lab = rgb2lab(image)
    X.append(lab[:,:,0])
    Y.append(lab[:,:,1:]/128)

X=np.array(X)
X=X.reshape(X.shape+(1,))
Y=np.array(Y)

X_vgg = list()
for i, sample in enumerate(img_list):
    sample = rgb2gray(sample)
    sample = gray2rgb(sample)
    X_vgg.append(sample)
X_vgg = np.array(X_vgg)
print("X_vgg",X_vgg.shape)
#encoder
vgg_input = tf.keras.Input(shape = X_vgg.shape[1:])
vgg = VGG16(
    include_top=False,
    weights='imagenet',
    input_tensor=None,
    input_shape=None,
    pooling=None,
    classes=1000,
    classifier_activation='softmax')(vgg_input)
vgg = layers.UpSampling2D((7,7))(vgg)


#decoder
layer1 = layers.Conv2D(128,(3,3), strides = (1,1), padding = 'same')(vgg)
layer1 = layers.Activation('relu')(layer1)

layer2 = layers.UpSampling2D((2,2))(layer1)

layer3 = layers.Conv2D(64,(3,3),strides = (1,1), padding='same')(layer2)
layer3 = layers.Activation('relu')(layer3)

layer4 = layers.Conv2D(64,(3,3),strides=(1,1),padding='same')(layer3)
layer4 = layers.Activation('relu')(layer4)

layer5 = layers.UpSampling2D((2,2))(layer4)

layer6 = layers.Conv2D(32,(3,3),strides=(1,1),padding='same')(layer5)
layer6 = layers.Activation('relu')(layer6)

layer7 = layers.Conv2D(2,(3,3),strides=(1,1),padding='same')(layer6)
layer7 = layers.Activation('tanh')(layer7)

decoder_out = layers.UpSampling2D()(layer7)

model = tf.keras.models.Model(vgg_input,decoder_out)
model.layers[1].trainable = False

print(model.summary())
# model_img = "model_arch.jpg"
# tf.keras.utils.plot_model(model, to_file = model_img, show_shapes=True, show_layer_names=True)

optimizer = tf.keras.optimizers.Adam(learning_rate=0.0001)
model.compile(optimizer=optimizer, loss='mse', metrics=['acc'])

model.fit(X_vgg, Y, epochs = 25, batch_size = 1)
model.save("model.h5")
print("Done")
