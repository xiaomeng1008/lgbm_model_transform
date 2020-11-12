# -*- coding: UTF-8 -*-
# @Time : 2020/09/11 16:37
# @Author : xiao meng
# @File ： LGBM_model_transformer.py
# @Function : 把LGBM模型输出的文件转为java可调用的格式样例（字段间以‘\t’分隔）：
# Tree 0
# 节点编号  节点类型          特征编号   分割阈值        离散特征值编号集合 左子树节点  右子树节点  是否为叶子节点
# Tree 1
# 节点编号  节点类型          特征编号   分割阈值        离散特征值编号集合 左子树节点  右子树节点  是否为叶子节点

import sys
from ModelTrans import ModelTrans

# 需要获取的字段信息的key值
KEY_DICT = {
    'TREE': 'Tree',
    'NUM_LEAVES': 'num_leaves',
    'SPLIT_FEATURES': 'split_feature',
    'THRESHOLD': 'threshold',
    'LEFT_CHILD': 'left_child',
    'RIGHT_CHILD': 'right_child',
    'DECISION_TYPE': 'decision_type',
    'CAT_BOUNDARIES': 'cat_boundaries',
    'CAT_THRESHOLD': 'cat_threshold',
    'DECISION_TYPE': 'decision_type',
    'NUM_CAT': 'num_cat'
}


def main():
    if len(sys.argv) < 4:
        print('input illegal, please execute command like this: python main.py input_model.txt output_model.txt 2,5,8')
        exit(1)
    input_model_file = sys.argv[1]
    output_model_file = sys.argv[2]
    cate_feature_indexs = sys.argv[3]
    model_trans = ModelTrans(input_model_file, output_model_file, cate_feature_indexs, KEY_DICT)
    gbm_tree_dict = model_trans.read_model()
    model_trans.transform_model(tree_dict=gbm_tree_dict)


if __name__ == '__main__':
    main()
