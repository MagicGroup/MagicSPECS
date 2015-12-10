Name:       perl-MooseX-Types-URI
Version:	0.08
Release:	3%{?dist}
# see lib/MooseX/Types/URI.pm
License:    GPL+ or Artistic
Group:      Development/Libraries
Summary:    URI related types and coercions for Moose
Source0:        http://search.cpan.org/CPAN/authors/id/E/ET/ETHER/MooseX-Types-URI-%{version}.tar.gz
Url:        http://search.cpan.org/dist/MooseX-Types-URI
Requires:   perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:  noarch

BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(Moose) >= 0.50
BuildRequires: perl(MooseX::Types)
BuildRequires: perl(MooseX::Types::Path::Class)
BuildRequires: perl(namespace::clean) >= 0.08
BuildRequires: perl(Test::use::ok)
BuildRequires: perl(URI)
BuildRequires: perl(URI::FromHash)

%{?perl_default_filter}

%description
This package provides Moose types for fun (and profit) with the URI classes.

It has slightly DWIMier types than the the URI classes have due to
implementation details, so the types should be more forgiving when
ducktyping will work anyway (e.g. URI::WithBase does not inherit URI).


%prep
%setup -q -n MooseX-Types-URI-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'

%{_fixperms} %{buildroot}/*

%check
make test

%files
%doc t/
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.08-3
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.08-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.08-1
- 更新到 0.08

* Thu Jun 19 2014 Liu Di <liudidi@gmail.com> - 0.03-8
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.03-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Petr Pisar <ppisar@redhat.com> - 0.03-6
- Perl 5.18 rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.03-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.03-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.03-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Petr Pisar <ppisar@redhat.com> - 0.03-2
- Perl 5.16 rebuild

* Thu Jan 12 2012 Iain Arnell <iarnell@gmail.com> 0.03-1
- update to latest upstream version
- clean up spec for modern rpmbuild
- use perl_default_filter
- use DESTDIR, not PERL_INSTALL_ROOT

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.02-7
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.02-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.02-5
- 661697 rebuild for fixing problems with vendorach/lib

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.02-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.02-3
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.02-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri May 29 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.02-1
- auto-update to 0.02 (by cpan-spec-update 0.01)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.01-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Oct 07 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.01-1
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.1)
