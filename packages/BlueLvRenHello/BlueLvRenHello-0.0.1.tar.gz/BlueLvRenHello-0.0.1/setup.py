#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:setup.py
# author:PigKnight
# datetime:2022/3/4 14:08
# software: PyCharm
"""
this is function description
"""
# import module your need
from distutils.core import setup
from setuptools import find_packages

setup(name='BlueLvRenHello',  # 包名
      version='0.0.1',  # 版本号
      description='',
      long_description='my first pypi',  # 包的介绍
      author='BlueLvRen',  # 作者
      author_email='',  # 作者的邮箱
      url='',  # 项目主页
      license='',  # 许可证信息
      install_requires=[],  # 表明当前模块依赖哪些包,若环境中没有,则会从pypi中下载安装
      classifiers=[  # 包的分类信息。所有支持的分类列表见：https://pypi.org/pypi?...
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          # 目标python版本
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.5',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          # 属于什么类型
          'Topic :: Utilities'
      ],
      keywords='',
      packages=find_packages('src'),  # 必填，就是包的代码主目录
      package_dir={'': 'src'},  # 必填
      include_package_data=True,
      )
