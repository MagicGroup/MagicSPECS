Name:       perl-MooseX-ConfigFromFile 
Version:    0.04
Release:    5%{?dist}
# see lib/MooseX/ConfigFromFile.pm
License:    GPL+ or Artistic 
Group:      Development/Libraries
Summary:    An abstract Moose role for setting attributes from a configfile 
Source:     http://search.cpan.org/CPAN/authors/id/B/BO/BOBTFISH/MooseX-ConfigFromFile-%{version}.tar.gz
Url:        http://search.cpan.org/dist/MooseX-ConfigFromFile
Requires:   perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:  noarch

BuildRequires: perl(ExtUtils::MakeMaker) 
BuildRequires: perl(Moose) >= 0.35
BuildRequires: perl(MooseX::Types::Path::Class) >= 0.04
BuildRequires: perl(Test::Fatal)
BuildRequires: perl(Test::More) >= 0.42
BuildRequires: perl(Try::Tiny)
BuildRequires: perl(namespace::autoclean)

%{?perl_default_filter}

%description
This is an abstract role which provides an alternate constructor for
creating objects using parameters passed in from a configuration file. The
actual implementation of reading the configuration file is left to concrete
subroles.

It declares an attribute 'configfile' and a class method 'new_with_config',
and requires that concrete roles derived from it implement the class method
'get_config_from_file'.

Attributes specified directly as arguments to 'new_with_config' supercede
those in the configfile.

%prep
%setup -q -n MooseX-ConfigFromFile-%{version}

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
%doc ChangeLog README t/
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.04-5
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Petr Pisar <ppisar@redhat.com> - 0.04-3
- Perl 5.16 rebuild

* Tue Jan 17 2012 Iain Arnell <iarnell@gmail.com> - 0.04-2
- rebuilt again for F17 mass rebuild

* Fri Jan 13 2012 Iain Arnell <iarnell@gmail.com> 0.04-1
- update to latest upstream version

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.03-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.03-2
- Perl mass rebuild

* Sun Mar 06 2011 Iain Arnell <iarnell@gmail.com> 0.03-1
- update to latest upstream version
- clean up spec for modern rpmbuild
- use perl_default_filter

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.02-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.02-6
- 661697 rebuild for fixing problems with vendorach/lib

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.02-5
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.02-4
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.02-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.02-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 05 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.02-1
- brush up for submission

* Mon Oct 27 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.02-0.1
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.5)

