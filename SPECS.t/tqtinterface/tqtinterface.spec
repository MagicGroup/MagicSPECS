%define git 1
%define gitdate 20120329
%define version 3.5.14
%define order 1
%define realname tqtinterface

%define qt_version 3

Name:			tqtinterface
Version:			%{version}
%if %{git}
Release:		8.%{gitdate}_%{order}%{?dist}
%else
Release:		%{order}%{?dist}
%endif
Summary:		Trinity Qt Interface
Summary(zh_CN.UTF-8):	Trinity 的 Qt 接口
Group: System Environment/Libraries
Group(zh_CN.UTF-8):		系统环境/库
License:			GPL
URL:			http://trinity.pearsoncomputing.net
%if %{git}
Source0:		%{realname}-git%{gitdate}.tar.xz
%else
Source0:		%{realname}-%{version}.tar.xz
%endif

Source1:	make_tqtinterface_git_package.sh

Prefix:		%{_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)
BuildRequires:  gettext
%if "%{qt_version}" == "3"
BuildRequires: tqt3-devel
%else
BuildRequires: qt4-devel
%endif

%description
This package includes libraries that abstract the underlying Qt system from
the actual Trinity code, allowing easy, complete upgrades to new versions of Qt.

It also contains various functions that have been removed from newer versions of Qt,
but are completely portable and isolated from other APIs such as Xorg.  This allows
the Trinity project to efficiently perform certain operations that are infeasible
or unneccessarily difficult when using pure Qt4 or above.

%description -l zh_CN.UTF-8
KDE3 的延续项目 Trinity 使用的 Qt 接口，以便以后可以方便的移植到新版本的 Qt 上。

%package devel
Summary: Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发文件
Group:   Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}
Requires: kdelibs4-devel

%description devel
%{summary}.

%description devel -l zh_CN.UTF-8
%{name} 的开发文件。


%prep
%if %{git}
%setup -q -n %{realname}-git%{gitdate}
%else
%setup -q -n %{realname}-%{version}
%endif

%build
unset QTDIR || :
. /etc/profile.d/tqt.sh
mkdir build
cd build
%{cmake} \
	-DINCLUDE_INSTALL_DIR:PATH=%{_includedir}/tqt \
%if "%{qt_version}" == "3"
	-DQT_VERSION=3 \
%else
	-DQT_VERSION=4 \
%endif
	..
make %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
cd build
make install DESTDIR=%{buildroot}
# for Qt4 conflict
#rm -rf %{buildroot}%{_includedir}/Qt
# 添加 .la 文件，不知道是否必要
rm -f %{buildroot}%{_libdir}/*.la

# 修正和 qt4 的 uic 冲突
sed -i '14,16s/uic/\/usr\/bin\/uic/g' %{buildroot}%{_bindir}/uic-tqt

magic_rpm_clean.sh


%clean
%{__rm} -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/libtq*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/libtq*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Wed Feb 15 2012 Liu Di <liudidi@gmail.com> - 3.5.14-8.20120215_1
- 为 Magic 3.0 重建

* Wed Feb 15 2012 Liu Di <liudidi@gmail.com> - 3.5.14-7.20120215_1
- 为 Magic 3.0 重建

* Wed Feb 15 2012 Liu Di <liudidi@gmail.com> - 3.5.14-6.20120215_1
- 为 Magic 3.0 重建

* Wed Feb 15 2012 Liu Di <liudidi@gmail.com> - 3.5.14-5.20120215_1
- 为 Magic 3.0 重建

* Wed Feb 15 2012 Liu Di <liudidi@gmail.com> - 3.5.14-4.20120215_1
- 为 Magic 3.0 重建

* Wed Feb 15 2012 Liu Di <liudidi@gmail.com> - 3.5.14-3.20120215_1
- 为 Magic 3.0 重建

* Fri Oct 28 2011 Liu Di <liudidi@gmail.com> - 3.5.14-1
- 升级到 git 20111028
