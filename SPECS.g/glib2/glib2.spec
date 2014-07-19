%global _changelog_trimtime %(date +%s -d "1 year ago")

Summary: A library of handy utility functions
Name: glib2
Version:	2.41.2
Release: 1%{?dist}
License: LGPLv2+
Group: System Environment/Libraries
URL: http://www.gtk.org
#VCS: git:git://git.gnome.org/glib
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source: http://download.gnome.org/sources/glib/%{majorver}/glib-%{version}.tar.xz

BuildRequires: pkgconfig
BuildRequires: gettext
BuildRequires: libattr-devel
# for sys/inotify.h
BuildRequires: glibc-devel
BuildRequires: zlib-devel
# for sys/sdt.h
BuildRequires: systemtap-sdt-devel
# Bootstrap build requirements
BuildRequires: automake autoconf libtool
BuildRequires: gtk-doc
BuildRequires: python-devel
BuildRequires: libffi-devel
BuildRequires: elfutils-libelf-devel
BuildRequires: chrpath

# required for GIO content-type support
Requires: shared-mime-info

%description
GLib is the low-level core library that forms the basis for projects
such as GTK+ and GNOME. It provides data structure handling for C,
portability wrappers, and interfaces for such runtime functionality
as an event loop, threads, dynamic loading, and an object system.


%package devel
Summary: A library of handy utility functions
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The glib2-devel package includes the header files for the GLib library.

%package doc
Summary: A library of handy utility functions
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
The glib2-doc package includes documentation for the GLib library.

%package fam
Summary: FAM monitoring module for GIO
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
BuildRequires: gamin-devel

%description fam
The glib2-fam package contains the FAM (File Alteration Monitor) module for GIO.

%package static
Summary: glib static
Requires: %{name}-devel = %{version}-%{release}

%description static
The %{name}-static subpackage contains static libraries for %{name}.

%package tests
Summary: Tests for the glib2 package
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description tests
The glib2-tests package contains tests that can be used to verify
the functionality of the installed glib2 package.

%prep
%setup -q -n glib-%{version}

# Workaround wrong gtk-doc.make timestamp
# https://bugzilla.gnome.org/show_bug.cgi?id=700350
touch -r Makefile.am gtk-doc.make

%build
# Support builds of both git snapshots and tarballs packed with autogoo
(if ! test -x configure; then NOCONFIGURE=1 ./autogen.sh; CONFIGFLAGS=--enable-gtk-doc; fi;
 %configure $CONFIGFLAGS \
           --enable-systemtap \
           --enable-static \
           --enable-installed-tests
)

make %{?_smp_mflags}

%install
# Use -p to preserve timestamps on .py files to ensure
# they're not recompiled with different timestamps
# to help multilib: https://bugzilla.redhat.com/show_bug.cgi?id=718404
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p -c"
# Also since this is a generated .py file, set it to a known timestamp,
# otherwise it will vary by build time, and thus break multilib -devel
# installs.
touch -r gio/gdbus-2.0/codegen/config.py.in $RPM_BUILD_ROOT/%{_datadir}/glib-2.0/codegen/config.py
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/*.so
chrpath --delete $RPM_BUILD_ROOT%{_libexecdir}/installed-tests/glib/gdbus-peer

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/gio/modules/*.{a,la}
rm -f $RPM_BUILD_ROOT%{_datadir}/glib-2.0/gdb/*.{pyc,pyo}
rm -f $RPM_BUILD_ROOT%{_datadir}/glib-2.0/codegen/*.{pyc,pyo}

# Multilib fixes for systemtap tapsets; see
# https://bugzilla.redhat.com/718404
for f in $RPM_BUILD_ROOT%{_datadir}/systemtap/tapset/*.stp; do
    (dn=$(dirname ${f}); bn=$(basename ${f});
     mv ${f} ${dn}/%{__isa_bits}-${bn})
done

mv  $RPM_BUILD_ROOT%{_bindir}/gio-querymodules $RPM_BUILD_ROOT%{_bindir}/gio-querymodules-%{__isa_bits}

touch $RPM_BUILD_ROOT%{_libdir}/gio/modules/giomodule.cache

# bash-completion scripts need not be executable
chmod 644 $RPM_BUILD_ROOT%{_datadir}/bash-completion/completions/*

%find_lang glib20


%post
/sbin/ldconfig
gio-querymodules-%{__isa_bits} %{_libdir}/gio/modules


%postun
/sbin/ldconfig
[ ! -x %{_bindir}/gio-querymodules-%{__isa_bits} ] || \
gio-querymodules-%{__isa_bits} %{_libdir}/gio/modules


%files -f glib20.lang
%doc AUTHORS COPYING NEWS README
%{_libdir}/libglib-2.0.so.*
%{_libdir}/libgthread-2.0.so.*
%{_libdir}/libgmodule-2.0.so.*
%{_libdir}/libgobject-2.0.so.*
%{_libdir}/libgio-2.0.so.*
%dir %{_datadir}/bash-completion
%dir %{_datadir}/bash-completion/completions
%{_datadir}/bash-completion/completions/gdbus
%{_datadir}/bash-completion/completions/gsettings
%{_datadir}/bash-completion/completions/gapplication
%dir %{_datadir}/glib-2.0
%dir %{_datadir}/glib-2.0/schemas
%dir %{_libdir}/gio
%dir %{_libdir}/gio/modules
%ghost %{_libdir}/gio/modules/giomodule.cache
%{_bindir}/gio-querymodules*
%{_bindir}/glib-compile-schemas
%{_bindir}/gsettings
%{_bindir}/gdbus
%{_bindir}/gapplication
%doc %{_mandir}/man1/gio-querymodules.1.gz
%doc %{_mandir}/man1/glib-compile-schemas.1.gz
%doc %{_mandir}/man1/gsettings.1.gz
%doc %{_mandir}/man1/gdbus.1.gz
%doc %{_mandir}/man1/gapplication.1.gz

%files devel
%{_libdir}/lib*.so
%{_libdir}/glib-2.0
%{_includedir}/*
%{_datadir}/aclocal/*
%{_libdir}/pkgconfig/*
%{_datadir}/glib-2.0/gdb
%{_datadir}/glib-2.0/gettext
%{_datadir}/glib-2.0/schemas/gschema.dtd
%{_datadir}/bash-completion/completions/gresource
%{_bindir}/glib-genmarshal
%{_bindir}/glib-gettextize
%{_bindir}/glib-mkenums
%{_bindir}/gobject-query
%{_bindir}/gtester
%{_bindir}/gdbus-codegen
%{_bindir}/glib-compile-resources
%{_bindir}/gresource
%{_datadir}/glib-2.0/codegen
%attr (0755, root, root) %{_bindir}/gtester-report
%doc %{_mandir}/man1/glib-genmarshal.1.gz
%doc %{_mandir}/man1/glib-gettextize.1.gz
%doc %{_mandir}/man1/glib-mkenums.1.gz
%doc %{_mandir}/man1/gobject-query.1.gz
%doc %{_mandir}/man1/gtester-report.1.gz
%doc %{_mandir}/man1/gtester.1.gz
%doc %{_mandir}/man1/gdbus-codegen.1.gz
%doc %{_mandir}/man1/glib-compile-resources.1.gz
%doc %{_mandir}/man1/gresource.1.gz
%{_datadir}/gdb/auto-load%{_libdir}/libglib-2.0.so.*-gdb.py*
%{_datadir}/gdb/auto-load%{_libdir}/libgobject-2.0.so.*-gdb.py*
%{_datadir}/systemtap/tapset/*.stp

%files doc
%doc %{_datadir}/gtk-doc/html/*

%files fam
%{_libdir}/gio/modules/libgiofam.so

%files static
%{_libdir}/libgio-2.0.a
%{_libdir}/libglib-2.0.a
%{_libdir}/libgmodule-2.0.a
%{_libdir}/libgobject-2.0.a
%{_libdir}/libgthread-2.0.a

%files tests
%{_libexecdir}/installed-tests
%{_datadir}/installed-tests

%changelog
* Thu Jul 17 2014 Liu Di <liudidi@gmail.com> - 2.41.2-1
- 更新到 2.41.2

* Thu Jun 26 2014 Liu Di <liudidi@gmail.com> - 2.41.1-1
- 更新到 2.41.1

* Wed Apr 09 2014 Liu Di <liudidi@gmail.com> - 2.40.0-1
- 更新到 2.40.0

* Tue Apr 08 2014 Liu Di <liudidi@gmail.com> - 2.39.92-1
- 更新到 2.39.92

* Tue Feb 18 2014 Richard Hughes <rhughes@redhat.com> - 2.39.90-1
- Update to 2.39.90

* Tue Feb 04 2014 Richard Hughes <rhughes@redhat.com> - 2.39.4-1
- Update to 2.39.4

* Tue Jan 14 2014 Richard Hughes <rhughes@redhat.com> - 2.39.3-1
- Update to 2.39.3

* Sun Dec 22 2013 Richard W.M. Jones <rjones@redhat.com> - 2.39.2-2
- Re-add static subpackage so that we can build static qemu as
  an AArch64 binfmt.

* Tue Dec 17 2013 Richard Hughes <rhughes@redhat.com> - 2.39.2-1
- Update to 2.39.2

* Mon Dec 09 2013 Richard Hughes <rhughes@redhat.com> - 2.39.1-2
- Backport a patch from master to stop gnome-settings-daemon crashing.

* Thu Nov 14 2013 Richard Hughes <rhughes@redhat.com> - 2.39.1-1
- Update to 2.39.1

* Mon Oct 28 2013 Richard Hughes <rhughes@redhat.com> - 2.39.0-1
- Update to 2.39.0

* Tue Sep 24 2013 Kalev Lember <kalevlember@gmail.com> - 2.38.0-1
- Update to 2.38.0

* Tue Sep 17 2013 Kalev Lember <kalevlember@gmail.com> - 2.37.93-1
- Update to 2.37.93

* Mon Sep 02 2013 Kalev Lember <kalevlember@gmail.com> - 2.37.7-1
- Update to 2.37.7

* Wed Aug 21 2013 Debarshi Ray <rishi@fedoraproject.org> - 2.37.6-1
- Update to 2.37.6

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 2.37.5-2
- Perl 5.18 rebuild

* Thu Aug  1 2013 Debarshi Ray <rishi@fedoraproject.org> - 2.37.5-1
- Update to 2.37.5

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 2.37.4-2
- Perl 5.18 rebuild

* Tue Jul  9 2013 Matthias Clasen <mclasen@redhat.com> - 2.37.4-1
- Update to 2.37.4

* Thu Jun 20 2013 Debarshi Ray <rishi@fedoraproject.org> - 2.37.2-1
- Update to 2.37.2

* Tue May 28 2013 Matthias Clasen <mclasen@redhat.com> - 2.37.1-1
- Update to 2.37.1
- Add a tests subpackage

* Sat May 04 2013 Kalev Lember <kalevlember@gmail.com> - 2.37.0-1
- Update to 2.37.0

* Sat Apr 27 2013 Thorsten Leemhuis <fedora@leemhuis.info> - 2.36.1-2
- Fix pidgin freezes by applying patch from master (#956872)

* Mon Apr 15 2013 Kalev Lember <kalevlember@gmail.com> - 2.36.1-1
- Update to 2.36.1

* Mon Mar 25 2013 Kalev Lember <kalevlember@gmail.com> - 2.36.0-1
- Update to 2.36.0

* Tue Mar 19 2013 Matthias Clasen <mclasen@redhat.com> - 2.35.9-1
- Update to 2.35.9

* Thu Feb 21 2013 Kalev Lember <kalevlember@gmail.com> - 2.35.8-1
- Update to 2.35.8

* Tue Feb 05 2013 Kalev Lember <kalevlember@gmail.com> - 2.35.7-1
- Update to 2.35.7

* Tue Jan 15 2013 Matthias Clasen <mclasen@redhat.com> - 2.35.4-1
- Update to 2.35.4

* Thu Dec 20 2012 Kalev Lember <kalevlember@gmail.com> - 2.35.3-1
- Update to 2.35.3

* Sat Nov 24 2012 Kalev Lember <kalevlember@gmail.com> - 2.35.2-1
- Update to 2.35.2

* Thu Nov 08 2012 Kalev Lember <kalevlember@gmail.com> - 2.35.1-1
- Update to 2.35.1
- Drop upstreamed codegen-in-datadir.patch
