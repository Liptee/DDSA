from tkinter import N
from skimage.io import imread, imshow, imsave
from skimage.util import random_noise 
import matplotlib.pyplot as plt
import cv2
import numpy as np

# Функция зашумления 
def shum(img, n): 
    #img - картинка 
    #n - степень зашумления 
    for i in range(n): 
        img = random_noise(img, mode="s&p")
    return img


# Прочитали катинку 
img = imread("/Users/anma/Desktop/Files/Study/Kuz_And/laba1/version_2_0/image_fix/anime1.jpg") 

#Вставляем картинку и степень зашумления 
img = shum(img, 2)
img = img*255

#Для избежания утери части информации надо перевести в юинт8
img = img.astype("uint8") 
imsave("C:/Users/anma/Desktop/Files/Study/Kuz_And/laba1/version_2_0/image_fix/noize_img.jpg", img)

#Применение фильтра
img_del_n = cv2.medianBlur(img,3)
imsave("C:/Users/anma/Desktop/Files/Study/Kuz_And/laba1/version_2_0/image_fix/del_noize_img.jpg", img_del_n)