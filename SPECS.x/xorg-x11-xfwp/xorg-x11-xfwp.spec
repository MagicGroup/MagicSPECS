%define pkgname xfwp
%define xfwp_version 1.0.2

Summary: X.Org X11 X firewall proxy
Summary(zh_CN.UTF-8): X.Org X11 X 防火墙代理
Name: xorg-x11-%{pkgname}
# NOTE: The package version should always be the upstream xfwp tarball version.
Version: %{xfwp_version}
Release: 6%{?dist}
License: MIT
Group: User Interface/X
Group(zh_CN.UTF-8): 用户界面/X
URL: http://www.x.org

Source0: http://ftp.nara.wide.ad.jp/pub/X11/x.org/individual/app/xfwp-%{xfwp_version}.tar.bz2
Source1: http://ftp.nara.wide.ad.jp/pub/X11/x.org/individual/app/proxymngr-1.0.2.tar.bz2
Source2: http://ftp.nara.wide.ad.jp/pub/X11/x.org/individual/app/xfindproxy-1.0.1.tar.bz2

Patch0: proxymngr-1.0.1-lbxproxy-die-die-die.patch
Patch1: proxymngr-1.0.1-config.patch

# FIXME: Temporary dependencies on autotools stuff for patch workaround.
BuildRequires: automake autoconf libtool

BuildRequires: pkgconfig
BuildRequires: libICE-devel libXt-devel
BuildRequires: xorg-x11-proto-devel
BuildRequires: xorg-x11-util-macros

# FIXME:These old provides should be removed
Provides: xfwp proxymngr xfindproxy

%description
The X firewall proxy (xfwp) is an application layer gateway proxy that
may be run on a network firewall host to forward X traffic  across  the
firewall.

%description -l zh_CN.UTF-8
X.Org X11 X 防火墙代。

%prep
%setup -q -c %{name}-%{version} -a1 -a2

%patch0 -p0 -b .lbx
%patch1 -p0 -b .config

%build
# Build everything.
# Have to reautofoo proxymngr until we sort out LBX stuff upstream.
{
   for pkg in * ; do
      pushd $pkg
      case $pkg in
         proxymngr*)
            aclocal ; libtoolize --force ; automake -avf ; autoconf
     ;;
  *)
     ;;
      esac
      %configure
      make %{?_smp_mflags}
      popd
   done
}

%install
# Install everything
{
   for pkg in * ; do
      pushd $pkg
      make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
      popd
   done
}

%files
%defattr(-,root,root,-)
%doc
%{_bindir}/proxymngr
%{_bindir}/xfindproxy
%{_bindir}/xfwp
%dir %{_sysconfdir}/X11/proxymngr
%{_sysconfdir}/X11/proxymngr/pmconfig
%{_mandir}/man1/proxymngr.1*
%{_mandir}/man1/xfindproxy.1*
%{_mandir}/man1/xfwp.1*

%changelog
* Sun Nov 15 2015 Liu Di <liudidi@gmail.com> - 1.0.2-6
- 为 Magic 3.0 重建

* Fri Nov 06 2015 Liu Di <liudidi@gmail.com> - 1.0.2-5
- 为 Magic 3.0 重建

* Tue Oct 27 2015 Liu Di <liudidi@gmail.com> - 1.0.2-4
- 为 Magic 3.0 重建

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Adam Jackson <ajax@redhat.com> 1.0.2-1
- xfwp 1.0.2
- proxymngr 1.0.2

* Fri Apr 01 2011 Adam Jackson <ajax@redhat.com> 1.0.1-14
- Fix pmconfig install path configuration

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Sep 25 2010 Parag Nemade <paragn AT fedoraproject.org> - 1.0.1-12
- Merge-review cleanup (#226652)

* Thu Mar 04 2010 Matěj Cepl <mcepl@redhat.com> - 1.0.1-11
- Fixed bad directory ownership of /usr/share/X11

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 Adam Jackson <ajax@redhat.com> 1.0.1-9
- Un-require xorg-x11-filesystem

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul 15 2008 Adam Jackson <ajax@redhat.com> 1.0.1-7
- Fix license tag.

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.1-6
- Autorebuild for GCC 4.3

* Tue Aug 21 2007 Adam Jackson <ajax@redhat.com> - 1.0.1-5
- Rebuild for build id

* Tue Jan 30 2007 Adam Jackson <ajax@redhat.com> 1.0.1-4
- Fix man page globs and rebuild for FC7.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - sh: line 0: fg: no job control
- rebuild

* Wed Jun 21 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-3
- Add BuildRequires on autoconf/automake for brew.
- Use "make install DESTDIR=..." instead of makeinstall macro.

* Tue May 30 2006 Adam Jackson <ajackson@redhat.com> 1.0.1-2
- Fix BuildRequires (#191813) and add some LBX avoidance.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> 1.0.1-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> 1.0.1-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 18 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-1
- Updated all tarballs to version 1.0.1 from X11R7.0

* Fri Dec 16 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-1
- Updated all tarballs to version 1.0.0 from X11R7 RC4.
- Changed manpage dir from man1x to man1 to match RC4 default.

* Mon Nov 14 2005 Jeremy Katz <katzj@redhat.com> 0.99.1-3
- require newer filesystem package (#172610)

* Sun Nov 13 2005 Mike A. Harris <mharris@redhat.com> 0.99.1-2
- Add "Obsoletes: XFree86, xorg-x11", as these utils used to be there in
  in monolithic X packaging.

* Fri Nov 11 2005 Mike A. Harris <mharris@redhat.com> 0.99.1-1
- Initial build of xfwp, proxymngr, xfindproxy from X11R7 RC2.
- Added "BuildRequires: lbxproxy" for proxymngr.
