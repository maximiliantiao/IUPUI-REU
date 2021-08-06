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
|  (1 px, 1 px)          |  88.359%     |  79.842%     |
|  (2 px, 2 px)          |  87.416%     |  67.647%     |
|  (3 px, 3 px)          |  87.486%     |  74.015%     |
|  (4 px, 4 px)          |  91.684%     |  68.222%     |
|  (5 px, 5 px)          |  96.931%     |  74.015%     |
|  (6 px, 6 px)          |  92.220%     |  85.276%     |
|  (7 px, 7 px)          |  90.357%     |  87.077%     |
|  (8 px, 8 px)          |  92.656%     |  47.803%     |
|  (9 px, 9 px)          |  89.162%     |  77.223%     |
|  (10 px, 10 px)        |  91.838%     |  85.825%     |
|  (11 px, 11 px)        |  90.000%     |  69.764%     |
|  (12 px, 12 px)        |  89.845%     |  51.842%     |
|  (13 px, 13 px)        |  86.486%     |  79.771%     |
|  (14 px, 14 px)        |  87.350%     |  25.915%     |
|  (15 px, 15 px)        |  85.968%     |  59.324%     |
|  (16 px, 16 px)        |  90.249%     |  42.475%     |

Source category is airplane, Target category is bird

Note: CNN used 20 epochs rather than the default 10.

|                        | MLP          | CNN          |
| ---------------------- | ------------ | ------------ |
| Trigger Patch Location | Backdoor ASR | Backdoor ASR |
|  (1 px, 1 px)          |  92.359%     |  30.969%     |
|  (2 px, 2 px)          |  97.574%     |  29.124%     |
|  (3 px, 3 px)          |  93.304%     |  77.272%     |
|  (4 px, 4 px)          |  90.559%     |  77.929%     |
|  (5 px, 5 px)          |  91.879%     |  69.595%     |
|  (6 px, 6 px)          |  96.478%     |  90.010%     |
|  (7 px, 7 px)          |  96.401%     |  86.092%     |
|  (8 px, 8 px)          |  95.410%     |  85.588%     |
|  (9 px, 9 px)          |  94.086%     |  71.839%     |
|  (10 px, 10 px)        |  94.654%     |  71.889%     |
|  (11 px, 11 px)        |  92.088%     |  64.640%     |
|  (12 px, 12 px)        |  93.468%     |  84.828%     |
|  (13 px, 13 px)        |  92.619%     |  33.979%     |
|  (14 px, 14 px)        |  94.620%     |  50.714%     |
|  (15 px, 15 px)        |  88.912%     |  42.751%     |
|  (16 px, 16 px)        |  93.045%     |  61.785%     |

## Experiment 3: Poisoning Rate and Backdoor Attack Success Rate

Trigger pattern size: 2 px by 2 px

Trigger pattern location: (1 px, 1 px) or top left corner of images

Poisoning rate: X% of the training dataset and 100% of testing dataset

Source category is airplane, Target category is cat

Number of malicious clients = 100 (all clients are malicious)

|                | MLP          | CNN          |
| -------------- | ------------ | ------------ |
| Poisoning Rate | Backdoor ASR | Backdoor ASR |
|   0%           | 15.264%      |  3.993%      |
|   5%           | 16.753%      |  4.545%      |
|  10%           | 40.132%      |  7.446%      |
|  15%           | 38.996%      |  7.130%      |
|  20%           | 68.460%      |  6.260%      |
|  25%           | 58.435%      |  6.000%      |
|  30%           | 75.238%      |  5.484%      |
|  35%           | 76.942%      |  8.237%      |
|  40%           | 89.974%      |  9.899%      |
|  45%           | 87.153%      |  5.574%      |
|  50%           | 91.071%      | 15.196%      |

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
| 10%          | 61.378%      | 46.374%      |
| 20%          | 88.841%      | 36.498%      |
| 30%          | 91.894%      | 73.759%      |
| 40%          | 88.440%      | 52.338%      |
| 50%          | 95.238%      | 35.101%      |
| 60%          | 87.124%      | 65.725%      |
| 70%          | 98.986%      |  9.339%      |
| 80%          | 99.392%      | 44.904%      |
| 90%          | 99.191%      | 45.116%      |
| 100%         | 99.296%      | 32.554%      |

Source category is airplane, Target category is bird

Note: CNN used 20 epochs rather than the default 10.

|              | MLP          | CNN          |
| ------------ | ------------ | ------------ |
| % of clients | Backdoor ASR | Backdoor ASR |
| 10%          | 58.354%      | 12.385%      |
| 20%          | 60.953%      | 58.402%      |
| 30%          | 78.506%      | 38.163%      |
| 40%          | 83.410%      | 54.973%      |
| 50%          | 84.579%      | 58.031%      |
| 60%          | 82.831%      | 41.594%      |
| 70%          | 87.155%      | 49.157%      |
| 80%          | 89.772%      | 31.137%      |
| 90%          | 88.587%      | 55.571%      |
| 100%         | 94.052%      | 19.099%      |

