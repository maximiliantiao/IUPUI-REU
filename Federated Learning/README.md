# Experiments with Federated Learning and Trigger Backdoor Attacks

Python code used came from these sources:

https://github.com/shaoxiongji/federated-learning

https://github.com/knjcode/cifar2png

https://github.com/kuangliu/pytorch-cifar

https://github.com/UMBCvision/Hidden-Trigger-Backdoor-Attacks

NOTE: Only experiments on CIFAR10 so far.

## Run

To execute a trigger backdoor attack, one must apply a trigger patch ([from Hidden Trigger Backdoor Attacks GitHub repository](https://github.com/UMBCvision/Hidden-Trigger-Backdoor-Attacks)). One must convert the CIFAR10 dataset to PNGs using the [cifar10_unpickle.py](https://github.com/maximiliantiao/IUPUI-REU/blob/main/Federated%20Learning/cifar10_unpickle.py) script and store them into a directory.

In main_nn.py and main_fed.py, load the CIFAR10 dataset using the ImageFolder module rather than from the cifar10 module from Pytorch.

The MLP and CNN models are produced by:
> python main_nn.py [-OPTIONS]

Federated learning with MLP and CNN is produced by:
> python main_fed.py [-OPTIONS]

See the arguments in [options.py](utils/options.py). 

To execute a trigger backdoor attack:
> python main_fed.py --dataset cifar --iid --poison True --src_cate [source image category] --trg_cate [target image category]

# Experiments

## Settings:

Dataset: CIFAR10 (i.i.d) dataset with 10 classes (airplane, automobile, bird, cat, deer, dog, frog, horse, ship, truck)

Trigger pattern: [Trigger Patch 11] (https://github.com/maximiliantiao/IUPUI-REU/blob/main/Federated%20Learning/triggers/trigger_11.png)

Used default arguments for training and testing. See [options.py](utils/options.py) for details.

## Experiment 1: Trigger patch size and Backdoor Attack Success Rate

Trigger pattern size: X px by X px

Trigger pattern location: (1 px, 1 px) or top left corner of images

Poisoning rate: 10% of the training dataset and 100% of testing dataset

Number of malicious clients = 100 (all clients are malicious)

Source category is airplane, Target category is cat

Note: CNN used 20 epochs rather than the default 10.

|                    | MLP          | CNN          |
| ------------------ | ------------ | ------------ |
| Trigger Patch Size | Backdoor ASR | Backdoor ASR |
|  1 px by 1 px      |  7.975%      |  4.878%      |
|  2 px by 2 px      | 14.989%      |  3.825%      |
|  3 px by 3 px      | 39.865%      |  7.184%      |
|  4 px by 4 px      | 78.928%      |  7.613%      |
|  5 px by 5 px      | 91.046%      |  5.128%      |
|  6 px by 6 px      | 93.498%      | 19.369%      |
|  7 px by 7 px      | 98.084%      | 13.303%      |
|  8 px by 8 px      | 98.792%      | 54.048%      |
|  9 px by 9 px      | 98.591%      | 57.034%      |
| 10 px by 10 px     | 99.397%      | 95.915%      |

Source category is airplane, Target category is bird

|                    | MLP          | CNN          |
| ------------------ | ------------ | ------------ |
| Trigger Patch Size | Backdoor ASR | Backdoor ASR |
|  1 px by 1 px      | 15.145%      | 10.034%      |
|  2 px by 2 px      | 30.975%      | 11.076%      |
|  3 px by 3 px      | 56.131%      |  9.854%      |
|  4 px by 4 px      | 95.467%      | 21.452%      |
|  5 px by 5 px      | 98.300%      | 59.649%      |
|  6 px by 6 px      | 99.795%      | 90.163%      |
|  7 px by 7 px      | 99.784%      | 92.745%      |
|  8 px by 8 px      | 99.742%      | 99.413%      |
|  9 px by 9 px      | 99.892%      | 97.594%      |
| 10 px by 10 px     | 99.898%      | 99.681%      |

## Experiment 2: Trigger patch location and Backdoor Attack Success Rate

Trigger pattern size: 5 px by 5 px

Trigger pattern location: (X px, X px) from the top left corner of images

Poisoning rate: 10% of the training dataset and 100% of testing dataset

Number of malicious clients = 100 (all clients are malicious)

Source category is airplane, Target category is cat

Note: CNN used 20 epochs rather than the default 10.

|                        | MLP          | CNN          |
| ---------------------- | ------------ | ------------ |
| Trigger Patch Location | Backdoor ASR | Backdoor ASR |
|  (1 px, 1 px)          |  88.359%     |  73.132%     |
|  (2 px, 2 px)          |  87.416%     |  94.266%     |
|  (3 px, 3 px)          |  87.486%     |  84.283%     |
|  (4 px, 4 px)          |  91.684%     |  80.209%     |
|  (5 px, 5 px)          |  96.931%     |  82.814%     |
|  (6 px, 6 px)          |  92.220%     |  85.372%     |
|  (7 px, 7 px)          |  90.357%     |  89.714%     |
|  (8 px, 8 px)          |  92.656%     |  80.679%     |
|  (9 px, 9 px)          |  89.162%     |  83.547%     |
|  (10 px, 10 px)        |  91.838%     |  83.774%     |
|  (11 px, 11 px)        |  90.000%     |  66.232%     |
|  (12 px, 12 px)        |  89.845%     |  75.151%     |
|  (13 px, 13 px)        |  86.486%     |  81.569%     |
|  (14 px, 14 px)        |  87.350%     |  77.684%     |
|  (15 px, 15 px)        |  85.968%     |  26.589%     |
|  (16 px, 16 px)        |  90.249%     |  71.186%     |

Source category is airplane, Target category is bird

Note: CNN used 20 epochs rather than the default 10.

|                        | MLP          | CNN          |
| ---------------------- | ------------ | ------------ |
| Trigger Patch Location | Backdoor ASR | Backdoor ASR |
|  (1 px, 1 px)          |  92.359%     |  44.684%     |
|  (2 px, 2 px)          |  97.574%     |  70.944%     |
|  (3 px, 3 px)          |  93.304%     |  71.916%     |
|  (4 px, 4 px)          |  90.559%     |  89.646%     |
|  (5 px, 5 px)          |  91.879%     |  87.776%     |
|  (6 px, 6 px)          |  96.478%     |  80.886%     |
|  (7 px, 7 px)          |  96.401%     |  81.785%     |
|  (8 px, 8 px)          |  95.410%     |  92.604%     |
|  (9 px, 9 px)          |  94.086%     |  80.473%     |
|  (10 px, 10 px)        |  94.654%     |  81.250%     |
|  (11 px, 11 px)        |  92.088%     |  68.846%     |
|  (12 px, 12 px)        |  93.468%     |  60.616%     |
|  (13 px, 13 px)        |  92.619%     |  60.133%     |
|  (14 px, 14 px)        |  94.620%     |  64.635%     |
|  (15 px, 15 px)        |  88.912%     |  49.118%     |
|  (16 px, 16 px)        |  93.045%     |  63.565%     |

## Experiment 3: Poisoning Rate and Backdoor Attack Success Rate

Trigger pattern size: 2 px by 2 px

Trigger pattern location: (1 px, 1 px) or top left corner of images

Poisoning rate: X% of the training dataset and 100% of testing dataset

Source category is airplane, Target category is cat

Number of malicious clients = 100 (all clients are malicious)

|                | MLP          | CNN          |
| -------------- | ------------ | ------------ |
| Poisoning Rate | Backdoor ASR | Backdoor ASR |
|   0%           | 15.264%      |  4.094%      |
|   5%           | 16.753%      |  8.799%      |
|  10%           | 40.132%      | 15.993%      |
|  15%           | 38.996%      |  8.620%      |
|  20%           | 68.460%      | 10.416%      |
|  25%           | 58.435%      | 12.369%      |
|  30%           | 75.238%      | 14.527%      |
|  35%           | 76.942%      |  9.337%      |
|  40%           | 89.974%      |  7.599%      |
|  45%           | 87.153%      | 12.668%      |
|  50%           | 91.071%      |  5.685%      |

Source category is airplane, Target category is bird

|                | MLP          | CNN          |
| -------------- | ------------ | ------------ |
| Poisoning Rate | Backdoor ASR | Backdoor ASR |
|   0%           | 12.195%      | 11.688%      |
|   5%           | 15.121%      | 16.582%      |
|  10%           | 39.726%      | 29.180%      |
|  15%           | 33.438%      | 67.766%      |
|  20%           | 48.076%      | 94.806%      |
|  25%           | 62.116%      | 96.746%      |
|  30%           | 83.698%      | 93.555%      |
|  35%           | 85.096%      | 91.855%      |
|  40%           | 85.714%      | 97.071%      |
|  45%           | 89.111%      | 98.432%      |
|  50%           | 97.164%      | 97.040%      |

## Experiment 4: # of Malicious Clients and Backdoor Attack Success Rate

Trigger pattern size: 5 px by 5 px

Trigger pattern location: (1 px, 1 px) or top left corner of images

Poisoning rate: 10% of the training dataset and 100% of testing dataset

Source category is airplane, Target category is cat

Note: CNN used 20 epochs rather than the default 10.

|              | MLP          | CNN          |
| ------------ | ------------ | ------------ |
| % of clients | Backdoor ASR | Backdoor ASR |
| 10%          | 61.378%      | 54.209%      |
| 20%          | 88.841%      | 58.603%      |
| 30%          | 91.894%      | 85.665%      |
| 40%          | 88.440%      | 70.658%      |
| 50%          | 95.238%      | 37.898%      |
| 60%          | 87.124%      | 89.165%      |
| 70%          | 98.986%      | 86.505%      |
| 80%          | 99.392%      | 82.289%      |
| 90%          | 99.191%      | 82.219%      |
| 100%         | 99.296%      | 83.663%      |

Source category is airplane, Target category is bird

Note: CNN used 20 epochs rather than the default 10.

|              | MLP          | CNN          |
| ------------ | ------------ | ------------ |
| % of clients | Backdoor ASR | Backdoor ASR |
| 10%          | 77.893%      | 42.051%      |
| 20%          | 88.295%      | 19.590%      |
| 30%          | 71.495%      | 46.756%      |
| 40%          | 83.103%      | 46.559%      |
| 50%          | 84.109%      | 34.017%      |
| 60%          | 79.156%      | 34.271%      |
| 70%          | 86.167%      | 11.178%      |
| 80%          | 79.770%      | 30.416%      |
| 90%          | 88.677%      | 70.408%      |
| 100%         | 89.740%      | 47.198%      |

