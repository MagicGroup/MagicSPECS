%define         soversion 1.7

Name:           sword           
Version:	1.7.4
Release:	1%{?dist}
Summary:        Free Bible Software Project
Summary(zh_CN.UTF-8): 免费圣经软件项目

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        GPLv2
URL:            http://www.crosswire.org/sword/
Source0:        http://www.crosswire.org/ftpmirror/pub/sword/source/v1.7/sword-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  openssl-devel
BuildRequires:  curl-devel
BuildRequires:  zlib-devel
BuildRequires:  libidn-devel
BuildRequires:  libicu-devel icu
BuildRequires:  clucene-core-devel
BuildRequires:  cppunit-devel

%description
The SWORD Project is the CrossWire Bible Society's free Bible software
project. Its purpose is to create cross-platform open-source tools--
covered by the GNU General Public License-- that allow programmers and
Bible societies to write new Bible software more quickly and easily. We
also create Bible study software for all readers, students, scholars,
and translators of the Bible, and have a growing collection of over 200
texts in over 50 languages.
%description -l zh_CN.UTF-8
免费圣经软件项目。

%package devel
Summary:  Development files for the sword project
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:    Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}
Requires: pkgconfig
Requires: curl-devel clucene-core-devel libicu-devel

%description devel
This package contains the development headers and libraries for the
sword API. You need this package if you plan on compiling software
that uses the sword API, such as Gnomesword or Bibletime.
%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package utils
Summary:  Utilities for the sword project
Summary(zh_CN.UTF-8): %{name} 的工具
Group:    System Enivonment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Requires: %{name}%{?_isa} = %{version}-%{release}

%description utils
This package contains the pre-built utilities for use with the SWORD
Project. The SWORD Project developers encourage you to use the latest
development version of the utilities rather than those released with
a packaged release as updates to the utilities do not affect the
release schedule of the library. However, these utilities were the
latest at the time of the current library release.

%description utils -l zh_CN.UTF-8
%{name} 的工具。

%package python
Summary:  Python bindings for Sword
Summary(zh_CN.UTF-8): %{name} 的 Python 绑定
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: python

%description python
Python bindings for The SWORD Library.
%description python -l zh_CN.UTF-8
%{name} 的 python 绑定。

%prep
%setup -q

%build
mkdir build
pushd build
%cmake -DLIBSWORD_LIBRARY_TYPE=Shared \
       -DSWORD_BINDINGS="Python" \
       -DBUILD_UTILITIES="Yes" \
       -DLIBSWORD_SOVERSION=%{soversion} \
       -DLIBDIR=%{_libdir} \
       ..
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
pushd build
%make_install
popd
mkdir -p %{buildroot}%{_datadir}/sword/modules

find %{buildroot} -type f -name "*.la" -delete -print

magic_rpm_clean.sh

%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc AUTHORS COPYING ChangeLog INSTALL LICENSE NEWS README
%doc samples doc
# Re-enable after upstream includes it with CMake builds
%config(noreplace) %{_sysconfdir}/sword.conf
%{_libdir}/libsword.so.%{soversion}
%{_datadir}/sword

%files devel
%doc CODINGSTYLE
%{_includedir}/sword/
%{_libdir}/libsword.so
%{_libdir}/pkgconfig/sword.pc

%files utils
%{_bindir}/vs2osisref
%{_bindir}/vs2osisreftxt
%{_bindir}/mod2vpl
%{_bindir}/imp2ld
%{_bindir}/diatheke
%{_bindir}/mkfastmod
%{_bindir}/mod2zmod
%{_bindir}/xml2gbs
%{_bindir}/imp2vs
%{_bindir}/installmgr
%{_bindir}/osis2mod
%{_bindir}/tei2mod
%{_bindir}/vpl2mod
%{_bindir}/mod2imp
%{_bindir}/addld
%{_bindir}/imp2gbs
%{_bindir}/mod2osis
%{_bindir}/emptyvss

%files python
%{python2_sitearch}/Sword.py
%{python2_sitearch}/Sword.pyc
%{python2_sitearch}/Sword.pyo
%{python2_sitearch}/_Sword.so
%{python2_sitearch}/sword-%{version}-py2.7.egg-info


%changelog
* Tue Sep 29 2015 Liu Di <liudidi@gmail.com> - 1.7.4-1
- 更新到 1.7.4

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
