import collections
import math
import os
import re
import time
import random
import pandas as pd
import matplotlib.pyplot as plt

import torch
from sklearn.metrics import classification_report, confusion_matrix
from torch.utils import data
from torch.nn import TransformerEncoder, TransformerEncoderLayer

from typing import Tuple
from torch import nn, Tensor

from kabuzi.docop import isrepeated


def accuracy(output, target, topk=(1,)):
    """ 计算 topk 准确率 """
    with torch.no_grad():
        maxk = max(topk)
        batch_size = target.size(0)

        _, pred = output.topk(maxk, 1, True, True)
        pred = pred.t()
        correct = pred.eq(target.view(1, -1).expand_as(pred))

        res = []
        for k in topk:
            correct_k = correct[:k].view(-1).float().sum(0, keepdim=True)
            res.append(correct_k.mul_(100.0 / batch_size))
        return res


def classification_report_(label, pred, save_path):
    """ 利用标签和预测值生成准确率报告和混淆矩阵保存在指定的文件中 """
    with open(isrepeated(os.path.join(save_path, 'classification_report.txt')), 'w') as f:
        f.write(classification_report(label, pred, digits=4))
    pd.DataFrame(confusion_matrix(label, pred)).to_excel(
        isrepeated(os.path.join(save_path, 'confusion matrix.xlsx')), index=True)


def grid_search(trainer, param, test=False):
    """ 网格搜索，trainer: 需要运行的文件名， param: 指定的超参数范围 """
    trainer = 'python ' + trainer
    keys, trainers, midtrainers = [], [], [trainer]
    dim = 1
    for key in param.keys():
        keys.append(key)
        dim *= len(param[key])
    for trainer in midtrainers:
        reset = trainer
        for key in param.keys():
            for i in param[key]:
                trainer += f' --{key} {i}'
                cond = re.findall('--(.*?) ', trainer)
                if cond == keys:
                    trainers.append(trainer)
                    if test is False:
                        os.system(trainer)
                if len(trainers) == dim:
                    with open(isrepeated('../runs/grid_research.txt'), 'w') as f:
                        f.write(f'number of param set: {len(trainers)}\n')
                        f.write('parameters:\n')
                        for l in trainers:
                            f.write(f'{l}\n')
                    # sys.exit()
                    break
                midtrainers.append(trainer)
                trainer = reset
            if len(trainers) == dim:
                break
        # time.sleep(1)
        # print("no break")
        if len(trainers) == dim:
            break


def random_search(trainer, param, limit):
    """ 随机搜索， trainer: 需要运行的文件名， param: 指定的超参数范围，limit: 随机搜索的时长，单位为秒 """
    end = time.time()
    trainer = 'python ' + trainer
    reset = trainer
    trainers = []
    while (time.time() - end) < limit:
        for key in param.keys():
            if isinstance(param[key], list):
                trainer += f' --{key} {random.choice(param[key])}'
            if isinstance(param[key], tuple) and len(param[key]) == 2:
                trainer += f' --{key} {random.uniform(param[key][0], param[key][1])}'
        if trainer not in trainers:
            trainers.append(trainer)
            # time.sleep(1)
            os.system(trainer)
        trainer = reset
    with open(isrepeated('../runs/random_research.txt'), 'w') as f:
        f.write(f'number of param set: {len(trainers)}\n')
        f.write('parameters:\n')
        for l in trainers:
            f.write(f'{l}\n')


def load_array(data_arrays, batch_size, is_train=True):
    """Construct a PyTorch data iterator."""
    dataset = data.TensorDataset(*data_arrays)
    return data.DataLoader(dataset, batch_size, shuffle=is_train)


# 自然语言处理
def tokenize(lines, token='word'):
    """将文本行拆分为单词或字符标记。"""
    if token == 'word':
        return [line.split() for line in lines]
    elif token == 'char':
        return [list(line) for line in lines]
    else:
        print('错误：未知令牌类型：' + token)


def truncate_pad(line, num_steps, padding_token):
    """截断或填充文本序列"""
    if len(line) > num_steps:
        return line[:num_steps]  # 截断
    return line + [padding_token] * (num_steps - len(line))  # 填充


def count_corpus(tokens):
    """统计标记的频率。"""
    if len(tokens) == 0 or isinstance(tokens[0], list):
        tokens = [token for line in tokens for token in line]
    return collections.Counter(tokens)


class Vocab:
    """文本词表"""
    def __init__(self, tokens=None, min_freq=0, reserved_tokens=None):
        if tokens is None:
            tokens = []
        if reserved_tokens is None:
            reserved_tokens = []
        counter = count_corpus(tokens)
        self.token_freqs = sorted(counter.items(), key=lambda x: x[1],
                                  reverse=True)
        self.unk, uniq_tokens = 0, ['<unk>'] + reserved_tokens
        uniq_tokens += [
            token for token, freq in self.token_freqs
            if freq >= min_freq and token not in uniq_tokens]
        self.idx_to_token, self.token_to_idx = [], dict()
        for token in uniq_tokens:
            self.idx_to_token.append(token)
            self.token_to_idx[token] = len(self.idx_to_token) - 1

    def __len__(self):
        return len(self.idx_to_token)

    def __getitem__(self, tokens):
        if not isinstance(tokens, (list, tuple)):
            return self.token_to_idx.get(tokens, self.unk)
        return [self.__getitem__(token) for token in tokens]

    def to_tokens(self, indices):
        if not isinstance(indices, (list, tuple)):
            return self.idx_to_token[indices]
        return [self.idx_to_token[index] for index in indices]


class TransformerEncoderModel(nn.Module):

    def __init__(self, d_model: int, nhead: int, d_hid: int,
                 nlayers: int, dropout: float = 0.5):
        super().__init__()
        self.model_type = 'Transformer'
        self.pos_encoder = PositionalEncoding(d_model, dropout)
        encoder_layers = TransformerEncoderLayer(d_model, nhead, d_hid, dropout)
        self.transformer_encoder = TransformerEncoder(encoder_layers, nlayers)

    def forward(self, src: Tensor, src_mask: Tensor) -> Tensor:
        """
        Args:
            src: Tensor, shape [seq_len, batch_size]
            src_mask: Tensor, shape [seq_len, seq_len]

        Returns:
            output Tensor of shape [seq_len, batch_size, ntoken]
        """
        src = torch.unsqueeze(src, 2)
        src = self.pos_encoder(src)
        output = self.transformer_encoder(src, src_mask)
        return output


class PositionalEncoding(nn.Module):

    def __init__(self, d_model: int, dropout: float = 0.1, max_len: int = 5000):
        super().__init__()
        self.dropout = nn.Dropout(p=dropout)

        position = torch.arange(max_len).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2) * (-math.log(10000.0) / d_model))
        pe = torch.zeros(max_len, 1, d_model)
        pe[:, 0, 0::2] = torch.sin(position * div_term)
        pe[:, 0, 1::2] = torch.cos(position * div_term)
        self.register_buffer('pe', pe)

    def forward(self, x: Tensor) -> Tensor:
        """
        Args:
            x: Tensor, shape [seq_len, batch_size, embedding_dim]
        """
        x = x + self.pe[:x.size(0)]
        return self.dropout(x)


def grad_clipping(net, theta):
    """Clip the gradient."""
    if isinstance(net, nn.Module):
        params = [p for p in net.parameters() if p.requires_grad]
    else:
        params = net.params
    norm = torch.sqrt(sum(torch.sum((p.grad**2)) for p in params))
    if norm > theta:
        for param in params:
            param.grad[:] *= theta / norm


def sequence_mask(X, valid_len, value=0):
    """Mask irrelevant entries in sequences."""
    maxlen = X.size(1)
    mask = torch.arange((maxlen), dtype=torch.float32,
                        device=X.device)[None, :] < valid_len[:, None]
    X[~mask] = value
    return X


class MaskedSoftmaxCELoss(nn.CrossEntropyLoss):
    """The softmax cross-entropy loss with masks."""

    # `pred` shape: (`batch_size`, `num_steps`, `vocab_size`)
    # `label` shape: (`batch_size`, `num_steps`)
    # `valid_len` shape: (`batch_size`,)
    def forward(self, pred, label, valid_len):
        weights = torch.ones_like(label)
        weights = sequence_mask(weights, valid_len)
        self.reduction = 'none'
        unweighted_loss = super(MaskedSoftmaxCELoss,
                                self).forward(pred.permute(0, 2, 1), label)
        weighted_loss = (unweighted_loss * weights).mean(dim=1)
        return weighted_loss


def bleu(pred_seq, label_seq, k):  #@save
    """计算BLEU"""
    pred_tokens, label_tokens = pred_seq.split(' '), label_seq.split(' ')
    len_pred, len_label = len(pred_tokens), len(label_tokens)
    score = math.exp(min(0, 1 - len_label / len_pred))
    for n in range(1, k + 1):
        num_matches, label_subs = 0, collections.defaultdict(int)
        for i in range(len_label - n + 1):
            label_subs[' '.join(label_tokens[i: i + n])] += 1
        for i in range(len_pred - n + 1):
            if label_subs[' '.join(pred_tokens[i: i + n])] > 0:
                num_matches += 1
                label_subs[' '.join(pred_tokens[i: i + n])] -= 1
        score *= math.pow(num_matches / (len_pred - n + 1), math.pow(0.5, n))
    return score


# 绘图
def plot(X, Y=None, xlabel=None, ylabel=None, figsize=(10, 5),
         xscale='linear', yscale='linear', legend=None,
         xlim=None, ylim=None, grid=True, lw=1, c='blue'):
    """ 多层多维数据绘制"""
    plt.figure(figsize=figsize)

    # Return True if `X` (tensor or list) has 1 axis
    def has_one_axis(X):
        return (hasattr(X, "ndim") and X.ndim == 1 or
                isinstance(X, list) and not hasattr(X[0], "__len__"))
    if has_one_axis(X):
        X = [X]
    if Y is None:
        X, Y = [[]] * len(X), X
    elif has_one_axis(Y):
        Y = [Y]
    if len(X) != len(Y):
        X = X * len(Y)
    for x, y, c in zip(X, Y, c):
        if len(x):
            plt.plot(x, y, lw=lw, c=c)
        else:
            plt.plot(y, lw=lw, c=c)
    set_axes(xlabel, ylabel, xlim, ylim, xscale, yscale, legend, grid)
    plt.tight_layout()
    plt.show()


def set_axes(xlabel, ylabel, xlim, ylim, xscale, yscale, legend, grid):
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xscale(xscale)
    plt.yscale(yscale)
    plt.xlim(xlim)
    plt.ylim(ylim)
    if legend:
        plt.legend(legend)
    plt.grid(grid)


reduce_sum = lambda x, *args, **kwargs: x.sum(*args, **kwargs)
astype = lambda x, *args, **kwargs: x.type(*args, **kwargs)
