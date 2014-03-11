%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%define dbus_ver        0.60
%define tp_glib_ver     0.14.3
%define farsight2_ver   0.0.29

Name:           telepathy-farsight
Version:        0.0.19
Release:        2%{?dist}
Summary:        Telepathy client to handle media streaming channels

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://telepathy.freedesktop.org/wiki/
Source0:        http://telepathy.freedesktop.org/releases/%{name}/%{name}-%{version}.tar.gz

BuildRequires:  glib2-devel
BuildRequires:  dbus-devel >= %{dbus_ver}
BuildRequires:  dbus-glib-devel >= %{dbus_ver}
BuildRequires:  telepathy-glib-devel >= %{tp_glib_ver}
BuildRequires:  farsight2-devel >= %{farsight2_ver}
BuildRequires:  gstreamer-python-devel >= 0.10.10
# Needed to remove rpath
BuildRequires:  chrpath


%description
%{name} is a Telepathy client that uses Farsight and GStreamer to
handle media streaming channels. It's used as a background process
by other Telepathy clients, rather than presenting any user interface
of its own.


%package        python
Summary:        Python binding for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}


%description    python
Python bindings for %{name}.


%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-python = %{version}-%{release}
Requires:       glib2-devel
Requires:       dbus-glib-devel >= %{dbus_ver}
Requires:       farsight2-devel >= %{farsight2_ver}
Requires:       telepathy-filesystem
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q


%build
%configure --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
# Remove rpath
chrpath --delete $RPM_BUILD_ROOT%{python_sitearch}/*.so


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc COPYING NEWS
%{_libdir}/*.so.*


%files python
%defattr(-,root,root,-)
%{python_sitearch}/*.so


%files devel
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/telepathy-1.0/%{name}/
%{_datadir}/gtk-doc/html/%{name}

%changelog
* Tue Feb 14 2012 Liu Di <liudidi@gmail.com> - 0.0.19-2
- 为 Magic 3.0 重建

* Fri Jun 10 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.0.19-1
- Update to 0.0.19.

* Wed May 11 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.0.18-1
- Update to 0.0.18.
- Bump minimum verson of tp-glib and farsight2.

* Wed Apr 13 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.0.17-1
- Update to 0.0.17.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 27 2011 Brian Pepple <bdpepple@gmail.com> - 0.0.16-2
- Rebuild for new farsight2

* Wed Dec 22 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.0.16-1
- Update to 0.0.16.
- Bump min version of tp-glib.

* Fri Sep 10 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.0.15-1
- Update to 0.0.15.
- Drop buildroot & clean section since they are no longer needed.

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.0.14-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu May 27 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.0.14-1
- Update to 0.0.14.

* Fri Jan  8 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.0.13-1
- Update to 0.0.13.

* Mon Oct 19 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.0.12-1
- Update to 0.0.12.

* Thu Sep 10 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.0.11-1
- Update to 0.0.11.

* Tue Sep  8 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.0.10-1
- Update to 0.0.10.

* Tue Aug 25 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.0.9-1
- Update to 0.0.9.

* Thu Aug  6 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.0.8-1
- Update to 0.0.8.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu May  7 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.0.7-1
- Update to 0.0.7.

* Tue Mar 17 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.0.6-1
- Update to 0.0.6.
- Bump min version of tp-glib needed.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 10 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.0.4-2
- Add devel requires on telepathy-filesystem.

* Sat Jan 17 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.0.4-1
- Initial spec.

