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
