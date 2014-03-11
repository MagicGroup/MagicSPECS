Summary: imake source code configuration and build system
Name: imake
Version: 1.0.5
Release: 6%{?dist}
License: MIT
Group: User Interface/X
URL: http://www.x.org

Source0: ftp://ftp.x.org/pub/individual/util/imake-1.0.5.tar.bz2
Source1: ftp://ftp.x.org/pub/individual/util/makedepend-1.0.4.tar.bz2
Source2: ftp://ftp.x.org/pub/individual/util/gccmakedep-1.0.2.tar.bz2
Source3: ftp://ftp.x.org/pub/individual/util/xorg-cf-files-1.0.4.tar.bz2
Source4: ftp://ftp.x.org/pub/individual/util/lndir-1.0.3.tar.bz2
Patch0: xorg-cf-files-1.0.0-misc.patch
Patch1: xorg-cf-files-1.0.0-ProjectRoot.patch
Patch2: xorg-cf-files-1.0.2-redhat.patch
Patch11: imake-1.0.2-abort.patch

BuildRequires: pkgconfig
BuildRequires: xorg-x11-util-macros
BuildRequires: xorg-x11-proto-devel

Provides: ccmakedep cleanlinks gccmakedep imake lndir makedepend makeg
Provides: mergelib mkdirhier mkhtmlindex revpath xmkmf

%description
Imake is a deprecated source code configuration and build system which
has traditionally been supplied by and used to build the X Window System
in X11R6 and previous releases.  As of the X Window System X11R7 release,
the X Window system has switched to using GNU autotools as the primary
build system, and the Imake system is now deprecated, and should not be
used by new software projects.  Software developers are encouraged to
migrate software to the GNU autotools system.

%prep
%setup -q -c %{name}-%{version} -a1 -a2 -a3 -a4
#%patch0 -p0 -b .imake
#%patch1 -p0 -b .ProjectRoot
%patch2 -p0 -b .redhat

# imake patches
pushd %{name}-%{version}
%patch11 -p1 -b .abort
popd

%build
# Build everything
{
   for pkg in imake makedepend gccmakedep lndir xorg-cf-files ; do
      pushd $pkg-*
      case $pkg in
         imake|xorg-cf-files)
            %configure --with-config-dir=%{_datadir}/X11/config
            ;;
         *)
            %configure
            ;;
      esac
      make
      popd
   done
}

%install
rm -rf $RPM_BUILD_ROOT

# Install everything
{
   for pkg in imake makedepend gccmakedep lndir xorg-cf-files ; do
      pushd $pkg-*
      case $pkg in
#         xorg-cf-files)
#            make install DESTDIR=$RPM_BUILD_ROOT libdir=%{_datadir}
#            ;;
         *)
            make install DESTDIR=$RPM_BUILD_ROOT
            ;;
      esac
      popd
   done
}
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc
%{_bindir}/ccmakedep
%{_bindir}/cleanlinks
%{_bindir}/gccmakedep
%{_bindir}/imake
%{_bindir}/lndir
%{_bindir}/makedepend
%{_bindir}/makeg
%{_bindir}/mergelib
%{_bindir}/mkdirhier
%{_bindir}/mkhtmlindex
%{_bindir}/revpath
%{_bindir}/xmkmf
%dir %{_datadir}/X11/config
%{_datadir}/X11/config/*.cf
%{_datadir}/X11/config/*.def
%{_datadir}/X11/config/*.rules
%{_datadir}/X11/config/*.tmpl
#%dir %{_mandir}/man1x
%{_mandir}/man1/ccmakedep.1*
%{_mandir}/man1/cleanlinks.1*
%{_mandir}/man1/gccmakedep.1*
%{_mandir}/man1/imake.1*
%{_mandir}/man1/lndir.1*
%{_mandir}/man1/makedepend.1*
%{_mandir}/man1/makeg.1*
%{_mandir}/man1/mergelib.1*
%{_mandir}/man1/mkdirhier.1*
%{_mandir}/man1/mkhtmlindex.1*
%{_mandir}/man1/revpath.1*
%{_mandir}/man1/xmkmf.1*

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.0.5-6
- 为 Magic 3.0 重建

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Mar 08 2012 Adam Jackson <ajax@redhat.com> 1.0.5-4
- imake 1.0.5
- lndir 1.0.3
- makedepend 1.0.4

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 06 2011 Adam Jackson <ajax@redhat.com> 1.0.4-2
- xorg-cf-files 1.0.4
- xorg-cf-files-1.0.2-xprint.patch: Drop, merged.

* Mon Nov 01 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.0.4-1
- imake 1.0.4
- makedepend 1.0.3
- lndir 1.0.2

* Mon Oct 25 2010 Adam Jackson <ajax@redhat.com> 1.0.2-15
- imake-1.0.2-abort.patch: Paper over an abort (#646561)

* Mon Oct 25 2010 Adam Jackson <ajax@redhat.com> 1.0.2-14
- Don't own things owned by filesystem (#569411)

* Mon Feb 22 2010 Matěj Cepl <mcepl@redhat.com> - 1.0.2-13
-  lndir should ignore .git directory (RH BZ #538249)

* Mon Oct 19 2009 Adam Jackson <ajax@redhat.com> 1.0.2-12
- xorg-cf-files 1.0.3.3.3

* Tue Oct 13 2009 Adam Jackson <ajax@redhat.com> 1.0.2-11
- makedepend 1.0.2

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb 08 2009 Adam Jackson <ajax@redhat.com> 1.0.2-8
- imake-1.0.2-find-pedantry.patch: Silence useless pedantry warning from
  find(1) when running cleanlinks. (#483126)

* Tue Jul 15 2008 Adam Jackson <ajax@redhat.com> 1.0.2-7
- Fix license tag.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.2-6
- Autorebuild for GCC 4.3

* Tue Aug 21 2007 Adam Jackson <ajax@redhat.com> - 1.0.2-5
- Rebuild for build id

* Mon Mar 26 2007 Adam Jackson <ajax@redhat.com> 1.0.2-4
- makedepend 1.0.1

* Tue Jul 18 2006 Than Ngo <than@redhat.com> 1.0.2-3
- cleanup patch files
- update source files

* Fri Jul 14 2006 Jesse Keating <jkeating@redhat.com> - 1.0.2-2
- rebuild

* Wed Jun 21 2006 Mike A. Harris <mharris@redhat.com> 1.0.2-1
- Update to imake-1.0.2, gccmakedep-1.0.2, xorg-cf-files-1.0.2

* Tue Apr 25 2006 Adam Jackson <ajackson@redhat.com> 1.0.1-4
- Fix ExtraXawReqs to reflect reality (libXp is unneeded)

* Mon Mar 06 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-3
- Updated xorg-cf-files-1.0.1-redhat.patch with fix for (#178177)

* Wed Mar 01 2006 Karsten Hopp <karsten@redhat.de> 1.0.1-2
- Buildrequires: xorg-x11-proto-devel

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> 1.0.1-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> 1.0.1-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 18 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-1
- Updated all packages to version 1.0.1 from X11R7.0

* Wed Dec 21 2005 Than Ngo <than@redhat.com> 1.0.0-4
- final fix for #173593

* Tue Dec 20 2005 Than Ngo <than@redhat.com> 1.0.0-3
- add correct XAppLoadDir #173593
- add more macros for fedora

* Mon Dec 19 2005 Than Ngo <than@redhat.com> 1.0.0-2
- add some macros to fix problem in building of manpages

* Sat Dec 17 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-1
- Updated all packages to version 1.0.0 from X11R7 RC4
- Added new lndir, gccmakedep tarballs.  (#173478)
- Changed manpage dirs from man1x to man1 to match upstream RC4 default.
- Removed all previous 'misc' patch, as we now pass --with-config-dir to
  configure to specify the location of the Imake config files.
- Renamed imake patch to xorg-cf-files-1.0.0-ProjectRoot.patch as it did not
  patch imake at all.  This should probably be changed to be a custom Red Hat
  host.def file that is added as a source line instead of randomly patching
  various files.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com> 0.99.2-5.1
- rebuilt

* Mon Nov 28 2005 Than Ngo <than@redhat.com> 0.99.2-5
- add correct ProjectRoot for modular X

* Wed Nov 16 2005 Than Ngo <than@redhat.com> 0.99.2-4 
- add missing host.conf

* Wed Nov 16 2005 Than Ngo <than@redhat.com> 0.99.2-3
- fix typo 

* Wed Nov 16 2005 Than Ngo <than@redhat.com> 0.99.2-2
- fix xmkmf to look config files in /usr/share/X11/config
  instead /usr/%%{_lib}/X11/config/
- add host.conf

* Fri Nov 11 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-1
- Updated to imake-0.99.2, xorg-cf-files-0.99.2, makedepend-0.99.2 from
  X11R7 RC2.

* Thu Nov 10 2005 Mike A. Harris <mharris@redhat.com> 0.99.1-1
- Initial build.
