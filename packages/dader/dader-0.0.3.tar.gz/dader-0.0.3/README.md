## DADER: Domain Adaptation for Deep Entity Resolution

![python](https://img.shields.io/badge/python-3.6.5-blue)
![pytorch](https://img.shields.io/badge/pytorch-1.7.1-brightgreen)

Entity resolution (ER) is a core problem of data integration. The state-of-the-art (SOTA) results on ER are achieved by deep learning (DL) based methods, trained with a lot of labeled matching/non-matching entity pairs. This may not be a problem when using well-prepared benchmark datasets. Nevertheless, for many real-world ER applications, the situation changes dramatically, with a painful issue to collect large-scale labeled datasets. In this paper, we seek to answer: If we have a well-labeled source ER dataset, can we train a DL-based ER model for target dataset, without any labels or with a few labels? This is known as domain adaptation (DA), which has achieved great successes in computer vision and natural language processing, but is not systematically studied for ER. Our goal is to systematically explore the benefits and limitations of a wide range of DA methods for ER. To this purpose, we develop a DADER (Domain Adaptation for Deep Entity Resolution) framework that significantly advances ER in applying DA. We define a space of design solutions for the three modules of DADER, namely Feature Extractor, Matcher, and Feature Aligner. We conduct so far the most comprehensive experimental study to explore the design space and compare different choices of DA for ER. We provide guidance for selecting appropriate design solutions based on extensive experiments.

<!-- <img src="figure/architecture.png" width="820" /> -->

This repository contains the implementation code of six representative methods of [DADER](https://dl.acm.org/doi/10.1145/3514221.3517870): MMD, K-order, GRL, InvGAN, InvGAN+KD, ED.

<!-- <img src="figure/designspace.png" width="700" /> -->


## DataSets
Public datasets used in the paper are from [DeepMatcher](https://github.com/anhaidgroup/deepmatcher/blob/master/Datasets.md), [Magellan](https://sites.google.com/site/anhaidgroup/useful-stuff/the-magellan-data-repository) and [WDC](http://webdatacommons.org/largescaleproductcorpus/v2/). The details of datasets are shown in "data/dataset.md"

<!-- <img src="figure/dataset.png" width="700" /> -->


## Quick Start
Step 1: Requirements
- Before running the code, please make sure your Python version is 3.6.5 and cuda version is 11.1. Then install necessary packages by :
- `pip install dader`

- If Pytorch is not installed automatically, you can install it using the following command:
- `pip install torch==1.7.1+cu110 torchvision==0.8.2+cu110 torchaudio==0.7.2 -f https://download.pytorch.org/whl/torch_stable.html`

Step 2: Run Example

    ```python
    #!/usr/bin/env python3
    from dader import data, model

    # load datasets
    src_x, src_y = data.load_data(path='source.csv')
    tgt_train_x, tgt_valid_x, tgt_train_y, tgt_valid_y = data.load_data(path='target.csv', valid_rate = 0.1)

    # load model
    model = model.Model(method='invgankd', architecture='Bert')
    # train & adapt
    model.run_train(src_x, src_y, tgt_train_x, tgt_train_y, tgt_valid_x, tgt_valid_y, pre=True, adapt=True, ada_max_epoch=5, beta=1)

    # predict
    model.run_predict(tgt_train_x)

    ```

