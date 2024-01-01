from multiprocessing import Pool
from matplotlib import pyplot as plt
import numpy as np
import sys
import cv2
import img_processor
plt.rcParams.update({'font.size': 8})

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

		
	## --------------     ROTATE  -------------  ###
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
	
	### --------------     HAZE REMOVAL 3x2  -------------  ###
#	f, axarr = plt.subplots(2,3)
#	
#	randint = np.random.randint(39000,size=3)
#	randint = [28620,8739,24554 ]
#	for i in range(3):
#		
#		img = cv2.imread('%s%s-jpg/%s_%d.jpg'%(kaggle_path, target,target,randint[i]))
#		hz_free_img = img_processor.remove_haze(img)
#		
#		axarr[0,i].title.set_text('id=%d'%(randint[i]))
#		axarr[0,i].imshow(img)
#		axarr[0,i].axis('off')
#		
#		axarr[1,i].imshow(hz_free_img)
#		axarr[1,i].axis('off')
#		
#		if i ==0:
#			axarr[1,0].title.set_text('After Haze Removal')
#			axarr[0,0].title.set_text('Before:   id=%d '%(randint[0]))

	print ('---'*30)
	plt.show()
	
	
	