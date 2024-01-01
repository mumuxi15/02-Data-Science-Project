#### Goals

_________________________________________________________________

Given a set of labeled satellite image chips, the project aims to develop an algorithm for labeling unlabeled image chips. The primary focus is on detecting the occurrence of 'artisanal mining,' commonly referred to as illegal mining, among a set of 16 labels categorized into three main groups: <span style="color:SALMON">  atmospheric conditions</span>,  <span style="color:LightSkyBlue"> common land uses</span> and  <span style="color:Plum"> rare land uses</span>. Image chips may receive none or more than one label from these groups.

The main objectives include:

1. **Train a Model with Labeled Image Chips:**
    - Develop an algorithm that effectively labels unlabeled satellite image chips, considering atmospheric conditions and land uses as label categories.
2. **Detection of Artisanal Mining (Illegal Mining):**
    - Create a model that reliably identifies the presence of 'artisanal mining' (illegal mining) as one of the rare labels among others.
    - Differentiate between various classes of land cover and land use, emphasizing the detection of illegal mining activities.
3. **Improved Understanding of Environmental Conditions:**
    - Utilize the model to enhance the understanding of environmental conditions, particularly in relation to deforestation and illegal mining activities on a global scale.
    - Contribute to the identification and interpretation of patterns and causes of deforestation through the labeled satellite imagery.



##### Challenge

The challenge of the project lies in addressing the highly imbalanced distribution of data labels among the 16 groups. Specifically, the difficulty arises from the fact that the 'artisanal mine' label constitutes less than 1% of the total population.

<p float="left">
    <img src="https://live.staticflickr.com/65535/49626992868_557450fa33.jpg" width="50%" />  <img src="https://lh3.googleusercontent.com/jn0yWdVFz-RplTsir-DZcRs0UYWSouwjwhknKi3J6-f-o4TPWBlL2AGNsKQa0NIBkPJ66XfUfKrB03-BmHo8vDq2dJhf6lZLRuhQmluBukP2V979NtW7NZ-5odX8mhEru029s6PDy40" width="49%" /> <em>Left Figure 1: Examples of image chips with labels.   Right Figure 2: Frequency distribution of labels</em></p>

Key Challenges:

1. **Blurry Image Challenge:**
    - A significant amount of satellite image chips appears to be blurry. Therefore a dehazing function may be necessary to enhance the clarity of these images before feeding them into the model.
    - Addressing blurry images is crucial for ensuring that the model can effectively learn and make accurate predictions, particularly in regions where haziness may impact the interpretability of features.
2. **Imbalanced Data Distribution:**
    - Imbalanced data can lead to model bias, where the model may struggle to accurately identify and classify the minority class due to insufficient examples for learning.
3. **Model Training Complexity:**
    - The model needs to be trained to handle the rarity of the 'artisanal mine' label while maintaining performance across the other more prevalent labels.
4. **Data Augmentation and Sampling Strategies:**
    - Balancing techniques, such as oversampling, undersampling, or the use of synthetic data, may need to be implemented to ensure fair learning across all classes.



#### System Requirement

------

AWS GPU instance (Amazon Cloud service) :

​	 **Image** : Deep Learning AMI (Ubuntu) Version 10.0 

​	 **Instance type** : p2.xlarge

Python Packages: , Keras 2.1.6, Tensorflow, opencv

Data Source  "[Planet: Understanding the Amazon from Space](https://www.kaggle.com/c/planet-understanding-the-amazon-from-space)". 



#### Process Data

------

``` python
python3 image_test.py
```

How was the image data processed?

The preprocessing of image data in a machine learning project involves several steps to prepare the data for training a model.

1. **Data Augmentation: Flip and Rotation:**

    - This could include random rotations, flips, zooming, and other transformations to generate variations of the original images.

2. **Handling Blurry Images:**

    - A significant amount of images are quite blurry due to the interference of turbulent air when light passes through the atmosphere. A dehazing function is applied to improve the clarity of the images. The dehazing process involves the estimation of atmospheric light, denoted as ***I***,  and can be used to subtract it from the image to obtain a haze-free image. The estimation of ***I*** is accomplished by identifying it as the maximum intensity among the brightest pixels in the dark channel of the image ^[1]^

3. **Handling Imbalanced Data:**

    - Using specialized loss functions such as binary cross-entropy, it is effective in handling imbalanced data by assigning higher penalties for misclassifying. 

4. **Feature Extraction:**

    - Feature extraction techniques have been employed using **Recurrent Neural Networks** (RNNs) and **DenseNet**

5. **Label Encoding:**

    - For labels are in a categorical form (e.g., 'cloudy','road , 'water'), they may be encoded into numerical format. One-hot encoding is a common technique for handling categorical labels in multi-label classification.

        

The outcome of the dehazing function is quite remarkable – the haze-free image undergoes a significant transformation, becoming considerably brighter and more vivid in color when compared to the original image. This transformation has had a positive impact on the model's performance. In addition to dehazing, we have also incorporated image transformations, such as rotations and flips, as part of our preprocessing pipeline. These transformations serve the purpose of augmenting the dataset, effectively increasing its size and diversifying the samples used for training. 

<img src="https://live.staticflickr.com/65535/53340498376_0a75c43194_c.jpg" width="80%" />
<em>Figure4 : Examples of satellite image chips before and after haze removal</em>



#### Model Explanation 

------

<img style="float:left; width:800px; display: block;margin-right: 350px" src="https://i.imgur.com/YQY8Lca.jpg" />

To capture intricate details, it becomes necessary to enhance the complexity of the model. In this context, I opted to employ one of the most recent advancements in neural network architectures – DenseNet (Dense Convolutional Network). DenseNet is an intelligent neural network design introduced by Zhuang Liu and Gao Huang in 2017.

One fundamental distinction from conventional Convolutional Neural Networks (CNNs) lies in how DenseNet connects its layers. While traditional CNN layers connect in a sequential manner, DenseNet uniquely establishes connections between each layer and every other layer in the network. This innovation significantly improves the flow of both information and gradients throughout the network. Consequently, DenseNet exhibits superior parameter efficiency and quicker training times.

I constructed a multi-output model based on the original DenseNet framework. To make it more memory-efficient, I reduced the filter count and adjusted the learning rate, as the original model tends to be resource-intensive. The model was meticulously trained on labeled image datasets over a duration of four hours, and the resulting model was saved as 'b01_dense121.h5.' Subsequently, this model was leveraged to generate labels for images."

#### How to run

------

- working process
  - EDA.ipynb  (Image labels Analysis, display images before and after haze removed)
  - Planet.ipynb 
  - Image_test (display images before and after dehaze function)
  
- Functions
  - a00_remove_haze.py  
  - a10_densenet_121.py
    -  Stores architecture of DenseNet121
  - a02_custom_metrics.py
    - Define metrics such as precison, recall and F2 score
- Output model
  - b01_dense121.h5 (DenseNet 121)
  - c01_predict.py
    - Predict labels of unlabelled test images





#### Reference

------

The dehaze function is based on  ["Single Image Haze Removal using Dark Channel Prior"](https://projectsweb.cs.washington.edu/research/insects/CVPR2009/award/hazeremv_drkchnl.pdf) paper.

Satellite images often suffer from darkness and blurriness caused by atmospheric turbulence. However, by mitigating the effects of haze and improving image quality, we can enhance the performance of neural networks. Leveraging my understanding of atmospheric physics and conducting research on Google Scholars, I developed a dehaze function based on a [paper](https://www.robots.ox.ac.uk/~vgg/rg/papers/hazeremoval.pdf) to address this challenge. Haze results from the scattering of light in the atmosphere before it reaches the camera. To estimate the intensity of scattered light, a constant value is derived by approximating the maximum pixel intensity within the darkest RGB channel. By utilizing OpenCV to convert images to a colorspace matrix and calculating the haze constant, we can restore the image by subtracting this value. As a result, the dehazed image appears brighter and exhibits better contrast, improving the quality of input data for neural networks.

![How hazy image is formed](https://www.researchgate.net/profile/Seung_Won_Jung2/publication/291385074/figure/fig14/AS:320880610693124@1453515307125/Formation-of-a-hazy-image.png)