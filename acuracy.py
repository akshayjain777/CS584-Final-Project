
import cv2
import sys
from numpy import dtype
from sewar.full_ref import ssim, psnr




img_path = 'test_sunset.jpg'
img_pred_path = "out_vgg_sunset_75.jpg"

img = cv2.imread(img_path)
img = cv2.resize(img,(224,224))
img_pred = cv2.imread(img_pred_path)


print("SSIM: ",ssim(img,img_pred))
print("PSNR: ",psnr(img,img_pred))
