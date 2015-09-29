
## include clucene support (not used since fedora 15)
#global clucene 1

Name:		strigi
Summary:        A desktop search program
Version:	0.7.8
Release:	11%{?dist}

License:	LGPLv2+
#URL:            https://projects.kde.org/projects/kdesupport/strigi
URL:            http://www.vandenoever.info/software/strigi/
Source0:	http://www.vandenoever.info/software/strigi/strigi-%{version}%{?pre:-%{pre}}.tar.bz2
#Source0:	http://rdieter.fedorapeople.org/strigi/strigi-%{version}%{?pre:-%{pre}}.tar.xz
Source1:	strigiclient.desktop
Source2:	strigi-daemon.desktop

## upstream patches
Patch11: libstreamanalyzer-0001-Fix-for-non-valid-values-in-Exif-field-ISOSpeedRatin.patch
Patch12: libstreamanalyzer-0002-order-matters-for-systems-that-have-things-already-i.patch
Patch13: libstreamanalyzer-0003-Fix-Krazy-issues.patch
Patch14: libstreamanalyzer-0004-ffmpeg-Rename-mutex-to-g_mutex.patch
Patch15: libstreamanalyzer-0005-use-rpath-only-when-needed.patch
Patch21: libstreams-0001-Generate-config.h-after-looking-for-dependencies.patch
Patch22: libstreams-0002-Reduce-noise-in-analysis-tools-complain-about-resour.patch
Patch23: libstreams-0003-Build-fix-for-gcc-4.8.patch
Patch24: libstreams-0004-Fix-Krazy-issues.patch
Patch25: libstreams-0005-use-rpath-only-when-needed.patch
Patch31: strigiclient-0001-use-rpath-only-when-needed.patch
Patch41: strigidaemon-0001-Fix-Krazy-issues.patch
Patch42: strigidaemon-0002-use-rpath-only-when-needed.patch
Patch51: strigiutils-0001-use-rpath-only-when-needed.patch

BuildRequires:  bison
BuildRequires:  bzip2-devel
BuildRequires:	cmake >= 2.4.5
%if 0%{?clucene:1}
BuildRequires:	clucene-core-devel
%endif
BuildRequires:  desktop-file-utils
BuildRequires:  expat-devel
BuildRequires:  pkgconfig(cppunit)
BuildRequires:  pkgconfig(dbus-1) dbus-x11
BuildRequires:  pkgconfig(exiv2)
BuildRequires:  pkgconfig(gamin)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(QtDBus) pkgconfig(QtGui)
BuildRequires:  pkgconfig(zlib)

Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description
Strigi is a fast and light desktop search engine. It can handle a large range
of file formats such as emails, office documents, media files, and file
archives. It can index files that are embedded in other files. This means email
attachments and files in zip files are searchable as if they were normal files
on your harddisk.

Strigi is normally run as a background daemon that can be accessed by many
other programs at once. In addition to the daemon, Strigi comes with powerful
replacements for the popular unix commands 'find' and 'grep'. These are called
'deepfind' and 'deepgrep' and can search inside files just like the strigi
daemon can.

%package	devel
Summary:	Development files for the strigi desktop search engine
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
%description	devel
Development files for the strigi desktop search engine

%package	libs
Summary:	Strigi libraries
%description	libs
Strigi search engine libraries


%prep
%setup -q -n %{name}-%{version}%{?pre:-%{pre}}

pushd libstreamanalyzer
%patch11 -p1 -b .11
%patch12 -p1 -b .12
%patch13 -p1 -b .13
%patch14 -p1 -b .14
%patch15 -p1 -b .15
popd
pushd libstreams
%patch21 -p1 -b .21
%patch22 -p1 -b .22
%patch23 -p1 -b .23
%patch24 -p1 -b .24
%patch25 -p1 -b .25
popd
pushd strigiclient
%patch31 -p1 -b .31
popd
pushd strigidaemon
%patch41 -p1 -b .41
%patch42 -p1 -b .42
popd
pushd strigiutils
%patch51 -p1 -b .51
popd


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} \
%if ! 0%{?clucene:1}
  -DENABLE_CLUCENE:BOOL=OFF \
  -DENABLE_CLUCENE_NG:BOOL=OFF \
%endif
  -DENABLE_DBUS:BOOL=ON \
  -DENABLE_FAM:BOOL=ON \
  -DENABLE_FFMPEG:BOOL=OFF \
  ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast -C %{_target_platform}  DESTDIR=%{buildroot}

desktop-file-install \
  --vendor="%{?dt_vendor}" \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE1}

# Add an autostart desktop file for the strigi daemon
install -p -m644 -D %{SOURCE2} %{buildroot}%{_sysconfdir}/xdg/autostart/strigi-daemon.desktop


%check
export CTEST_OUTPUT_ON_FAILURE=1
# make non-fatal, some failures on big-endian archs
make test -C %{_target_platform} ||:


%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%doc AUTHORS COPYING ChangeLog
%{_bindir}/*
%{_datadir}/applications/*strigiclient.desktop
%{_datadir}/dbus-1/services/*.service
%{_sysconfdir}/xdg/autostart/strigi-daemon.desktop
%if 0%{?clucene}
%{_libdir}/strigi/strigiindex_clucene.so
%endif

%files devel
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/libstreamanalyzer.pc
%{_libdir}/pkgconfig/libstreams.pc
%dir %{_libdir}/cmake/
%{_libdir}/cmake/Strigi/
%{_libdir}/cmake/LibSearchClient/
%{_libdir}/cmake/LibStreamAnalyzer/
%{_libdir}/cmake/LibStreams/
%{_includedir}/strigi/

%files libs
%{_datadir}/strigi/
%{_libdir}/libsearchclient.so.0*
%{_libdir}/libstreamanalyzer.so.0*
%{_libdir}/libstreams.so.0*
%{_libdir}/libstrigihtmlgui.so.0*
%{_libdir}/libstrigiqtdbusclient.so.0*
%dir %{_libdir}/strigi/
%{_libdir}/strigi/strigiea_*.so
%{_libdir}/strigi/strigila_*.so
%{_libdir}/strigi/strigita_*.so


%changelog
* Wed Jun 24 2015 Rex Dieter <rdieter@fedoraproject.org> - 0.7.8-11
- rebuild (exiv2)

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Apr 17 2015 Rex Dieter <rdieter@fedoraproject.org> 0.7.8-9
- rebuild (gcc5)

* Wed Feb 18 2015 Rex Dieter <rdieter@fedoraproject.org> 0.7.8-8
- rebuild (gcc5)

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Rex Dieter <rdieter@fedoraproject.org> 0.7.8-5
- tests failing on big endians (#1071527)

* Wed Jan 01 2014 Rex Dieter <rdieter@fedoraproject.org> - 0.7.8-4
- cleanup, drop deprecated bits
- -devel: drop dep on cmake
- pull in some upstream patches (particular rpath fixes)
- %%check: +make test

* Tue Dec 03 2013 Rex Dieter <rdieter@fedoraproject.org> 0.7.8-3
- rebuild (exiv2)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 06 2013 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0.7.8-1
- update to 0.7.8 (#981869)
- drop backported patches (already included in 0.7.8)
- no longer BuildRequires boost-devel
- -devel: Requires: cmake for directory ownership

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.7-8.20120626
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jul 30 2012 Rex Dieter <rdieter@fedoraproject.org> 0.7.7-7.20120626
- rebuild (boost)

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.7-6.20120626
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 26 2012 Rex Dieter <rdieter@fedoraproject.org> 0.7.7-5.20120626
- backport upstream patches (as of 20120626)

* Wed May 02 2012 Rex Dieter <rdieter@fedoraproject.org> 0.7.7-4
- rebuild (exiv2)

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.7-3
- Rebuilt for c++ ABI breakage

* Mon Jan 09 2012 Rex Dieter <rdieter@fedoraproject.org> 0.7.7-2
- gcc47 patch

* Mon Jan 09 2012 Rex Dieter <rdieter@fedoraproject.org> 0.7.7-1
- 0.7.7
- upstream xpm patch

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.6-4
- Rebuilt for glibc bug#747377

* Mon Oct 17 2011 Rex Dieter <rdieter@fedoraproject.org> 0.7.6-3
- Revert commit that breaks parsing of some PDF files

* Fri Oct 14 2011 Rex Dieter <rdieter@fedoraproject.org> - 0.7.6-2
- rebuild (exiv2)

* Tue Oct 04 2011 Rex Dieter <rdieter@fedoraproject.org> 0.7.6-1
- 0.7.6
- BR: boost-devel
- pkgconfig-style deps

* Tue Aug 16 2011 Rex Dieter <rdieter@fedoraproject.org> 0.7.5-5
- libstreams rpm analyzer fixed upstream

* Sun Aug 07 2011 Rex Dieter <rdieter@fedoraproject.org> 0.7.5-4
- enable dbus/fam support

* Sun Aug 07 2011 Rex Dieter <rdieter@fedoraproject.org> 0.7.5-3
- explicitly mark convenience libs static

* Fri Aug 05 2011 Rex Dieter <rdieter@fedoraproject.org> 0.7.5-2
- rebuild

* Fri Jul 29 2011 Rex Dieter <rdieter@fedoraproject.org> 0.7.5-1
- strigi-0.7.5 (#726507)

* Mon Jun 06 2011 Rex Dieter <rdieter@fedoraproject.org> 0.7.2-10
- drop clucene support, for now (f16+)

* Thu Jun 02 2011 Rex Dieter <rdieter@fedoraproject.org> 0.7.2-9
- move strigiindex_clucene.so to main pkg
- drop .desktop --vendor (f16+)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 01 2011 Rex Dieter <rdieter@fedoraproject.org> - 0.7.2-7
- rebuild (exiv2)

* Fri Nov 05 2010 Thomas Janssen <thomasj@fedoraproject.org> 0.7.2-6
- rebuild for new libxml2

* Mon Jul 12 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.7.2-5
- disable rpmanalyzer support, until crasher(s) fixed (#609541)
- tidy up spec

* Wed Jun 30 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.7.2-4
- strigi flac analyser crashes with floating point (arithmetic) exception (kdebug234398)

* Mon May 31 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.7.2-3
- rebuild (exiv2)

* Fri Feb 12 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.7.2-2
- %%build: +%%_cmake_skip_rpath

* Fri Feb 12 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.7.2-1
- strigi-0.7.2

* Mon Jan 11 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.7.1-1
- strigi-0.7.1

* Mon Jan 04 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.7.0-2
- rebuild (exiv2)

* Tue Aug 04 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.7.0-1
- strigi-0.7.0 (final)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-0.2.RC1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 Rex Dieter <rdieter@fedoraproject.org> 0.7-0.1.RC1
- strigi-0.7-RC1
- use %%_isa where appropriate
- %%files: track lib sonames
- strigi-daemon.desktop: +Hidden=true (ie, disable autostart by default)

* Mon Jun 29 2009 Lukáš Tinkl <ltinkl@redhat.com> - 0.6.5-2
- don't start strigi daemon unconditionally (#487322)

* Fri May 29 2009 Lukáš Tinkl <ltinkl@redhat.com> - 0.6.5-1
- Strigi 0.6.5

* Tue Apr 21 2009 Jaroslav Reznik <jreznik@redhat.com> - 0.6.4-4
- fix crash with / char in path (#496620, kde#185551)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 04 2009 Deji Akingunola <dakingun@gmail.com> - 0.6.4-2
- Add patch to build with gcc-4.4

* Mon Feb 02 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.6.4-1
- strigi-0.6.4
- Summary: s/for KDE//
- *.desktop: validate, remove OnlyShowIn=KDE
- -devel: move *.cmake here

* Mon Jan 12 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.6.3-1
- strigi-0.6.3

* Tue Jan 06 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.6.2-1
- strigi-0.6.2
- use %%cmake macro

* Thu Dec 18 2008 Rex Dieter <rdieter@fedoraproject.org> - 0.5.11.1-2 
- respin (exiv2)

* Thu Nov 27 2008 Lorenzo Villani <lvillani@binaryhelix.net> - 0.5.11.1-1
- drop _default_patch_fuzz
- rebase strigi-multilib patch
- No official 0.5.11.1 tarballs were released but we need 0.5.11.1, apply a
  diff between 0.5.11 and 0.5.11.1 svn tags

* Sun Jul 20 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0.5.11-1
- Update to 0.5.11
- Drop compile-fix and lucenetest_fix patches (fixed upstream)

* Sat May 10 2008 Deji Akingunola <dakingun@gmail.com> - 0.5.9-2
- Disable 'make test' for now, seems the buildroot cannot find java

* Sat May 03 2008 Deji Akingunola <dakingun@gmail.com> - 0.5.9-1
- Update to 0.5.9 (bugfix release)

* Thu Mar 06 2008 Deji Akingunola <dakingun@gmail.com> - 0.5.8-2
- Use upstream's default build options (disable inotify support, #436096)

* Thu Feb 21 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0.5.8-1
- Update to 0.5.8
- Fix LIB_DESTINATION (#433627)
- Drop GCC 4.3 patch (fixed upstream)

* Sat Feb 09 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0.5.7-4
- Rebuild for GCC 4.3

* Fri Jan 11 2008 Deji Akingunola <dakingun@gmail.com> - 0.5.7-3
- Fix build failure with gcc-4.3

* Tue Nov 13 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0.5.7-2
- Rebuild for new exiv2

* Tue Oct 30 2007 Deji Akingunola <dakingun@gmail.com> - 0.5.7-1
- Update to 0.5.7 release
- Fix multilibs conflict (Bug #343221, patch by Kevin Kofler)

* Sun Sep 09 2007 Deji Akingunola <dakingun@gmail.com> - 0.5.5-2
- Rebuild for BuildID changes

* Sat Aug 11 2007 Deji Akingunola <dakingun@gmail.com> - 0.5.5-1
- Update to 0.5.5 release

* Mon Aug 06 2007 Deji Akingunola <dakingun@gmail.com> - 0.5.4-1
- Update to 0.5.4 proper
- License tag update

* Sun Jul 29 2007 Deji Akingunola <dakingun@gmail.com> - 0.5.4-0.1.svn20070729
- New KDE SVN snapshot version for KDE 4.0 beta 1 (bz#20015)

* Wed May 16 2007 Deji Akingunola <dakingun@gmail.com> - 0.5.1-5
- Split out a strigi-libs subpackage as suggested in BZ#223586
_ Include a strigidaemon autostart desktop file

* Sat May 05 2007 Deji Akingunola <dakingun@gmail.com> - 0.5.1-4
- Add dbus-devel BR.

* Sat May 05 2007 Deji Akingunola <dakingun@gmail.com> - 0.5.1-3
- Misc. fixes from package review

* Fri May 04 2007 Deji Akingunola <dakingun@gmail.com> - 0.5.1-2
- Updates from reviews:
-	Have the -devel subpackage require pkgconfig
-	Add a versioned dependency on cmake and remove dbus-qt buildrequire

* Fri May 04 2007 Deji Akingunola <dakingun@gmail.com> - 0.5.1-1
- New release

* Wed May 02 2007 Deji Akingunola <dakingun@gmail.com> - 0.3.11-3
- Allow building on FC6

* Thu Feb 22 2007 Deji Akingunola <dakingun@gmail.com> - 0.3.11-2
- Assorted fixed arising from reviews

* Wed Jan 17 2007 Deji Akingunola <dakingun@gmail.com> - 0.3.11-1
- Initial packaging for Fedora Extras
