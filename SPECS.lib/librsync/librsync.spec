Summary:        Rsync libraries
Summary(zh_CN.UTF-8): 同步库
Name:           librsync
Version:        0.9.7
Release:        23%{?dist}
License:        LGPLv2+
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL:            http://librsync.sourceforge.net/
Source:         http://downloads.sourceforge.net/sourceforge/%{name}/%{name}-%{version}.tar.gz
Patch0:         librsync-0.9.7-lfs_overflow.patch
Patch1:         librsync-0.9.7-getopt.patch
Patch2:         librsync-0.9.7-man_pages.patch
Patch3:         librsync-0.9.7-format-security.patch
BuildRequires:  zlib-devel, bzip2-devel, %{_includedir}/popt.h, libtool
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
librsync implements the "rsync" algorithm, which allows remote
differencing of binary files. librsync computes a delta relative to a
file's checksum, so the two files need not both be present to generate
a delta.

This library was previously known as libhsync up to version 0.9.0.

The current version of this package does not implement the rsync
network protocol and uses a delta format slightly more efficient than
and incompatible with rsync 2.4.6.

%description -l zh_CN.UTF-8
这个库实现了 "rsync" 算法，允许远程比较二进制文件。

%package devel
Summary:        Headers and development libraries for librsync
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains header files necessary for developing programs
based on librsync. It was previously known as libhsync up to version
0.9.0.

The current version of this package does not implement the rsync
network protocol and uses a delta format slightly more efficient than
and incompatible with rsync 2.4.6.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q
%patch0 -p1 -b .lfs_overflow
%patch1 -p1 -b .getopt
%patch2 -p1 -b .man_pages
%patch3 -p1 -b .format-security

%build
libtoolize
autoreconf -f -i
%configure --enable-shared
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

install -D -m 755 .libs/rdiff $RPM_BUILD_ROOT%{_bindir}/rdiff
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}.{la,a}
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc AUTHORS COPYING NEWS README
%{_libdir}/librsync.so.1*
%{_bindir}/rdiff
%{_mandir}/man1/rdiff.1*

%files devel
%defattr(-,root,root)
%{_libdir}/librsync.so
%{_includedir}/%{name}*
%{_mandir}/man3/librsync.3*

%changelog
* Mon Nov 09 2015 Liu Di <liudidi@gmail.com> - 0.9.7-23
- 为 Magic 3.0 重建

* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 0.9.7-22
- 为 Magic 3.0 重建

* Wed Jul 30 2014 Liu Di <liudidi@gmail.com> - 0.9.7-21
- 为 Magic 3.0 重建

* Sat Feb 23 2013 Robert Scheck <robert@fedoraproject.org> 0.9.7-20
- Made autoreconf copying the missing auxiliary files (#914147)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.7-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.7-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.7-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.7-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.7-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Robert Scheck <robert@fedoraproject.org> 0.9.7-14
- Rebuilt against gcc 4.4 and rpm 4.6

* Sat Dec 20 2008 Robert Scheck <robert@fedoraproject.org> 0.9.7-13
- Run libtoolize before %%configure to avoid libtool 2.2 errors
- Added a patch to make rdiff aware of -i and -z getopt options
- Updated man page for how to use rdiff and removed a dead link

* Sun Feb 10 2008 Robert Scheck <robert@fedoraproject.org> 0.9.7-12
- Rebuilt against gcc 4.3
- Updated the source URL to match with the guidelines

* Tue Aug 28 2007 Robert Scheck <robert@fedoraproject.org> 0.9.7-11
- Updated the license tag according to the guidelines
- Buildrequire %%{_includedir}/popt.h for separate popt (#249352)

* Mon May 07 2007 Robert Scheck <robert@fedoraproject.org> 0.9.7-10
- rebuilt

* Thu Dec 14 2006 Robert Scheck <robert@fedoraproject.org> 0.9.7-9
- removed static library from librsync-devel (#213780)

* Mon Oct 09 2006 Gavin Henry <ghenry@suretecsystems.com> 0.9.7-8
- rebuilt

* Tue Oct 03 2006 Robert Scheck <robert@fedoraproject.org> 0.9.7-7
- rebuilt

* Mon Sep 25 2006 Robert Scheck <robert@fedoraproject.org> 0.9.7-6
- added an upstream patch to solve a lfs overflow (#207940)

* Wed Sep 20 2006 Robert Scheck <robert@fedoraproject.org> 0.9.7-5
- some spec file cleanup, added %%{?dist} and rebuild

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 0.9.7-4
- rebuild on all arches

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sun Jan 23 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0:0.9.7-2
- Recreate autotools files with autoreconf to fix x86_64 build.

* Wed Nov 10 2004 Adrian Reber <adrian@lisas.de> - 0:0.9.7-0.fdr.1
- updated to 0.9.7 (#2248)
- changed source URL to be downloadable with wget

* Fri Aug 8 2003 Ben Escoto <bescoto@stanford.edu> 0.9.6-0.fdr.3
- Build no longer requires GNU tools
- Install shared library and rdiff executable by default

* Sun Jul 20 2003 Ben Escoto <bescoto@stanford.edu> 0.9.5.1-0.fdr.2
- Repackaged Laurent Papier's <papier@sdv.fr> rpm.
