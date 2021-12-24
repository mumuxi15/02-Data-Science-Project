"""
Predict labels fro unlabelled image
Set tensorflow environment
source activate tensorflow_p36
Cloudy should have no other labels
"""
import matplotlib.pyplot as plt
from keras.models import load_model
import keras.backend as K
import seaborn as sns
import numpy as np
import pandas as pd
import cv2
from a02_custom_metrics import precision,recall,F2_score
from a01_custom_layer import Scale

def output_labels(i,model=dense):
    weather_, land_ = model.predict(X_val[i].reshape(1,256,256,3))
    label = []
    label.append(weather[np.argmax(weather_, axis=1)[0]])
    b = (land_>0.5)*1
    for i in np.where(b[0]==1)[0]:
        label.append(land_use[i])
    if 'cloudy' in label:
        if len(label) > 1:
            label[0] = 'partly_cloudy'
    title = ' '.join(label)
    return title
    
def expose_mines(rows=4,columns=4,model=dense):
    """display illegal mines
    """
    fig = plt.figure(figsize=(16, 16))
    for i in range(1, columns*rows +1):
        ax = fig.add_subplot(rows, columns, i)
        j = np.random.choice(mines_id)
        img  = X_val[j]
        title = test.tags[j]
        ax.set_title(title)
        ax.set_axis_off()
        plt.imshow(img)
        

kaggle_path = '/home/ubuntu/.kaggle/competitions/planet-understanding-the-amazon-from-space/'
weather = [ 'clear', 'partly_cloudy','cloudy', 'haze']
land_use = ['primary', 'agriculture', 'road', 'water','cultivation', 'habitation','bare_ground', 
        'conventional_mine', 'selective_logging', 'artisinal_mine', 'blooming','slash_burn', 'blow_down' ]
read = lambda i: cv2.imread(kaggle_path+f'test_clean/test_{i}.jpg')

dense = load_model('b01_dense121.h5',custom_objects={'F2_score': F2_score,'Scale':Scale})
X_val = np.array(list(map(read,range(8000))))

test = pd.DataFrame(data=list(map(output_labels,range(0,10000))),columns = ['tags'])
mines_id = test[test.tags.str.contains('artisinal_mine')].index.values

expose_mines()
plt.show()
