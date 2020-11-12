# -*- coding: UTF-8 -*-
# @Time : 2020/09/13 11:06
# @Author : xiao meng
# @File ： Tools.py
# @Function : tools


class Tools(object):
    def __init__(self):
        pass

    def convert(self, data):
        '''
        整数转为32位整数列表,小端模式
        :param data: data由调用者确保输入为整数正数
        :return:
        '''
        int_list = []
        while data > 0:
            db = str(bin(data + 2 ** 32)[-32:])
            dh = int(db, 2)
            int_list.append(dh)
            data = data >> 32
        return int_list

    def find_in_bit_set(self, bits, n, pos):
        bit_lis = self.convert(bits)
        i1 = int(pos / 32)
        if i1 >= n:
            return False
        i2 = pos % 32
        return (bit_lis[i1] >> i2) & 1

