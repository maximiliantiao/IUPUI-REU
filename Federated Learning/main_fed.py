#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python version: 3.6

import copy
import numpy as np
from torchvision import datasets, transforms
import torch
from utils.sampling import mnist_iid, mnist_noniid, cifar_iid
from utils.options import args_parser
from models.Update import LocalUpdate
from models.Nets import MLP, CNNMnist, CNNCifar, ResNet18
from models.Fed import FedAvg
from models.test import test_img
from paste_patch import paste_patch
from remove_patch import remove_patch


if __name__ == '__main__':
    # Parse args ###################################################################################
    args = args_parser()
    args.device = torch.device('cuda:{}'.format(args.gpu) if torch.cuda.is_available() and args.gpu != -1 else 'cpu')

    if args.poison == 'False':
        # Load clean dataset and split users ###########################################################
        if args.dataset == 'mnist':
            trans_mnist = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))])
            dataset_train = datasets.MNIST('../data/mnist/', train=True, download=True, transform=trans_mnist)
            dataset_test = datasets.MNIST('../data/mnist/', train=False, download=True, transform=trans_mnist)
            # sample users
            if args.iid:
                dict_users = mnist_iid(dataset_train, args.num_users)
            else:
                dict_users = mnist_noniid(dataset_train, args.num_users)
        elif args.dataset == 'cifar':
            trans_cifar = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
            dataset_train = datasets.ImageFolder('./cifar10_pngs/train', transform=trans_cifar)
            dataset_test = datasets.ImageFolder('./cifar10_pngs/test', transform=trans_cifar)
            if args.iid:
                dict_users = cifar_iid(dataset_train, args.num_users)
            else:
                exit('Error: only consider IID setting in CIFAR10')
        else:
            exit('Error: unrecognized dataset')
        img_size = dataset_train[0][0].shape

        # Build model #################################################################################
        if args.model == 'cnn' and args.dataset == 'cifar':
            net_glob = CNNCifar(args=args).to(args.device)
        elif args.model == 'cnn' and args.dataset == 'mnist':
            net_glob = CNNMnist(args=args).to(args.device)
        elif args.model == 'mlp':
            len_in = 1
            for x in img_size:
                len_in *= x
            net_glob = MLP(dim_in=len_in, dim_hidden=200, dim_out=args.num_classes).to(args.device)
        elif args.model == 'resnet18':
            net_glob = ResNet18().to(args.device)
        else:
            exit('Error: unrecognized model')
        # print(net_glob)
        
        # Training Clean ##############################################################################
        print("Training and testing on clean dataset")
        net_glob.train()
        # copy weights
        w_glob = net_glob.state_dict()
        loss_train = []
        cv_loss, cv_acc = [], []
        val_loss_pre, counter = 0, 0
        net_best = None
        best_loss = None
        val_acc_list, net_list = [], []

        if args.all_clients: 
            print("Aggregation over all clients")
            w_locals = [w_glob for i in range(args.num_users)]
        for iter in range(args.epochs):
            loss_locals = []
            if not args.all_clients:
                w_locals = []
            m = max(int(args.frac * args.num_users), 1)
            idxs_users = np.random.choice(range(args.num_users), m, replace=False)
            for idx in idxs_users:
                local = LocalUpdate(args=args, dataset=dataset_train, idxs=dict_users[idx])
                w, loss = local.train(net=copy.deepcopy(net_glob).to(args.device))
                if args.all_clients:
                    w_locals[idx] = copy.deepcopy(w)
                else:
                    w_locals.append(copy.deepcopy(w))
                loss_locals.append(copy.deepcopy(loss))
            # update global weights
            w_glob = FedAvg(w_locals)

            # copy weight to net_glob
            net_glob.load_state_dict(w_glob)

            # print loss
            loss_avg = sum(loss_locals) / len(loss_locals)
            print('Round {:3d}, Average loss {:.3f}'.format(iter, loss_avg))
            loss_train.append(loss_avg)

        # Testing Clean ##############################################################################
        net_glob.eval()
        # acc_train, loss_train = test_img(net_glob, dataset_train, args)
        acc_test, loss_test = test_img(net_glob, dataset_test, args)
        # print("Training accuracy: {:.2f}".format(acc_train))
        print("Testing accuracy: {:.2f}".format(acc_test))

    elif args.poison == 'True':
        size = 5
        poisoning_rate = 10
        location = 1
        args.advries = 100
        for _ in range(0, 1, 1):
            # Paste trigger patch onto dataset ############################################################
            paste_patch(args.src_cate, args.trg_cate, size, location, poisoning_rate)

            # Load poisoned dataset and split users #######################################################
            if args.dataset == 'cifar':
                trans_cifar = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
                dataset_train = datasets.ImageFolder('./cifar10_pngs/train', transform=trans_cifar)
                poisoned_dataset_train = datasets.ImageFolder('./poisoned_cifar10_pngs/train', transform=trans_cifar)
                dataset_test = datasets.ImageFolder('./poisoned_cifar10_pngs/test', transform=trans_cifar)
                if args.iid:
                    dict_users = cifar_iid(dataset_train, args.num_users - args.advries, True, poisoned_dataset_train, args.advries)
                else:
                    exit('Error: only consider IID setting in CIFAR10')
            else:
                exit('Error: unrecognized dataset')
            img_size = dataset_train[0][0].shape

            # Build model #################################################################################
            if args.model == 'cnn' and args.dataset == 'cifar':
                net_glob = CNNCifar(args=args).to(args.device)
            elif args.model == 'cnn' and args.dataset == 'mnist':
                net_glob = CNNMnist(args=args).to(args.device)
            elif args.model == 'mlp':
                len_in = 1
                for x in img_size:
                    len_in *= x
                net_glob = MLP(dim_in=len_in, dim_hidden=200, dim_out=args.num_classes).to(args.device)
            elif args.model == 'resnet18':
                net_glob = ResNet18().to(args.device)
            else:
                exit('Error: unrecognized model')
            # print(net_glob)

            # Training Poisoned ###########################################################################
            print("Training and testing on poisoned dataset")
            net_glob.train()
            # copy weights
            w_glob = net_glob.state_dict()
            loss_train = []
            cv_loss, cv_acc = [], []
            val_loss_pre, counter = 0, 0
            net_best = None
            best_loss = None
            val_acc_list, net_list = [], []

            if args.all_clients: 
                print("Aggregation over all clients")
                w_locals = [w_glob for i in range(args.num_users)]
            for iter in range(args.epochs):
                loss_locals = []
                if not args.all_clients:
                    w_locals = []
                m = max(int(args.frac * args.num_users), 1)
                idxs_users = np.random.choice(range(args.num_users), m, replace=False)
                for idx in idxs_users:
                    if idx > args.num_users - args.advries and idx < args.num_users + args.advries:
                        local = LocalUpdate(args=args, dataset=poisoned_dataset_train, idxs=dict_users[idx])
                    else:
                        local = LocalUpdate(args=args, dataset=dataset_train, idxs=dict_users[idx])
                    w, loss = local.train(net=copy.deepcopy(net_glob).to(args.device))
                    if args.all_clients:
                        w_locals[idx] = copy.deepcopy(w)
                    else:
                        w_locals.append(copy.deepcopy(w))
                    loss_locals.append(copy.deepcopy(loss))
                # update global weights
                w_glob = FedAvg(w_locals)

                # copy weight to net_glob
                net_glob.load_state_dict(w_glob)

                # print loss
                loss_avg = sum(loss_locals) / len(loss_locals)
                print('Round {:3d}, Average loss {:.3f}'.format(iter, loss_avg))
                loss_train.append(loss_avg)

            # Testing Poisoned ############################################################################
            net_glob.eval()
            # acc_train, loss_train = test_img(net_glob, dataset_train, args)
            acc_test, loss_test = test_img(net_glob, dataset_test, args)
            # print("Training accuracy: {:.2f}".format(acc_train))
            print("Testing accuracy: {:.2f}".format(acc_test))

            # Remove trigger patch from dataset ###########################################################
            print("Removing trigger patch from datasets")
            remove_patch(args.trg_cate, args.src_cate)