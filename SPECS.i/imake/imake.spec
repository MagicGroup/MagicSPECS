Summary: imake source code configuration and build system
Name: imake
Version: 1.0.6
Release: 1%{?dist}
License: MIT
Group: User Interface/X
URL: http://www.x.org

Source0: ftp://ftp.x.org/pub/individual/util/imake-1.0.6.tar.bz2
Source1: ftp://ftp.x.org/pub/individual/util/makedepend-1.0.4.tar.bz2
Source2: ftp://ftp.x.org/pub/individual/util/gccmakedep-1.0.2.tar.bz2
Source3: ftp://ftp.x.org/pub/individual/util/xorg-cf-files-1.0.4.tar.bz2
Source4: ftp://ftp.x.org/pub/individual/util/lndir-1.0.3.tar.bz2
Patch2: xorg-cf-files-1.0.2-redhat.patch
Patch11: imake-1.0.2-abort.patch
Patch12: imake-fputs.patch

BuildRequires: pkgconfig
BuildRequires: xorg-x11-util-macros
BuildRequires: xorg-x11-proto-devel

Provides: ccmakedep cleanlinks gccmakedep lndir makedepend makeg
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
%patch2 -p0 -b .redhat

# imake patches
pushd %{name}-%{version}
%patch11 -p1 -b .abort
%patch12 -p1 -b .fputs
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
#            make install DESTDIR=$RPM_BUILD_ROOT libdir=%%{_datadir}
#            ;;
         *)
            make install DESTDIR=$RPM_BUILD_ROOT
            ;;
      esac
      popd
   done
}

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
#%%dir %%{_mandir}/man1x
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
* Mon Jan 20 2014 Adam Jackson <ajax@redhat.com> 1.0.6-1
- imake 1.0.6

* Mon Dec 09 2013 Adam Jackson <ajax@redhat.com> 1.0.5-8
- Fix imake build with -Werror=format-security (#1037129)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 07 2013 Jon Ciesla <limburgher@gmail.com> 1.0.5-7
- Merge review fixes, BZ 225898.

* Thu Jan 03 2013 Adam Jackson <ajax@redhat.com> 1.0.5-6
- Drop unused patches

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Mar 08 2012 Adam Jackson <ajax@redhat.com> 1.0.5-4
- imake 1.0.5
- lndir 1.0.3
- makedepend 1.0.4
