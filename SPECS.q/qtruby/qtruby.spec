#define svn_number rc1
%define real_name qtruby

%define kde4_enable_final_bool ON

Name: %{real_name}
Summary: qtruby
Summary(zh_CN.UTF-8): qtruby
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Version: 4.14.3
Release: 4%{?dist}
License: LGPL
URL: http://extragear.kde.org/apps/kipi
Source0: http://mirrors.ustc.edu.cn/kde/stable/%{version}/src/%{real_name}-%{version}.tar.xz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: gettext
BuildRequires: cmake >= 2.6.2
BuildRequires: gettext
BuildRequires: ruby-devel

%description


%description -l zh_CN.UTF-8
。

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
%setup -q -n %{real_name}-%{version}

%build
mkdir build
cd build
%cmake -DCUSTOM_RUBY_SITE_ARCH_DIR=%{ruby_sitearchdir} -DCUSTOM_RUBY_SITE_LIB_DIR=%{ruby_sitelibdir} ..

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
%{_bindir}/*
%{_libdir}/*.so.*
%{ruby_sitearchdir}/*
%{ruby_sitelibdir}/*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_datadir}/qtruby4/cmake/*
%{_libdir}/*.so

%changelog
* Tue Sep 22 2015 Liu Di <liudidi@gmail.com> - 4.14.3-4
- 为 Magic 3.0 重建

* Fri Sep 11 2015 Liu Di <liudidi@gmail.com> - 4.14.3-3
- 为 Magic 3.0 重建

* Tue Dec 30 2014 Liu Di <liudidi@gmail.com> - 4.14.3-2
- 更新到 4.14.3

* Thu Oct 30 2014 Liu Di <liudidi@gmail.com> - 4.14.2-2
- 更新到 4.14.2

* Fri Jul 18 2014 Liu Di <liudidi@gmail.com> - 4.13.3-2
- 更新到 4.13.3

* Sun Jun 22 2014 Liu Di <liudidi@gmail.com> - 4.13.2-2
- 为 Magic 3.0 重建

* Thu Jun 19 2014 Liu Di <liudidi@gmail.com> - 4.13.2-1
- 更新到 4.13.2

* Sun Jun 01 2014 Liu Di <liudidi@gmail.com> - 4.13.1-1
- 更新到 4.13.1

* Sat Apr 26 2014 Liu Di <liudidi@gmail.com> - 4.13.0-2
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 4.9.3-2
- 为 Magic 3.0 重建

* Tue Aug 11 2009 Ni Hui <shuizhuyuanluo@126.com> - 3.2.3-1mgc
- 更新至 3.2.3
- 拆出开发包
- 己丑  六月廿一
