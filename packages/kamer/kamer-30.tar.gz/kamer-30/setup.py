#!/usr/bin/env python3
# OTP-CR-117/19 otp.informationdesk@icc-cpi.int http://pypi.org/project/genocide
#
# This file is placed in the Public Domain.

import os

from setuptools import setup

def uploadlist(dir):
    upl = []

    for file in os.listdir(dir):
        if not file or file.startswith('.'):
            continue
        d = dir + os.sep + file
        if os.path.isdir(d):   
            upl.extend(uploadlist(d))
        else:
            if file.endswith(".pyc") or file.startswith("__pycache"):
                continue
            upl.append(d)
    return upl

def read():
    return open("README.rst", "r").read()

setup(
    name='kamer',
    version='30',
    url='https://github.com/bthate/kamer',
    author='Bart Thate',
    author_email='bthate67@gmail.com',
    description="OTP-CR-117/19 - prosecute king netherlands for genocide - http://genocide.rtfd.io",
    license='Public Domain',
    zip_safe=True,
    scripts=["bin/kamer"],
    packages=["kamer"],
    long_description=read(),
    include_package_data=True,
    data_files=[("share/doc/kamer", uploadlist("docs"))],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: Public Domain',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Utilities'],
)
