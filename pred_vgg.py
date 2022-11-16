import tensorflow as tf
import numpy as np
from skimage.color import rgb2lab, lab2rgb, rgb2gray, gray2rgb
from skimage.io import imsave

img_path="test_sunset.jpg"
img = tf.keras.preprocessing.image.load_img(img_path,target_size=(224,224))
img_vgg = tf.keras.preprocessing.image.load_img(img_path,target_size=(150,150))
img = tf.keras.preprocessing.image.img_to_array(img)
img_vgg = tf.keras.preprocessing.image.img_to_array(img_vgg)

lab = rgb2lab(img/256)
X = lab[:,:,0]
print("X shape",X.shape)
imsave("in.jpg",X)
img_vgg /= 255
img_vgg = rgb2gray(img_vgg)
img_vgg = gray2rgb(img_vgg)
img_vgg = img_vgg.reshape((1,150,150,3))
model_path = 'model_vgg_75.h5'
model = tf.keras.models.load_model(model_path)
pred = model.predict(img_vgg)

pred *= 128

final = np.zeros((224,224,3))
print("final shape",final.shape)
final[:,:,0] = lab[:,:,0]
final[:,:,1:] = pred
final = lab2rgb(final)
imsave("out_vgg_sunset_75.jpg",final)

print("Done")