#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Version : Python 3.6

import os
import torch
import torch.optim as optim

from WillMindS.config import Config
from WillMindS.dataloader import WordEmbeddingLoader, RelationLoader, SemEvalDataLoader
from WillMindS.model import CRCNN, PairwiseRankingLoss
from WillMindS.evaluate import Eval


def print_result(predict_label, id2rel, start_idx=8001):
    with open('predicted_result.txt', 'w', encoding='utf-8') as fw:
        for i in range(0, predict_label.shape[0]):
            fw.write('{}\t{}\n'.format(
                start_idx+i, id2rel[int(predict_label[i])]))


def change_lr(optimizer, new_lr):
    for param_group in optimizer.param_groups:
        param_group['lr'] = new_lr


def train(model, criterion, loader, config):
    train_loader, dev_loader, _ = loader
    optimizer = optim.SGD(model.parameters(), lr=config.lr, weight_decay=config.L2_decay)

    print(model)
    print('traning model parameters:')
    for name, param in model.named_parameters():
        if param.requires_grad:
            print('%s :  %s' % (name, str(param.data.shape)))
    print('--------------------------------------')
    print('start to train the model ...')

    eval_tool = Eval(config)
    max_f1 = -float('inf')
    current_lr = config.lr
    for epoch in range(1, config.epoch+1):
        if epoch > 5:
            current_lr *= 0.95
            change_lr(optimizer, current_lr)
        #未采用原论文的词嵌入时，使用这种学习率变化可以得到比较好的结果。
        #原论文见3.3节
        #current_lr = config.lr / epoch

        for step, (data, label) in enumerate(train_loader):
            model.train()
            data = data.to(config.device)
            label = label.to(config.device)

            optimizer.zero_grad()
            scores = model(data)
            loss = criterion(scores, label)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 5)
            optimizer.step()

        _, train_loss, _ = eval_tool.evaluate(model, criterion, train_loader)
        f1, dev_loss, _ = eval_tool.evaluate(model, criterion, dev_loader)

        print('[%03d] train_loss: %.3f | dev_loss: %.3f | micro f1 on dev: %.4f'
              % (epoch, train_loss, dev_loss, f1), end=' ')
        if f1 > max_f1:
            max_f1 = f1
            torch.save(model.state_dict(), os.path.join(
                config.model_dir, 'model.pkl'))
            print('>>> save models!')
        else:
            print()


def test(model, criterion, loader, config):
    print('--------------------------------------')
    print('start test ...')

    _, _, test_loader = loader
    model.load_state_dict(torch.load(
        os.path.join(config.model_dir, 'model.pkl')))
    eval_tool = Eval(config)
    f1, test_loss, predict_label = eval_tool.evaluate(
        model, criterion, test_loader)
    print('test_loss: %.3f | micro f1 on test:  %.4f' % (test_loss, f1))
    return predict_label


if __name__ == '__main__':
    config = Config()
    print('--------------------------------------')
    print('some config:')
    config.print_config()

    print('--------------------------------------')
    print('start to load data ...')
    word2id, word_vec = WordEmbeddingLoader(config).load_embedding()
    rel2id, id2rel, class_num = RelationLoader(config).get_relation()
    loader = SemEvalDataLoader(rel2id, word2id, config)

    train_loader, dev_loader = None, None
    if config.mode == 1:  # train mode
        train_loader = loader.get_train()
        dev_loader = loader.get_dev()
    test_loader = loader.get_test()
    loader = [train_loader, dev_loader, test_loader]
    print('finish!')

    print('--------------------------------------')
    model = CRCNN(word_vec=word_vec, class_num=class_num, config=config)
    model = model.to(config.device)
    criterion = PairwiseRankingLoss(config=config)

    if config.mode == 1:  # train mode
        train(model, criterion, loader, config)
    predict_label = test(model, criterion, loader, config)
    print_result(predict_label, id2rel)