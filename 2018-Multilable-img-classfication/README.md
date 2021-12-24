#### System Requirement

------

I used AWS GPU instance (Amazon Cloud service) :

​	 **Image** : Deep Learning AMI (Ubuntu) Version 10.0 

​	 **Instance type** : p2.xlarge

Python Packages: , Keras 2.1.6, Tensorflow, opencv

#### Data

------

Let's get started with downloading following files from kaggle competition  "[Planet: Understanding the Amazon from Space](https://www.kaggle.com/c/planet-understanding-the-amazon-from-space)". 

- train-jpg.tar.7z  
- test-jpg.tar.7z 
- train_v2.csv       -   labels for the train set

Extract jpg from 7z file

``` bash
7za x train-jpg.tar.7z
tar xf train-jpg.tar
```

The dataset consists of 41,789 labeled and 71,000 unlabeled  satellite image chips that look like following. (The labels were added for readers and are separated by space)

<img style="float:left; width:600px;" src="https://i.imgur.com/GsW5QR2.jpg" />

Fig 1. Examples of labeled image chips. Satellite image chips have different labels depending on its content. Each image chip consists of one unique atmospheric label and zero or multiple land use labels. 

- Weather labels: clear, cloudy, hazy, partly cloudy. 
- Land use labels
  - Commonly appeared: primary, agriculture, road, water, cultivation, habitation, bare ground
  - Rare: conventional mine,  selective logging, artisanal mine,  blooming, slash burn, blow down

*Hint: artisanal mine is another word for illegal mine*

The aim is to generate labels for describing the image content and find those labeled artisanal mine. 

#### Pre-process

------

``` python
python3 a00_remove_haze.py
```

The next step is run a00_remove_haze.py, the dehaze function will remove the haze, clear the images and increase image contrast. This improves precision recall significantly especially on the land use labels. The dehaze function is based on  ["Single Image Haze Removal using Dark Channel Prior"](https://www.robots.ox.ac.uk/~vgg/rg/papers/hazeremoval.pdf) paper.

The next step is run a00_remove_haze.py, the dehaze function will remove the haze, clear the images and increase image contrast. This improves precision recall significantly especially on the land use labels. The dehaze function is based on  ["Single Image Haze Removal using Dark Channel Prior"](https://www.robots.ox.ac.uk/~vgg/rg/papers/hazeremoval.pdf) paper.

![How hazy image is formed](https://www.researchgate.net/profile/Seung_Won_Jung2/publication/291385074/figure/fig14/AS:320880610693124@1453515307125/Formation-of-a-hazy-image.png)

In most cases light is scattered in the atmosphere before it reaches the camera and such scattered light is the main cause of blurry images or hazy images. a00_remove_haze.py  function estimates th scattered light intensity as the maximum pixel intensity. Thus by removing the scattered light images can be restored. Following are some examples  of before and after haze removal function. As demonstrated below, it works great on both images labelled clear and hazy.

![How hazy image is formed](https://raw.githubusercontent.com/mumuxi15/mumuxi15.github.io/master/img/rainforest/dehaze.jpg)

#### Build a Neural Network Model

------

To learn fine details we need to increase the model complexity . Here I chose to use one of the latest Neural Network architectures, DenseNet (Dense Convolutional Network), a smarter neural network designed by [Zhuang Liu and Gao Huang](https://arxiv.org/pdf/1608.06993v3.pdf) in  2017. 

The big difference to CNN is that DenseNet connects each layer to every other layer. Whereas traditional convolutional networks layers connect sequentially. DenseNet improved a flow of information and gradients throughout the network, therefore, it has better parameter efficiency and is quicker to train. 

I built a multi output model based on the original DenseNet code and reduced filter number and learning rate as the original model is too memory consuming. I trained the model on the labeled image sets for 4 hours and saved the model as b01_dense121.h5. Then used it to generate labels for images. 

#### How to run

------

- working process
  - EDA.ipynb  (Image labels Analysis, display images before and after haze removed)
  - Planet.ipynb 

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




# Dataflow

<img style="float:left; width:800px; display: block;margin-right: 350px" src="https://i.imgur.com/YQY8Lca.jpg" />