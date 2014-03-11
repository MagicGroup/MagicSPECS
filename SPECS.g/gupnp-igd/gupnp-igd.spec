%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           gupnp-igd
Version:        0.2.1
Release:        2%{?dist}
Summary:        Library to handle UPnP IGD port mapping        

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://www.gupnp.org/
Source0:        http://www.gupnp.org/sources/%{name}/%{name}-%{version}.tar.gz

BuildRequires:  glib2-devel
BuildRequires:  gupnp-devel
BuildRequires:  pygtk2-devel


%description
%{name} is a library to handle UPnP IGD port mapping.


%package        python
Summary:        Python bindings for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    python
The %{name}-python package contains the Python bindings for
%{name}.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-python = %{version}-%{release}
Requires:       pkgconfig


%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q


%build
%configure --disable-static
# quite rpmlint error about unused-direct-shlib-dependency
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
magic_rpm_clean.sh

%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc README COPYING
%{_libdir}/*.so.*


%files python
%defattr(-,root,root,-)
%dir %{python_sitearch}/gupnp
%{python_sitearch}/gupnp/*.py*
%{python_sitearch}/gupnp/igd.so


%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}-1.0*.pc
%{_datadir}/gtk-doc/html/%{name}/
%{_libdir}/girepository-1.0/GUPnPIgd-1.0.typelib
%{_datadir}/gir-1.0/GUPnPIgd-1.0.gir

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.2.1-2
- 为 Magic 3.0 重建

* Mon Jan 16 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.2.1-1
- Update to 0.2.1.
- Drop gcc patch. Fixed upstream.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Peter Robinson <pbrobinson@gmail.com> - 0.1.7-6
- Bump for new gupnp

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Dec 26 2010 Peter Robinson <pbrobinson@gmail.com> - 0.1.7-4
- Add patch to fix FTBFS # 631415

* Thu Dec 23 2010 Dan Horák <dan[at]danny.cz> - 0.1.7-3
- workaround make 3.82 issue in python/Makefile

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sat May 22 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.1.7-1
- Update to 0.1.7.

* Sat Jan 30 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.1.6-1
- Update to 0.1.6.

* Sun Dec  6 2009 Peter Robinson <pbrobinson@gmail.com> - 0.1.5-1
- Update to 0.1.5.

* Mon Nov 16 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.1.4-1
- Update to 0.1.4.

* Thu Sep 17 2009 Bastien Nocera <bnocera@redhat.com> 0.1.3-3
- Rebuild for new gupnp

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 10 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.1.3-1
- Update to 0.1.3.

* Sat May 16 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.1.2-1
- Update to 0.1.2.

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 18 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.1.1-2
- Quite rpmlint error about unused-direct-shlib-dependency.

* Wed Dec 31 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.1.1-1
- Initial Fedora spec.

