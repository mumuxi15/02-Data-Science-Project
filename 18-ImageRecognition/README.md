#### System Requirement

------

AWS GPU instance (Amazon Cloud service) :

​	 **Image** : Deep Learning AMI (Ubuntu) Version 10.0 

​	 **Instance type** : p2.xlarge

Python Packages: , Keras 2.1.6, Tensorflow, opencv



#### Background

------

The project "Planet: Understanding the Amazon from Space" is in collaboration with Planet, a company that operates a vast constellation of Earth-imaging satellites, and their partner SCCON in Brazil.

The aim is to develop algorithms that can accurately label satellite image chips with information about atmospheric conditions, as well as various classes of land cover and land use. This involves discerning diverse features such as weather conditions, forests, rivers, and more, gold minings. The significance of this challenge lies in better comprehending the occurrence and causes of deforestation on a global scale, and subsequently crafting effective responses.

##### Objective

- Develop a model to label satellite image chips with atmospheric conditions and various classes of land cover and land use such as conventional mine, artisanal mine, blooming, slash burn, blow dow
- Spot those images suggestive of illegal mining activities



#### Data

------

Data Source  "[Planet: Understanding the Amazon from Space](https://www.kaggle.com/c/planet-understanding-the-amazon-from-space)". 

Extract jpg from 7z file

``` bash
7za x train-jpg.tar.7z
tar xf train-jpg.tar
```

The dataset comprises 41,789 labeled and 71,000 unlabeled satellite image chips, visually represented as follows (with added labels for clarity, separated by spaces). Each labelled image chips accompanied by descriptive labels indicating the content of the image. These labeled image chips are characterized by a single distinct atmospheric label and can feature zero or multiple land use labels to further define their content.

<img style="float:left; width:600px;" src="https://i.imgur.com/GsW5QR2.jpg" />

#### Pre-process Data

------

``` python
python3 image_test.py
```

How was the image data preprocessed?

While inspecting the image chips, I noticed that a significant portion of them appeared to be quite blurry. This could be attributed to the interference of turbulent air when light passes through the atmosphere.  Consequently, a critical preprocessing step involved addressing this issue through dehazing. The dehazing process involves the estimation of atmospheric light, denoted as ***I***,  and can be used to subtract it from the image to obtain a haze-free image. The estimation of ***I*** is accomplished by identifying it as the maximum intensity among the brightest pixels in the dark channel of the image ^[1]^ . 



The outcome is quite remarkable – the haze-free image undergoes a significant transformation, becoming considerably brighter and more vivid in color when compared to the original image. This transformation has had a positive impact on the model's performance. In addition to dehazing, we have also incorporated image transformations, such as rotations and flips, as part of our preprocessing pipeline. These transformations serve the purpose of augmenting the dataset, effectively increasing its size and diversifying the samples used for training. 



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

![How hazy image is formed](https://www.researchgate.net/profile/Seung_Won_Jung2/publication/291385074/figure/fig14/AS:320880610693124@1453515307125/Formation-of-a-hazy-image.png)