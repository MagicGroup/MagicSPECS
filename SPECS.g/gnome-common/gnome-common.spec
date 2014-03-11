Name:           gnome-common
Version:        3.7.4
Release:        2%{?dist}
Summary:        Useful things common to building gnome packages from scratch

Group:          Development/Tools
BuildArch:      noarch
License:        GPLv3
URL:            http://developer.gnome.org
Source0:        http://download.gnome.org/sources/%{name}/3.6/%{name}-%{version}.tar.xz

# This will pull in the latest version; if your package requires something older,
# well, BuildRequire it in that spec.  At least until such time as we have a
# build system that is intelligent enough to inspect your source code
# and auto-inject those requirements.
Requires: automake
Requires: autoconf
Requires: libtool
Requires: gettext
Requires: pkgconfig

%description
This package contains sample files that should be used to develop pretty much
every GNOME application.  The programs included here are not needed for running
gnome apps or building ones from distributed tarballs.  They are only useful
for compiling from CVS sources or when developing the build infrastructure for
a GNOME application.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}
cp doc-build/README doc-README
# No sense making a doc subdir in the rpm pkg for one file.
cp doc/usage.txt usage.txt

%install
make install DESTDIR=$RPM_BUILD_ROOT

%files
%doc doc-README usage.txt ChangeLog
%{_bindir}/*
%{_datadir}/aclocal/*
%{_datadir}/%{name}

%changelog
* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 16 2013 Richard Hughes <hughsient@gmail.com> - 3.7.4-1
- Update to 3.7.4

* Mon Jan 14 2013 Marek Kasik <mkasik@redhat.com> - 3.6.0-2
- Backport patch for support of automake-1.13

* Tue Oct 16 2012 Kalev Lember <kalevlember@gmail.com> - 3.6.0-1
- Update to 3.6.0

* Tue Sep 18 2012 Kalev Lember <kalevlember@gmail.com> - 3.5.91-1
- Update to 3.5.91

* Tue Aug 21 2012 Richard Hughes <hughsient@gmail.com> - 3.5.5-1
- Update to 3.5.5

* Thu Jul 19 2012 Marek Kasik <mkasik@redhat.com> - 3.4.0.1-3
- Backport patch for support of automake-1.12

* Tue Jul 17 2012 Jiri Popelka <jpopelka@redhat.com> - 3.4.0.1-2
- Match actual license

* Tue Mar 27 2012 Kalev Lember <kalevlember@gmail.com> - 3.4.0.1-1
- Update to 3.4.0.1

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Aug 18 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.0-1
- Update to 3.1.0

* Sun Apr  3 2011 Christopher Aillon <caillon@redhat.com> - 2.34.0-1
- Update to 2.34.0

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.28.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Mar 26 2010 Colin Walters <walters@verbum.org> - 2.28.0-2
- Readd Requires on components; optimizing for the case where
  you want to have gnome-common but not the autotools is total
  nonsense.  "automake" pulls in the latest which is good enough;
  if your package BuildRequires an older version, well add that
  to the package.

* Mon Sep 21 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.0-1
- Update to 2.28.0

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.26.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun  3 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.0-2
- Support automake 1.11

* Sun Mar 29 2009  Matthias Clasen <mclasen@redhat.com> - 2.26.0-1
- Update to 2.26.0

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.24.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 21 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 2.24.0-1
- Update to version 2.24.0

* Mon Apr 7 2008 Toshio Kuratomi <toshio@fedoraproject.org> - 2.20.0-1
- Update to version 2.20.0.

* Sun Aug 12 2007 Toshio Kuratomi <a.badger@gmail.com> - 2.18.0-1
- Update to version that matches gnome-2.18.
- Update license tag to strict GPLv2.

* Wed Dec 06 2006 Toshio Kuratomi <toshio@tiki-lounge.com> - 2.12.0-4
- Add a patch from gnome-common cvs to address bug #218717 (gnome-common
  does not work with automake-1.10).

* Mon Sep 04 2006 Toshio Kuratomi <toshio-tiki-lounge.com> - 2.12.0-3
- Bump and rebuild for FC6.

* Thu Feb 16 2006 Toshio Kuratomi <toshio-tiki-lounge.com> - 2.12.0-2
- Bump and rebuild for FC5.

* Tue Oct 18 2005 Toshio Kuratomi <toshio-tiki-lounge.com> - 2.12.0-1
- Upgrade to 2.12.0.
- Add dist tag.

* Thu May 12 2005 Toshio Kuratomi <toshio-tiki-lounge.com> - 2.8.0-3
- Bump and rebuild to get versions synced across architectures.

* Fri Mar 18 2005 Toshio Kuratomi <toshio-tiki-lounge.com> - 2.8.0-2
- Rebuild for FC4t1

* Tue Sep 14 2004 Toshio Kuratomi <toshio-tiki-lounge.com> - 0:2.8.0-1
- Update to 2.8.0
  + This release supports automake thru version 1.9 and has had a lot of
    deprecated stuff cleaned out.
- Removed BuildRequires.  A base mach build environment will build it now.
- Removed Requires.  Although gnome-common still requires autoconf and
  friends, it doesn't require a specific version of them.  There's no virtual
  provides in the automake14,15,16,17 automake packages that could help here.

* Mon Mar 22 2004 Toshio Kuratomi <toshio-tiki-lounge.com> - 0:2.4.0-0.fdr.3
- Add COPYING file to the docs
- Add bin/Changelog to the docs as ChangeLog.bin

* Sun Dec 28 2003 Toshio Kuratomi <toshio-tiki-lounge.com> - 0:2.4.0-0.fdr.2
- Update the Requires line (rpm doesn't automatically detect most of the
  dependencies.)
- Remove the AUTHORS file as it's currently empty

* Fri Dec 19 2003 Toshio Kuratomi <toshio-tiki-lounge.com> - 0:2.4.0-0.fdr.1
- Initial RPM release.
