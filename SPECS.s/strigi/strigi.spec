
%define snap 20120626

Name:		strigi
Version:	0.7.7
Release:	8.20120626%{?dist}
Summary:	A desktop search program
Group:		Applications/Productivity
License:	LGPLv2+
#URL:           http://strigi.sf.net/
URL:            http://www.vandenoever.info/software/strigi/
#Source0:	http://www.vandenoever.info/software/strigi/strigi-%{version}%{?pre:-%{pre}}.tar.bz2
Source0:	http://rdieter.fedorapeople.org/strigi/strigi-%{version}%{?pre:-%{pre}}.tar.xz
Source1:	strigiclient.desktop
Source2:	strigi-daemon.desktop
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

## upstream patches
# strigidaemon
Patch101: 0001-Minor.-Fix-grammar-typo-in-cmake-output.patch
Patch102: 0002-gcc47-fix-unistd.h-header-required-unconditionally-f.patch
Patch103: 0003-Fix-return-value-wrong-type.patch
# libstreamanalizer
Patch201: 0001-Fix-xpm-and-xbm-index.patch
Patch202: 0002-Extract-tracknumber-and-track-count-from-a-value-lik.patch
Patch203: 0003-Fixed-indexing-of-m3u-files.patch
Patch204: 0004-Fix-FLAC-Files-Remove-addtional-db-in-replaygain.patch
Patch205: 0005-Fix-flac-analizer-was-importing-only-one-artist-tag.patch
Patch206: 0006-Fix-non-numeric-genres-in-id3-v2-mp3-are-ignored.patch
Patch207: 0007-Opps-Rmoving-a-wrong-commited-file-id3endanalyzer.cp.patch
Patch208: 0008-fix-parsing-of-genre-field-in-id3v2-tags-and-clean-c.patch

BuildRequires:  bison
BuildRequires:  boost-devel
BuildRequires:  bzip2-devel
BuildRequires:	cmake >= 2.4.5
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
Group:		Development/Libraries
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
%description	devel
Development files for the strigi desktop search engine

%package	libs
Summary:	Strigi libraries
Group:		Development/Libraries
%description	libs
Strigi search engine libraries


%prep
%setup -q -n %{name}-%{version}%{?pre:-%{pre}}

pushd strigidaemon
%patch101 -p1
%patch102 -p1
%patch103 -p1
popd
pushd libstreamanalyzer
%patch201 -p1
%patch202 -p1
%patch203 -p1
%patch204 -p1
%patch205 -p1
%patch206 -p1
%patch207 -p1
%patch208 -p1
popd


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} \
  -DENABLE_CLUCENE:BOOL=OFF \
  -DENABLE_CLUCENE_NG:BOOL=OFF \
  -DENABLE_DBUS:BOOL=ON \
  -DENABLE_FAM:BOOL=ON \
  -DENABLE_FFMPEG:BOOL=OFF \
  %{?_cmake_skip_rpath} \
  ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot}
make install/fast -C %{_target_platform}  DESTDIR=%{buildroot}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE1}

# Add an autostart desktop file for the strigi daemon
install -p -m644 -D %{SOURCE2} %{buildroot}%{_sysconfdir}/xdg/autostart/strigi-daemon.desktop
magic_rpm_clean.sh

%clean
rm -rf %{buildroot}


%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog
%{_bindir}/*
%{_datadir}/applications/*strigiclient.desktop
%{_datadir}/dbus-1/services/*.service
%{_sysconfdir}/xdg/autostart/strigi-daemon.desktop
%if 0%{?clucene}
%{_libdir}/strigi/strigiindex_clucene.so
%endif

%files devel
%defattr(-,root,root,-)
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/libstreamanalyzer.pc
%{_libdir}/pkgconfig/libstreams.pc
%{_libdir}/strigi/StrigiConfig.cmake
%{_libdir}/libsearchclient/
%{_libdir}/libstreamanalyzer/
%{_libdir}/libstreams/
%{_includedir}/strigi/

%files libs
%defattr(-,root,root,-)
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
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 0.7.7-8.20120626
- 为 Magic 3.0 重建

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

* Mon Jan 03 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.7.0-2 
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
