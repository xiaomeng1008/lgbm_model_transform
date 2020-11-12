# -*- coding: UTF-8 -*-
# @Time : 2020/09/13 14:06
# @Author : xiao meng
# @File ： test.py
# @Function : test

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
    input_model_file = r'.\lgbm_model\gbm_1600_model.txt'
    output_model_file = r'.\lgbm_model\gbm_test_java2.txt'
    cate_feature_indexs = '22,23,24,25'
    model_trans = ModelTrans(input_model_file, output_model_file, cate_feature_indexs, KEY_DICT)
    gbm_tree_dict = model_trans.read_model()
    model_trans.transform_model(tree_dict=gbm_tree_dict)


if __name__ == '__main__':
    main()