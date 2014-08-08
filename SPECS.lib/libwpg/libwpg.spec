Name:           libwpg
Version: 0.3.0
Release: 1%{?dist}
Summary:        Library for reading WordPerfect Graphics images
Summary(zh_CN.UTF-8): 读取 WordPerfect 图形图像的库

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        GPLv2+
URL:            http://libwpg.sourceforge.net/
Source0:        http://download.sourceforge.net/libwpg/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libwpd-devel >= 0.10
BuildRequires:  doxygen

%description
Libwpg project is a library and to work with graphics in WPG
(WordPerfect Graphics) format. WPG is the format used among others
in Corel sofware, such as WordPerfect and Presentations.

%description -l zh_CN.UTF-8
Libwpg 是读取 WPG 格式图像的库。

%package devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发文件
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name}-devel 软件包包含了使用 %{name} 开发应用程序所需的库和头文件。

%package tools
Summary:        Tools to convert WordPerfect Graphics images
SUmmary(zh_CN.UTF-8): 转换 WordPerfect 图形图像的工具
Group:          Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体

%description tools
This package contains tools to work with graphics in WPG (WordPerfect
Graphics) format. WPG is the format used among others in Corel sofware,
such as WordPerfect and Presentations.

%description tools -l zh_CN.UTF-8
本软件包包含了 WPG 格式图像的处理工具。


%prep
%setup -q

%build
%configure
make %{?_smp_mflags}
sed 's/\r//' -i ChangeLog
find docs/doxygen/html |xargs touch -r docs/doxygen/doxygen.cfg

%install
rm -rf $RPM_BUILD_ROOT
# Documentation is intentionally not installed here,
# it is included as -devel %%doc
make SUBDIRS="" install DESTDIR=$RPM_BUILD_ROOT
make -C src install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS 
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%doc docs/doxygen/html
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files tools
%defattr(-,root,root,-)
%{_bindir}/*

%changelog
* Fri Aug 08 2014 Liu Di <liudidi@gmail.com> - 0.3.0-1
- 更新到 0.3.0

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.2.0-4
- 为 Magic 3.0 重建

* Sun Oct 28 2012 Liu Di <liudidi@gmail.com> - 0.2.0-3
- 为 Magic 3.0 重建

* Sun Oct 28 2012 Liu Di <liudidi@gmail.com> - 0.2.0-2
- 为 Magic 3.0 重建

* Tue Oct 25 2011 Liu Di <liudidi@gmail.com> - 0.2.0-1
- 升级到 0.2.0
