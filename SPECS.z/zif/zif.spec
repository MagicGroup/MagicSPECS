Summary:   Simple wrapper for rpm and the Fedora package metadata
Name:      zif
Version:   0.3.5
Release:   2%{?dist}
License:   GPLv2+
URL:       http://people.freedesktop.org/~hughsient/zif/
Source0:   http://people.freedesktop.org/~hughsient/zif/releases/%{name}-%{version}.tar.xz

Requires: wget

BuildRequires: glib2-devel >= 2.16.1
BuildRequires: rpm-devel
BuildRequires: sqlite-devel
BuildRequires: libsoup-devel
BuildRequires: libtool
BuildRequires: libarchive-devel
BuildRequires: docbook-utils
BuildRequires: gnome-doc-utils
BuildRequires: gtk-doc
BuildRequires: xz-devel
BuildRequires: bzip2-devel
BuildRequires: zlib-devel
BuildRequires: gpgme-devel
BuildRequires: intltool
BuildRequires: gettext
BuildRequires: libattr-devel
BuildRequires: gobject-introspection-devel

%description
Zif is a simple yum-compatible library that provides read-write
access to the rpm database and the Fedora metadata for PackageKit.

Zif is not designed as a replacement to yum, nor to be used by end users.

%package tools
Summary: Command line tools for using libzif
Requires: %{name} = %{version}-%{release}

%description tools
This provides the zif command line tool that can be used as an
alternative to yum. It is not normally required.

%package devel
Summary: GLib Libraries and headers for zif
Requires: %{name} = %{version}-%{release}
Requires: bzip2-devel
Requires: zlib-devel
Requires: gpgme-devel

%description devel
GLib headers and libraries for zif.

%prep
%setup -q

%build
%configure \
        --enable-gtk-doc \
        --disable-static \
        --disable-dependency-tracking

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/libzif*.la

%find_lang Zif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f Zif.lang
%defattr(-,root,root,-)
%doc README AUTHORS NEWS COPYING
%{_libdir}/*libzif*.so.*
%dir %{_sysconfdir}/zif
%dir %{_localstatedir}/lib/zif
%ghost %verify(not md5 size mtime) %{_localstatedir}/lib/zif/history.db
%config(noreplace) %{_sysconfdir}/zif/zif.conf
%{_libdir}/girepository-1.0/*.typelib

%files tools
%{_bindir}/zif
%config %{_sysconfdir}/bash_completion.d/*-completion.bash
%{_mandir}/man1/*.1.gz

%files devel
%defattr(-,root,root,-)
%{_libdir}/libzif*.so
%{_libdir}/pkgconfig/zif.pc
%dir %{_includedir}/libzif
%{_includedir}/libzif/*.h
%{_datadir}/gtk-doc
%{_datadir}/gir-1.0/*.gir

%changelog
* Thu Jan 17 2013 Tomas Bzatek <tbzatek@redhat.com> - 0.3.5-2
- Rebuilt for new libarchive

* Tue Jan 08 2013 Richard Hughes <richard@hughsie.com> 0.3.5-1
- New upstream release
- Don't fail 'zif refresh-cache' if a repo is unavailable
- Fix 'zif remove-with-deps' to not remove user-action packages
- Set the correct basearch for ARM processors

* Sun Nov 25 2012 Richard Hughes <richard@hughsie.com> 0.3.4-1
- New upstream release
- Cold startup is now much quicker. Typically this makes the command
  line 'zif' executable 80% faster to startup.
- Store the metdata checksum in an xattr to speed up checking metadata
- Turn off header validation when loading the rpmdb

* Fri Oct 26 2012 Richard Hughes <richard@hughsie.com> 0.3.3-1
- New upstream release
- Enable any debuginfo repos if the user searches for a debuginfo package
- Fix a lot of GObject Introspection tags and add a small python example
- Support the skip_if_unavailable config option

* Fri Sep 21 2012 Richard Hughes <richard@hughsie.com> 0.3.2-1
- New upstream release
- Import all the GPG keys found from gpgkey in a repo file

* Mon Aug 06 2012 Richard Hughes <richard@hughsie.com> 0.3.1-1
- New upstream release with new soname, rebuilds required.

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 02 2012 Richard Hughes <richard@hughsie.com> 0.3.0-1
- New upstream release with new soname, rebuilds required.

* Wed Apr 11 2012 Richard Hughes <richard@hughsie.com> 0.2.9-1
- New upstream release

* Wed Feb 22 2012 Richard Hughes <richard@hughsie.com> 0.2.8-2
- Rebuild for new librpm.

* Wed Feb 22 2012 Richard Hughes <richard@hughsie.com> 0.2.8-1
- New upstream release

* Fri Feb 03 2012 Richard Hughes <richard@hughsie.com> 0.2.7-1
- New upstream release
- Check the mirrorlist contains at least one non-comment or empty line
- Fix getting the update details for packages that installed multiarch
- Fix 'zif update kernel' to not remove the running version

* Thu Jan 26 2012 Tomas Bzatek <tbzatek@redhat.com> - 0.2.6-4
- Rebuilt for new libarchive

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 15 2011 Alex Lancaster <alexlan[AT]fedoraproject org> - 0.2.6-2
- Rebuild for new libarchive soname bump

* Tue Nov 01 2011 Richard Hughes <richard@hughsie.com> 0.2.6-1
- New upstream release with a few bugfixes and new features.

* Mon Oct 03 2011 Richard Hughes <richard@hughsie.com> 0.2.5-1
- New upstream release with a few bugfixes and new features.

* Mon Sep 23 2011 Richard Hughes <richard@hughsie.com> 0.2.4-1
- New upstream release with a few bugfixes and new features.
- The 'zif' binary has been split out into a -tools subpackage

* Mon Sep 05 2011 Richard Hughes <richard@hughsie.com> 0.2.3-1
- New upstream release with a few bugfixes and new features.

* Mon Aug 01 2011 Richard Hughes <richard@hughsie.com> 0.2.2-1
- New upstream release with a few bugfixes and new features.

* Mon Jul 04 2011 Richard Hughes <richard@hughsie.com> 0.2.1-1
- New upstream release with many bugfixes and performance improvements.

* Tue Jun 07 2011 Richard Hughes <richard@hughsie.com> 0.2.0-2
- Actually upload the new sources.

* Tue Jun 07 2011 Richard Hughes <richard@hughsie.com> 0.2.0-1
- New upstream release with many bugfixes and performance improvements.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 24 2011 Richard Hughes <richard@hughsie.com> 0.1.5-1
- New upstream release with many bugfixes and performance improvements.

* Wed Jan 19 2011 Matthias Clasen <mclasen@redhat.com> 0.1.4-2
- Rebuild against new rpm

* Fri Jan 07 2011 Richard Hughes <richard@hughsie.com> 0.1.4-1
- New upstream release with many bugfixes and performance improvements.

* Mon Dec 13 2010 Richard Hughes <richard@hughsie.com> 0.1.3-3
- Make zif-devel BR gpgme-devel to fix PackageKit compile in mock.

* Mon Dec 13 2010 Richard Hughes <richard@hughsie.com> 0.1.3-2
- Backport a patch to fix the compile of external applications which use
  libzif and complain about a missing ZifDelta header.

* Mon Dec 13 2010 Richard Hughes <richard@hughsie.com> 0.1.3-1
- New upstream release with many bugfixes and performance improvements.

* Mon Nov 01 2010 Richard Hughes <richard@hughsie.com> 0.1.2-1
- New upstream release with many bugfixes and performance improvements.

* Tue Oct 05 2010 Parag Nemade <paragn AT fedoraproject.org> 0.1.1-2
- drop the ldconfig and pkgconfig as a Requires.

* Mon Oct 04 2010 Richard Hughes <richard@hughsie.com> 0.1.1-1
- New upstream release with many bugfixes and performance improvements.

* Fri Oct 01 2010 Richard Hughes <richard@hughsie.com> 0.1.0-4
- Take ownership of the gtk-doc directory, and use another macro.

* Fri Oct 01 2010 Richard Hughes <richard@hughsie.com> 0.1.0-3
- Remove group from devel subpackage, and make the description better.

* Fri Oct 01 2010 Richard Hughes <richard@hughsie.com> 0.1.0-2
- Address some review comments, many thanks.

* Wed Sep 08 2010 Richard Hughes <richard@hughsie.com> 0.1.0-1
- Initial package for review.
