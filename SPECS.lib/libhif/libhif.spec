Summary:   Simple package library built on top of hawkey and librepo
Name:      libhif
Version:   0.1.2
Release:   4%{?dist}
License:   LGPLv2+
URL:       https://github.com/hughsie/libhif
Source0:   http://people.freedesktop.org/~hughsient/releases/libhif-%{version}.tar.xz

# Backported from upstream
Patch0:    0001-repos-Don-t-error-out-for-missing-treeinfo-files.patch

BuildRequires: glib2-devel >= 2.16.1
BuildRequires: libtool
BuildRequires: docbook-utils
BuildRequires: gtk-doc
BuildRequires: gobject-introspection-devel
BuildRequires: hawkey-devel >= 0.4.6
BuildRequires: rpm-devel >= 4.11.0
BuildRequires: librepo-devel >= 1.1.5
BuildRequires: libsolv-devel

%description
This library provides a simple interface to hawkey and librepo and is currently
used by PackageKit and rpm-ostree.

%package devel
Summary: GLib Libraries and headers for libhif
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
GLib headers and libraries for libhif.

%prep
%setup -q
%patch0 -p1

%build
%configure \
        --enable-gtk-doc \
        --disable-static \
        --disable-silent-rules

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/libhif*.la

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc README.md AUTHORS NEWS COPYING
%{_libdir}/libhif.so.1*
%{_libdir}/girepository-1.0/*.typelib

%files devel
%{_libdir}/libhif.so
%{_libdir}/pkgconfig/libhif.pc
%dir %{_includedir}/libhif
%{_includedir}/libhif/*.h
%{_datadir}/gtk-doc
%{_datadir}/gir-1.0/*.gir

%changelog
* Mon Jul 28 2014 Kalev Lember <kalevlember@gmail.com> - 0.1.2-4
- Rebuilt for hawkey soname bump

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 0.1.2-3
- Rebuilt for gobject-introspection 1.41.4

* Sat Jul 19 2014 Kalev Lember <kalevlember@gmail.com> 0.1.2-2
- Fix a PK crash with locally mounted iso media (#1114207)

* Thu Jul 17 2014 Richard Hughes <richard@hughsie.com> 0.1.2-1
- Update to new upstream version
- Add HifContext accessor in -private for HifState
- Add name of failing repository
- Create an initial sack in HifContext
- Error if we can't find any package matching provided name
- Fix a mixup of HifStateAction and HifPackageInfo
- Improve rpm callback handling for packages in the cleanup state
- Only set librepo option if value is set
- Respect install root for rpmdb Packages monitor

* Mon Jun 23 2014 Richard Hughes <richard@hughsie.com> 0.1.1-1
- Update to new upstream version
- Fix a potential crash when removing software
- Only add system repository if it exists
- Pass install root to hawkey

* Tue Jun 10 2014 Richard Hughes <richard@hughsie.com> 0.1.0-1
- Initial version for Fedora package review

