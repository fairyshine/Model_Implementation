# 关系抽取模型-CNN
[![PWC](https://img.shields.io/endpoint.svg?url=https://paperswithcode.com/badge/relation-classification-via-convolutional/relation-extraction-on-semeval-2010-task-8)](https://paperswithcode.com/sota/relation-extraction-on-semeval-2010-task-8?p=relation-classification-via-convolutional)

Implementation of [Relation Classification via Convolutional Deep Neural Network](https://www.aclweb.org/anthology/C14-1220.pdf).

## 运行

```shell
python src/run.py
```

## 数据
* [SemEval2010 Task8](https://drive.google.com/file/d/0B_jQiLugGTAkMDQ5ZjZiMTUtMzQ1Yy00YWNmLWJlZDYtOWY1ZDMwY2U4YjFk/view?sort=name&layout=list&num=50) \[[paper](https://www.aclweb.org/anthology/S10-1006.pdf)\]  放入data/文件夹，再运行preprocess.py
* [Embedding - Turian et al.(2010)](http://metaoptimize.s3.amazonaws.com/hlbl-embeddings-ACL2010/hlbl-embeddings-scaled.EMBEDDING_SIZE=50.txt.gz) \[[paper](https://www.aclweb.org/anthology/P10-1040.pdf)\]  放入data/embedding/文件夹

## 说明

仅实现Sentence Level Feature部分，Lexical Level Feature要加入的话，直接与其拼接即可。

## Reference Link

* https://github.com/onehaitao/CNN-relation-extraction
* https://github.com/ShomyLiu/pytorch-pcnn
* https://github.com/FrankWork/conv_relation