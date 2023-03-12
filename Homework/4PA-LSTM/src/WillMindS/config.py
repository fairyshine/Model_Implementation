#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Version : Python 3.6

import argparse
from omegaconf import OmegaConf
import torch
import os
import random
import json
import numpy as np


class Config(object):
    def __init__(self):
        # get init config
        args = self.__get_config()
        # omegeconf版引入
        for key in args:
            print('key: ',key)
            setattr(self, key, args.__getattr__(key))
        ''' argparse版引入
        for key in args.__dict__:
            print('key: ',key)
            setattr(self, key, args.__dict__[key])
        '''

        # select device
        self.device = None
        if self.cuda >= 0 and torch.cuda.is_available():
            self.device = torch.device('cuda:{}'.format(self.cuda))
        else:
            self.device = torch.device('cpu')

        # determine the model name and model dir
        if self.model_name is None:
            self.model_name = 'model'
        self.model_dir = os.path.join(self.output_dir, self.model_name)
        if not os.path.exists(self.model_dir):
            os.makedirs(self.model_dir)

        # backup data
        self.__config_backup(args)

        # set the random seed
        self.__set_seed(self.seed)

    def __get_config(self):
        parser = argparse.ArgumentParser()
        parser.description = 'Only config path to set. All model settings are in config folder.'
        parser.add_argument("--config-path", type=str, default="config/basic.yaml",
                        help="the folder of config")
        args = parser.parse_args()
        return OmegaConf.load(args.config_path)

    def __set_seed(self, seed=1234):
        os.environ['PYTHONHASHSEED'] = '{}'.format(seed)
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)  # set seed for cpu
        torch.cuda.manual_seed(seed)  # set seed for current gpu
        torch.cuda.manual_seed_all(seed)  # set seed for all gpu

    def __config_backup(self, args):
        config_backup_path = os.path.join(self.model_dir, 'config.json')
        with open(config_backup_path, 'w', encoding='utf-8') as fw:
            OmegaConf.save(config=args, f=fw)

    def print_config(self):
        for key in self.__dict__:
            print(key, end=' = ')
            print(self.__dict__[key])


if __name__ == '__main__':
    config = Config()
    config.print_config()
