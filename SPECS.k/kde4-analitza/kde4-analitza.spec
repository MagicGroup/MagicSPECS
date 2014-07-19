%ifnarch %{arm}
%global opengl 1
%endif
#define svn_number rc1
%define real_name analitza

%define kde4_enable_final_bool OFF

Name: kde4-%{real_name}
Summary: Library of mathematical features
Summary(zh_CN.UTF-8): KDE4 用的数学库
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Version: 4.13.3
Release: 3%{?dist}
License: LGPL
URL: http://extragear.kde.org/apps/kipi
%define rversion %version
Source0:  http://download.kde.org/stable/%{rversion}/src/%{real_name}-%{version}.tar.xz
# add SHOULD_BUILD_OPENGL option, to be able to disable support
# on arm because plotter3d assumes qreal=double all over the place
Patch1: analitza-4.10.1-opengl_optional.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: gettext
BuildRequires: cmake >= 2.6.2
BuildRequires: libkdelibs4-devel >= %{version}

%if 0%{?opengl:1}
BuildRequires: pkgconfig(QtOpenGL)
%endif
BuildRequires: readline-devel

%description
Library of mathematical features

%description -l zh_CN.UTF-8
KDE4 用的数学库。

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
%package devel
Summary: Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发文件
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}

%description devel
Contains the development files.

%description devel -l zh_CN.UTF-8
%{name} 的开发文件。包含 libbtcore 的开发文件。

%prep
%setup -q -n %{real_name}-%{rversion}
%patch1 -p1 

%build
mkdir build
cd build
%cmake_kde4 \
  %{!?opengl:-DSHOULD_BUILD_OPENGL:BOOL=OFF} \
  ..

make %{?_smp_mflags}

%install
cd build
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

magic_rpm_clean.sh

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{kde4_bindir}/*
%{kde4_libdir}/*.so.*
%{kde4_appsdir}/libanalitza/plots/*.plot*

%files devel
%defattr(-,root,root,-)
%{kde4_libdir}/*.so
%{kde4_includedir}/*
%{kde4_libdir}/cmake/*

%changelog
* Fri Jul 18 2014 Liu Di <liudidi@gmail.com> - 4.13.3-3
- 更新到 4.13.3

* Wed Jun 18 2014 Liu Di <liudidi@gmail.com> - 4.13.2-3
- 更新到 4.13.2

* Sat May 24 2014 Liu Di <liudidi@gmail.com> - 4.13.1-3
- 为 Magic 3.0 重建

* Thu May 22 2014 Liu Di <liudidi@gmail.com> - 4.13.1-2
- 更新到 4.13.1

* Thu May 22 2014 Liu Di <liudidi@gmail.com> - 4.13.0-2
- 为 Magic 3.0 重建

* Wed Apr 23 2014 Liu Di <liudidi@gmail.com> - 4.13.0-2
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 4.9.3-2
- 为 Magic 3.0 重建

* Tue Aug 11 2009 Ni Hui <shuizhuyuanluo@126.com> - 3.2.3-1mgc
- 更新至 3.2.3
- 拆出开发包
- 己丑  六月廿一
