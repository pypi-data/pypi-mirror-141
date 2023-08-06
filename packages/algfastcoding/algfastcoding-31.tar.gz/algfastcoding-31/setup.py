# -*-coding:GBK-*-
"""
* 作者：王若宇
* 时间：2022/1/25 14:00
* 功能：打包Python软件包用于发布到pypi.org
* 说明：请看读我.txt，库发布后可使用学而思库管理工具下载
"""
import sys

from setuptools import setup
from xes import AIspeak

if __name__ == '__main__':
    sys.argv += ["sdist"]
setup(
    name='algfastcoding',
    version='31',
    packages=['algfastcoding'],
    url='https://alggfzslt.freeflarum.com/d/6',
    license='MIT License',
    author='ALG',
    author_email='3104374883@qq.com',
    description='高效编程库纪念版/' + AIspeak.translate('高效编程库纪念版'),
    long_description='这个库，什么功能都有！！/' + AIspeak.translate('这个库，什么功能都有！！'),
    requires=["pywin32", str("pypiwin32"), "qrcode", ]  # "win32gui"]
)
