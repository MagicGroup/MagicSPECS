%define plugindir %{_libdir}/esmtp-plugins

Summary:        SMTP client library
Summary(zh_CN.UTF-8): SMTP 客户端库
Name:           libesmtp
Version:        1.0.6
Release:        8%{?dist}
License:        LGPLv2+
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Source:         http://www.stafford.uklinux.net/libesmtp/%{name}-%{version}.tar.bz2
URL:            http://www.stafford.uklinux.net/libesmtp/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  openssl-devel pkgconfig

%description
LibESMTP is a library to manage posting (or submission of) electronic
mail using SMTP to a preconfigured Mail Transport Agent (MTA) such as
Exim. It may be used as part of a Mail User Agent (MUA) or another
program that must be able to post electronic mail but where mail
functionality is not the program's primary purpose.

%description -l zh_CN.UTF-8
SMTP 客户端库。

%package devel
Summary: Headers and development libraries for libESMTP
Summary(zh_CN.UTF-8): %{name} 的开发包
# example file is under the GPLv2+
License: LGPLv2+ and GPLv2+
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}, openssl-devel

%description devel
LibESMTP is a library to manage posting (or submission of) electronic
mail using SMTP to a preconfigured Mail Transport Agent (MTA) such as
Exim.

The libesmtp-devel package contains headers and development libraries
necessary for building programs against libesmtp.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep 
%setup -q

# Keep rpmlint happy about libesmtp-debuginfo...
chmod a-x htable.c

%build

if pkg-config openssl ; then
  export CFLAGS="$CFLAGS $RPM_OPT_FLAGS `pkg-config --cflags openssl`"
  export LDFLAGS="$LDFLAGS `pkg-config --libs-only-L openssl`"
fi
%configure --with-auth-plugin-dir=%{plugindir} --enable-pthreads \
  --enable-require-all-recipients --enable-debug \
  --enable-etrn --disable-isoc --disable-more-warnings --disable-static
make %{?_smp_mflags}
cat << "EOF" > libesmtp.pc
prefix=%{_prefix}
exec_prefix=%{_prefix}
libdir=%{_libdir}
includedir=%{_includedir}

Name: libESMTP
Version: %{version}
Description: SMTP client library.
Requires: openssl
Libs: -pthread -L${libdir} -lesmtp
Cflags:
EOF

cat << "EOF" > libesmtp-config
#! /bin/sh
exec pkg-config "$@" libesmtp
EOF

magic_rpm_clean.sh

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install INSTALL='install -p'
rm $RPM_BUILD_ROOT/%{_libdir}/*.la
rm $RPM_BUILD_ROOT/%{_libdir}/esmtp-plugins/*.la
install -p -m644 -D libesmtp.pc $RPM_BUILD_ROOT%{_libdir}/pkgconfig/libesmtp.pc
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING.LIB NEWS Notes README
%{_libdir}/libesmtp.so.*
%{plugindir}

%files devel
%defattr(-,root,root,-)
%doc examples COPYING
%{_bindir}/libesmtp-config
%{_prefix}/include/*
%{_libdir}/libesmtp.so
%{_libdir}/pkgconfig/libesmtp.pc

%changelog
* Mon Nov 09 2015 Liu Di <liudidi@gmail.com> - 1.0.6-8
- 为 Magic 3.0 重建

* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 1.0.6-7
- 为 Magic 3.0 重建

* Tue Jul 15 2014 Liu Di <liudidi@gmail.com> - 1.0.6-6
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.0.6-5
- 为 Magic 3.0 重建

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec  3 2010 Pawel Salek <pawsa@theochem.kth.se> - 1.0.6-1
- update to upstream 1.0.6

* Sat Jun 12 2010 Pawel Salek <pawsa@theochem.kth.se> - 1.0.4-14

- fix bug 599428: use 'version' macro instead of '_version'.
- Use SSL patch by Ludwig Nussel of SUSE (bugzilla att id 399130).

* Tue Mar  9 2010 Pawel Salek <pawsa@theochem.kth.se> - 1.0.4-13
- fix CVE-2009-2408 (#571817).

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.0.4-12
- rebuilt with new openssl

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 1.0.4-9
- rebuild with new openssl

* Sat Nov  1 2008 Manuel "lonely wolf" Wolfshant <wolfy@fedoraproject.org> - 1.0.4-8
- do not package libtool files from the plugin directory

* Fri Apr  4 2008 Pawel Salek <pawsa@theochem.kth.se> - 1.0.4-7
- attempt at multilib support (#342011).

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.4-6
- Autorebuild for GCC 4.3

* Wed Dec 05 2007 Release Engineering <rel-eng at fedoraproject dot org> - 1.0.4-5
 - Rebuild for deps

* Sun Nov 18 2007 Patrice Dumas <pertusus@free.fr> - 1.0.4-4
- use --disable-static

* Thu Nov 15 2007 Pawel Salek <pawsa@theochem.kth.se> - 1.0.4-3
- drop static libs as suggested in bug 377731.

* Mon Sep 11 2006 Pawel Salek <pawsa@theochem.kth.se> - 1.0.4-2
- rebuild for FC6.

* Fri Mar 24 2006 Pawel Salek <pawsa@theochem.kth.se> - 1.0.4-1
- Update to 1.0.4 - redo build and ssl patches.

* Wed Mar  1 2006 Pawel Salek <pawsa@theochem.kth.se> - 1.0.3r1-8
- Rebuild for Fedora Extras 5

* Sun Dec  4 2005 Pawel Salek <pawsa@theochem.kth.se> - 1.0.3r1-7
- Fix bug 173332 completely, including licence issues.

* Thu Nov 17 2005 Pawel Salek <pawsa@theochem.kth.se> - 1.0.3r1-6
- fix #173332.

* Tue Nov 15 2005 Dan Williams <dcbw@redhat.com> - 1.0.3r1-5
- rebuild against newer crypto libs

* Wed Oct 19 2005 Pawel Salek <pawsa@theochem.kth.se> - 1.0.3r1-4
- fix crashes on certificates with subjectAltName extension. Fix #166844.

* Sun Jun 12 2005 Pawel Salek <pawsa@theochem.kth.se> - 1.0.3r1-3
- Add libesmtp-build.patch - fix building under FC4.

* Thu Sep 30 2004 Miloslav Trmac <mitr@redhat.com> - 1.0.3r1-2
- Include libesmtp-config in libesmtp-devel (#125426, patch by Robert Scheck)

* Tue Jul 13 2004 John Dennis <jdennis@redhat.com> 1.0.3r1-1
- bring up to latest upstream release

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jan 29 2004 Bill Nottingham <notting@redhat.com> 1.0.2-1
- upgrade to 1.0.2 (#113894)

* Fri Oct  3 2003 Bill Nottingham <notting@redhat.com> 1.0.1-1
- update to 1.0.1, rebuild to fix some broken 64-bit libs

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Jan  7 2003 Nalin Dahyabhai <nalin@redhat.com> 0.8.12-4
- include compilation flags for openssl as defined for pkg-config
- don't blow up on compile because key schedules aren't arrays

* Tue Nov  5 2002 Bill Nottingham <notting@redhat.com> 0.8.12-3
- build on various platforms

* Tue Jul 23 2002 Bill Nottingham <notting@redhat.com> 0.8.12-2
- fix broken lib (no pthread dependency)
