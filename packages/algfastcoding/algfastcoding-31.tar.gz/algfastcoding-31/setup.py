# -*-coding:GBK-*-
"""
* ���ߣ�������
* ʱ�䣺2022/1/25 14:00
* ���ܣ����Python��������ڷ�����pypi.org
* ˵�����뿴����.txt���ⷢ�����ʹ��ѧ��˼�����������
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
    description='��Ч��̿�����/' + AIspeak.translate('��Ч��̿�����'),
    long_description='����⣬ʲô���ܶ��У���/' + AIspeak.translate('����⣬ʲô���ܶ��У���'),
    requires=["pywin32", str("pypiwin32"), "qrcode", ]  # "win32gui"]
)
