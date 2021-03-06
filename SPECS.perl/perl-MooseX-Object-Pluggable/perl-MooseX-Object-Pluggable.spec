Name:           perl-MooseX-Object-Pluggable
Version:	0.0014
Release:	3%{?dist}
Summary:        Make your Moose classes pluggable
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/MooseX-Object-Pluggable/
Source0:        http://search.cpan.org/CPAN/authors/id/E/ET/ETHER/MooseX-Object-Pluggable-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Module::Pluggable::Object)
BuildRequires:  perl(Moose) >= 0.35

# nixed right now, as pod coverage tests fail.  These are developer tests, and
# will not impact the running of the module.
#BuildRequires:  perl(Test::Pod), perl(Test::Pod::Coverage)

Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

# keep rpmlint happy
Requires:       perl(strict), perl(warnings), perl(Moose)

# otherwise we have a ton of "provides" from files in doc.  We only really
# provide one package, so...
AutoProv:       no
Provides:       perl(MooseX::Object::Pluggable) = %{version}

%description
This module aids in the development and deploment of plugin-enabled
Moose-based classes.  It extends the Moose framework via roles to enable
this behavior.

%prep
%setup -q -n MooseX-Object-Pluggable-%{version}

perl -pi -e 's|^#!perl|#!/usr/bin/perl|; s|^#!/usr/local|#!/usr|' t/*.t

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make pure_install PERL_INSTALL_ROOT=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} %{buildroot}/*

%check
make test

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes README t/
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.0014-3
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.0014-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.0014-1
- 更新到 0.0014

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.0011-15
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0011-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0011-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Aug 02 2013 Petr Pisar <ppisar@redhat.com> - 0.0011-12
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0011-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0011-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Petr Pisar <ppisar@redhat.com> - 0.0011-9
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0011-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.0011-7
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0011-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.0011-5
- 661697 rebuild for fixing problems with vendorach/lib

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.0011-4
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.0011-3
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0011-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed May 20 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.0011-1
- auto-update to 0.0011 (by cpan-spec-update 0.01)
- altered br on perl(Moose) (0.17 => 0.35)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0009-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 10 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.0009-2
- rebuild against new Moose level

* Tue Dec 30 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.0009-1
- update to 0.0009

* Tue Jul 08 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.0007-2
- ...and fix build failure

* Tue Jul 08 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.0007-1
- update to 0.0007

* Wed Mar 05 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.0005-2
- rebuild for new perl

* Thu Apr 19 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.0005-1
- update to 0.0005
- update BR's
- add bits from t/lib/ to %%doc -- examples are always useful

* Wed Jan 24 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.0004-2
- bump

* Wed Jan 24 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.0004-1
- update to 0.0004

* Wed Jan 17 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.0002-1
- Specfile autogenerated by cpanspec 1.70.
