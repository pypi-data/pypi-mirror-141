from setuptools import setup
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='puredb',
    version='2022.03.09.16.02',
    description='封装自用的leveldb',
    long_description=long_description,
    author='chenzongwei',
    author_email='17695480342@163.com',
    py_modules=['puredb'],
    install_requires=['leveled','loguru'],
    python_requires='>=3',
    license='MIT',
    packages=setuptools.find_packages(),
    requires=[]
)

