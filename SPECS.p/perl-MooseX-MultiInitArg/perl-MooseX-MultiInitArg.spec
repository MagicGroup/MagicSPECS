Name:       perl-MooseX-MultiInitArg 
Version:    0.02 
Release:    2%{?dist}
# lib/MooseX/MultiInitArg.pm -> GPL+ or Artistic
# lib/MooseX/MultiInitArg/Attribute.pm -> GPL+ or Artistic
# lib/MooseX/MultiInitArg/Trait.pm -> GPL+ or Artistic
License:    GPL+ or Artistic 
Group:      Development/Libraries
Summary:    Attributes with aliases for constructor arguments 
Source:     http://search.cpan.org/CPAN/authors/id/F/FR/FRODWITH/MooseX-MultiInitArg-%{version}.tar.gz 
Url:        http://search.cpan.org/dist/MooseX-MultiInitArg
Requires:   perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
BuildArch:  noarch
BuildRequires: perl
BuildRequires: perl(Module::Build::Tiny) >= 0.023
# Run-time:
BuildRequires: perl(Carp)
BuildRequires: perl(Moose)
BuildRequires: perl(Moose::Role)
BuildRequires: perl(strict)
BuildRequires: perl(warnings)
# Tests:
BuildRequires: perl(Test::More)
BuildRequires: perl(Test::Pod) >= 1.22

%{?perl_default_filter}

%description
If you've ever wanted to be able to call an attribute any number of
things while you're passing arguments to your object constructor, Now
You Can. This is an attribute metaclass / trait to allow easy new()-time
attribute aliasing.

%prep
%setup -q -n MooseX-MultiInitArg-%{version}

%build
perl Build.PL --installdirs vendor
./Build

%install
./Build install --destdir $RPM_BUILD_ROOT --create_packlist 0
%{_fixperms} $RPM_BUILD_ROOT

%check
./Build test

%files
%doc Changes LICENSE README 
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.02-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Aug 02 2013 Petr Pisar <ppisar@redhat.com> - 0.02-1
- 0.02 bump

* Fri Aug 02 2013 Petr Pisar <ppisar@redhat.com> - 0.01-15
- Perl 5.18 rebuild

* Sun Feb 17 2013 Iain Arnell <iarnell@gmail.com>     0.01 -14
- clean up spec for modern rpmbuild
- BuildRequire EU::MM
- pass skipdeps to Makefile.PL

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.01-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.01-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Petr Pisar <ppisar@redhat.com> - 0.01-11
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.01-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.01-9
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.01-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.01-7
- 661697 rebuild for fixing problems with vendorach/lib

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.01-6
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.01-5
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.01-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.01-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 18 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.01-2
- update description

* Sat Jan 17 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.01-1
- update for submission

* Mon Jan 05 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.01-0
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.7)

