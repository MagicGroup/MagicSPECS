Name:           perl-Syntax-Keyword-Junction
Version:        0.003008
Release:        5%{?dist}
Summary:        Perl6 style Junction operators in Perl5
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Syntax-Keyword-Junction/
Source0:        http://www.cpan.org/authors/id/F/FR/FREW/Syntax-Keyword-Junction-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.30
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(if)
BuildRequires:  perl(overload)
BuildRequires:  perl(parent)
BuildRequires:  perl(Sub::Exporter::Progressive) >= 0.001006
# Tests:
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(Test::Requires) >= 0.07
BuildRequires:  perl(syntax)
# Optional tests:
BuildRequires:  perl(Sub::Exporter) >= 0.986
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(if)
Requires:       perl(overload)
Requires:       perl(Sub::Exporter::Progressive) >= 0.001006

# Remove under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Sub::Exporter::Progressive\\)$

%description
This is a lightweight module which provides 'Junction' operators, the most
commonly used being any and all. Inspired by the Perl6 design docs,
<http://dev.perl.org/perl6/doc/design/exe/E06.html>.

%prep
%setup -q -n Syntax-Keyword-Junction-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%doc Changes LICENSE README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Thu Sep 17 2015 Liu Di <liudidi@gmail.com> - 0.003008-5
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.003008-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.003008-3
- Perl 5.22 rebuild

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.003008-2
- Perl 5.20 rebuild

* Tue Jul 08 2014 Petr Pisar <ppisar@redhat.com> - 0.003008-1
- 0.003008 bump

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.003007-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Nov 25 2013 Petr Pisar <ppisar@redhat.com> - 0.003007-1
- 0.003007 bump

* Thu Aug 08 2013 Petr Pisar <ppisar@redhat.com> - 0.003006-1
- 0.003006 bump

* Mon Aug 05 2013 Petr Pisar <ppisar@redhat.com> 0.003004-1
- Specfile autogenerated by cpanspec 1.78.
