Summary: The Reliable Event Logging Protocol library
Summary(zh_CN.UTF-8): 可靠事件日志协议库
Name: librelp
Version: 1.2.8
Release: 3%{?dist}
License: GPLv3+
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL: http://www.rsyslog.com/
Source0: http://download.rsyslog.com/librelp/%{name}-%{version}.tar.gz
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires: gnutls-devel >= 1.4.0
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Librelp is an easy to use library for the RELP protocol. RELP (stands
for Reliable Event Logging Protocol) is a general-purpose, extensible
logging protocol.

%description -l zh_CN.UTF-8
可靠事件日志协议库。

%package devel
Summary: Development files for the %{name} package
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
Librelp is an easy to use library for the RELP protocol. The
librelp-devel package contains the header files and libraries needed
to develop applications using librelp.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT/%{_libdir}/*.la
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun
if [ "$1" = "0" ] ; then
    /sbin/ldconfig
fi

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README doc/*html
%{_libdir}/librelp.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/librelp.so
%{_libdir}/pkgconfig/relp.pc

%changelog
* Mon Nov 09 2015 Liu Di <liudidi@gmail.com> - 1.2.8-3
- 为 Magic 3.0 重建

* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 1.2.8-2
- 更新到 1.2.8

* Wed Jul 30 2014 Liu Di <liudidi@gmail.com> - 1.2.7-1
- 更新到 1.2.7

* Wed Apr 23 2014 Liu Di <liudidi@gmail.com> - 1.2.5-2
- 为 Magic 3.0 重建

* Thu Mar 27 2014 François Cami <fcami@fedoraproject.org> - 1.2.5-1
- rebase to 1.2.5

* Wed Jul 31 2013 Tomas Heinrich <theinric@redhat.com> - 1.2.0-1
- rebase to 1.2.0
- add gnutls-devel to BuildRequires

* Wed Apr 10 2013 Tomas Heinrich <theinric@redhat.com> - 1.0.3-1
- rebase to 1.0.3

* Thu Apr 04 2013 Tomas Heinrich <theinric@redhat.com> - 1.0.2-1
- rebase to 1.0.2

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 21 2012 Tomas Heinrich <theinric@redhat.com> - 1.0.1-1
- upgrade to upstream version 1.0.1

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 15 2010 Tomas Heinrich <theinric@redhat.com> - 1.0.0-1
- upgrade to upstream version 1.0.0

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed May  7 2008 Tomas Heinrich <theinric@redhat.com> 0.1.1-2
- removed "BuildRequires: autoconf automake"

* Tue Apr 29 2008 Tomas Heinrich <theinric@redhat.com> 0.1.1-1
- initial build
