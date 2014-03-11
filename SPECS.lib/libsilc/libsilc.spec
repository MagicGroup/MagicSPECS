Summary: SILC Client Library
Name:    libsilc
Version: 1.1.10
Release: 8%{dist}
License: GPLv2 or BSD
Group:   System Environment/Libraries
URL:     http://www.silcnet.org/
Source0: http://www.silcnet.org/download/toolkit/sources/silc-toolkit-%{version}.tar.bz2
Patch0:  silc-toolkit-1.1-wordsize.patch
Patch1:  silc-toolkit-1.1.5-docinst.patch
Patch2:  silc-toolkit-1.1.10-libs.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: libidn-devel
BuildRequires: libtool, autoconf, automake

%description
SILC Client Library libraries for clients to connect to SILC networks.

SILC (Secure Internet Live Conferencing) is a protocol which provides
secure conferencing services on the Internet over insecure channel.

%package devel
Summary: Headers and shared libraries for %{name}
Group:   Development/Libraries
Requires: libsilc = %{version}-%{release}
Requires: pkgconfig

%description devel
The SILC Toolkit development libraries and headers. Required for building
SILC clients.

%package doc
Summary: Development documentation for %{name}
Group:   Documentation

%description doc
The SILC Toolkit documentation in HTML format. Useful for writing new SILC
applications.

%prep
%setup -q -n silc-toolkit-%{version}
%patch0 -p1 -b .wordsize
%patch1 -p1 -b .docinst
%patch2 -p1 -b .libs

# filter out libsilc module SONAME Provides (#245323)
cat << \EOF > %{name}-prov
#!/bin/sh
sed -e '\,/silc/modules/,d' |\
%{__find_provides} $*
EOF

%define _use_internal_dependency_generator 0
%define __find_provides %{_builddir}/silc-toolkit-%{version}/%{name}-prov
chmod +x %{__find_provides}

%build
autoreconf -f -i
%configure --libdir=%{_libdir} --enable-shared --without-libtoolfix \
           --includedir=%{_includedir}/silc --with-simdir=%{_libdir}/silc/modules \
           --docdir=%{_docdir}/%{name}-%{version} CFLAGS="$RPM_OPT_FLAGS"

# WARNING! smp flags cause bad binaries!
make

%install
# clear the buildroot
rm -rf $RPM_BUILD_ROOT

# make install
make DESTDIR=$RPM_BUILD_ROOT install
chmod 0755 ${RPM_BUILD_ROOT}%{_libdir}/lib* ${RPM_BUILD_ROOT}%{_libdir}/silc/modules/*.so

# move doc files that would be deleted by rpm
mkdir docinst
mv $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/{toolkit,tutorial} docinst/
# fix encoding of zlib.html
mv docinst/toolkit/zlib.html docinst/toolkit/zlib.html.orig
iconv -f iso-8859-15 -t utf8 -o docinst/toolkit/zlib.html docinst/toolkit/zlib.html.orig
rm -f docinst/toolkit/zlib.html.orig

# remove files we don't want into the package, but are being installed to buildroot
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/silcalgs.conf $RPM_BUILD_ROOT%{_sysconfdir}/silcd.conf

# remove .a and .la
rm -f $RPM_BUILD_ROOT%{_libdir}/libsilc.a
rm -f $RPM_BUILD_ROOT%{_libdir}/libsilc.la
rm -f $RPM_BUILD_ROOT%{_libdir}/libsilcclient.a
rm -f $RPM_BUILD_ROOT%{_libdir}/libsilcclient.la

# Fix encoding of CREDITS
mv CREDITS CREDITS.orig
iconv -f iso-8859-15 -t utf8 -o CREDITS CREDITS.orig

%check
# If this fails, the filter-provides script needs an update.
[ -d $RPM_BUILD_ROOT%{_libdir}/silc/modules ]

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

# the main package libsilc
%files
%defattr(-,root,root,-)
%doc COPYING BSD GPL doc/FAQ CREDITS
%{_libdir}/libsilc-1.1.so.*
%{_libdir}/libsilcclient-1.1.so.*
%dir %_libdir/silc
%dir %_libdir/silc/modules
%{_libdir}/silc/modules/*.so
%defattr(0644, root, root, 0755)

# sub-package libsilc-devel
%files devel
%defattr(-,root,root,-)
%{_libdir}/libsilc.so
%{_libdir}/libsilcclient.so
%{_libdir}/pkgconfig/silc.pc
%{_libdir}/pkgconfig/silcclient.pc
%dir %_includedir/silc
%{_includedir}/silc/*.h

%files doc
%defattr(-,root,root,-)
%doc COPYING BSD GPL
%doc docinst/toolkit
%doc docinst/tutorial


%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.1.10-8
- 为 Magic 3.0 重建

* Thu Nov 15 2012 Liu Di <liudidi@gmail.com> - 1.1.10-7
- 为 Magic 3.0 重建

* Wed Jan 11 2012 Liu Di <liudidi@gmail.com> - 1.1.10-6
- 为 Magic 3.0 重建

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 08 2010 Stu Tomlinson <stu@nosnilmot.com> 1.1.10-4
- Use recommended %%defattr attributes from packaging guidelines

* Wed Jul 07 2010 Stu Tomlinson <stu@nosnilmot.com> 1.1.10-3
- Include license texts in -doc subpackage

* Mon May 31 2010 Stu Tomlinson <stu@nosnilmot.com> 1.1.10-2
- Drop patch to use system libidn now that system libidn hides
  required symbols (#597889)

* Sun Sep 06 2009 Stu Tomlinson <stu@nosnilmot.com> 1.1.10-1
- Update to 1.1.10

* Fri Sep 04 2009 Stu Tomlinson <stu@nosnilmot.com> 1.1.8-7
- Backport patch to fix stack corruption (CVE-2008-7160) (#521256)

* Fri Sep 04 2009 Stu Tomlinson <stu@nosnilmot.com> 1.1.8-6
- Backport patch to fix additional string format vulnerabilities (#515648)

* Wed Aug 05 2009 Stu Tomlinson <stu@nosnilmot.com> 1.1.8-5
- Backport patch to fix string format vulnerability (#515648)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 23 2008 Stu Tomlinson <stu@nosnilmot.com> 1.1.8-2
- Fix building with libtool 2.2

* Wed Dec 03 2008 Stu Tomlinson <stu@nosnilmot.com> 1.1.8-1
- Update to 1.1.8

* Sat Aug 23 2008 Stu Tomlinson <stu@nosnilmot.com> 1.1.7-2
- Fix the patch to make headers multilib safe, which fixes connecting
  to servers (#459578)

* Wed Aug 20 2008 Stu Tomlinson <stu@nosnilmot.com> 1.1.7-2
- Address package review issues (#224458):
  Remove unnecessary direct dependency on libdl from libsilcclient
  Link libsilcclient against libsilc
  Make provides filtering more robust
  Update description

* Thu Mar 20 2008 Stu Tomlinson <stu@nosnilmot.com> 1.1.7-1
- Update to 1.1.7, fixes buffer overflow in PKCS#1 message decoding (#438382)

* Tue Mar 04 2008 Stu Tomlinson <stu@nosnilmot.com> 1.1.6-1
- Update to 1.1.6

* Sat Feb 09 2008 Stu Tomlinson <stu@nosnilmot.com> 1.1.5-3
- Rebuild for gcc 4.3

* Sat Jan 26 2008 Stu Tomlinson <stu@nosnilmot.com> 1.1.5-2
- Link to system libidn instead of statically linking our own copy (#215934)
- Reintroduce documentation subpackage
- spec file cleanups
- fix encoding of CREDITS file to be UTF-8
- Patch to fix buffer overflow generating fingerprints (#372021)

* Fri Dec 07 2007 Stu Tomlinson <stu@nosnilmot.com> 1.1.5-1
- Update to 1.1.5, now fully event based, so clients don't need to
  poll every few milliseconds, reducing power consumption

* Mon Sep 24 2007 Michael Schwendt <mschwendt@users.sf.net> 1.0.2-4
- filter out libsilc module SONAME Provides (#245323)
- add a check section with a test that fails when the modules move

* Tue Aug 21 2007 Warren Togami <wtogami@redhat.com> 1.0.2-3
- rebuild

* Wed Oct 04 2006 Warren Togami <wtogami@redhat.com> 1.0.2-2
- fix multilib file conflicts in -devel

* Wed Jun 28 2006 Warren Togami <wtogami@redhat.com> 1.0.2-1
- remove .a and .la files

* Wed Dec 21 2005 Stu Tomlinson <stu@nosnilmot.com> 1.0.2-0
- Update to 1.0.2

* Sat Apr 9  2005 Stu Tomlinson <stu@nosnilmot.com>  0.9.12-11
- use RPM_OPT_FLAGS (#153261)

* Fri Apr 1  2005 Warren Togami <wtogami@redhat.com> 0.9.12-10
- remove huge doc subpackage to save space, not useful

* Wed Mar 16 2005 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Feb 28 2005 Warren Togami <wtogami@redhat.com> 0.9.12-8
- gcc4 rebuild

* Wed Sep 1 2004 Warren Togami <wtogami@redhat.com> 0.9.12-7
- rawhide import
- minor spec changes

* Tue Sep 1 2004 Toni Willberg <toniw@iki.fi>
- 0.9.12-0.fdr.5 - Had to remove smp_mflags because build fails with them (Michael Schwendt)
* Tue Aug 31 2004 Toni Willberg <toniw@iki.fi>
- 0.9.12-0.fdr.5 - corrections to lib and include path (from Michael Schwendt)
* Tue Aug 31 2004 Toni Willberg <toniw@iki.fi>
- 0.9.12-0.fdr.4 - post/postun /sbin/ldconfig
  (Patch 823 from Stu Tomlinson)
* Tue Aug 31 2004 Toni Willberg <toniw@iki.fi>
- 0.9.12-0.fdr.3 - Move libs to %%{_libdir} and add a silc.pc
  (Patch 815 from Stu Tomlinson)
* Tue Aug 17 2004 Toni Willberg <toniw@iki.fi>
- fix so permissions and hardcoded paths (patch from Michael Schwendt)
* Mon Jul 5 2004 Toni Willberg <toniw@iki.fi>
- Fixed various errors
* Sun Jul 4 2004 Toni Willberg <toniw@iki.fi>
- Initial version for Fedora
