#!/usr/bin/env python
# -*- coding:utf-8 -*-

def unique_sub_str(source: str) -> list:
    sun_str_list = []
    for i in range(len(source)):
        for j in range(len(source)):
            # 如果 i>j 则会出现切片值为空, 如 source[1:0], 字符串[开始索引：结束索引：步长],
            # 切取字符串为开始索引到结束索引-1内的字符串
            if i <= j:
                sun_str_list.append(source[i:j+1])

    return sun_str_list


if __name__ == '__main__':
    result = unique_sub_str('abcd')
    print(result)
