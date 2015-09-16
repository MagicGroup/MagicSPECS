Name:		perl-Sub-Exporter
Version:	0.987
Release:	1%{?dist}
Summary:	Sophisticated exporter for custom-built routines
License:	GPL+ or Artistic
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/Sub-Exporter/
Source0:	http://search.cpan.org/CPAN/authors/id/R/RJ/RJBS/Sub-Exporter-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
# Build
BuildRequires:	perl(ExtUtils::MakeMaker)
# Module
BuildRequires:	perl(Carp)
BuildRequires:	perl(Data::OptList) >= 0.1
BuildRequires:	perl(Package::Generator)
BuildRequires:	perl(Params::Util) >= 0.14
BuildRequires:	perl(Sub::Install) >= 0.92
# Test suite
BuildRequires:	perl(base)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(Test::More)
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	perl(Package::Generator)

# Don't want doc-file provides or dependencies
%global __provides_exclude_from ^%{_datadir}/doc/%{name}-%{version}/
%global __requires_exclude_from ^%{_datadir}/doc/%{name}-%{version}/

%description
Sub::Exporter provides a sophisticated alternative to Exporter.pm. It allows
for renaming, currying/sub-generation, and other cool stuff.

ACHTUNG! If you're not familiar with Exporter or exporting, read
Sub::Exporter::Tutorial first!

%prep
%setup -q -n Sub-Exporter-%{version}

# Fix shellbangs
find t/ -type f -exec sed -i -e 's|^#!perl|#!/usr/bin/perl|' {} \;

# Filter bogus provides/requires if we don't have rpm ≥ 4.9
%global provfilt /bin/sh -c "%{__perl_provides} | grep -Ev '^perl[(]Test::SubExporter.*[)]'"
%define __perl_provides %{provfilt}
%global reqfilt /bin/sh -c "%{__perl_requires} | grep -Ev '^perl[(](base|Test::SubExporter.*)[)]'"
%define __perl_requires %{reqfilt}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
%{_fixperms} %{buildroot}

%check


%clean
rm -rf %{buildroot}

%files
%doc Changes README t/
%dir %{perl_vendorlib}/Sub/
%dir %{perl_vendorlib}/Sub/Exporter/
%{perl_vendorlib}/Sub/Exporter.pm
%{perl_vendorlib}/Sub/Exporter/Util.pm
%doc %{perl_vendorlib}/Sub/Exporter/Cookbook.pod
%doc %{perl_vendorlib}/Sub/Exporter/Tutorial.pod
%{_mandir}/man3/Sub::Exporter.3pm*
%{_mandir}/man3/Sub::Exporter::Cookbook.3pm*
%{_mandir}/man3/Sub::Exporter::Tutorial.3pm*
%{_mandir}/man3/Sub::Exporter::Util.3pm*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.987-1
- 更新到 0.987

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.984-5
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.984-4
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.984-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 0.984-2
- Perl 5.16 rebuild

* Tue Jun  5 2012 Paul Howarth <paul@city-fan.org> - 0.984-1
- Update to 0.984 (documentation fixes)
- Add filters for provides/requires from the test suite
- BR: perl(base) and perl(Exporter) for the test suite

* Sun Mar 18 2012 Paul Howarth <paul@city-fan.org> - 0.982-11
- Drop %%defattr, redundant since rpm 4.4

* Sat Mar  3 2012 Paul Howarth <paul@city-fan.org> - 0.982-10
- Explicitly require perl(Package::Generator)
- Make %%files list more explicit
- Mark POD files as %%doc
- Use DESTDIR rather than PERL_INSTALL_ROOT
- Don't need to remove empty directories from buildroot
- Don't use macros for commands
- Use tabs

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.982-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jun 29 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.982-8
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.982-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.982-6
- Rebuild to fix problems with vendorarch/lib (#661697)

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.982-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.982-4
- Rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.982-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.982-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 11 2009 Chris Weyl <cweyl@alumni.drew.edu> - 0.982-1
- Update to 0.982

* Sun Oct 26 2008 Chris Weyl <cweyl@alumni.drew.edu> - 0.981-1
- Update to 0.981

* Thu Oct 23 2008 Chris Weyl <cweyl@alumni.drew.edu> - 0.980-1
- Update to 0.980

* Mon Jun 30 2008 Chris Weyl <cweyl@alumni.drew.edu> - 0.979-1
- Update to 0.979
- Drop BR's on: perl(Test::Pod::Coverage), perl(Test::Pod)

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.978-2
- Rebuild for perl 5.10 (again)

* Thu Jan 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.978-1
- Update to 0.978
- Fix license tag
- Rebuild for new perl

* Thu Aug 09 2007 Chris Weyl <cweyl@alumni.drew.edu> - 0.975-1
- Update to 0.975

* Fri Jun 01 2007 Chris Weyl <cweyl@alumni.drew.edu> - 0.974-1
- Update to 0.974

* Sat Dec 09 2006 Chris Weyl <cweyl@alumni.drew.edu> - 0.972-1
- Update to 0.972

* Thu Sep 07 2006 Chris Weyl <cweyl@alumni.drew.edu> - 0.970-2
- Bump

* Sat Sep 02 2006 Chris Weyl <cweyl@alumni.drew.edu> - 0.970-1
- Specfile autogenerated by cpanspec 1.69.1
