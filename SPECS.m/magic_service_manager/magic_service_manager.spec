Summary: Magic Linux system service manager
Summary(zh_CN.UTF-8): Magic Linux 系统服务管理器
Name: magic_service_manager
Version: 0.1
Release: 2%{?dist}
URL: http://www.magiclinux.org
License: GPL v3 or later
Group: Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
Source: %{name}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)

BuildRequires: cmake >= 2.4.7
BuildRequires: qt4-devel >= 4.4.0
BuildRequires: automoc

# not strictly required, but needed in non-root mode for kdesu binary
Requires: kdelibs4

%description
Magic Linux system service manager.

%description -l zh_CN.UTF-8
Magic Linux 系统服务管理器。

%prep
%setup -q -n %{name}

%build
mkdir build
cd build
export CFLAGS=$RPM_OPT_FLAGS
cmake -DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DCMAKE_BUILD_TYPE=release ..

make %{?_smp_mflags}

%install
cd build
%{__rm} -rf %{buildroot}
%{__make} DESTDIR=%{buildroot} install

%clean
%{__rm} -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files
%defattr(-,root,root)
%doc COPYING
%{_bindir}/*
%{_datadir}/applications/*
%{_datadir}/apps/*

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.1-2
- 为 Magic 3.0 重建

* Thu Aug 20 2009 Ni Hui <shuizhuyuanluo@126.com> - 0.1-1mgc
- 首次生成 rpm 包
- 己丑  七月初一
