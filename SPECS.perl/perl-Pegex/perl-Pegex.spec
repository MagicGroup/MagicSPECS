Name:           perl-Pegex
Version:        0.60
Release:        7%{?dist}
Summary:        Pegex Parser Generator
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Pegex/
Source0:        http://search.cpan.org/CPAN/authors/id/I/IN/INGY/Pegex-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.30
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  perl(File::ShareDir::Install)
# Run-time
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(JSON::XS)
BuildRequires:  perl(overload)
BuildRequires:  perl(re)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(YAML::XS)
# Tests
BuildRequires:  perl(base)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::More)
%if !%{defined perl_bootstrap}
# Break dependency cycle: perl-Pegex → perl-TestML → perl-Pegex
BuildRequires:  perl(TestML)
BuildRequires:  perl(TestML::Bridge)
BuildRequires:  perl(TestML::Compiler::Lite)
BuildRequires:  perl(TestML::Util)
%endif
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(Data::Dumper)
Requires:       perl(JSON::XS)
Requires:       perl(warnings)
Requires:       perl(YAML::XS)

%description
Pegex is a Acmeist parser framework. It is a PEG parser grammar syntax,
combined with PCRE compatible regular expressions as the match tokens.
Pegex draws heavily from Perl 6 rules, but works equivalently in many
modern programming languages.

%prep
%setup -q -n Pegex-%{version}
# Remove bundled modules
rm -r ./inc
sed -i -e '/^inc\//d' MANIFEST

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
%{_fixperms} $RPM_BUILD_ROOT/*

%check
%if %{defined perl_bootstrap}
# Break dependency cycle: perl-Pegex → perl-TestML → perl-Pegex
make test TEST_FILES="$(find t -name '*.t' \
    \! -exec grep -q -e 'use TestML' {} \; -print | tr \"\\n\" ' ')"
%else
make test
%endif

%files
%doc Changes CONTRIBUTING LICENSE README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Fri Feb 19 2016 Liu Di <liudidi@gmail.com> - 0.60-7
- 为 Magic 3.0 重建

* Fri Feb 19 2016 Liu Di <liudidi@gmail.com> - 0.60-6
- 为 Magic 3.0 重建

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.60-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.60-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.60-3
- Perl 5.22 re-rebuild of bootstrapped packages

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.60-2
- Perl 5.22 rebuild

* Wed Feb 04 2015 Gerd Pokorra <gp@zimt.uni-siegen.de> 0.60-1
- Update to 0.60
- BuildRequires perl(File::ShareDir::Install) added

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.45-3
- Perl 5.20 re-rebuild of bootstrapped packages

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.45-2
- Perl 5.20 rebuild

* Fri Aug 08 2014 Gerd Pokorra <gp@zimt.uni-siegen.de> 0.45-1
- Update to 0.45

* Thu Aug 07 2014 Petr Pisar <ppisar@redhat.com> - 0.44-2
- Finish bootstrap

* Thu Jul 31 2014 Petr Pisar <ppisar@redhat.com> - 0.44-1
- 0.44 bump

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Aug 02 2013 Petr Pisar <ppisar@redhat.com> - 0.21-2
- Perl 5.18 rebuild

* Mon Feb 18 2013 Gerd Pokorra <gp@zimt.uni-siegen.de> 0.21-1
- Update to 0.21

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 0.11-6
- Perl 5.16 rebuild
- Specify all dependencies

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.11-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 27 2011 Gerd Pokorra <gp@zimt.uni-siegen.de> 0.11-2
- rebuild with new Perl version

* Wed Oct 27 2010 Gerd Pokorra <gp@zimt.uni-siegen.de> 0.11-1
- remove unnecessary BuildRequires

* Sun Oct 03 2010 Gerd Pokorra <gp@zimt.uni-siegen.de> 0.10-1
- BuildRequires perl(Test::Builder) added
- Specfile autogenerated by cpanspec 1.78.
