%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%define gst_ver 0.10.33
%define gst_plugins_base_ver 0.10.33
%define gst_plugins_bad 0.10.17
%define gst_python 0.10.10

Name:           farsight2
Version:        0.0.31
Release:        1%{?dist}
Summary:        Libraries for videoconferencing

Group:          System Environment/Libraries
License:	LGPLv2+
URL:            http://farsight.freedesktop.org/wiki/
Source0:        http://farsight.freedesktop.org/releases/%{name}/%{name}-%{version}.tar.gz

BuildRequires:	glib2-devel >= 2.16
BuildRequires:  gstreamer-devel >= %{gst_ver}
BuildRequires:	gstreamer-plugins-base-devel >= %{gst_plugins_base_ver}
BuildRequires:	gstreamer-python-devel >= %{gst_python}
BuildRequires:	libnice-devel >= 0.1.0
BuildRequires:	gupnp-igd-devel
BuildRequires:	python-devel
BuildRequires:	pygobject2-devel >= 2.16.0

Requires:	gstreamer-plugins-good >= 0.10.29
Requires:	gstreamer-plugins-bad-free >= %{gst_plugins_bad}


%description
%{name} is a collection of GStreamer modules and libraries for
videoconferencing.


%package   	python
Summary:	Python binding for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}


%description	python
Python bindings for %{name}.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:	%{name}-python = %{version}-%{release}
Requires:       gstreamer-devel  >= %{gst_ver}
Requires:       gstreamer-plugins-base-devel >= %{gst_plugins_base_ver}
Requires:       pkgconfig


%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q


%check
#make check


%build
%configure								\
  --with-package-name='Fedora farsight2 package'			\
  --with-package-origin='http://download.fedora.redhat.com/fedora'	\
  --disable-static

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/*.so.*
%dir %{_libdir}/%{name}-0.0
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/0.0
%dir %{_datadir}/%{name}/0.0/fsrtpconference
%{_libdir}/%{name}-0.0/libmulticast-transmitter.so
%{_libdir}/%{name}-0.0/librawudp-transmitter.so
%{_libdir}/%{name}-0.0/libnice-transmitter.so
%{_libdir}/%{name}-0.0/libshm-transmitter.so
%{_datadir}/%{name}/0.0/fsrtpconference/default-codec-preferences
%{_datadir}/%{name}/0.0/fsrtpconference/default-element-properties
%{_libdir}/gstreamer-0.10/libfsfunnel.so
%{_libdir}/gstreamer-0.10/libfsrtpconference.so
%{_libdir}/gstreamer-0.10/libfsvideoanyrate.so
%{_libdir}/gstreamer-0.10/libfsrtcpfilter.so
%{_libdir}/gstreamer-0.10/libfsmsnconference.so
%{_libdir}/gstreamer-0.10/libfsrawconference.so


%files python
%defattr(-,root,root,-)
%{python_sitearch}/farsight.so


%files devel
%defattr(-,root,root,-)
%{_libdir}/libgstfarsight-0.10.so
%{_libdir}/pkgconfig/%{name}-0.10.pc
%{_includedir}/gstreamer-0.10/gst/farsight/
%{_datadir}/gtk-doc/html/%{name}-libs-0.10/
%{_datadir}/gtk-doc/html/%{name}-plugins-0.10/


%changelog
* Mon Oct 10 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.0.31-1
- Update to 0.0.31.
- Fix directory ownership.

* Sat Sep 17 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.0.30-1
- Update to 0.0.30.

* Fri Jun 17 2011 Peter Robinson <pbrobinson@gmail.com> 0.0.29-2
- rebuild for new gupnp/gssdp

* Fri Jun 10 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.0.29-1
- Update to 0.0.29.

* Wed May 11 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.0.28-1
- Update to 0.0.28.
- Bump minimum version of gstreamer needed.

* Tue May  3 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.0.27-1
- Update to 0.0.27.

* Wed Feb 23 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.0.26-1
- Update to 0.0.26.

* Tue Feb 15 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.0.25-1
- Update to 0.0.25.

* Thu Feb 10 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.0.24-1
- Update to 0.0.24.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 20 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.0.23-1
- Update to 0.0.23.
- Bump min version of libnice.

* Mon Nov  1 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.0.22-1
- Update to 0.0.22.
- Add shm-transmitter plugin to files.
- Drop clean section and buildroot. No longer needed.
- Bump min requires for pyobject2 & glib2.

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.0.21-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Jul 18 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.0.21-1
- Update to 0.0.21.
- Drop bad-cast patch. Fixed upstream.

* Thu Jul  8 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.0.20-2
- Add patch to fix a bad cast.

* Wed Jun  2 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.0.20-1
- Update to 0.0.20.

* Wed May 19 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.0.19-1
- Update to 0.0.19.

* Wed May  5 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.0.18-1
- Update to 0.0.18.

* Mon Feb  1 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.0.17-2
- Change require to gst-plugins-bad-free due to plugin move.

* Tue Jan  5 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.0.17-1
- Update to 0.0.17.

* Wed Dec 16 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.0.16-2
- Rebuild for new gupnp-igd.

* Tue Oct  6 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.0.16-1
- Update to 0.0.16.

* Thu Sep 17 2009 Bastien Nocera <bnocera@redhat.com> 0.0.15-2
- Rebuild for new gupnp

* Thu Sep  3 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.0.15-1
- Update to 0.0.15.

* Thu Aug 06 2009 Warren Togami <wtogami@redhat.com> - 0.0.14-1
- 0.0.14

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 Warren Togami <wtogami@redhat.com> - 0.0.12-3
- rebuild

* Mon Jun 22 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.0.12-2
- Remove unnecessary requires on gst-plugins-farsight.

* Sat May 30 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.0.12-1
- Update to 0.0.12.

* Tue May 26 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.0.11-1
- Update to 0.0.11.

* Wed May 20 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.0.10-1
- Update to 0.0.10.

* Tue Apr  7 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.0.9-1
- Update to 0.0.9.

* Tue Mar 17 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.0.8-1
- Update to 0.0.8.
- Bump min version of gstreamer needed.

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 19 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.0.7-2
- Add BR on gupnp-igd-devel, pygobject2-devel, and pygtk2-devel.

* Fri Jan  9 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.0.7-1
- Update to 0.0.7.

* Mon Jan  5 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.0.6-4
- Add BR on libnice-devel and build libnice transmitter.
- Set gstreamer package name & origin.

* Fri Jan 02 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.0.6-3
- Rebuild.

* Wed Dec 31 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.0.6-2
- Preserve time stamps.

* Tue Dec 16 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.0.6-1
- Initial Fedora spec.
