from multiprocessing import Pool
from matplotlib import pyplot as plt
import numpy as np
import sys
import cv2
import img_processor

if __name__ == "__main__":
	kaggle_path = '/Users/mumuxi/.kaggle/competitions/planet-understanding-the-amazon-from-space/'
	target = 'train'
	
	
	img = cv2.imread(kaggle_path+target+'-jpg/'+target+'_20.jpg')
	
	
	### --------------     HAZE REMOVAL -------------  ###
	hz_free_img = img_processor.remove_haze(img)
	
	f, axarr = plt.subplots(1,2)
	axarr[0].imshow(img)
	axarr[1].imshow(hz_free_img)
	axarr[0].title.set_text('Before')
	axarr[1].title.set_text('After Haze Removal')
	
	### --------------     ROTATE  -------------  ###
	rotated_img = cv2.rotate(hz_free_img, cv2.ROTATE_180)
	f, axarr = plt.subplots(1,2)
	axarr[0].imshow(hz_free_img)
	axarr[1].imshow(rotated_img)
	axarr[1].title.set_text('Rotate 180')
	
	
	### --------------     FLIP  -------------  ###
	flip_img = cv2.flip(hz_free_img, 0)
	
	f, axarr = plt.subplots(1,2)
	axarr[0].imshow(hz_free_img)
	axarr[1].imshow(flip_img)
	axarr[1].title.set_text('Flip')

	print ('---'*30)
	plt.show()
	
	
	