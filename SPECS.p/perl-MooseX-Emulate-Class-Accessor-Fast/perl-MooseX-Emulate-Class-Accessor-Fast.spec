Name:       perl-MooseX-Emulate-Class-Accessor-Fast
Version:    0.00903
Release:    13%{?dist}
# lib/MooseX/Adopt/Class/Accessor/Fast.pm -> GPL+ or Artistic
# lib/MooseX/Emulate/Class/Accessor/Fast.pm -> GPL+ or Artistic
License:    GPL+ or Artistic
Group:      Development/Libraries
Summary:    Emulate Class::Accessor::Fast behavior using Moose attributes
Source:     http://search.cpan.org/CPAN/authors/id/F/FL/FLORA/MooseX-Emulate-Class-Accessor-Fast-%{version}.tar.gz
Url:        http://search.cpan.org/dist/MooseX-Emulate-Class-Accessor-Fast
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:   perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:  noarch

BuildRequires: perl(ExtUtils::MakeMaker) >= 6.42
BuildRequires: perl(Moose)               >= 0.84
BuildRequires: perl(Moose::Role)
BuildRequires: perl(namespace::clean)
# tests
BuildRequires: perl(Test::More)
BuildRequires: perl(Test::Exception)
BuildRequires: perl(Class::Accessor::Fast)

### auto-added reqs!
Requires:  perl(Moose) >= 0.84
Requires:  perl(namespace::clean)

%description
This module attempts to emulate the behavior of Class::Accessor::Fast
as accurately as possible using the Moose attribute system. The public
API of "Class::Accessor::Fast" is wholly supported, but the private
methods are not.  If you are only using the public methods (as you
should) migration should be a matter of switching your "use base" line
to a "with" line.


%prep
%setup -q -n MooseX-Emulate-Class-Accessor-Fast-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'

%{_fixperms} %{buildroot}/*

%check
make test

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README Changes
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.00903-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.00903-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Aug 02 2013 Petr Pisar <ppisar@redhat.com> - 0.00903-11
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.00903-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.00903-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Petr Pisar <ppisar@redhat.com> - 0.00903-8
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.00903-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.00903-6
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.00903-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.00903-4
- 661697 rebuild for fixing problems with vendorach/lib

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.00903-3
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.00903-2
- rebuild against perl 5.10.1

* Sat Sep 19 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.00903-1
- auto-update to 0.00903 (by cpan-spec-update 0.01)

* Sat Aug 08 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.00902-1
- auto-update to 0.00902 (by cpan-spec-update 0.01)
- altered br on perl(Moose) (0.74 => 0.84)
- added a new req on perl(Moose) (version 0.84)
- added a new req on perl(namespace::clean) (version 0)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.00900-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May 31 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.00900-1
- auto-update to 0.00900 (by cpan-spec-update 0.01)

* Sun May 17 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.00802-1
- auto-update to 0.00802 (by cpan-spec-update 0.01)
- altered br on perl(Moose) (0.31 => 0.74)

* Sun Apr 19 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.00801-1
- update to 0.00801

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.00800-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 10 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.00800-1
- update for submission

* Tue Feb 10 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.00800-0
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.8)
