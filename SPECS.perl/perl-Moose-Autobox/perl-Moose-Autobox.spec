Name:       perl-Moose-Autobox 
Version:	0.15
Release:	1%{?dist}
# lib/Moose/Autobox.pm -> GPL+ or Artistic
License:    GPL+ or Artistic 
Group:      Development/Libraries
Summary:    Autoboxed wrappers for native Perl datatypes 
Source:     http://search.cpan.org/CPAN/authors/id/R/RJ/RJBS/Moose-Autobox-%{version}.tar.gz 
Url:        http://search.cpan.org/dist/Moose-Autobox
Requires:   perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:  noarch

BuildRequires: perl(autobox) >= 2.23
BuildRequires: perl(Carp)
BuildRequires: perl(Data::Dumper)
BuildRequires: perl(ExtUtils::MakeMaker) >= 6.42
BuildRequires: perl(Moose) >= 0.42
BuildRequires: perl(Moose::Role)
BuildRequires: perl(parent)
BuildRequires: perl(Perl6::Junction) >= 1.40000
BuildRequires: perl(Scalar::Util)
BuildRequires: perl(Test::Exception) >= 0.21
BuildRequires: perl(Test::More) >= 0.89

# not automagically picked up
Requires:      perl(autobox)

%{?perl_default_filter}

%description
Moose::Autobox provides an implementation of SCALAR, ARRAY, HASH & CODE
for use with autobox. 


%prep
%setup -q -n Moose-Autobox-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'

%{_fixperms} %{buildroot}/*

%check
make test

%files
%doc Changes README examples/ 
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.15-1
- 更新到 0.15

* Thu Jun 19 2014 Liu Di <liudidi@gmail.com> - 0.12-8
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Aug 02 2013 Petr Pisar <ppisar@redhat.com> - 0.12-5
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Petr Pisar <ppisar@redhat.com> - 0.12-2
- Perl 5.16 rebuild
- Specify all dependencies

* Sat Mar 24 2012 Iain Arnell <iarnell@gmail.com> 0.12-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.11-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Oct 03 2010 Iain Arnell <iarnell@gmail.com> 0.11-1
- update to latest upstream

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.09-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.09-2
- rebuild against perl 5.10.1

* Mon Aug 31 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.09-1
- submission

* Fri Aug 07 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.09-0
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.8)

