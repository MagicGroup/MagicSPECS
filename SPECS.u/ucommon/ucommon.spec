# Copyright (c) 2008, 2009 David Sugar, Tycho Softworks.
# This file is free software; as a special exception the author gives
# unlimited permission to copy and/or distribute it, with or without
# modifications, as long as this notice is preserved.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY, to the extent permitted by law; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.

Name:          ucommon
Version:       6.6.1
Release:       3%{?dist}
Summary:       Portable C++ framework for threads and sockets

License:       LGPLv3+
URL:           http://www.gnu.org/software/commoncpp
Source0:       http://dev.gnutelephony.org/dist/tarballs/ucommon-%{version}.tar.gz

BuildRequires: cmake
BuildRequires: doxygen
BuildRequires: graphviz-gd
BuildRequires: openssl-devel


%description
GNU uCommon C++ is a lightweight library to facilitate using C++ design
patterns even for very deeply embedded applications, such as for systems using
uclibc along with POSIX threading support. For this reason, uCommon disables
language features that consume memory or introduce runtime overhead. UCommon
introduces some design patterns from Objective-C, such as reference counted
objects, memory pools, and smart pointers. UCommon introduces some new concepts
for handling of thread locking and synchronization.  Starting with release
5.0, GNU uCommon also bundles GNU Common C++ libraries.


%package bin
Summary:       GNU uCommon system and support applications
Requires:      %{name}%{?_isa} = %{version}-%{release}

%description bin
This is a collection of command line tools that use various aspects of the
ucommon library. Some may be needed to prepare files or for development of
applications.


%package devel
Summary:       Headers for building GNU uCommon applications
Requires:      %{name}%{?_isa} = %{version}-%{release}
Requires:      openssl-devel%{?_isa}
Requires:      pkgconfig

%description devel
This package provides header and support files needed for building
applications that use the uCommon and commoncpp libraries.


%package doc
Summary: Generated class documentation for GNU uCommon

%description doc
Generated class documentation for GNU uCommon library from header files in
HTML format.


%prep
%setup -q


%build
%cmake .
make %{?_smp_mflags}
make doc


%install
%make_install INSTALL="install -p"

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc AUTHORS README NEWS SUPPORT ChangeLog
%license COPYING COPYING.LESSER
%{_libdir}/libucommon.so.7*
%{_libdir}/libusecure.so.7*
%{_libdir}/libcommoncpp.so.7*

%files bin
%{_bindir}/args
%{_bindir}/mdsum
%{_bindir}/pdetach
%{_bindir}/sockaddr
%{_bindir}/zerofill
%{_bindir}/scrub-files
%{_bindir}/car
%{_bindir}/keywait
%{_mandir}/man1/args.*
%{_mandir}/man1/car.*
%{_mandir}/man1/mdsum.*
%{_mandir}/man1/pdetach.*
%{_mandir}/man1/scrub-files.*
%{_mandir}/man1/sockaddr.*
%{_mandir}/man1/zerofill.*
%{_mandir}/man1/keywait.*

%files devel
%{_bindir}/ucommon-config
%{_bindir}/commoncpp-config
%{_datadir}/%{name}/
%{_includedir}/ucommon/
%{_includedir}/commoncpp/
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man1/ucommon-config.*
%{_mandir}/man1/commoncpp-config.*

%files doc
%doc doc/html/*


%changelog
* Thu Nov 05 2015 Liu Di <liudidi@gmail.com> - 6.6.1-3
- 为 Magic 3.0 重建

* Fri Oct 16 2015 Liu Di <liudidi@gmail.com> - 6.6.1-2
- 为 Magic 3.0 重建

* Mon Oct 05 2015 Sandro Mani <manisandro@gmail.com> - 6.6.1-1
- Update to 6.6.1

* Wed Sep 09 2015 Sandro Mani <manisandro@gmail.com> - 6.6.0-1
- Update to 6.6.0

* Wed Sep 02 2015 Sandro Mani <manisandro@gmail.com> - 6.5.7-1
- Update to 6.5.7

* Mon Aug 24 2015 Sandro Mani <manisandro@gmail.com> - 6.5.4-1
- Update to 6.5.4

* Sun Aug 23 2015 Sandro Mani <manisandro@gmail.com> - 6.5.3-1
- Update to 6.5.3

* Thu Aug 13 2015 Sandro Mani <manisandro@gmail.com> - 6.5.1-1
- Update to 6.5.1

* Mon Aug 03 2015 Sandro Mani <manisandro@gmail.com> - 6.4.4-1
- Update to 6.4.4

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 6.1.3-4
- Rebuilt for GCC 5 C++11 ABI change

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May 03 2014 David Sugar <dyfet@gnutelephony.org> - 6.1.3-1
- Change to using cmake in rpm build
- Upstream fixes for specific memory corruption issues

* Mon Apr 14 2014 David Sugar <dyfet@gnutelephony.org> - 6.1.1-1
- Greater commoncpp compatibility

* Mon Jan 06 2014 David Sugar <dyfet@gnutelephony.org> - 6.1.0-1
- Keywait utility added
- Fixes for correcting commoncpp exception handling

* Sun Jul 28 2013 David Sugar <dyfet@gnutelephony.org> - 6.0.7-1
- Fix for fsys error state reset on file open

* Sun May 05 2013 David Sugar <dyfet@gnutelephony.org> - 6.0.4-1
- Fix for commoncpp address list comparisons

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 29 2012 David Sugar <dyfet@gnutelephony.org> - 6.0.2-1
- Added hmac to usecure

* Tue Nov 20 2012 David Sugar <dyfet@gnutelephony.org> - 6.0.0-1
- new version 6 ucommon api.

* Mon Aug 06 2012 David Sugar <dyfet@gnutelephony.org> - 5.5.0-1
- new listof and mapof classes
- other transitional api changes related to future 6.0 release

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul 05 2012 David Sugar <dyfet@gnutelephony.org> - 5.4.3-1
- fix for threaded queue and stack object creation

* Wed Jun 27 2012 David Sugar <dyfet@gnutelephony.org> - 5.4.2-1
- upstream fixes for zrtp issues in commoncpp host address
- upstream fix for ConditionalAccess

* Tue Jun 26 2012 David Sugar <dyfet@gnutelephony.org> - 5.4.1-1
- new upstream release
- string and process api's extended and clarified
- transitional to 6.0

* Sat Mar 31 2012 David Sugar <dyfet@gnutelephony.org> - 5.2.2-1
- new upstream release
- resolved multi-arch for library paths
- fixed stringpager
- added additional old commoncpp classes back
- honor LC_COLLATE for sorting

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2.0-2
- Rebuilt for c++ ABI breakage

* Sat Jan 21 2012 David Sugar <dyfet@gnutelephony.org> - 5.2.0-1
- New upstream release
- Improved Common C++ compatibility
- New pdetach utility

* Sun Jan 15 2012 David Sugar <dyfet@gnutelephony.org> - 5.1.2-1
- New upstream release

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.4-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jul 11 2011 David Sugar <dyfet@gnutelephony.org> - 5.0.4-0
- template issue with std templates resolved.

* Thu Jun 16 2011 David Sugar <dyfet@gnutelephony.org> - 5.0.3-0
- new linked_pointer to walk address lists.
- new utility sockaddr to check resolver results.

* Sat Jun 11 2011 David Sugar <dyfet@gnutelephony.org> - 5.0.2-0
- cryptographic archiver added
- extended the cipher key management api
- added shell interactive functions

* Sat May 21 2011 David Sugar <dyfet@gnutelephony.org> - 5.0.0-0
- new version 5 abi of ucommon library
- includes GNU Common C++ rebuilt as a library of the ucommon core library.

* Sun May 08 2011 David Sugar <dyfet@gnutelephony.org> - 4.3.3-0
- dup generics and service path added.

* Sun Apr 24 2011 David Sugar <dyfet@gnutelephony.org> - 4.3.2-0
- Bugfixes for named list handling.
- further expansion of string processing and file handling functions.

* Tue Apr 05 2011 David Sugar <dyfet@gnutelephony.org> - 4.3.1-0
- clarifications and bug fixes for abi.

* Sun Apr 03 2011 David Sugar <dyfet@gnutelephony.org> - 4.3.0-0
- major extensions of fsys and keyfile as well as new shell path api.

* Sat Mar 26 2011 David Sugar <dyfet@gnutelephony.org> - 4.2.1-0
- extended keyfile for copy constructor and saving keys.

* Sun Mar 20 2011 David Sugar <dyfet@gnutelephony.org> - 4.2.0-0
- some fixes in linked object abi.
- some cleanup of utility argument parsing and follow options.

* Sat Feb 26 2011 David Sugar <dyfet@gnutelephony.org> - 4.1.6-0
- change to security model for memory mapped objects

* Thu Feb 24 2011 David Sugar <dyfet@gnutelephony.org> - 4.1.5-0
- new generics and fixes for timers

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Oct 01 2010 David Sugar <dyfet@gnutelephony.org> - 4.0.2-0
- new utilities bundled with ucommon library

* Sun Sep 26 2010 David Sugar <dyfet@gnutelephony.org> - 4.0.0-0
- new abi release.

* Sat Sep 18 2010 David Sugar <dyfet@gnutelephony.org> - 3.4.0-0
- simplified packaging and better runtime focus.
- ccscript moved to bayonne, ccaudio detached.

* Tue Aug 10 2010 David Sugar <dyfet@gnutelephony.org> - 3.3.4-0
- major breakage in shell::getsym found and fixed.

* Sun Aug 08 2010 David Sugar <dyfet@gnutelephony.org> - 3.3.3-0
- daemon detach and restart support.
- completion of string to numeric conversions.

* Thu Aug 05 2010 David Sugar <dyfet@gnutelephony.org> - 3.3.1-0
- system logging integrated into shell api.
- string initialization and expression fixes.

* Sun Aug 01 2010 David Sugar <dyfet@gnutelephony.org> - 3.3.0-0
- internationalization bindings with gnu gettext support.
- reorganized utils into ucommon-bin subpackage.

* Sun Jul 11 2010 David Sugar <dyfet@gnutelephony.org> - 3.2.1-0
- uuid generation support and further shell parsing features.

* Sat Jul 03 2010 David Sugar <dyfet@gnutelephony.org> - 3.2.0-0
- extensive fixing in shell class and introduction of piping.

* Sat Jun 26 2010 David Sugar <dyfet@gnutelephony.org> - 3.1.2-0
- fixed clearing of key data when secure objects are released.
- fixed and updated shell parsing class.
- extended secure api so we can also use gnutls, maybe later nss.

* Tue Jun 22 2010 David Sugar <dyfet@gnutelephony.org> - 3.1.0-0
- new ucommon crytographic library added.

* Sun Jun 20 2010 David Sugar <dyfet@gnutelephony.org> - 3.0.6-0
- some further abi extension of the socket class.

* Mon Jun 14 2010 David Sugar <dyfet@gnutelephony.org> - 3.0.5-0
- some abi conflict issues with libc macros on some targets.

* Fri Jun 11 2010 David Sugar <dyfet@gnutelephony.org> - 3.0.4-0
- further revision on the tcp buffering api.

* Fri Jun 11 2010 David Sugar <dyfet@gnutelephony.org> - 3.0.3-2
- critical fix for reusable objects
- new core full duplex buffered io class, tcp and file buffering
- standardized hostname and service address resolver operations
- atomic operations introduced

* Sun Jun 06 2010 David Sugar <dyfet@gnutelephony.org> - 3.0.1-0
- threaded queue management and reuse templates and related bugs fixed.

* Fri Jun 04 2010 David Sugar <dyfet@gnutelephony.org> - 3.0.0-0
- merged ccscript and ccaudio with ucommon to create single framework.

* Tue May 18 2010 David Sugar <dyfet@gnutelephony.org> - 2.1.4-0
- object containers, unicode support, and datetime api enhanced.

* Sun May 02 2010 David Sugar <dyfet@gnutelephony.org> - 2.1.3-0
- critical fix for ieq string function.
- new unicode string class and api introduced.

* Sun Apr 25 2010 David Sugar <dyfet@gnutelephony.org> - 2.1.2-0
- improved portability and api changes for datetime.

* Sun Apr 11 2010 David Sugar <dyfet@gnutelephony.org> - 2.1.1-0
- new abi release

* Fri Dec 18 2009 David Sugar <dyfet@gnutelephony.org> - 2.0.7-1
- fixed install script handling upstream and fixed pedantic gcc 4.4 issues.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue May 05 2009 David Sugar <dyfet@gnutelephony.org> - 2.0.5-4
- removed static libraries, fixed other build issues (#498736)

* Sun May 03 2009 David Sugar <dyfet@gnutelephony.org> - 2.0.5-3
- spec file further revised for redhat/fedora (#498736)

