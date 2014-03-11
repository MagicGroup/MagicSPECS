# SPEC file for libnjb, primary target is the Fedora Extras
# RPM repository.

Name:		libnjb
Version:	2.2.7
Release:	3%{?dist}
Summary:	A software library for talking to the Creative Nomad Jukeboxes and Dell DJs
URL:		http://libnjb.sourceforge.net/

Group:		System Environment/Libraries
Source0:	http://download.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
License:	BSD
Requires:	udev
BuildRequires:	libusb-devel
BuildRequires:	zlib-devel
BuildRequires:	ncurses-devel
BuildRequires:	doxygen

%description
This package provides a software library for communicating with the
Creative Nomad Jukebox line of MP3 players.

%package examples
Summary:        Example programs for libnjb
Group:          Applications/Multimedia
Requires:       %{name} = %{version}-%{release}

%description examples
This package provides example programs for communicating with the
Creative Nomad Jukebox and Dell DJ line of MP3 players.

%package devel
Summary:        Development files for libnjb
Group:          System Environment/Libraries
Requires:       %{name} = %{version}-%{release}
# doc subpackage removed in newer releases, and included
# in the -devel package.
Provides:	libnjb-doc
Obsoletes:	libnjb-doc <= 2.2-1
Requires:	libusb-devel
Requires:	zlib-devel
Requires:	ncurses-devel

%description devel
This package provides development files for the libnjb
library for Creative Nomad/Zen/Jukebox and Dell DJ line of MP3 players.

%prep
%setup -q

%build
%configure --disable-static --program-prefix=njb-
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall
# Remove libtool archive remnant
rm -f $RPM_BUILD_ROOT%{_libdir}/libnjb.la
# Install udev rules file.
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d
install -p -m 644 libnjb.rules $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/60-libnjb.rules
# Copy documentation to a good place
install -p -m 644 AUTHORS ChangeLog ChangeLog-old FAQ \
INSTALL LICENSE HACKING $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
# Touch generated files to make them always have the same time stamp.
touch -r configure.ac \
      $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/html/* \
      $RPM_BUILD_ROOT%{_includedir}/*.h \
      $RPM_BUILD_ROOT%{_libdir}/pkgconfig/*.pc
# Remove the Doxygen HTML documentation, this get different
# each time it is generated and thus creates multiarch conflicts.
# I don't want to pre-generate it but will instead wait for upstream
# to find a suitable solution that will always bring the same files,
# or that Doxygen is fixed not to do this.
#rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/html
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%{_libdir}/*.so.*
%config(noreplace) %{_sysconfdir}/udev/rules.d/*
%files examples
%defattr(-, root, root)
%{_bindir}/*

%files devel
%defattr(-, root, root)
%{_libdir}/*.so
%dir %{_docdir}/%{name}-%{version}
%{_docdir}/%{name}-%{version}/*
%{_includedir}/*.h
%{_libdir}/pkgconfig/*.pc


%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 2.2.7-3
- 为 Magic 3.0 重建

* Mon Oct 29 2012 Liu Di <liudidi@gmail.com> - 2.2.7-2
- 为 Magic 3.0 重建

* Sat Jun 25 2011 Linus Walleij <triad@df.lth.se> 2.2.7-1
- New upstream release, fixing longstanding bug. Nuke HAL support.
* Wed Jun 15 2011 Linus Walleij <triad@df.lth.se> 2.2.6-10
- Tag libnjb devices with a specific ID for autodetection
* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild
* Sat Dec 4 2010 Linus Walleij <triad@df.lth.se> 2.2.6-8
- Fix up ages old udev rules to match latest standards.
* Sat Dec 4 2010 Linus Walleij <triad@df.lth.se> 2.2.6-7
- Rebuild for new glibc, think this is good.
* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild
* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild
* Fri Jul 11 2008 Linus Walleij <triad@df.lth.se> 2.2.6-4
- Loose console permissions. See if docs build fine again.
* Sat Feb 9 2008 Linus Walleij <triad@df.lth.se> 2.2.6-3
- Rebuild for GCC 4.3.
* Wed Oct 24 2007 Linus Walleij <triad@df.lth.se> 2.2.6-2
- Flat out KILL the Doxygen HTML docs to resolve multiarch conflicts.
  Either upstream (that's me!) needs to work around the HTML files being 
  different each time OR Doxygen must stop generating anchors that
  hash the system time, creating different files with each generation.
  Pre-generating the docs is deemed silly. (Someone will disagree.)
* Wed Sep 5 2007 Linus Walleij <triad@df.lth.se> 2.2.6-1
- Long overdue upstream release.
- Shape up udev rules so they look like the libsane stuff.
- Add HAL FDI file.
* Fri Aug 17 2007 Linus Walleij <triad@df.lth.se> 2.2.5-4
- Fixup libnjb udev rules to work with new udev and HAL.
* Mon Aug 28 2006 Linus Walleij <triad@df.lth.se> 2.2.5-3
- Rebuild for Fedora Extras 6.
* Tue Feb 14 2006 Linus Walleij <triad@df.lth.se> 2.2.5-2
- Rebuild for Fedora Extras 5.
* Sun Jan 29 2006 Linus Walleij <triad@df.lth.se> 2.2.5-1
- New upstream release.
* Wed Jan 25 2006 Linus Walleij <triad@df.lth.se> 2.2.4-2
- Fix udev problem, let go of hotplug, fix console perms.
- Still working on libusb vs udev issues.
* Wed Oct 12 2005 Linus Walleij <triad@df.lth.se> 2.2.4-1
- New upstream release.
* Mon Sep 19 2005 Linus Walleij <triad@df.lth.se> 2.2.3-1
- New upstream release.
* Tue Sep 6 2005 Linus Walleij <triad@df.lth.se> 2.2.2-1
- New upstream release.
* Wed Aug 11 2005 Linus Walleij <triad@df.lth.se> 2.2.1-7
- Forgot one extraneous docdir, removing it.
* Wed Aug 10 2005 Linus Walleij <triad@df.lth.se> 2.2.1-6
- Even more fixes after more feedback from Michael.
* Tue Aug 9 2005 Linus Walleij <triad@df.lth.se> 2.2.1-5
- More fixes after feedback from Michael Schwendt.
* Sun Aug 7 2005 Linus Walleij <triad@df.lth.se> 2.2.1-4
- More fixes after feedback from Ralf Corsepius.
* Sat Aug 6 2005 Linus Walleij <triad@df.lth.se> 2.2.1-3
- Remove unnecessary macros.
* Mon Aug 1 2005 Linus Walleij <triad@df.lth.se> 2.2.1-2
- More work on Fedora compliance.
* Sat Jul 30 2005 Linus Walleij <triad@df.lth.se> 2.2.1-1
- Fedora extrafication, created a -devel package.
* Mon Jun 27 2005 Linus Walleij <triad@df.lth.se> 2.2-1
- Fixed a lot of RPM modernization for 2.2 release
* Mon May 23 2005 Linus Walleij <triad@df.lth.se> 2.1.2-1
- Interrim 2.1.2 release. Fixed program prefix.
* Fri May 13 2005 Linus Walleij <triad@df.lth.se> 2.1.1-1
- Interrim 2.1.1 release. Fixed library versioning.
* Tue May 10 2005 Linus Walleij <triad@df.lth.se> 2.1-1
- Final 2.1 release. Removed the checkings for old hotplug versions.
* Fri Mar 4 2005 Ed Welch <ed_welch@inbox.net> 2.0-1mdk
- Mandrake rpm for final 2.0 release.
* Wed Mar 2 2005 Linus Walleij <triad@df.lth.se> 2.0-1
- Final 2.0 release.
* Mon Feb 21 2005 Linus Walleij <triad@df.lth.se> 2.0-0.RC1
- Release candidate 1 for 2.0.
* Tue Feb 8 2005 Linus Walleij <triad@df.lth.se> 2.0-0.20050208
- Third CVS snapshot for the pre-2.0 series.
* Thu Jan 20 2005 Linus Walleij <triad@df.lth.se> 2.0-0.20050120
- Second CVS snapshot for the pre-2.0 series.
* Mon Jan 10 2005 Linus Walleij <triad@df.lth.se> 2.0-0.20050110
- A CVS snapshot for the first pre-2.0 series.
* Tue Nov 30 2004 Linus Walleij <triad@df.lth.se> 1.3-0.20041130
- A CVS snapshot for the new API and all.
* Wed Sep 29 2004 Linus Walleij <triad@df.lth.se> 1.2-0.20040929
- A CVS snapshot, much needed, which also works
* Fri Sep 24 2004 Linus Walleij <triad@df.lth.se> 1.2-0.20040924
- A CVS snapshot, much needed.
* Tue May 25 2004 Linus Walleij <triad@df.lth.se> 1.1-1
- Added hook to redistribute pkgconfig module
* Wed Apr 25 2004 Linus Walleij <triad@df.lth.se> 1.1-1
- Final 1.1 release!
* Wed Apr 21 2004 Linus Walleij <triad@df.lth.se> 1.0.2-0.20040421
- A new CVS snapshot.
* Fri Apr 9 2004 Linus Walleij <triad@df.lth.se> 1.0.2-0.20040409
- A new CVS snapshot.
* Sun Feb 22 2004 Linus Walleij <triad@df.lth.se> 1.0.2-0.20040222
- A new CVS snapshot. Adressing several bugs.
* Fri Jan 9 2004 Linus Walleij <triad@df.lth.se> 1.0.1-0.20040109
- A new CVS release adressing bugs, better numbering scheme
* Tue Dec 9 2003 Linus Walleij <triad@df.lth.se> 1.0.1-1
- Addressed some issues in 1.0
* Tue Dec 9 2003 Linus Walleij <triad@df.lth.se> 1.0-2
- Second package for samples
* Sat Dec 6 2003 Linus Walleij <triad@df.lth.se> 1.0-1
- Final 1.0 release
* Sun Aug 17 2003 Linus Walleij <triad@df.lth.se> 1.1.0b-6
- Seventh RPM
* Sun Aug 17 2003 Linus Walleij <triad@df.lth.se> 1.1.0b-5
- Sixth RPM
* Thu Jul 31 2003 Linus Walleij <triad@df.lth.se> 1.1.0b-4
- Fifth RPM
* Wed Jun 11 2003 Linus Walleij <triad@df.lth.se> 1.1.0b-3
- Fourth RPM.
* Mon Apr 21 2003 Linus Walleij <triad@df.lth.se> 1.1.0b-2
- Third RPM, big improvements in hotplug installation.
* Sun Mar 30 2003 Linus Walleij <triad@df.lth.se> 1.1.0b
- Second CVS RPM
* Thu Dec 26 2002 Dwight Engen <dengen40@yahoo.com> 0.9.1
- First RPM'ed
