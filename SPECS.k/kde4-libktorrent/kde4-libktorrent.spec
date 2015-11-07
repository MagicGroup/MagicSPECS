#define svn_number rc1
%define real_name libktorrent

%define kde4_enable_final_bool OFF

%define build_apidocs 1

Name: kde4-libktorrent
Summary: Library providing torrent downloading code
Summary(zh_CN.UTF-8): torrent 下载库
License: GPL v2 or Later
Group: Applications/Internet
Group(zh_CN.UTF-8): 应用程序/互联网
URL: http://ktorrent.org
Version:	1.3.1
Release: 2%{?dist}
%define majorver %(echo %{version} | awk -F. '{print $2"."$3}')
Source0: http://ktorrent.pwsp.net/downloads/4.%{majorver}/%{real_name}-%{version}.tar.bz2

# recognize more peer id, patch1 written by nihui, Oct.23rd 2010
Patch1: libktorrent-1.0.4-more-peerid.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: cmake >= 2.6.2
BuildRequires: gettext
BuildRequires: libkdelibs4-devel >= 4.0.82
BuildRequires: gmp-devel
BuildRequires: boost-devel
BuildRequires: libgcrypt-devel
%if %build_apidocs
BuildRequires: doxygen
BuildRequires: graphviz
%endif

%description
Library providing torrent downloading code.

%description -l zh_CN.UTF-8
torrent 下载库。

%package devel
Summary: Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发文件
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}

%description devel
Contains the development files.

%description devel -l zh_CN.UTF-8
%{name} 的开发文件。包含 libktorrent 的开发文件。

%if %build_apidocs
%package apidocs
Summary: libktorrent API documentation
Summary(zh_CN.UTF-8): libktorrent API 文档
Group: Development/Documentation
Group(zh_CN.UTF-8): 开发/文档

%description apidocs
This package includes the libktorrent API documentation in HTML
format for easy browsing.

%description devel -l zh_CN.UTF-8
本软件包包含了 HTML 格式的 libktorrent API 文档。
%endif

%prep
%setup -q -n %{real_name}-%{version}

#%patch1 -p1 -b .peerid

%build
mkdir build
cd build
%cmake_kde4 ..

make %{?_smp_mflags}

%if %build_apidocs
# generate api doc
make docs
%endif

%install
cd build
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

%if %build_apidocs
mkdir -p %{buildroot}%{kde4_htmldir}/en
cp -a apidocs/html %{buildroot}%{kde4_htmldir}/en/libktorrent-apidocs
# spurious executables, pull in perl dep(s)
find %{buildroot}%{kde4_htmldir}/en/ -name 'installdox' -exec rm -fv {} ';'
%endif

magic_rpm_clean.sh

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING
%{kde4_libdir}/libktorrent.so.*
%{kde4_localedir}/*

%files devel
%defattr(-,root,root,-)
%{kde4_appsdir}/cmake/modules/*
%{kde4_libdir}/libktorrent.so
%{kde4_includedir}/libktorrent/*

%if %build_apidocs
%files apidocs
%defattr(-,root,root,-)
%{kde4_htmldir}/en/libktorrent-apidocs/
%endif

%changelog
* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 1.3.1-2
- 为 Magic 3.0 重建

* Tue Jun 03 2014 Liu Di <liudidi@gmail.com> - 1.3.1-1
- 更新到 1.3.1

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.3.0-2
- 为 Magic 3.0 重建

* Tue Aug 11 2009 Ni Hui <shuizhuyuanluo@126.com> - 3.2.3-1mgc
- 更新至 3.2.3
- 拆出开发包
- 己丑  六月廿一
