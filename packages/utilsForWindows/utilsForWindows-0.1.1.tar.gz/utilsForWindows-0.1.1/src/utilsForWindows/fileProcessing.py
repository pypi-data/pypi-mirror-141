#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:fileProcessing.py
# author:PigKnight
# datetime:2022/3/6 16:57
# software: PyCharm
"""
this is function description
"""
# import module your need
import os
import sys
import fire
import click


# 文件批量查看
def info_list(path='.', order='size'):
    if not os.path.isdir(path):
        print('请输入正确的文件夹路径')
        sys.exit()
    filename_list = os.listdir(path)
    dict_list = []

    if order not in ['name', 'path', 'size']:
        order = 'size'

    # 获得排序后的字典列表
    for filename in filename_list:
        filepath = os.path.join(path, filename)
        shortname, extension = os.path.splitext(filename)
        if os.path.isfile(filepath):
            file_info = {'shortname': shortname, 'extension': extension, 'path': filepath, 'size': os.path.getsize(filepath)}
            dict_list.append(file_info)

    file_list_ordered = sorted(dict_list, key=lambda keys: keys.get(order))

    return file_list_ordered


# 文件批量重命名
def rename_list(**kwargs):
    # 参数接收
    path = kwargs.get('path') or '.'
    order = kwargs.get('order') or 'size'
    pre = kwargs.get('pre') or ''
    name = kwargs.get('name')
    suf = kwargs.get('suf') or ''

    # 确认工作目录
    os.chdir(path)
    flag = input("将要处理的目录为:{0}，是否确认(Y/N)".format(os.getcwd()))
    if flag.upper() != 'Y':
        print("任务已取消！")
        sys.exit()

    # 获取工作目录文件信息
    file_list_ordered = info_list(path=path, order=order)

    # 批量重命名
    os.chdir(path)
    sum = len(file_list_ordered)
    for index in range(1, sum+1):
        file = file_list_ordered[index-1]
        old_filename = file['shortname'] + file['extension']
        if name:
            new_filename = '{0}{1}{2}{3}{4}'.format(pre, name, suf, str(index), file['extension'])
        else:
            new_filename = '{0}{1}{2}{3}{4}'.format(pre, file['shortname'], suf, str(index),  file['extension'])
            print(new_filename)
        try:
            os.rename(old_filename, new_filename)
            print("{0} 已被重命名为 {1}，当前进度：{2}/{3}".format(old_filename, new_filename, index, sum))
        except Exception as e:
            print("{0} 重命名失败!当前进度：{1}/{2}，错误原因：{3}".format(old_filename, index, sum, e))

    print('文件已重命名完成!')


@click.command()
@click.option('--method', '-m', required=True, type=click.Choice(['rename_list', 'rl']),
              help='File processing to be performed')
@click.option('--path', '-p', required=False, type=str, help='Path to the file to process')
@click.option('--order', '-o', required=False, type=click.Choice(['name', 'path', 'size']), help='Used for order')
@click.option('--order_rule', '-or', required=False, default='desc', type=click.Choice(['desc', 'asc']),
              help='order with desc/asc')
@click.option('--pre', required=False, type=str, help='Used for file renaming as a prefix')
@click.option('--name', required=False, type=str, help='Used for file renaming as a filename')
@click.option('--suf', required=False, type=str, help='Used for file renaming as a suffix')
def file_processing(**kwargs):
    if kwargs['method'] in ['rename_list', 'rl']:
        rename_list(**kwargs)  # 文件批量重命名


# fire.Fire(rename_list)
if __name__ == '__main__':
    file_processing()
