
Name:    compat-telepathy-farstream
Version: 0.4.0
Release: 6%{?dist}
Summary: Telepathy client library to handle Call channels

License: LGPLv2+
URL:     http://telepathy.freedesktop.org/wiki/Telepathy-Farsight
Source0: http://telepathy.freedesktop.org/releases/telepathy-farstream/telepathy-farstream-%{version}.tar.gz

BuildRequires: pkgconfig(telepathy-glib) >= 0.17.5
BuildRequires: pkgconfig(farstream-0.1) >= 0.1.0
BuildRequires: pkgconfig(dbus-1)
BuildRequires: pkgconfig(dbus-glib-1)

%description
%{name} is a Telepathy client library that uses Farstream to handle
Call channels.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
## upstream never intended this to be parallel-installable, since this
## is -devel and not runtime, conflicting could be better than introducing
## a multitude of hacks (changing include dir(s), lib*.so symlink, and .pc references) 
Conflicts: telepathy-farstream-devel >= 0.6
%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n telepathy-farstream-%{version}


%build
%configure \
  --disable-static \
  --disable-python \
  --disable-gtk-doc-html

make %{?_smp_mflags} V=1


%install
make install DESTDIR=%{buildroot}

# HACK to make parallel-installable
mv %{buildroot}%{_includedir}/telepathy-1.0 \
   %{buildroot}%{_includedir}/telepathy-1.0-compat
mv %{buildroot}%{_libdir}/libtelepathy-farstream.so \
   %{buildroot}%{_libdir}/libtelepathy-farstream-0.4.so
mv %{buildroot}%{_libdir}/pkgconfig/telepathy-farstream.pc \
   %{buildroot}%{_libdir}/pkgconfig/telepathy-farstream-0.4.pc
sed -i \
  -e 's|-ltelepathy-farstream|-ltelepathy-farstream-0.4|' \
  -e 's|-I${includedir}/telepathy-1.0|-I${includedir}/telepathy-1.0-compat|' \
  %{buildroot}%{_libdir}/pkgconfig/telepathy-farstream-0.4.pc

## unpackaged files
rm -fv %{buildroot}%{_libdir}/lib*.la
rm -rfv %{buildroot}%{_datadir}/gtk-doc/


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc NEWS README COPYING
%{_libdir}/libtelepathy-farstream.so.2*

%files devel
%{_libdir}/libtelepathy-farstream-0.4.so
%{_libdir}/pkgconfig/telepathy-farstream-0.4.pc
%dir %{_includedir}/telepathy-1.0-compat
%{_includedir}/telepathy-1.0-compat/telepathy-farstream/


%changelog
* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 0.4.0-6
- 为 Magic 3.0 重建

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 0.4.0-5
- 为 Magic 3.0 重建

* Wed Oct 31 2012 Rex Dieter <rdieter@fedoraproject.org> 0.4.0-4
- drop Conflicts, make truly parallel-installable

* Fri Oct 05 2012 Rex Dieter <rdieter@fedoraproject.org> - 0.4.0-3
- compat telepathy-farstream-0.4 pkg

* Thu Apr 05 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.4.0-2
- Rebuild against farstream

* Thu Apr  5 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.4.0-1
- Update to 0.4.0.

* Tue Apr 03 2012 Brian Pepple <bpepple@fedoraproject.org. - 0.2.3-2
- Rebuild against new tp-glib.

* Tue Mar 20 2012 Brian Pepple <bpepple@fedorapoject.org> - 0.2.3-1
- Update to 0.2.3.

* Tue Mar 13 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.2.2-2
- Add obsolete/provides on python subpackage.

* Fri Mar  9 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.2.2-1
- Update 0.2.2.

* Wed Mar  7 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.2.1-3
- Enable python bindings.

* Mon Mar  5 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.2.1-2
- Use macro for version in provides.
- Change reference Farsight in description to Farstream.

* Sun Mar  4 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.2.1-1
- Update to 0.2.1.
- Add BR on farstream-devel.
- Bump minimum version of tp-glib.
- Add obsolete/provide on telepathy-farsight.

* Mon Nov 21 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.1.2-1
- Initial Fedora spec file.
- Disable the python bindings for now.

