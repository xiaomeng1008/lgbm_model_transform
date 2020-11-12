# -*- coding: UTF-8 -*-
# @Time : 2020/09/12 16:37
# @Author : xiao meng
# @File ： ModelTrans.py
# @Function : 模型转换

from Tools import Tools


class ModelTrans(object):
    def __init__(self, input_model_path, output_model_path, cate_feature_indexs, key_dict):
        self.input_model_path = input_model_path
        self.output_model_path = output_model_path
        self.cate_feature_indexs = list(map(int, cate_feature_indexs.split(',')))
        self.key_dict = key_dict

    def read_model(self):
        '''
        读取模型文件
        :return: {tree_id:{key:value}} ,{cate_feature_id:[values]}
        '''
        tree_dict = dict()
        tree_id = 0
        tree_key = ''
        with open(self.input_model_path, encoding='utf-8', mode='r') as fd:
            for line in fd.readlines():
                line = line.rstrip('\n')
                if (self.key_dict.get('TREE') + '=') in line:
                    if (self.key_dict.get('TREE') + '=' + str(tree_id)) in line:
                        print(self.key_dict.get('TREE') + '=' + str(tree_id))
                        tree_key = self.key_dict.get('TREE') + '\t' + str(tree_id)
                        tree_dict[tree_key] = dict()
                        tree_id += 1
                else:
                    key, value = self.get_trees(line)
                    if key is not None:
                        tree_dict[tree_key][key] = value
        return tree_dict

    # def get_cate_feature_values(self, data):
    #     '''
    #     获取分类特征的特征值枚举
    #     :param data:
    #     :return: {feature_index:[feature_values]}
    #     '''
    #     feature_values_dict = dict()
    #     value_list = data.replace(self.key_dict.get('FEATURE_INFOS'), '').replace('=', '').split(' ')
    #     for i in self.cate_feature_indexs:
    #         cate_feature_values = value_list[i]
    #         values = cate_feature_values.split(':')
    #         feature_values_dict[str(i)] = ','.join(values)
    #     return feature_values_dict

    def get_trees(self, tree_data):
        '''
        获取所有tree的信息
        :param tree_data:
        :return: 字段名,字段值
        '''
        for value in self.key_dict.values():
            if value + '=' in tree_data:
                name = tree_data.split('=')[0]
                value = tree_data.split('=')[1]
                return name, value
        return None, None

    def transform_model(self, tree_dict):
        '''
        生成java调用格式文件
        :param model_dict:
        :return:
        '''
        with open(self.output_model_path, encoding='utf-8', mode='w') as fd:
            for tree in tree_dict:
                fd.write(tree)
                fd.write('\n')
                tree_info_dic = self.get_tree_info(tree, tree_dict)
                lef_node_num = tree_info_dic.get(self.key_dict.get('NUM_LEAVES'))
                inner_node_num = lef_node_num -1
                # 内部节点信息
                for i in range(0, inner_node_num):
                    inner_node_info = self.get_inner_node_info(i, tree_info_dic)
                    fd.write(inner_node_info)
                    fd.write('\n')
                # 叶子节点信息
                for j in range(-1, -(int(lef_node_num) + 1), -1):
                    leaf_node_info = self.get_leaf_node_info(j)
                    fd.write(leaf_node_info)
                    fd.write('\n')
        return

    def get_tree_info(self, tree, tree_dict):
        '''
        获取指定树的信息
        :param tree:
        :param tree_dict:
        :return:
        '''
        tree_info_map = dict()
        tree_info_map[self.key_dict.get('NUM_LEAVES')] = int(tree_dict.get(tree).get(self.key_dict.get('NUM_LEAVES')))
        tree_info_map[self.key_dict.get('SPLIT_FEATURES')]  = tree_dict.get(tree).get(self.key_dict.get('SPLIT_FEATURES')).split(' ')
        tree_info_map[self.key_dict.get('THRESHOLD')] = tree_dict.get(tree).get(self.key_dict.get('THRESHOLD')).split(' ')
        tree_info_map[self.key_dict.get('LEFT_CHILD')]  = tree_dict.get(tree).get(self.key_dict.get('LEFT_CHILD')).split(' ')
        tree_info_map[self.key_dict.get('RIGHT_CHILD')]  = tree_dict.get(tree).get(self.key_dict.get('RIGHT_CHILD')).split(' ')
        if int(tree_dict.get(tree).get(self.key_dict.get('NUM_CAT'))) != 0:
            tree_info_map[self.key_dict.get('CAT_BOUNDARIES')] = tree_dict.get(tree).get(self.key_dict.get('CAT_BOUNDARIES')).split(' ')
            tree_info_map[self.key_dict.get('CAT_THRESHOLD')] = tree_dict.get(tree).get(self.key_dict.get('CAT_THRESHOLD')).split(' ')
        tree_info_map[self.key_dict.get('DECISION_TYPE')] = tree_dict.get(tree).get(self.key_dict.get('DECISION_TYPE')).split(' ')
        return tree_info_map

    def get_inner_node_info(self, node_id, tree_info_dic):
        '''
        获取内部节点的信息
        :param node_id:
        :param tree_info_dic:
        :return:
        '''

        inner_node_info_list = []
        # 节点编号
        inner_node_info_list.append(str(node_id))
        # 特征编号
        split_features_list = tree_info_dic.get(self.key_dict.get('SPLIT_FEATURES'))
        feature_id = split_features_list[node_id]
        # 分割阈值
        split_value_list = tree_info_dic.get(self.key_dict.get('THRESHOLD'))
        split_value = split_value_list[node_id]
        # 特征类型 & 离散值集合
        if int(feature_id) in self.cate_feature_indexs:
            feature_type = 'Categorical'
            # cat_values = 'List(' + cate_feature_dict.get(feature_id) + ')' ## 进行修改 ###########
            cat_idx = int(split_value)
            cat_boundarie_list = list(map(int, tree_info_dic.get(self.key_dict.get('CAT_BOUNDARIES'))))
            cat_threshold_list = list(map(int, tree_info_dic.get(self.key_dict.get('CAT_THRESHOLD'))))
            cat_thrsholds = self.get_cat_threshold(cat_idx, cat_boundarie_list, cat_threshold_list)
            cat_thrshold_list = 'List(' + cat_thrsholds + ')'
        else:
            feature_type = 'Continuous'
            cat_thrshold_list = 'List()'
        # 左子树
        left_node_list = tree_info_dic.get(self.key_dict.get('LEFT_CHILD'))
        left_child = left_node_list[node_id]
        # 右子树
        right_node_list = tree_info_dic.get(self.key_dict.get('RIGHT_CHILD'))
        right_child = right_node_list[node_id]
        inner_node_info_list.append(feature_type)
        inner_node_info_list.append(feature_id)
        inner_node_info_list.append(split_value)
        inner_node_info_list.append(cat_thrshold_list)
        inner_node_info_list.append(left_child)
        inner_node_info_list.append(right_child)
        inner_node_info_list.append('0')
        content = '\t'.join(inner_node_info_list)
        return content

    def get_leaf_node_info(self, node_id):
        '''
        获取叶节点信息
        :param node_id:
        :return:
        '''
        leaf_node_info_list = []
        # 节点编号
        leaf_node_info_list.append(str(node_id))
        # 类型
        leaf_node_info_list.append('-')
        # 特征编号
        leaf_node_info_list.append('-1')
        # 分割阈值
        leaf_node_info_list.append('-1')
        # 离散值编号集合
        leaf_node_info_list.append('-')
        # 左子树节点
        leaf_node_info_list.append('-1')
        # 右子树节点
        leaf_node_info_list.append('-1')
        # 是否为叶子节点
        leaf_node_info_list.append('1')
        return '\t'.join(leaf_node_info_list)

    def get_cat_threshold(self, cat_idx, cat_boundaries, cat_threshold):
        '''
        获取分类特征的threshold
        :param cat_idx:
        :param cat_boundaries:
        :param cat_threshold:
        :return:
        '''
        cat_threshold_list = []
        for i in range(cat_boundaries[cat_idx], cat_boundaries[cat_idx + 1]):
            for j in range(0, 32):
                cat = (i - cat_boundaries[cat_idx]) * 32 + j
                tools = Tools()
                if tools.find_in_bit_set(cat_threshold[cat_idx], cat_boundaries[cat_idx + 1] - cat_boundaries[cat_idx], cat):
                    cat_threshold_list.append(str(cat))
        return ','.join(cat_threshold_list)