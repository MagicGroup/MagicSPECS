Summary:    Perl backend for Qooxdoo
Name:       perl-qooxdoo-compat
Version:    0.7.3
Release:    16%{?dist}
License:    LGPLv2 or EPL
Group:      Development/Languages
URL:        http://qooxdoo.org/
Source0:    http://downloads.sourceforge.net/qooxdoo/qooxdoo-%{version}-backend.tar.gz
Patch0:     perl-qooxdoo-compat-0.7.3-strict.patch
BuildArch:  noarch
Requires:   perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
This package provides the Perl backend for Qooxdoo, a comprehensive
and innovative Ajax application framework. This package supports
Qooxdoo 0.7.

%prep
%setup -q -n qooxdoo-%{version}-backend
%patch0 -p1

%build
# nothing to build

%install
%{__rm} -rf %{buildroot}

%{__install} -Dp -m 0644  backend/perl/Qooxdoo/JSONRPC.pm \
    %{buildroot}%{perl_vendorlib}/Qooxdoo/JSONRPC.pm

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, -)
%doc AUTHORS LICENSE README RELEASENOTES TODO VERSION

%{perl_vendorlib}/Qooxdoo

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.7.3-16
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.7.3-15
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.7.3-14
- 为 Magic 3.0 重建

* Mon Jan 30 2012 Liu Di <liudidi@gmail.com> - 0.7.3-13
- 为 Magic 3.0 重建

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.7.3-11
- Perl mass rebuild

* Fri Jun 10 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.7.3-10
- Perl 5.14 mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.7.3-8
- 661697 rebuild for fixing problems with vendorach/lib

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.7.3-7
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.7.3-6
- rebuild against perl 5.10.1

* Wed Aug 12 2009 Ville Skyttä <ville.skytta@iki.fi> - 0.7.3-5
- Use upstream gzipped tarball instead of zip.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Oct  6 2008 Terje Rosten <terje.rosten@ntnu.no> - 0.7.3-2
- Fix ownership of dir

* Sun Oct  5 2008 Terje Rosten <terje.rosten@ntnu.no> - 0.7.3-1
- initial build

