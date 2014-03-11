#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2008 Terje Rosten <terjeros@phys.ntnu.no>
# License: BSD
from distutils.core import setup
desc = 'Python library to extract EXIF data from tiff and jpeg files'
setup(name        = 'EXIF',
      version     = '1.1.0',
      author      = 'Ianaré Sévi',
      description =  desc,
      long_description =  desc,
      url         = 'https://github.com/ianare/exif-py',
      license     = 'BSD license',
      py_modules  = ['EXIF'],
      scripts     = ['EXIF'],
      classifiers = ['Development Status :: 5 - Production/Stable',
                     'Intended Audience :: Developers',
                     'License :: OSI Approved :: BSD License',
                     'Operating System :: OS Independent',
                     'Programming Language :: Python',
                     'Topic :: Graphics :: Software Development :: Libraries :: Python Modules ',
                     'User Interface :: Command-line',
                     ],
      )
