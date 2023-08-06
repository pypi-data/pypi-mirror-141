import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='apcase',
    version='0.0.4',
    packages=setuptools.find_packages(),
    url='http://www.itfeat.com',
    license='MIT',
    author='YosonHao',
    author_email='haoyuexing@gmail.com',
    description='itfeat',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
