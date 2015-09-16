Name:       perl-MooseX-Role-WithOverloading 
Version:	0.16
Release:	1%{?dist}
# lib/MooseX/Role/WithOverloading.pm -> GPL+ or Artistic
License:    GPL+ or Artistic 
Group:      Development/Libraries
Summary:    Roles which support overloading 
Source:     http://search.cpan.org/CPAN/authors/id/E/ET/ETHER/MooseX-Role-WithOverloading-%{version}.tar.gz
Url:        http://search.cpan.org/dist/MooseX-Role-WithOverloading
Requires:   perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

BuildRequires: perl(aliased)
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(Moose) >= 0.94
BuildRequires: perl(Moose::Exporter)
BuildRequires: perl(Moose::Role) >= 1.15
BuildRequires: perl(Moose::Util::MetaRole)
BuildRequires: perl(MooseX::Types::Moose)
BuildRequires: perl(namespace::autoclean)
BuildRequires: perl(namespace::clean)
BuildRequires: perl(overload)
BuildRequires: perl(Test::CheckDeps) >= 0.002
BuildRequires: perl(Test::More) >= 0.88
BuildRequires: perl(Test::NoWarnings) >= 1.04
BuildRequires: perl(XSLoader)

%{?perl_default_filter}

%description
MooseX::Role::WithOverloading allows you to write a Moose::Role
that defines overloaded operators and allows those operator
overloadings to be composed into the classes/roles/instances it's
compiled to, while plain roles would lose the overloading.

%prep
%setup -q -n MooseX-Role-WithOverloading-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
%{_fixperms} %{buildroot}

%check
make test

%files
%doc Changes LICENSE README 
%{perl_vendorarch}/auto/MooseX/
%{perl_vendorarch}/MooseX/
%{_mandir}/man3/*.3*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.16-1
- 更新到 0.16

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Feb 27 2014 Paul Howarth <paul@city-fan.org> - 0.13-3
- We have Test::CheckDeps now

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 0.13-2
- Perl 5.18 rebuild

* Fri Feb 15 2013 Iain Arnell <iarnell@gmail.com> 0.13-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Petr Pisar <ppisar@redhat.com> - 0.09-5
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.09-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 08 2011 Iain Arnell <iarnell@gmail.com> 0.09-1
- update to latest upstream version
- update BR perl(Moose::Role) >= 1.15

* Wed Oct 06 2010 Iain Arnell <iarnell@gmail.com> 0.08-1
- update to latest upstream version

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.05-2
- Mass rebuild with perl-5.12.0

* Sat Feb 06 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.05-1
- submission

* Sat Feb 06 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.05-0
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.8)

