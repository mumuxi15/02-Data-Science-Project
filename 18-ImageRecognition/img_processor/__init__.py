#!/usr/bin/env python3
import cv2
import numpy as np 

		
class PhotoEditor:
	def __init__(self):
		return
	
	def clamp(self, minimum, x, maximum):
			return max(minimum, min(x, maximum))
		
	def find_dark_channel(self, img):
		return np.unravel_index(np.argmin(img), img.shape)[2]
		
	def dehaze_function(self, img, light_intensity, windowSize=20, t0=0.55, w=0.95, img_width=256):
		"""output haze_free image
		Sliding windows and calculate transimission coef t
		"""
		outimg = np.zeros(img.shape, img.dtype)
		for y in range(img_width):
			for x in range(img_width):
				x_low = max(x-(windowSize//2), 0)
				y_low = max(y-(windowSize//2), 0)
				x_high = min(x+(windowSize//2), img_width)
				y_high = min(y+(windowSize//2), img_width)
				sliceimg = img[y_low:y_high, x_low:x_high]
				dark_channel = self.find_dark_channel(sliceimg)
				t = 1.0 - (w * img.item(y, x, dark_channel) / light_intensity)
				outimg.itemset((y,x,0), self.clamp(0, ((img.item(y,x,0) - light_intensity) / max(t, t0) + light_intensity), 255))
				outimg.itemset((y,x,1), self.clamp(0, ((img.item(y,x,1) - light_intensity) / max(t, t0) + light_intensity), 255))
				outimg.itemset((y,x,2), self.clamp(0, ((img.item(y,x,2) - light_intensity) / max(t, t0) + light_intensity), 255))
		return outimg
		
		
	def find_intensity_of_atmospheric_light(self, img, gray,img_width=256):
		"""return Atomospheric light I
		find max intensity of the brightest pixels in the dark channel
		"""
		dark_channel = self.find_dark_channel(img)
		coords = np.argwhere(img[:,:,dark_channel] == np.max(img[:,:,dark_channel]) )
		I = [gray[c[0],c[1]] for c in coords]
		return max(I)
	
	def add_CLAHE(self, img):
		clahe = cv2.createCLAHE(clipLimit=3., tileGridSize=(8,8))
		lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)  # convert from BGR to LAB color space
		l, a, b = cv2.split(lab)  # split on 3 different channels
		l2 = clahe.apply(l)  # apply CLAHE to the L-channel
		lab = cv2.merge((l2,a,b))  # merge channels
		return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR) 
		
	def remove_haze(self, img):
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		light_intensity = self.find_intensity_of_atmospheric_light(img,gray)
		new_img = self.dehaze_function(img, light_intensity)
		return self.add_CLAHE(new_img)
	

	
def remove_haze(img):
	
	PS = PhotoEditor()
	img = PS.remove_haze(img)
	return img
