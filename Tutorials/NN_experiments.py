#!/usr/bin/env python
# coding: utf-8

"""
Sources:
https://towardsdatascience.com/a-practical-example-in-transfer-learning-with-pytorch-846bb835f2db
https://pytorch.org/tutorials/beginner/finetuning_torchvision_models_tutorial.html#load-data
"""

import torch
import torch.nn.functional as Ff
import torch.nn as nn
import torch.optim as optim
import numpy as np
import torchvision
from torchvision import datasets, models, transforms
import os
import copy

NUM_EPOCHS = 20
BATCH_SIZE = 8
NUM_WORKERS = 4
FEATURE_EXTRACT = True

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# Tranformations
transform_train = transforms.Compose([
    transforms.Resize(224),
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
])

transform_test = transforms.Compose([
    transforms.Resize(224),
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
])

# Datasets and DataLoaders
train_dataset = torchvision.datasets.CIFAR10(root='./data', train=True,
                                        download=True, transform=transform_train)
train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=BATCH_SIZE,
                                          shuffle=True, num_workers=NUM_WORKERS)

test_dataset = torchvision.datasets.CIFAR10(root='./data', train=False,
                                       download=True, transform=transform_test)
test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=BATCH_SIZE,
                                         shuffle=True, num_workers=NUM_WORKERS)

def set_parameter_requires_grad(model, feature_extracting):
    if feature_extracting:
        for param in model.parameters():
            param.requires_grad = False

def initialize_model(model_name, num_classes, feature_extract, use_pretrained=True):
    # Initialize these variables which will be set in this if statement. Each of these
    #   variables is model specific.
    model_ft = None

    if model_name == "resnet":
        """ Resnet18
        """
        model_ft = models.resnet18(pretrained=use_pretrained)
        set_parameter_requires_grad(model_ft, feature_extract)
        num_ftrs = model_ft.fc.in_features
        model_ft.fc = nn.Linear(num_ftrs, num_classes)

    elif model_name == "alexnet":
        """ Alexnet
        """
        model_ft = models.alexnet(pretrained=use_pretrained)
        set_parameter_requires_grad(model_ft, feature_extract)
        num_ftrs = model_ft.classifier[6].in_features
        model_ft.classifier[6] = nn.Linear(num_ftrs, num_classes)

    elif model_name == "vgg":
        """ VGG11_bn
        """
        model_ft = models.vgg11_bn(pretrained=use_pretrained)
        set_parameter_requires_grad(model_ft, feature_extract)
        num_ftrs = model_ft.classifier[6].in_features
        model_ft.classifier[6] = nn.Linear(num_ftrs, num_classes)

    elif model_name == "squeezenet":
        """ Squeezenet
        """
        model_ft = models.squeezenet1_0(pretrained=use_pretrained)
        set_parameter_requires_grad(model_ft, feature_extract)
        model_ft.classifier[1] = nn.Conv2d(512, num_classes, kernel_size=(1,1), stride=(1,1))
        model_ft.num_classes = num_classes

    elif model_name == "densenet":
        """ Densenet
        """
        model_ft = models.densenet121(pretrained=use_pretrained)
        set_parameter_requires_grad(model_ft, feature_extract)
        num_ftrs = model_ft.classifier.in_features
        model_ft.classifier = nn.Linear(num_ftrs, num_classes)

    else:
        print("Invalid model name, exiting...")
        exit()

    return model_ft


def train_and_test(net):
    BEST_MODEL_PATH = 'best_model.pth'
    best_accuracy = 0.0

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(net.parameters(), lr=0.01, momentum=0.9)
    # Send the model to GPU
    net = net.to(device)

    for epoch in range(NUM_EPOCHS):

        # Training
        net.train()
        for images, labels in iter(train_loader):
            images = images.to(device)
            labels = labels.to(device)
            optimizer.zero_grad()
            outputs = net(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

        # Testing
        net.eval()
        test_error_count = 0.0
        for images, labels in iter(test_loader):
            images = images.to(device)
            labels = labels.to(device)
            outputs = net(images)
            test_error_count += float(torch.sum(torch.abs(labels - outputs.argmax(1))))

        test_accuracy = 1.0 - float(test_error_count) / float(len(test_dataset))
        print('%d: %f' % (epoch, test_accuracy))
        if test_accuracy > best_accuracy:
            torch.save(net.state_dict(), BEST_MODEL_PATH)
            best_accuracy = test_accuracy

    print("Best accuracy: %f" % (best_accuracy))

# Can use resnet, alexnet, vgg, squeezenet, or densenet

torch.cuda.empty_cache()

# net = initialize_model("resnet", 10, FEATURE_EXTRACT)
# print("Resnet")
# train_and_test(net)

# net = initialize_model("alexnet", 10, FEATURE_EXTRACT)
# print("Alexnet")
# train_and_test(net)

net = initialize_model("vgg", 10, FEATURE_EXTRACT)
print(net)
print("VGG")
train_and_test(net)

# net = initialize_model("squeezenet", 10, FEATURE_EXTRACT)
# print("Squeezenet")
# train_and_test(net)

# net = initialize_model("densenet", 10, FEATURE_EXTRACT)
# print("Densenet")
# train_and_test(net)
