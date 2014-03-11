Name:           icon-naming-utils
Version:        0.8.90
Release:        8%{?dist}
Summary: 	A script to handle icon names in desktop icon themes

Group:          Development/Tools
License:        GPLv2
BuildArch:	noarch
URL:            http://tango.freedesktop.org/Standard_Icon_Naming_Specification
Source0:        http://tango.freedesktop.org/releases/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  perl(XML::Simple)
BuildRequires:  automake
Requires:	pkgconfig

Patch0:		icon-naming-utils-0.8.7-paths.patch

%description
A script for creating a symlink mapping for deprecated icon names to
the new Icon Naming Specification names, for desktop icon themes.

%prep
%setup -q
%patch0 -p1 -b .paths


%build
# the paths patch patches Makefile.am
autoreconf
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# hmm, it installs an -uninstalled.pc file ...
rm -f $RPM_BUILD_ROOT%{_datadir}/pkgconfig/icon-naming-utils-uninstalled.pc


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING AUTHORS README
%{_bindir}/icon-name-mapping
%{_datadir}/icon-naming-utils
%{_datadir}/pkgconfig/icon-naming-utils.pc

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.8.90-8
- 为 Magic 3.0 重建

* Tue Dec 13 2011 Liu Di <liudidi@gmail.com> - 0.8.90-7
- 为 Magic 3.0 重建

* Tue Dec 13 2011 Liu Di <liudidi@gmail.com> - 0.8.90-6
- 为 Magic 3.0 重建

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.90-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Aug 11 2009 Ville Skyttä <ville.skytta@iki.fi> - 0.8.90-4
- Use bzipped upstream tarball.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.90-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.90-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb 22 2009 Matthias Clasen <mclasen@redhat.com> - 0.8.90-1
- Update to 0.8.90

* Wed Jan 14 2009 Parag <pnemade@redhat.com> - 0.8.7-2
- spec file cleanup as suggested in merge-review rh#225894

* Tue Jul 22 2008 Matthias Clasen <mclasen@redhat.com> - 0.8.7-1
- Update to 0.8.7

* Sun Nov 18 2007 Matthias Clasen <mclasen@redhat.com> - 0.8.6-2
- Use a standard group to placate rpmlint

* Mon Sep 17 2007 Matthias Clasen <mclasen@redhat.com> - 0.8.6-1
- Update to 0.8.6

* Tue Aug 14 2007 Matthias Clasen <mclasen@redhat.com> - 0.8.3-1
- Update to 0.8.3

* Mon Feb 26 2007 Matthias Clasen <mclasen@redhat.com> - 0.8.2-1
- Update to 0.8.2
- Small spec file cleanups

* Mon Aug 21 2006 Matthias Clasen <mclasen@redhat.com> - 0.8.1-1.fc6
- Update to 0.8.1

* Thu Aug  3 2006 Matthias Clasen <mclasen@redhat.com> - 0.8.0-1.fc6
- Update to 0.8.0

* Wed Aug 02 2006 Warren Togami <wtogami@redhat.com> - 0.7.3-1
- add disttag

* Wed Jul 12 2006 Matthias Clasen <mclasen@redhat.com> - 0.7.3-1
- Update to 0.7.3

* Thu Jun  8 2006 Matthias Clasen <mclasen@redhat.com> - 0.7.2-2
- Rebuild

* Tue May  9 2006 Matthias Clasen <mclasen@redhat.com> - 0.7.2-1
- Update to 0.7.2

* Tue Apr 25 2006 Matthias Clasen <mclasen@redhat.com> - 0.7.1-1
- Update to 0.7.1

* Mon Feb  6 2006 Matthias Clasen <mclasen@redhat.com> - 0.6.7-1
- Update to 0.6.7

* Tue Jan 17 2006 Matthias Clasen <mclasen@redhat.com> - 0.6.5-1
- Initial import
