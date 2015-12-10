Name:           tslib
Version:        1.0
Release:        8%{?dist}
Summary:        Touchscreen Access Library
Summary(zh_CN.UTF-8): 触摸屏访问库

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        LGPLv2
URL:            http://tslib.berlios.de/
Source0:        http://download.berlios.de/tslib/tslib-%{version}.tar.bz2
Patch0:         tslib-1.0-backport-O_CREAT.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libtool


%description
The idea of tslib is to have a core library that provides standardised
services, and a set of plugins to manage the conversion and filtering as
needed.

The plugins for a particular touchscreen are loaded automatically by the
library under the control of a static configuration file, ts.conf.
ts.conf gives the library basic configuration information.  Each line
specifies one module, and the parameters for that module.  The modules
are loaded in order, with the first one processing the touchscreen data
first. 

%description -l zh_CN.UTF-8
触摸屏访问库。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.
%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q
%patch0 -p2 -b .ocreat
./autogen.sh

%build
%configure --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README
%config(noreplace) %{_sysconfdir}/ts.conf
%{_bindir}/ts*
%{_libdir}/*.so.*
%dir %{_libdir}/ts
%{_libdir}/ts/*.so

%files devel
%defattr(-,root,root,-)
%{_includedir}/tslib.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/tslib-0.0.pc


%changelog
* Sat Nov 14 2015 Liu Di <liudidi@gmail.com> - 1.0-8
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.0-7
- 为 Magic 3.0 重建

* Sun Oct 04 2015 Liu Di <liudidi@gmail.com> - 1.0-6
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1.0-5
- 为 Magic 3.0 重建

* Fri Feb 17 2012 Liu Di <liudidi@gmail.com> - 1.0-4
- 为 Magic 3.0 重建

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Apr 14 2009 kwizart < kwizart at gmail.com > - 1.0-1
- Initial package

