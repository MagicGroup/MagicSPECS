#!/bin/bash

baseurl="https://svn.java.net/svn/jsp~svn/tags/"
pkgname="javax.servlet.jsp"

version=`grep Version: *spec | sed -e 's/Version:\s*\(.*\)/\1/'`
echo $version

svn export "${baseurl}/${pkgname}-${version}"
tar cvJf ${pkgname}-${version}.tar.xz  ${pkgname}-${version}/



