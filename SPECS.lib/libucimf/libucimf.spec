Name:           libucimf
Version:        2.3.8
Release:        4%{?dist}

Summary:        Unicode Console Input Method Framework
Summary(zh_CN.UTF-8):	在 Unicode 控制台环境下提供输入法支持的框架

Group:          System Environment/Libraries
Group(zh_CN.UTF-8):	系统环境/库
License:        LGPLv2+
URL:            http://code.google.com/p/ucimf/
Source0:        http://ucimf.googlecode.com/files/%{name}-%{version}.tar.gz
Patch0:		libucimf-unistd.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


Requires(post):   /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
Unicode Console Input Method Framework。

%description -l zh_CN.UTF-8
在 Unicode 控制台环境下提供输入法支持的框架。

#需要分出static或去掉
%package devel
Summary:        Headers for developing programs that will use %name
Summary(zh_CN.UTF-8): %name 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8):	开发/库
Requires:       %{name} = %{version}-%{release}

%description devel
This package contains the headers that programmers will need to
develop applications which will use %name.

%description devel -l zh_CN.UTF-8
%name 的开发包。


%prep
%setup -q
%patch0 -p1

%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=${RPM_BUILD_ROOT} install
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root, -)
%doc COPYING ChangeLog INSTALL NEWS
%{_sysconfdir}/*.conf
%{_bindir}/ucimf_*
%{_libdir}/*.so.*


%files devel
%defattr(-, root, root, -)
%{_includedir}/*
%{_datadir}/*
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/ucimf/*
%{_libdir}/pkgconfig/*

%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 2.3.8-4
- 为 Magic 3.0 重建

* Fri Aug 01 2014 Liu Di <liudidi@gmail.com> - 2.3.8-3
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 2.3.8-2
- 为 Magic 3.0 重建

* Mon Nov 21 2011 Liu Di <liudidi@gmail.com> - 2.3.7-1
- 升级到 2.3.7
