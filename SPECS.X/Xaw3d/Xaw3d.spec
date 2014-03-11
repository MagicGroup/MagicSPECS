Summary: A version of the MIT Athena widget set for X
Name: Xaw3d
Version: 1.6.1
Release: 3%{?dist}
Group: System Environment/Libraries
Source: http://xorg.freedesktop.org/archive/individual/lib/libXaw3d-%{version}.tar.bz2
Patch1: Xaw3d-1.5E-cast.patch
Patch3: Xaw3d-1.6.1-i18n.patch
Patch4: Xaw3d-1.5-box.c.patch
Patch5: Xaw3d-1.5-debian-fixes.patch
Patch7: Xaw3d-1.6.1-3Dlabel.patch
Patch8: Xaw3d-1.5E-close-destroy-crash.patch
Patch9: Xaw3d-1.6.1-compat.patch
Patch10: Xaw3d-1.6.1-fontset.patch
Patch11: Xaw3d-1.6.1-hsbar.patch

License: MIT
URL: http://xorg.freedesktop.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: libXmu-devel
BuildRequires: libXt-devel
BuildRequires: libSM-devel
BuildRequires: libXext-devel
BuildRequires: libX11-devel
BuildRequires: libXpm-devel
BuildRequires: xorg-x11-util-macros
BuildRequires: bison
BuildRequires: flex
BuildRequires: ed

%description
Xaw3d is an enhanced version of the MIT Athena Widget set for
the X Window System.  Xaw3d adds a three-dimensional look to applications
with minimal or no source code changes.

You should install Xaw3d if you are using applications which incorporate
the MIT Athena widget set and you'd like to incorporate a 3D look into
those applications.

%package devel
Summary: Header files and static libraries for development using Xaw3d
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: libXmu-devel
Requires: libXt-devel
Requires: libSM-devel
Requires: libXext-devel
Requires: libX11-devel
Requires: libXpm-devel

%description devel
Xaw3d is an enhanced version of the MIT Athena widget set for
the X Window System.  Xaw3d adds a three-dimensional look to those
applications with minimal or no source code changes. Xaw3d-devel includes
the header files and static libraries for developing programs that take
full advantage of Xaw3d's features.

You should install Xaw3d-devel if you are going to develop applications
using the Xaw3d widget set.  You'll also need to install the Xaw3d
package.


%prep
%setup -q -n libXaw3d-%{version}
%patch1 -p1
%patch3 -p1 -b .i18n
%patch4 -p1
# This doesn't apply cleanly, but has not been applied
#%patch5 -p1 -b .debian
%patch7 -p1 -b .3Dlabel
%patch8 -p1 -b .close-destroy-crash
%patch9 -p1 -b .compat
%patch10 -p1 -b .fontset
%patch11 -p1 -b .hsbar


%build
%configure --disable-static --enable-arrow-scrollbars
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/libXaw3d.la
rm -r $RPM_BUILD_ROOT%{_docdir}


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root)
%doc ChangeLog COPYING README src/README.XAW3D
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/pkgconfig/xaw3d.pc
%{_includedir}/X11/Xaw3d

%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1.6.1-3
- 为 Magic 3.0 重建

* Sat Feb 25 2012 Orion Poplawski <orion@cora.nwra.com> - 1.6.1-2
- Rebase compat patch

* Sat Feb 25 2012 Orion Poplawski <orion@cora.nwra.com> - 1.6.1-1
- Update to 1.6.1

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5E-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5E-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 1 2010 Hans de Goede <hdegoede@redhat.com> - 1.5E-19
- Do not make missing font sets a fatal error (#658526)

* Tue Nov 9 2010 Hans de Goede <hdegoede@redhat.com> - 1.5E-18
- Drop Xaw3d-1.5E-lex.patch it was not applied for a reason (#587349)

* Mon Nov 8 2010 Hans de Goede <hdegoede@redhat.com> - 1.5E-17
- Also apply the Xaw3d-1.5E-secure, Xaw3d-1.5E-thumb and Xaw3d-1.5E-cast
  (replacing xaw3d.patch) patches from http://gitorious.org/xaw3d (#587349)
- Apply accidentally not applied Xaw3d-1.5E-lex.patch

* Mon Nov 8 2010 Orion Poplawski <orion@cora.nwra.com> - 1.5E-16
- Add patches from http://gitorious.org/xaw3d

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5E-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Mar 15 2009 Hans de Goede <hdegoede@redhat.com> 1.5E-14
- Fix a bunch of (potentially harmfull) compiler warnings

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5E-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Oct  6 2008 Hans de Goede <hdegoede@redhat.com> 1.5E-12
- Remove obsolete PreReq and Prefix stuff from specfile
- Fix BuildRoot to match the guidelines
- Require base package by full EVR from devel package
- Drop non relevant Patches and Sources
- Rebase the still relevant patches
- Actually apply the still relevant patches
- Add a patch from Debian fixing an infinite loop (rh436998)
- Add patches from Debian fixes various potential bufferoverflows

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.5E-11.1
- Autorebuild for GCC 4.3

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.5E-10.1
- rebuild

* Wed Jun 07 2006 Than Ngo <than@redhat.com> 1.5E-10 
- BR on bison ed flex #194184 

* Wed Jun  7 2006 Jeremy Katz <katzj@redhat.com> - 1.5E-9
- rebuild for -devel deps

* Tue Apr 25 2006 Adam Jackson <ajackson@redhat.com> 1.5E-8
- Rebuild for new imake build rules

* Tue Feb 28 2006 Than Ngo <than@redhat.com> 1.5E-7
- update Url  #183314

* Mon Feb 13 2006 Jesse Keating <jkeating@redhat.com> - 1.5E-6.2.2
- rebump for build order issues during double-long bump

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.5E-6.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.5E-6.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov 16 2005 Than Ngo <than@redhat.com> 1.5E-6
- fix for modular X

* Tue Nov 05 2005 Warren Togami <wtogami@redhat.com> 1.5E-5
- req individual X dependencies
- remove X11R6 references

* Thu Mar 03 2005 Than Ngo <than@redhat.com> 1.5E-4
- rebuilt

* Thu Jan 20 2005 Than Ngo <than@redhat.com> 1.5E-3
- bump release

* Thu Jan 20 2005 Than Ngo <than@redhat.com> 1.5E-2
- enable ARROW_SCROLLBARS, MULTIPLANE_PIXMAPS

* Tue Nov 30 2004 Than Ngo <than@redhat.com> 1.5E-1
- update to 1.5E, #130310
- fix compiler warning #110766

* Tue Nov 23 2004 Than Ngo <than@redhat.com> 1.5-25
- rebuilt

* Tue Nov 23 2004 Than Ngo <than@redhat.com> 1.5-24
- add patch to fix build problem with xorg-x11, #140475

* Mon Jul 26 2004 Than Ngo <than@redhat.com> 1.5-23
- added requires on XFree86-devel

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Nov 26 2003 Than Ngo <than@redhat.com> 1.5-20
- added missing Buildprereq: XFree86-devel (bug #110601, #109692, #110735)
- fixed arguments in scrollbar (bug #110766)

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Nov  7 2002 han Ngo <than@redhat.com> 1.5-17
- fix some building problems

* Thu Sep  5 2002 Preston Brown <pbrown@redhat.com> 1.5-16
- -DARROW_SCROLLBAR for rms

* Thu Aug  8 2002 Than Ngo <than@redhat.com> 1.5-15
- Added patch file to fix i18n issue, ynakai@redhat.com

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Feb 26 2002 Than Ngo <than@redhat.com> 1.5-12
- rebuild in new enviroment

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Wed Feb 28 2001 Than Ngo <than@redhat.com>
- add requires Xaw3d = %%{version}
- add prereq /sbin/ldconfig

* Tue Oct 10 2000 Than Ngo <than@redhat.com>
- fix link which causes faulty update (Bug #17895)

* Mon Jul 24 2000 Bill Nottingham <notting@redhat.com>
- ia64 tweaks

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jul 10 2000 Bernhard Rosenkraenzer <bero@redhat.de>
- Restore Xaw3d 1.5 - the addition of the backward compatibility library
  killed the current one.
- get rid of the CDEBUGFLAGS="" hack, the current gcc fixes it

* Mon Jul 03 2000 Than Ngo <than@redhat.de>
- fix Imakefile to static Xawd3d

* Sat Jun 17 2000 Than Ngo <than@redhat.de>
- add backward compatibility libXaw3d.so.6 (Bug# 12261)

* Mon May 15 2000 Bill Nottingham <notting@redhat.com>
- fix unaligned traps on ia64

* Mon May  8 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 1.5

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 21)

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Fri Dec 18 1998 Preston Brown <pbrown@redhat.com>
- bumped spec number for initial rh 6.0 build

* Fri Nov 06 1998 Preston Brown <pbrown@redhat.com>
- added security/update patch from debian (the X11R6.3 patch). Thanks guys. :)

* Wed Oct 14 1998 Cristian Gafton <gafton@redhat.com>
- handle the symlink with triggers instead of getting rid of it

* Mon Oct  5 1998 Jeff Johnson <jbj@redhat.com>
- remove backward compatible symlink.

* Wed May 06 1998 Cristian Gafton <gafton@redhat.com>
- fixed the bad symlink
- BuildRoot

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue Nov 04 1997 Erik Troan <ewt@redhat.com>
- don't lave an improper return code from %%pre

* Mon Nov 03 1997 Cristian Gafton <gafton@redhat.com>
- take care of the old location of the Xaw3d includes in case that one exist
- updated Prereq: field

* Mon Oct 26 1997 Cristian Gafton <gafton@redhat.com
- fixed the -devel package for the right include files path

* Mon Oct 13 1997 Donnie Barnes <djb@redhat.com>
- minor spec file cleanups

* Wed Oct 01 1997 Erik Troan <ewt@redhat.com>
- i18n widec.h patch needs to be applied on all systems

* Sun Sep 14 1997 Erik Troan <ewt@redhat.com>
- changed axp check to alpha

* Mon Jun 16 1997 Erik Troan <ewt@redhat.com>
- built against glibc
