"""Adaptation to train target encoder."""
import torch
import torch.nn as nn
import os
import csv
import datetime

def evaluate(encoder, matcher, data_loader, device='cpu', **kwargs):
    """Evaluation for encoder and matcher on target dataset."""
    # set eval state for Dropout and BN layers
    encoder.eval()
    matcher.eval()

    loss = 0
    acc = 0
    tp = 0
    fp = 0
    p = 0

    # set loss function
    criterion = nn.CrossEntropyLoss()

    # evaluate network
    for (seq, mask, segment, labels, exm_id) in data_loader:
        seq = seq.to(device)
        mask = mask.to(device)
        segment = segment.to(device)
        labels = labels.to(device)

        with torch.no_grad():
            feat = encoder(seq, mask, segment)
            preds = matcher(feat)
        loss += criterion(preds, labels).item()
        pred_cls = preds.data.max(1)[1]

        acc += pred_cls.eq(labels.data).cpu().sum().item()
        for i in range(len(labels)):
            if labels[i] == 1:
                p += 1
                if pred_cls[i] == 1:
                    tp += 1
            else:
                if pred_cls[i] == 1:
                    fp += 1

    div_safe = 0.000001
    print("===== RES =====")
    recall = tp/(p+div_safe)
    precision = tp/(tp+fp+div_safe)
    f1 = 2*recall*precision/(recall + precision + div_safe)
    print("recall",recall)
    print("precision",precision)
    print("f1",f1)

    loss /= len(data_loader)
    acc /= len(data_loader.dataset)
    return f1

def evaluate_ED(encoder, matcher, data_loader, device='cpu', **kwargs):
    """Evaluation for ED."""
    # set eval state for Dropout and BN layers
    encoder.eval()
    matcher.eval()

    # init loss and accuracy
    loss = 0
    acc = 0
    tp = 0
    fp = 0
    p = 0

    # set loss function
    criterion = nn.CrossEntropyLoss()

    # evaluate network
    for (seq, mask, labels) in data_loader:
        seq = seq.to(device)
        mask = mask.to(device)
        labels = labels.to(device)

        with torch.no_grad():
            feat,_,pooler_output = encoder(seq, mask)
            preds = matcher(pooler_output)

        loss += criterion(preds, labels).item()
        pred_cls = preds.data.max(1)[1]

        acc += pred_cls.eq(labels.data).cpu().sum().item()
        for i in range(len(labels)):
            if labels[i] == 1:
                p += 1
                if pred_cls[i] == 1:
                    tp += 1
            else:
                if pred_cls[i] == 1:
                    fp += 1


    div_safe = 0.000001
    recall = tp/(p+div_safe)    
    precision = tp/(tp+fp+div_safe)
    f1 = 2*recall*precision/(recall + precision + div_safe)
    print("recall",recall)
    print("precision",precision)
    print("f1",f1)

    loss /= len(data_loader)
    acc /= len(data_loader.dataset)
    return f1


def eval_predict(encoder, matcher, data_loader, device='cpu', **kwargs):
    """Evaluation for encoder and matcher on target dataset."""
    # set eval state for Dropout and BN layers
    encoder.eval()
    matcher.eval()
    predict = []
    # evaluate network
    for (seq, mask, segment, labels, exm_id) in data_loader:
        seq = seq.to(device)
        mask = mask.to(device)
        segment = segment.to(device)
        labels = labels.to(device)

        with torch.no_grad():
            feat = encoder(seq, mask, segment)
            preds = matcher(feat)
        pred_cls = preds.data.max(1)[1]
        prob = preds.data.cpu().numpy().tolist()
        prob1 = [[x[1]] for x in prob]
        predict += prob1
    folder = "output/"
    if not os.path.exists(folder):
        os.makedirs(folder)
    now_time = datetime.datetime.now()
    file_name = folder+'predict_'+str(now_time)+'.csv'
    with open(file_name,'w',encoding='utf-8') as obj:
        writer = csv.writer(obj)
        writer.writerows(predict)
    return file_name

def eval_predict_ED(encoder, matcher, data_loader, device='cpu', **kwargs):
    """Evaluation for encoder and matcher on target dataset."""
    # set eval state for Dropout and BN layers
    encoder.eval()
    matcher.eval()
    predict = []
    # evaluate network
    for (seq, mask, labels) in data_loader:
        seq = seq.to(device)
        mask = mask.to(device)
        labels = labels.to(device)

        with torch.no_grad():
            feat,_,pooler_output = encoder(seq, mask)
            preds = matcher(pooler_output)
        pred_cls = preds.data.max(1)[1]
        prob = preds.data.cpu().numpy().tolist()
        prob1 = [[x[1]] for x in prob]
        predict += prob1

    folder = "output/"
    if not os.path.exists(folder):
        os.makedirs(folder)
    now_time = datetime.datetime.now()
    file_name = folder+'predict_'+now_time+'.csv'
    with open(file_name,'w',encoding='utf-8') as obj:
        writer = csv.writer(obj)
        writer.writerows(predict)
    return file_name
