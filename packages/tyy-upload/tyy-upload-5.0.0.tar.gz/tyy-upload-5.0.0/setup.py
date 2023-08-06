# coding=utf-8

from setuptools import setup, find_packages

setup(
    name="tyy-upload",
    version="5.0.0",
    description="upload file",
    author="hxl",
    maintainer="hxl",
    packages=find_packages(),
    license='MIT License',
    entry_points={
        'console_scripts': [
            'tupload=file_upload.upload:start'
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]

)


