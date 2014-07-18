#define svn_number rc1
%define real_name libkomparediff2

%define kde4_enable_final_bool OFF

Name: kde4-%{real_name}
Summary: Library to compare files and strings
Summary(zh_CN.UTF-8): 比较文件和字符串的库
License: GPL v2 or Later
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL: http://ktorrent.org
Version: 4.13.3
Release: 2%{?dist}
Source0: http://download.kde.org/stable/%{version}/src/%{real_name}-%{version}.tar.xz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: cmake >= 2.6.2
BuildRequires: gettext
BuildRequires: libkdelibs4-devel >= 4.0.82
BuildRequires: qt4-xmlpatterns-devel >= 4.8.4

%description
Cantor is an application that lets you use your favorite mathematical 
applications from within a nice KDE-integrated Worksheet Interface. 
It offers assistant dialogs for common tasks and allows you to share 
your worksheets with others.

%description -l zh_CN.UTF-8
Cantor 是一个 KDE 集成程序，可以让你用你喜欢的数学程序做为后端进行
工作表处理。

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
%setup -q -n %{real_name}-%{version}

%build
mkdir build
cd build
%cmake_kde4 ..

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
%doc COPYING
%{kde4_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{kde4_includedir}/*
%{kde4_libdir}/*.so
%{kde4_libdir}/cmake/libkomparediff2/*.cmake

%changelog
* Fri Jul 18 2014 Liu Di <liudidi@gmail.com> - 4.13.3-2
- 更新到 4.13.3

* Thu Jun 19 2014 Liu Di <liudidi@gmail.com> - 4.13.2-2
- 更新到 4.13.2

* Wed Jun 04 2014 Liu Di <liudidi@gmail.com> - 4.13.1-2
- 更新到 4.13.1

* Wed Jun 04 2014 Liu Di <liudidi@gmail.com> - 4.13.0-2
- 为 Magic 3.0 重建

* Tue Apr 29 2014 Liu Di <liudidi@gmail.com> - 4.13.0-2
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 4.9.3-2
- 为 Magic 3.0 重建

* Tue Aug 11 2009 Ni Hui <shuizhuyuanluo@126.com> - 3.2.3-1mgc
- 更新至 3.2.3
- 拆出开发包
- 己丑  六月廿一
