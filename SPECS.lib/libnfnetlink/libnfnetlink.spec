Name:           libnfnetlink
Version:        1.0.1
Release:        6%{?dist}
Summary:        Netfilter netlink userspace library
Summary(zh_CN.UTF-8): Netfilter netlink 用户空间库
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        GPLv2+
URL:            http://netfilter.org
Source0:        http://netfilter.org/projects/libnfnetlink/files/%{name}-%{version}.tar.bz2
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:	kernel-headers
BuildRequires:  automake autoconf libtool pkgconfig

%description
libnfnetlink is a userspace library that provides some low-level
nfnetlink handling functions.  It is used as a foundation for other, netfilter
subsystem specific libraries such as libnfnetlink_conntrack, libnfnetlink_log
and libnfnetlink_queue.

%description -l zh_CN.UTF-8
Netfilter netlink 用户空间库。

%package        devel
Summary:        Netfilter netlink userspace library
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}
Requires:	kernel-headers

%description    devel
libnfnetlink is a userspace library that provides some low-level
nfnetlink handling functions.  It is used as a foundation for other, netfilter
subsystem specific libraries such as libnfnetlink_conntrack, libnfnetlink_log
and libnfnetlink_queue.

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
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README COPYING
%{_libdir}/*.so.*


%files devel
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%dir %{_includedir}/libnfnetlink
%{_includedir}/libnfnetlink/*.h

%changelog
* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 1.0.1-6
- 为 Magic 3.0 重建

* Tue Jul 22 2014 Liu Di <liudidi@gmail.com> - 1.0.1-5
- 为 Magic 3.0 重建

* Fri Apr 18 2014 Liu Di <liudidi@gmail.com> - 1.0.1-4
- 为 Magic 3.0 重建

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 30 2012 Paul Komkoff <i@stingr.net> - 1.0.1-1
- new upstream version

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 28 2011 Paul P. Komkoff Jr <i@stingr.net> - 1.0.0-3
- post-1.0 build fixes
- switch to gplv2+
- use packaged COPYING for license

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Sep 28 2009 Paul P. Komkoff Jr <i@stingr.net> - 1.0.0-1
- upstream release

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.41-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar  6 2009 Paul P. Komkoff Jr <i@stingr.net> - 0.0.41-1
- upstream release

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.40-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 19 2009 Paul P. Komkoff Jr <i@stingr.net> - 0.0.40-1
- upstream release

* Tue Jan 13 2009 Caolán McNamara <caolanm@redhat.com> - 0.0.39-4
- rebuild to get provides pkgconfig(libnfnetlink)

* Sun Sep 21 2008 Ville Skyttä <ville.skytta at iki.fi> - 0.0.39-3
- Fix Patch0:/%%patch mismatch.

* Thu Aug  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.0.39-2
- fix license tag

* Fri Jul  4 2008 Paul P. Komkoff Jr <i@stingr.net> - 0.0.39
- grab latest upstream release

* Fri Feb 22 2008 Paul P. Komkoff Jr <i@stingr.net> - 0.0.33-0.1.svn7211
- grab latest upstream changes and fixes, along with new version number
- do not mess with bundled nfnetlink.h, use <linux/netfilter/nfnetlink.h>

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.0.30-2
- Autorebuild for GCC 4.3

* Thu Aug 30 2007 Paul P. Komkoff Jr <i@stingr.net> - 0.0.30-1
- new upstream version

* Sun Mar 25 2007 Paul P. Komkoff Jr <i@stingr.net> - 0.0.25-2
- grab ownership of some directories

* Fri Feb  9 2007 Paul P. Komkoff Jr <i@stingr.net> - 0.0.25-1
- upstream version 0.0.25

* Sun Sep 10 2006 Paul P. Komkoff Jr <i@stingr.net>
- rebuilt

* Wed Jul 12 2006 Felipe Kellermann <stdfk@terra.com.br> - 0.0.16-1
- Adds pkgconfig to devel files.
- Version 0.0.16.

* Mon May  8 2006 Paul P Komkoff Jr <i@stingr.net> - 0.0.14-3
- Include borrowed gpl.txt as LICENSE in %doc

* Sun Mar 26 2006 Paul P Komkoff Jr <i@stingr.net> - 0.0.14-1
- Preparing for submission to fedora extras

