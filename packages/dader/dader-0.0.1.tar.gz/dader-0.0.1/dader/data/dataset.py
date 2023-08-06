import numpy as np
from sklearn.model_selection import train_test_split
from ._utils import read_csv, read_tsv, norm


def file2list(path,use_attri):
    data = read_csv(path)
    pairs = []
    labels = [0]*(len(data)-1)
    if len(data[1]) > 1: # with gold labels
        labels = [int(x[1].strip()) for x in data[1:]]
    # print(sum(labels), labels[:100],data[:3])
    if use_attri:
        for x in data[1:]:
            pair = ""
            for row in x[:2]:
                tmp = row.split(",")
                for i in use_attri:
                    pair += tmp[i]
                    pair += " "
                pair += "[SEP]"
            pairs.append(norm(pair))
    else:
        # for x in data[1:]:
        #     pairs.append(norm(x[0])+" [SEP] "+norm(x[1]))

        # exp dataset version
        for x in data[1:]:
            pairs.append(norm(x[0]))
    print("Data Example:")
    print(pairs[:3],labels[:3])
    return pairs, labels


def load_data(path, use_attri=None, valid_rate=None):
    # read data from path: line[left.title,left.name, ...  Tab right.title,right.name, ...  Tab label]
    pairs, labels = file2list(path,use_attri)

    # split to train/valid
    if valid_rate:
        train_x, valid_x, train_y, valid_y = train_test_split(pairs, labels,
                                                                test_size=valid_rate,
                                                                stratify=labels,
                                                                random_state=0)
        return train_x, valid_x, train_y, valid_y                                                   
    else:
        return pairs, labels
