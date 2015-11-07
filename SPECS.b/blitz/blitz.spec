Summary: C++ library for scientific computing
Summary(zh_CN.UTF-8): 科学计算的 C++ 库
Name: blitz
Version: 0.10
Release: 3%{?dist}
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License: GPL
URL: http://oonumerics.org/blitz/
Source: http://downloads.sourceforge.net/project/blitz/blitz/Blitz%2B%2B%20%{version}/%{name}-%{version}.tar.gz
Patch:	%{name}-gcc47.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Prefix: %{_prefix}

%description
Blitz++ is a C++ class library for scientific computing which provides
performance on par with Fortran 77/90. It uses template techniques to
achieve high performance. The current versions provide dense arrays and
vectors, random number generators, and small vectors and matrices.

%description -l zh_CN.UTF-8
这是一个进行科学计算的 C++ 类库，提供了与 Fortran 77/90 相当的性能，
因为它使用了模板技术。当前版本提供了稠密数组和矢量，随机数发生器及
小向量和矩阵。

%package devel
Summary: Libraries, includes, etc. used to develop an application with %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig
%description devel
This are the header files and libraries needed to develop a %{name}
application

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package doc
Summary: The Blitz html docs
Summary(zh_CN.UTF-8): %{name} 的网页格式文档
Group: Documentation
Group(zh_CN.UTF-8): 文档
%description doc
HTML documentation files for the Blitz Library

%description doc -l zh_CN.UTF-8
%{name} 的网页格式文档。

%prep
%setup -q
%patch -p1

%build
%configure --enable-shared --disable-static --disable-cxx-flags-preset \
    --enable-64bit --enable-fortran \
    --disable-fortran-flags-preset 

make %{?_smp_mflags}
make info
make html
make pdf

# blitz.pc is created directly by configure
# I use sed to add %%libdir/blitz to the include directories of the library
# so that different bzconfig.h can be installed for different archs
# 
# The problem is reported here
# https://sourceforge.net/tracker/?func=detail&aid=2273091&group_id=63961&atid=505791
%{__sed} -i -e "s/Cflags: -I\${includedir}/Cflags: -I\${includedir} -I\${libdir}\/blitz\/include/" blitz.pc

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
make DESTDIR=%{buildroot} install-info

mkdir -p %{buildroot}%{_libdir}/blitz/include/blitz
mv %{buildroot}%{_includedir}/blitz/gnu %{buildroot}%{_libdir}/blitz/include/blitz

# Put in doc only the source code
rm -rf examples/.deps
rm -rf examples/Makefile*

magic_rpm_clean.sh

%check
make %{?_smp_mflags} check-testsuite

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post devel
/sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir || :

%preun devel
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir || :
fi

%files
%doc AUTHORS LEGAL COPYRIGHT COPYING COPYING.LESSER README LICENSE
%{_libdir}/*so.*

%files devel
%doc examples
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_libdir}/blitz
%{_includedir}/*
%{_infodir}/*
%exclude %{_libdir}/*.la
%exclude %{_infodir}/dir

%files doc
%doc COPYRIGHT COPYING COPYING.LESSER README LICENSE
%doc doc/blitz.pdf
%doc doc/blitz.html
%doc examples

%changelog
* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 0.10-3
- 为 Magic 3.0 重建

* Tue Mar 04 2014 Liu Di <liudidi@gmail.com> - 0.10-2
- 更新到 0.10

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 0.9-2
- 为 Magic 3.0 重建

* Sun Oct 14 2007 Ni Hui <shuizhuyuanluo@126.com> - 0.9-0.1mgc
- first spec file
