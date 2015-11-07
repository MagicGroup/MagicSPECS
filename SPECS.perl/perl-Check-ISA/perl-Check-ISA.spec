
Name:       perl-Check-ISA 
Version:    0.04 
Release:        17%{?dist}
# see lib/Check/ISA.pm
License:    GPL+ or Artistic
Group:      Development/Libraries
Summary:    DWIM, correct checking of an object's class 
Source:     http://search.cpan.org/CPAN/authors/id/N/NU/NUFFIN/Check-ISA-%{version}.tar.gz 
Url:        http://search.cpan.org/dist/Check-ISA
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 
Requires:   perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:  noarch

BuildRequires: perl(ExtUtils::MakeMaker) 
BuildRequires: perl(Sub::Exporter)
BuildRequires: perl(Test::More)
BuildRequires: perl(Test::use::ok)
# optional tests
BuildRequires: perl(Moose), perl(Moose::Role)
BuildRequireS: perl(asa)

%description
This module provides several functions to assist in testing whether a value
is an object, and if so, ask about its class.


%prep
%setup -q -n Check-ISA-%{version}

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


%clean
rm -rf %{buildroot} 

%files
%defattr(-,root,root,-)
%doc Changes 
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.04-17
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.04-16
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.04-15
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.04-14
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.04-13
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.04-12
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 0.04-10
- Perl mass rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.04-9
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.04-7
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.04-6
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.04-5
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Nov 25 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.04-2
- bump

* Tue Nov 18 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.04-1
- update for submission

* Tue Nov 18 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.04-0.1
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.5)

