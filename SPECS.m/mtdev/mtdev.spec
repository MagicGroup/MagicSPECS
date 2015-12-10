%global tarball mtdev
#global gitdate 20110105

Name:           mtdev
Version:        1.1.5
Release:        4%{?gitdate:.%{gitdate}git%{gitversion}}%{?dist}
Summary:        Multitouch Protocol Translation Library
Summary(zh_CN.UTF-8): 多点触摸协议转换库

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        MIT
URL:            http://bitmath.org/code/mtdev/

%if 0%{?gitdate}
Source0:        %{tarball}-%{gitdate}.tar.bz2
Source1:        make-git-snapshot.sh
Source2:        commitid
%else
Source0:        http://bitmath.org/code/%{name}/%{name}-%{version}.tar.bz2
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  autoconf automake libtool
BuildRequires:  xorg-x11-util-macros >= 1.5.0-1

%description
%{name} is a stand-alone library which transforms all variants of kernel MT
events to the slotted type B protocol. The events put into mtdev may be from
any MT device, specifically type A without contact tracking, type A with
contact tracking, or type B with contact tracking.

%description -l zh_CN.UTF-8
多点触摸协议转换库。

%package devel
Summary:        Multitouch Protocol Translation Library Development Package
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description devel
Multitouch protocol translation library development package.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n %{tarball}-%{?gitdate:%{gitdate}}%{!?gitdate:%{version}}

%build
autoreconf -v --install || exit 1
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALL="install -p"

# We intentionally don't ship *.la files
rm -f %{buildroot}%{_libdir}/*.la
magic_rpm_clean.sh

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING README 
%{_libdir}/libmtdev.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/mtdev.h
%{_includedir}/mtdev-plumbing.h
%{_includedir}/mtdev-mapping.h
%{_libdir}/libmtdev.so
%{_libdir}/pkgconfig/mtdev.pc
%{_bindir}/mtdev-test

%changelog
* Tue Nov 10 2015 Liu Di <liudidi@gmail.com> - 1.1.5-4
- 为 Magic 3.0 重建

* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1.1.5-3
- 为 Magic 3.0 重建

* Thu Jan 01 2015 Liu Di <liudidi@gmail.com> - 1.1.5-2
- 为 Magic 3.0 重建

* Fri Jan 01 2015 Liu Di <liudidi@gmail.com> - 1.1.5-1
- 更新到 1.1.5

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 1.1.0-4.20110105
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-3.20110105
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2.20110105
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 05 2011 Peter Hutterer <peter.hutterer@redhat.com> 1.1.0-1.20110105
- Update to release 1.1.0

* Tue Aug 03 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.0.8-1.20100803
- Update to release 1.0.8

* Thu Jul 08 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.0.1-2.20100706
- Require util-macros >= 1.5

* Tue Jul 06 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.0.1-1.20100706
- Initial package
