Name:           sword           
Version:        1.6.2
Release:        10%{?dist}
Summary:        Free Bible Software Project

Group:          System Environment/Libraries
License:        GPLv2
URL:            http://www.crosswire.org/sword/
Source0:        http://www.crosswire.org/ftpmirror/pub/sword/source/v1.6/sword-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  openssl-devel
BuildRequires:  curl-devel
BuildRequires:  zlib-devel
BuildRequires:  libidn-devel
BuildRequires:  libicu-devel icu
BuildRequires:  clucene-core-devel
BuildRequires:  cppunit-devel

Patch0:         sword-no-curl-types.patch
Patch1:         sword-1.6.2-clucene2.patch
Patch2:		sword-gcc47-fix.patch

%description
The SWORD Project is the CrossWire Bible Society's free Bible software
project. Its purpose is to create cross-platform open-source tools--
covered by the GNU General Public License-- that allow programmers and
Bible societies to write new Bible software more quickly and easily. We
also create Bible study software for all readers, students, scholars,
and translators of the Bible, and have a growing collection of over 200
texts in over 50 languages.

%package devel
Summary:  Development files for the sword project
Group:    Development/Libraries
Requires: %{name} = %{version}
Requires: pkgconfig
Requires: curl-devel clucene-core-devel libicu-devel

%description devel
This package contains the development headers and libraries for the
sword API. You need this package if you plan on compiling software
that uses the sword API, such as Gnomesword or Bibletime.


%prep
%setup -q
%patch0 -p1 -b .no-curl-types
%patch1 -p1 -b .clucene2
%patch2 -p0 -b .gcc47

%build
%configure --disable-static --with-icu --with-clucene=%{_prefix}
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}%{_datadir}/sword/modules

find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'

%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog INSTALL LICENSE NEWS README
%doc samples doc
%config(noreplace) %{_sysconfdir}/sword.conf
%{_bindir}/*
%{_libdir}/sword/
%{_libdir}/libsword-%{version}.so
%{_datadir}/sword

%files devel
%defattr(-,root,root,-)
%doc CODINGSTYLE
%{_includedir}/sword
%{_libdir}/pkgconfig/sword.pc
%{_libdir}/libsword.so

%changelog
* Fri Feb 01 2013 Parag Nemade <paragn AT fedoraproject DOT org> - 1.6.2-10
- Rebuild for icu 50

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun May 20 2012 Deji Akingunola <dakingun@gmail.com> - 1.6.2-8
- Rebuild for icu soname change

* Wed Feb 22 2012 Deji Akingunola <dakingun@gmail.com> - 1.6.2-7
- Fix compile error with gcc-4.7

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct  2 2011 Tom Callaway <spot@fedoraproject.org> - 1.6.2-5
- fix compile against clucene2

* Fri Sep 09 2011 Caolán McNamara <caolanm@redhat.com> - 1.6.2-4
- rebuild for icu 4.8.1

* Mon Mar 07 2011 Caolán McNamara <caolanm@redhat.com> - 1.6.2-3
- rebuild for icu 4.6

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Oct 22 2010 Deji Akingunola <dakingun@gmail.com> - 1.6.2-1
- Update to version 1.6.2

* Fri Apr 02 2010 Caolán McNamara <caolanm@redhat.com> - 1.6.1-3
- rebuild for icu 4.4

* Sat Mar 20 2010 Deji Akingunola <dakingun@gmail.com> - 1.6.1-2
- Work around regression in curl-7.20.0 (Patch by Karl Kleinpaste), fix #569685

* Wed Jan 13 2010 Deji Akingunola <dakingun@gmail.com> - 1.6.1-1
- Update to version 1.6.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu May 14 2009 Deji Akingunola <dakingun@gmail.com> - 1.6.0-1
- Update to version 1.6.0

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 04 2009 Deji Akingunola <dakingun@gmail.com> - 1.5.11-3
- Add patch to build with gcc-4.4

* Tue Jun 03 2008 Caolán McNamara <caolanm@redhat.com> - 1.5.11-2
- rebuild for new icu

* Mon May 26 2008 Deji Akingunola <dakingun@gmail.com> - 1.5.11-1
- Update to version 1.5.11

* Thu Feb 21 2008 Deji Akingunola <dakingun@gmail.com> - 1.5.10-3
- Fix command injection bug (Bug #433723) 

* Thu Jan 10 2008 Deji Akingunola <dakingun@gmail.com> - 1.5.10-2
- Fix build issue with gcc43 

* Mon Nov 05 2007 Deji Akingunola <dakingun@gmail.com> - 1.5.10-1
- Update to version 1.5.10

* Tue Sep 25 2007 Deji Akingunola <dakingun@gmail.com> - 1.5.9-7
- Fix the build failure due to glibc open() check

* Sat Aug 25 2007 Deji Akingunola <dakingun@gmail.com> - 1.5.9-6
- Rebuild

* Fri Aug 03 2007 Deji Akingunola <dakingun@gmail.com> - 1.5.9-5
- License tag update
- Rebuild for new icu

* Sat Jan 20 2007 Deji Akingunola <dakingun@gmail.com> - 1.5.9-4
- Fix an error (libicu-devel not icu-devel)

* Sat Jan 20 2007 Deji Akingunola <dakingun@gmail.com> - 1.5.9-3
- Add Requires for the -devel subpackage

* Sun Jan 14 2007 Deji Akingunola <dakingun@gmail.com> - 1.5.9-2
- Rebuild with lucene support

* Wed Nov 08 2006 Deji Akingunola <dakingun@gmail.com> - 1.5.9-1
- New release
- Build with icu support

* Wed Sep 20 2006 Deji Akingunola <dakingun@gmail.com> - 1.5.8-9
- Take over from Michael A. Peters
- Rebuild for FC6

* Sat Jun 03 2006 Michael A. Peters <mpeters@mac.com> - 1.5.8-8
- Added pkgconfig to devel package Requires

* Fri Feb 17 2006 Michael A. Peters <mpeters@mac.com> - 1.5.8-7
- Rebuild in devel branch

* Wed Dec 14 2005 Michael A. Peters <mpeters@mac.com> - 1.5.8-6
- rebuild in devel branch with new compiler suite
- remove specific release from devel requires of main package
- do not build with %%{_smp_mflags}

* Mon Nov 21 2005 Michael A. Peters <mpeters@mac.com> - 1.5.8-5
- disable static library

* Sun Nov 13 2005 Michael A. Peters <mpeters@mac.com> - 1.5.8-4.1
- Rebuild against new openssl

* Sat Oct 29 2005 Michael A. Peters <mpeters@mac.com> - 1.5.8-4
- Added Arabic support files from Developer mailing list (they have
- been added to the upstream SVN version)

* Thu Jun 09 2005 Michael A. Peters <mpeters@mac.com> - 1.5.8-3
- fix line breaks

* Mon Jun 06 2005 Michael A. Peters <mpeters@mac.com> - 1.5.8-1
- initial CVS checkin for Fedora Extras
