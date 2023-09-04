from multiprocessing import Pool
import numpy as np
import cv2
import sys
"""Single image dehazing.
   Create new images in test-clean folders
"""

class Channel_value:
    val = -1.0
    intensity = -1.0
    
class ImageProcessing:
  def __init__(self):
    self.path = '/home/ubuntu/.kaggle/competitions/planet-understanding-the-amazon-from-space/'
    
def find_dark_channel(img): #get darkest RBG channel
    return np.unravel_index(np.argmin(img), img.shape)[2]

def clamp(minimum, x, maximum):
    return max(minimum, min(x, maximum))

def find_intensity_of_atmospheric_light(img, gray,img_width=256):
    """return Atomospheric light A 
       find max intensity of the brightest pixels in the dark channel
    """
    toplist = [Channel_value()] * 2
    dark_channel = find_dark_channel(img)
    coords = np.argwhere(img[:,:,dark_channel] == np.max(img[:,:,dark_channel]) )
    I = [gray[c[0],c[1]] for c in coords]
    return max(I)

def dehaze_function(img, light_intensity, windowSize, t0, w,img_width=256):
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
            dark_channel = find_dark_channel(sliceimg)
            t = 1.0 - (w * img.item(y, x, dark_channel) / light_intensity)
            outimg.itemset((y,x,0), clamp(0, ((img.item(y,x,0) - light_intensity) / max(t, t0) + light_intensity), 255))
            outimg.itemset((y,x,1), clamp(0, ((img.item(y,x,1) - light_intensity) / max(t, t0) + light_intensity), 255))
            outimg.itemset((y,x,2), clamp(0, ((img.item(y,x,2) - light_intensity) / max(t, t0) + light_intensity), 255))
    return outimg

def dehaze_function_tensorflow(img,t0=0.55, w=0.95, N=256, channel=3):
    """" break to batches using tensorflow, however, works but slow. need to learn more tensorflow  """
    light_intensity = A[_id]
    images = tf.reshape(img, [1, N, N, channel], name='image')
    img_patches = tf.extract_image_patches(images=images, ksizes=[1, 10, 10, 1], 
                                      strides=[1, 1, 1, 1], rates=[1, 1, 1, 1], 
                                      padding='VALID')
    with tf.Session() as sess:
        outimg = np.zeros((N,N,channel), 'uint8')
        for y in range(N):
            for x in range(N):
                patch = img_patches[0,y,x,]
                patch = tf.reshape(patch,[10,10,channel]).eval()
                patch[patch==0] = 255
                dark_channel = np.unravel_index(np.argmin(patch), patch.shape)[2]
                t = 1.0 - (w * img.item(y, x, dark_channel) / light_intensity)
#                 print (y,x,dark_channel,light_intensity,img.item(y, x, dark_channel))
                outimg.itemset((y,x,0), clamp(0, ((img.item(y,x,0) - light_intensity) / max(t, t0) + light_intensity), 255))
                outimg.itemset((y,x,1), clamp(0, ((img.item(y,x,1) - light_intensity) / max(t, t0) + light_intensity), 255))
                outimg.itemset((y,x,2), clamp(0, ((img.item(y,x,2) - light_intensity) / max(t, t0) + light_intensity), 255))
        return outimg
    
def calculate_haziness(img):
    """input img array 
       output haziness w (0,1)
    """
    miu, v, sigma = 5.1,2.9,.2461
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #image to gray scale
    A = find_intensity_of_atmospheric_light(img, gray)
    D = img.min(2).sum()/(img.shape[0]*img.shape[1])
    B = img.max(2).sum()/(img.shape[0]*img.shape[1])
    C = B - D
    w = math.e**(-0.5*(miu*(A-D)/A+v*C/A))
    return w

def add_CLAHE(img):
    clahe = cv2.createCLAHE(clipLimit=3., tileGridSize=(8,8))
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)  # convert from BGR to LAB color space
    l, a, b = cv2.split(lab)  # split on 3 different channels
    l2 = clahe.apply(l)  # apply CLAHE to the L-channel
    lab = cv2.merge((l2,a,b))  # merge channels
    outimg = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR) 
    return outimg

def dehaze_img(_id):
    img = read(_id)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    light_intensity = find_intensity_of_atmospheric_light(img,gray)
    haze_free_img = dehaze_function(img, light_intensity, 20, t0=0.55, w=0.95)
    outimg = add_CLAHE(haze_free_img)     
    cv2.imwrite(kaggle_path+f'test_clean/test_{_id}.jpg', outimg)
    
kaggle_path = '/home/ubuntu/.kaggle/competitions/planet-understanding-the-amazon-from-space/'
read = lambda i: cv2.imread(kaggle_path+f'test-jpg/test_{i}.jpg')
# read = lambda i: cv2.imread(kaggle_path+f'train-jpg/train_{i}.jpg')

if __name__ == "__main__": 
    begin = int(sys.argv[1])
    end = int(sys.argv[2])
    d = range(begin,end,1)

    chunks = [d[x:x+1000] for x in range(0, len(d), 1000)]
    pool = Pool(2)
    for rang in chunks:
        print (rang)
        pool.map(dehaze_img,rang)
    pool.close()
    pool.join()
