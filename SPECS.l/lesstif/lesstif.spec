Summary: OSF/Motif library clone
Name: lesstif
Version: 0.95.2
Release: 5%{?dist}
License: LGPLv2+
# in Xm-2.1/
# some files are MIT
# LTV6Editres.c XpmAttrib.c XpmCrBufFrI.c XpmCrBufFrP.c XpmCrDatFrI.c 
# XpmCrDatFrP.c Xpmcreate.c XpmCrIFrBuf.c XpmCrIFrDat.c XpmCrIFrP.c 
# XpmCrPFrBuf.c XpmCrPFrDat.c XpmCrPFrI.c Xpmdata.c Xpmhashtab.c XpmImage.c 
# XpmInfo.c Xpmmisc.c Xpmparse.c XpmRdFToBuf.c XpmRdFToDat.c XpmRdFToI.c 
# XpmRdFToP.c Xpmrgb.c Xpmscan.c Xpms_popen.c XpmWrFFrBuf.c XpmWrFFrDat.c 
# XpmWrFFrI.c XpmWrFFrP.c
# Transltns.c is machine generated (no license, assuming public domain)

# MIT, short version: lib/config/mxmkmf.in

# in includes
# MIT:
# XmI/LTV5EditresP.h XmI/LTV6EditresP.h XmI/XpmI.h Xm/XpmP.h

# clients/Motif-2.1/mwm/
# MIT:
# mwm.h cursors.c decorate.c desktop.c events.c functions.c menus.c misc.c
# mwm.c pan.c props.c resize.c screens.c windows.c
# no restriction
# colormaps.c icons.c move.c pager.c
# GPLV2+
# gethostname.c mwmparse.h

# clients/Motif-2.1/uil/
# no license (LGPLv2+?)
# Expression.c

Group: System Environment/Libraries
Source0: http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Source1: lesstif-xmbind
# mwm session file
Source2: mwm.desktop
Patch0: lesstif-0.95.2-motif-config.patch
Patch1: lesstif-0.95.0-XxxxProperty-64bit.patch
Patch2: lesstif-0.95.0-PutPixel32.patch

Url: http://www.lesstif.org/

BuildRequires: libXp-devel libXt-devel libXext-devel 
BuildRequires: freetype-devel fontconfig-devel
# lynx is used to transform html in txt
BuildRequires: lynx
# for tests
# the libGLw-devel leads to a circular build dependency and the test suite
# is not run, so this BuildRequires is not used.
#BuildRequires: libGLw-devel
BuildRequires: bitmap-devel
# needed for aclocal, to find the aclocal dir for the autoconf macro
BuildRequires: automake
Requires: xorg-x11-xinit 
# obsolete older openmotif may hurt third party repos
# not obsoleting it will leave openmotif on upgrade. 
# Rex makes a MUST not to have this obsolete
#Obsoletes: openmotif <=  2.3.0-0.2.1
# openmotif21 provides the same soname than lesstif. Both seem to work 
# fine with some apps (ddd, xpdf) but show binary incompatibility with
# nedit and runtime incompatible with grace. Moreover openmotif21 libs
# are in /usr/X11R6/lib, and therefore may not be found by the linker.
# A conflict would break upgrade paths.
Obsoletes: openmotif21 <= 2.1.30-17.1.1

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


%description
LessTif is a free replacement for OSF/Motif, which provides a full
set of widgets for application development (menus, text entry areas,
scrolling windows, etc.). LessTif is source compatible with OSF/Motif.

This package provides the lesstif runtime libraries.


%package clients
Summary: Command line utilities for LessTif
License: LGPLv2+
Group: Applications/System
Requires: %{name} = %{version}-%{release}

%description clients
Command line utilities for LessTif:

* xmbind configures the virtual key bindings of LessTif applications.
* uil is a user interface language compiler.

%package mwm
Summary: Lesstif Motif window manager clone based on fvwm
License: GPLv2+
Group: User Interface/Desktops
Requires: %{name} = %{version}-%{release}

%description mwm
"mwm" window manager that adheres largely to the Motif mwm specification.
Based on fvwm.


%package devel
Summary: Header files for LessTif/Motif development
Group: Development/Libraries
Requires: libXt-devel libXp-devel libXext-devel
Requires: imake
# for %{_datadir}/aclocal/
Requires: automake
Requires: %{name} = %{version}-%{release}

# Obsoletes older fedora releases. May hurt third party repos
Obsoletes: openmotif-devel <=  2.3.0-0.2.1


%description devel
Lesstif-devel contains the header files required to develop 
Motif based applications using LessTif. If you want to develop 
LessTif applications, you'll need to install lesstif-devel 
along with lesstif.


%prep
%setup -q
chmod a-x COPYING* doc/www.lesstif.org/BUG-HUNTING.html
%patch0 -p1
%patch1 -p1
%patch2 -p1


%build
# --enable-shared --disable-static is the default
# the x libs and includes are empty in the default case, but we need to 
# have a non empty include defined (for a substitution in mwm)


# --enable-production is needed in order to avoid 
# http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2006-4124
%configure \
  --enable-shared \
  --disable-static \
  --with-xdnd \
  --enable-production \
  --disable-debug \
  --x-includes=%{_includedir} \
  --x-libraries=%{_libdir} CFLAGS="-lfontconfig" 

# Don't use rpath!
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags} \
 mwmddir='%{_sysconfdir}/mwm' libdir='%{_libdir}' \
 appdir='%{_datadir}/X11/app-defaults' configdir='%{_datadir}/X11/config'


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT \
 mwmddir='%{_sysconfdir}/mwm' libdir='%{_libdir}' \
 appdir='%{_datadir}/X11/app-defaults' configdir='%{_datadir}/X11/config' \
 INSTALL="install -p"

# Handle debuginfo dangling-relative-symlink
# rpm doesn't handle symlinks properly when generating debuginfo
rm -rf clients/Motif-2.1/xmbind/xmbind.c
cp -a clients/Motif-1.2/xmbind/xmbind.c \
      clients/Motif-2.1/xmbind/xmbind.c

rm $RPM_BUILD_ROOT%{_libdir}/*.la
rm -rf $RPM_BUILD_ROOT%{_prefix}/LessTif

# install a script that launches xmbind in xinit
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/xinitrc.d
install -p -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/xinitrc.d/xmbind.sh

# install mwm xsession file
mkdir -p $RPM_BUILD_ROOT%{_datadir}/xsessions/
install -p -m644 %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/xsessions/

# correct the paths in mxmkmf
sed -i -e 's:"\${xprefix}/lib/X11/config":"%{_datadir}/X11/config":' \
 -e 's:"\${lprefix}/lib/LessTif/config":"%{_datadir}/X11/config":' \
 $RPM_BUILD_ROOT%{_bindir}/mxmkmf
# use .in timestamp, since the .in and resulting files are the same
touch -r lib/config/mxmkmf.in $RPM_BUILD_ROOT%{_bindir}/mxmkmf

# this is referenced into mwm
mkdir -p $RPM_BUILD_ROOT%{_includedir}/X11/bitmaps/

# will be in in %%doc
rm $RPM_BUILD_ROOT%{_sysconfdir}/mwm/README $RPM_BUILD_ROOT%{_sysconfdir}/mwm/alt.map

# prepare docs
rm -rf __dist_clean_docs
cp -a doc __dist_clean_docs
find __dist_clean_docs -name 'Makefile*' -exec rm {} \;
# correct timestamps of html files generated from man pages
# and remove man pages
for suffix in 1 5 3; do
   for file in __dist_clean_docs/lessdox/*/*.$suffix; do
      basefile=`basename $file .$suffix`
      dir=`dirname $file`
      touch -r $file $dir/$basefile.html
      rm $file
   done
done
# remove the empty directory
rmdir __dist_clean_docs/lessdox/functions

# the corresponding file is not shipped
rm $RPM_BUILD_ROOT%{_mandir}/man*/ltversion*
rm __dist_clean_docs/lessdox/clients/ltversion.html

# remove host.def, it lives in the imake package
rm $RPM_BUILD_ROOT%{_datadir}/X11/config/host.def

# use ChangeLog file timestamp to have the same timestamp on all arches
# for noarch files
touch -r ChangeLog $RPM_BUILD_ROOT%{_datadir}/X11/config/LessTif.tmpl \
 $RPM_BUILD_ROOT%{_includedir}/Xm/Xm.h


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING COPYING.LIB CREDITS AUTHORS BUG-REPORTING FAQ README
%doc NEWS ReleaseNotes.html ReleaseNotes.txt
%{_libdir}/lib*.so.*
%{_mandir}/man1/lesstif*
%{_mandir}/man5/VirtualBindings*

%files mwm
%defattr(-,root,root,-)
%doc clients/Motif-2.1/mwm/README clients/Motif-2.1/mwm/alt.map
%dir %{_sysconfdir}/mwm/
%config(noreplace) %{_sysconfdir}/mwm/system.mwmrc
%{_includedir}/X11/bitmaps/
%{_bindir}/mwm
%{_mandir}/man*/mwm*
%{_datadir}/xsessions/mwm.desktop
%{_datadir}/X11/app-defaults/Mwm

%files clients
%defattr(-,root,root,-)
%{_sysconfdir}/X11/xinit/xinitrc.d/*xmbind.sh
%{_bindir}/xmbind*
%{_bindir}/uil
%{_mandir}/man1/uil*
%{_mandir}/man1/xmbind*

%files devel
%defattr(-,root,root,-)
%doc  __dist_clean_docs/*
%{_bindir}/motif-config
%{_bindir}/mxmkmf
%{_includedir}/Dt/
%{_includedir}/Mrm/
%{_includedir}/Xm/
%{_includedir}/uil/
%{_libdir}/lib*.so
# not shipped
#%{_mandir}/man1/ltversion*
%{_mandir}/man3/*
%{_datadir}/aclocal/ac_find_motif.m4
%{_datadir}/X11/config/*


%changelog
* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 0.95.2-5
- 为 Magic 3.0 重建

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.95.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.95.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.95.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jul 28 2009 Hans de Goede <hdegoede@redhat.com> 0.95.2-1
- New upstream release 0.95.2

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.95.0-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.95.0-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 30 2009 Hans de Goede <hdegoede@redhat.com> 0.95.0-27
- Update description for new trademark guidelines

* Mon Jul  7 2008 Patrice Dumas <pertusus@free.fr> 0.95.0-26
- debian lesstif2_0.95.0-2.1

* Mon Jun 16 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.95.0-25
- Fix PutPixel32 crashing on 64 bit (bz 437133)

* Mon May 12 2008 Patrice Dumas <pertusus@free.fr> 0.95.0-24
- remove the BuildRequires: libGLw-devel, it leads to circular build 
  dependency with no gain

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.95.0-23
- Autorebuild for GCC 4.3

* Sun Oct 21 2007 Patrice Dumas <pertusus@free.fr> 0.95.0-22
- add freetype libs in motif-config

* Sun Oct 21 2007 Patrice Dumas <pertusus@free.fr> 0.95.0-21.1
- remove libdir reference in motif-config, should fix multiarch conflict
  (#341841)

* Sun Sep 16 2007 Patrice Dumas <pertusus@free.fr> 0.95.0-20
- Correct patch XxxxProperty-64bit based on E. Sheldrake input (bz 284431)

* Sat Sep  1 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.95.0-19
- Fix more 64 bit XChange/GetWindowProperty issues (inspired by the
  cut and paste 64 bit fix which was an XChange/GetWindowProperty issue too)
- Fix z88: http://www.z88.uni-bayreuth.de/ not working with lesstif
- Stop lessstif from spewing messages about XtUngrab... (bz 210384)

* Thu Aug 30 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.95.0-18
- Fix cut and paste from / to lesstif apps on 64 bits machines (bz 243508)
- Fix accelkeys which use more then one modifier (bz 214018)

* Thu Aug 30 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.95.0-17
- Update included Debian 0.94.4-2 patch to the Debian 0.95.0-2 patch
- Not only include but also actually apply Debian's patches (bz 261821)
- Add 2 patches with small fixes from lesstif CVS (bz 261821)
- Do not apply lesstif-64.patch it causes more issues then it fixes (bz 253456)

* Wed Aug 15 2007 Patrice Dumas <pertusus@free.fr> 0.95.0-16
- conform better to openmotif API, lesstif-64.patch, by 
  kgallowa at redhat.com
- fix licenses
- keep timestamps
- add mwm xsession file

* Fri Jan  5 2007 Patrice Dumas <pertusus@free.fr> 0.95.0-15
- Obsolete openmotif21 versions provided in older fedora core releases.
  openmotif21 provides the same soname than lesstif, with some 
  incompatibility, and a conflict would break upgrade paths (fix #215560)

* Thu Jan  4 2007 Patrice Dumas <pertusus@free.fr> 0.95.0-14
- don't Obsoletes openmotif with lesstif

* Tue Jan  2 2007 Gilboa Davara <gilboad AT gmail.com> 0.95.0-13
- Fix invalid mouse scroll wheel bind (fix #221055)

* Mon Jan  1 2007 Patrice Dumas <pertusus@free.fr> 0.95.0-12
- Obsolete openmotif versions provided in older fedora core releases to allow
  easier upgrades. Fixes #221083. But may hurt third party packages of 
  openmotif, as reported in #208380

* Mon Jan  1 2007 Patrice Dumas <pertusus@free.fr> 0.95.0-11
- add debian patcheset
- Conflict with openmotif versions provided in older fedora core releases
  (should fix #221083)

* Thu Aug 31 2006 Patrice Dumas <pertusus@free.fr> 0.95.0-10
- remove Conflicts: openmotif-devel, it isn't needed for fedora and
  may hurt external packaging of openmotif. Fix #208380

* Thu Aug 31 2006 Patrice Dumas <pertusus@free.fr> 0.95.0-9
- add Requires: libXext-devel to lesstif-devel

* Wed Aug 30 2006 Tom "spot" Callaway <tcallawa@redhat.com> 0.95.0-8
- better fix for xpdf/ddd (thanks Hans de Goede)
- 64 bit cleanups (thanks Hans de Goede)
- resolve rpmlint error from rpm-braindead behavior on handling symlinks 
  with debuginfo
- fix CAN-2005-0605
- nuke host.def, imake owns that

* Wed Aug 30 2006 Patrice Dumas <pertusus@free.fr> 0.95.0-7
- add a patch such that motif-config honors libdir

* Wed Aug 30 2006 Patrice Dumas <pertusus@free.fr> 0.95.0-6
- split out a clients package that contains xmbind and uil

* Wed Aug 23 2006 Patrice Dumas <pertusus@free.fr> 0.95.0-5
- fix in Dt for x86_64, adapted from Dominik's patch
- don't hardcode /usr/include and /usr/lib
- add a Conflict for openmotif-devel

* Mon Aug 21 2006 Patrice Dumas <pertusus@free.fr> 0.95.0-4
- BuildRequires fontconfig-devel

* Mon Aug 21 2006 Patrice Dumas <pertusus@free.fr> 0.95.0-3
- BuildRequires libGLw-devel
- remove openmotif Obsoletes/Provides
- add versioning to the Obsoletes/Provides for lesstif-clients

* Sun Aug 20 2006 Patrice Dumas <pertusus@free.fr> 0.95.0-2
- BuildRequires automake for the shipped autoconf macro
- add %%dist in release
- tie mwm to the lesstif version and release

* Sat Aug 19 2006 Patrice Dumas <pertusus@free.fr> 0.95.0-1
- update to 0.95.0
- fix paths in mwm and mxmkmf
- adapt to modular X

* Fri Nov 26 2004 Thomas Woerner <twoerner@redhat.com> 0.93.36-7
- fixed CAN-2004-0687 (integer overflows) and CAN-2004-0688 (stack overflows)
  in embedded Xpm library (#135080)
- latest Xpm patches: CAN-2004-0914 (#135081)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Mar 17 2004 Karsten Hopp <karsten@redhat.de> 0.93.36-5.2 
- remove XFree86 requirement, lesstif doesn't require an X server 
  to be installed on the same machine lesstif is installed on
  (#118478)

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Dec 17 2002 Thomas Woerner <twoerner@redhat.com> 0.93.36-2
- renamed RPM tags in changelog

* Sat Nov  9 2002 Than Ngo <than@redhat.com> 0.93.36-1
- update to 0.93.36

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jun 19 2002 Than Ngo <than@redhat.com> 0.93-18-4
- fixed bug #66939

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Feb 27 2002 Than Ngo <than@redhat.com> 0.93-18-2
- rebuild

* Tue Feb 19 2002 Bernhard Rosenkraenzer <bero@redhat.com> 0.93.18-1
- 0.93.18
- Fix download URL

* Wed Jan 16 2002 Than Ngo <than@redhat.com> 0.93-15-4
- get rid of lesstif-mwm, use mwm in openmotif
- fix lesstif so that it can be installed with openmotif
- build only lesstif 1.x since openmotif is in 8.0

* Thu Nov 29 2001 Than Ngo <than@redhat.com> 0.93.15-2
- add missing header files

* Wed Nov 28 2001 Than Ngo <than@redhat.com> 0.93.15-1
- updated to 0.93.15
- fixed bug #56780, #56573, #56821
- sub package mwm
- libXbae and libXlt as separate packages
- disable lesstif 2.x
- clean up patch file for 0.93.15

* Mon Aug 13 2001 Than Ngo <than@redhat.com> 0.92-32-6
- fix bug #51595, #51411 

* Wed Aug  8 2001 Than Ngo <than@redhat.com>
- owns some directories (bug #51154)

* Tue Jul 24 2001 Tim Powers <timp@redhat.com>
- fix dangling symlinks (/usr/X11R6/LessTif/Motif1.2/bin was missing from the filelist)

* Wed Jul 04 2001 Than Ngo <than@redhat.com> 0.92.32-3
- fix package group (Bug #47281)
- Copyright -> License

* Tue Jun 12 2001 Than Ngo <than@redhat.com>
- enable Motif 1.2 as default

* Sat May 02 2001 Than Ngo <than@redhat.com>
- update to 0.92.32
- enable Motif 2.1
- add conflict with openmotif
- add BuildRequires

* Mon Feb 05 2001 Than Ngo <than@redhat.com>
- Obsoletes Xbae, It's a part in lesstif and is up to date.

* Tue Dec 19 2000 Than Ngo <than@redhat.com>
- update to 0.92.0
- bzip2 sources
- add %%clean

* Mon Jul 24 2000 Prospector <prospector@redhat.com>
- rebuilt

* Thu Jul 13 2000 Than Ngo <than@redhat.de>
- fix permission of Xm and Mrm

* Wed Jul 12 2000 Than Ngo <than@redhat.de>
- rebuilt

* Wed May 31 2000 Than Ngo <than@redhat.de>
- update to 0.91.0
- fix conflict with openmotif
- remove part lesstif 2.0
- cleanup specfile

* Sun Apr 16 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 0.90.0
- handle gzip'ed man pages

* Tue Feb  1 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- fix a typo in files list (lib*.a, not lib.*a)

* Wed Jan 19 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 0.89.9
- Fix packaging issues (Bug #8607)
- bzip2 source to save space
- disable debugging

* Sun Nov 21 1999 Bernhard Rosenkraenzer <bero@redhat.com>
- 0.89.4
- some spec file cleanups
- handle RPM_OPT_FLAGS

* Thu Jul 2 1999 Tim Powers <timp@redhat.com>
- added 1.2-devel and 2.0-devel descriptions and file lists
- made default build 2.0
- changed decriptions for all packages
- added Requires: to 1.2-devel, 2.0-devel, clients, and mwm
- built for Powertools

* Thu Apr 30 1998 C. Scott Ananian <cananian@alumni.princeton.edu>      (0.83+)
- Updated to lessdoc-current.
- Removes Lessdox package (integrated into lesstif)

* Tue Mar 31 1998 C. Scott Ananian <cananian@alumni.princeton.edu>      (0.83+)
- Removed pedantic.patch
- Removed lesstif-M12 (Motif 1.2 wrapper)
- Reviewed installation and fixed %%files sections.
- Added patch to fix a bug which causes mozilla to crash.
- Added patch to fix the include prefix on install.

* Sun Jul 20 1997 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>        (0.80-2)
- added to all %%doc %%attr macros (this allow build package from normal user
  account),
- some simplification in %%files (%doc).
* Wed Jul 9 1997 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
- added using %%{PACKAGE_VERSION} macro in "Source:" and %files,
- added additional parameter "--enable-build-12" to runing configure,
- added %%posun and %%clear,
- in %%post and %%postun ldconfig is called as parameter with "-p"
  (this feature is avalable in rpm >= 2.4.3 and you must have this
  version and if you want recompile package from src.rpm you must have new
  version rpm),
- added package lesstif-M12 simpe Motif 1.2 wrapper,
- simplified %%install section,
- added %%attr macros in %%files sections,
- added striping shared libraries,
- added URL field,
- added Lessdox - a html development documentation to lesstif-devel,
- added lesstif-0.80public-nopedantic.patch, this allow compile lesstif on
  sparc by removing "-pedantic" from CFLAGS.
