#coding=utf-8
from distutils.core import setup
setup(
    name='testup',#对外我们模块的名字
    versoin='1.0',#版本号
    description="这是第一个对外发布的模块，测试哦",#描述
    author='zhaoll',#作者
    author_email='zhaoll@163.com',
    py_modules=['testup.test_A','testup.test_A1']#要发布的模块
)