#!/bin/bash
git clone git://gitorious.org/deltarpm/deltarpm
mv deltarpm deltarpm-git$1
tar Jcvf deltarpm-git$1.tar.xz deltarpm-git$1
