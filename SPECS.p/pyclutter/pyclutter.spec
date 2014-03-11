# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           pyclutter
Version:        1.3.2
Release:        5%{?dist}
Summary:        Python modules that allow you to use the Clutter toolkit

Group:          Development/Languages
License:        LGPLv2+
URL:            http://www.clutter-project.org/
Source0:        http://www.clutter-project.org/sources/%{name}/1.3/%{name}-%{version}.tar.bz2
Patch0:		pyclutter-1.3.2-clutter-1.9.2-compat.patch

BuildRequires:  pygtk2-devel
BuildRequires:  gtk2-devel
BuildRequires:  clutter-devel

%description
This archive contains the Python modules that allow you to use the
Clutter toolkit in Python programs.

%package devel
Summary:        Pyclutter development environment
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       python-devel clutter-devel pygobject2-devel

%description devel
Header files and libraries for building a extension library for the
Pyclutter

%prep
%setup -q
%patch0 -p1 -b .compat

%build
%configure --enable-docs
make %{?_smp_mflags} V=1

%install
make DESTDIR=%{buildroot} install INSTALL="%{__install} -p" 

#Remove libtool archives.
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%{python_sitearch}/clutter/
%{_datadir}/%{name}/

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}-1.0/
%{_datadir}/gtk-doc/html/%{name}/
%{_libdir}/pkgconfig/pyclutter-1.0.pc

%changelog
* Mon Nov 28 2011 Adam Jackson <ajax@redhat.com> 1.3.2-5
- pyclutter-1.3.2-clutter-1.9.2-compat.patch: Fix FTBFS against new clutter

* Thu Nov 24 2011 Matthias Clasen <mclasen@redhat.com> 1.3.2-4
- Rebuild against new clutter

* Wed Nov 16 2011 Adam Jackson <ajax@redhat.com> 1.3.2-3
- Rebuild to break bogus libpng dep

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec  8 2010 Peter Robinson <pbrobinson@gmail.com> - 1.3.2-1
- New upstream 1.3.2 release

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sat Apr  3 2010 Peter Robinson <pbrobinson@gmail.com> - 1.0.2-1
- New upstream 1.0.2 release
- Fix build, drop pyclutter-gst and pyclutter-gst as they're now separate

* Mon Jan 25 2010 Peter Robinson <pbrobinson@gmail.com> - 1.0.0-1
- New upstream 1.0.0, python spec fixups

* Mon Aug 03 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 0.9.2-1
- new version 0.9.2
- remove cairo subpackage

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild


* Fri Jan 23 2009 Allisson Azevedo <allisson@gmail.com> 0.8.2-1
- Update to 0.8.2

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.8.0-2
- Rebuild for Python 2.6

* Wed Oct 15 2008 Allisson Azevedo <allisson@gmail.com> 0.8.0-1
- Update to 0.8.0

* Wed Oct  8 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 0.8.0-0.1.20081008r3353
- Update to SVN snapshot of pyclutter 0.8 until official release comes out.
- Fixes broken deps.

* Thu Sep 11 2008 Jesse Keating <jkeating@redhat.com> - 0.6.2-4
- Rebuild for new clutter

* Thu Aug 28 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 0.6.2-3
- Fix unowned directory

* Wed May 28 2008 Allisson Azevedo <allisson@gmail.com> 0.6.2-2
- Rebuild against clutter-cairo

* Tue May 20 2008 Allisson Azevedo <allisson@gmail.com> 0.6.2-1
- Update to 0.6.2

* Fri Feb 22 2008 Allisson Azevedo <allisson@gmail.com> 0.6.0-1
- Update to 0.6.0

* Sat Dec 15 2007 Daniel P. Berrange <berrange@redhat.com> - 0.4.2-2.fc8
- Added sub-packages for gtk and gst bindings (rhbz #365981)

* Wed Oct  3 2007 Allisson Azevedo <allisson@gmail.com> 0.4.2-1
- Update to 0.4.2

* Mon Sep  3 2007 Allisson Azevedo <allisson@gmail.com> 0.4.1-1
- Update to 0.4.1

* Sun Mar 29 2007 Allisson Azevedo <allisson@gmail.com> 0.2.0-5
- Fix requires for devel package

* Sun Mar 28 2007 Allisson Azevedo <allisson@gmail.com> 0.2.0-4
- Fix requires and buildrequires
- Modify defattr for devel package

* Sun Mar 27 2007 Allisson Azevedo <allisson@gmail.com> 0.2.0-3
- Fix .spec

* Sun Mar 24 2007 Allisson Azevedo <allisson@gmail.com> 0.2.0-2
- Fix .spec

* Sun Mar 23 2007 Allisson Azevedo <allisson@gmail.com> 0.2.0-1
- Initial RPM release
