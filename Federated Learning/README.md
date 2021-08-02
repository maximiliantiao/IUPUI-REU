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

Trigger pattern location: (0 px, 0 px) or top left corner of images

Poisoning rate: 10% of the training dataset and 100% of testing dataset

Source category is airplane, Target category is cat
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

## Experiment 2: Trigger patch location and Backdoor Attack Success Rate

Trigger pattern size: 5 px by 5 px

Trigger pattern location: (X px, X px) from the top left corner of images

Poisoning rate: 10% of the training dataset and 100% of testing dataset

Source category is airplane, Target category is cat

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

## Experiment 3: Poisoning Rate and Backdoor Attack Success Rate

Trigger pattern size: 5 px by 5 px

Trigger pattern location: (0 px, 0 px) or top left corner of images

Poisoning rate: X% of the training dataset and 100% of testing dataset

Source category is airplane, Target category is cat

| Poisoning Rate | Backdoor ASR |
| -------------- | ------------ |
|  1%            |  7.142%      |
|  2%            |  7.142%      |
|  3%            | 11.494%      |
|  4%            |  7.372%      |
|  5%            | 13.246%      |
|  6%            | 15.526%      |
|  7%            | 16.074%      |
|  8%            | 17.179%      |
|  9%            | 26.112%      |
| 10%            | 21.996%      |

## Experiment 4: # of Malicious Clients and Backdoor Attack Success Rate

Trigger pattern size: 5 px by 5 px

Trigger pattern location: top left corner of images

Poisoning rate: 10% of the training dataset and 100% of testing dataset

Source category is airplane, Target category is cat

|              | MLP          | CNN          |
| ------------ | ------------ | ------------ |
| % of clients | Backdoor ASR | Backdoor ASR |
| 10%          |              |
| 20%          |              |
| 30%          |              |
| 40%          |              |
| 50%          |              |
| 60%          |              |
| 70%          |              |
| 80%          |              |
| 90%          |              |
| 100%         |              |


