%define debug_package %{nil}
%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(0)")}

Name:           xcb-proto
Version:        1.10
Release:        1%{?dist}
Summary:        XCB protocol descriptions

Group:          Development/Libraries
License:        MIT
URL:            http://xcb.freedesktop.org/
Source0:        http://xcb.freedesktop.org/dist/%{name}-%{version}.tar.bz2
BuildArch:      noarch

BuildRequires:	python
Requires:       pkgconfig

%description
XCB is a project to enable efficient language bindings to the X11 protocol.
This package contains the protocol descriptions themselves.  Language
bindings use these protocol descriptions to generate code for marshalling
the protocol.

%prep
%setup -q

%build
# Bit of a hack to get the pc file in /usr/share, so we can be noarch.
%configure --libdir=%{_datadir}
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc COPYING NEWS README TODO doc/xml-xcb.txt
%{_datadir}/pkgconfig/xcb-proto.pc
%dir %{_datadir}/xcb/
%{_datadir}/xcb/*.xsd
%{_datadir}/xcb/*.xml
%{python_sitelib}/xcbgen

%changelog
* Fri Jan 17 2014 Adam Jackson <ajax@redhat.com> 1.10-1
- xcb-proto 1.10

* Mon Dec 02 2013 Adam Jackson <ajax@redhat.com> 1.9-1
- xcb-proto 1.9

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 16 2012 Adam Jackson <ajax@redhat.com> 1.8-1
- xcb-proto 1.8

* Tue Sep 04 2012 Adam Jackson <ajax@redhat.com> 1.7-3
- Backport 5a4e42f3 and d42d7918 to fix DRI2 and XKB, respectively.

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jan 11 2012 Adam Jackson <ajax@redhat.com> 1.7-1
- xcb-proto 1.7

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Jan 13 2010 Dave Airlie <airlied@redhat.com> 1.6-1
- xcb-proto 1.6

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 25 2009 Adam Jackson <ajax@redhat.com> 1.5-1
- xcb-proto 1.5

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Adam Jackson <ajax@redhat.com> 1.4-1
- xcb-proto 1.4

* Wed Dec 17 2008 Adam Jackson <ajax@redhat.com> 1.3-1
- xcb-proto 1.3

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.2-3
- Rebuild for Python 2.6

* Thu Sep 11 2008 Adam Jackson <ajax@redhat.com> 1.2-2
- Add additional selinux requests. (#461844)

* Wed Sep 10 2008 Adam Jackson <ajax@redhat.com> 1.2-1
- xcb-proto 1.2

* Mon Nov 12 2007 Adam Jackson <ajax@redhat.com> 1.1-1
- xcb-proto 1.1

* Fri Jun 29 2007 Adam Jackson <ajax@redhat.com> 1.0-1
- Initial revision.
