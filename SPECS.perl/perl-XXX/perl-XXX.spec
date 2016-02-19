Name:           perl-XXX
Version:        0.29
Release:        4%{?dist}
Summary:        See Your Data in the Nude
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/XXX/
Source0:        http://search.cpan.org/CPAN/authors/id/I/IN/INGY/XXX-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(File::Find)
BuildRequires:  perl(strict)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(warnings)
BuildRequires:  perl(YAML)
Requires:       perl(:MODULE_COMPAT_%(eval "$(perl -V:version)"; echo $version))
Requires:       perl(Data::Dumper)
Requires:       perl(YAML)

%description
XXX.pm exports a function called XXX that you can put just about
anywhere in your Perl code to make it die with a YAML dump of the
arguments to its right.

The charm of XXX-debugging is that it is easy to type and rarely
requires parens and stands out visually so that you remember to remove
it.

XXX.pm also exports WWW, YYY and ZZZ which do similar debugging things.

To use Data::Dumper instead of YAML:
   use XXX -dumper;

%prep
%setup -q -n XXX-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=true
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
%{_fixperms} %{buildroot}/*

%check
make test

%files
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.29-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.29-2
- Perl 5.22 rebuild

* Mon Oct 13 2014 Petr Šabata <contyk@redhat.com> - 0.29-1
- 0.29 bump

* Wed Sep 10 2014 Petr Šabata <contyk@redhat.com> - 0.28-1
- 0.28 bump

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.27-2
- Perl 5.20 rebuild

* Wed Aug 20 2014 Petr Šabata <contyk@redhat.com> - 0.27-1
- 0.27 bump

* Fri Aug 08 2014 Petr Šabata <contyk@redhat.com> - 0.24-1
- 0.24 bump

* Fri Aug 01 2014 Petr Šabata <contyk@redhat.com> - 0.23-1
- 0.23 bump

* Mon Jun 23 2014 Petr Šabata <contyk@redhat.com> - 0.21-1
- 0.21 bump; no code changes

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 0.18-6
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 10 2012 Petr Pisar <ppisar@redhat.com> - 0.18-3
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Sep 05 2011 Petr Sabata <contyk@redhat.com> - 0.18-1
- 0.18 bump
- Remove now obsolete BuildRoot and defattr

* Wed Jun 29 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.17-4
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 23 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.17-2
- 661697 rebuild for fixing problems with vendorach/lib

* Tue Sep 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.17-1
- 633760 update

* Fri May 14 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.12-7
- Bump release for perl-5.12.0 rebuild.

* Tue Apr 27 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.12-6
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.12-4
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Apr 22 2009 Marcela Mašláňová <mmaslano@redhat.com> 0.12-2
- add BR Test::More and ExtUtils::MakeMaker

* Tue Apr 14 2009 Marcela Mašláňová <mmaslano@redhat.com> 0.12-1
- initial packaging
