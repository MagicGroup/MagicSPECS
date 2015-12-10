Name:           perl-Class-Tiny
Version:        1.001
Release:        6%{?dist}
Summary:        Minimalist class construction
License:        ASL 2.0
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Class-Tiny/
Source0:        http://www.cpan.org/authors/id/D/DA/DAGOLDEN/Class-Tiny-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.17
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time
BuildRequires:  perl(Carp)
%if 0%(perl -e 'print $] < 5.014')
BuildRequires:  perl(Devel::GlobalDestruction)
%endif
%if 0%(perl -e 'print $] >= 5.010')
BuildRequires:  perl(mro)
%else
BuildRequires:  perl(MRO::Compat)
%endif 
# Tests
BuildRequires:  perl(base)
BuildRequires:  perl(CPAN::Meta) >= 2.120900
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(lib)
BuildRequires:  perl(subs)
BuildRequires:  perl(Test::FailWarnings)
BuildRequires:  perl(Test::More) >= 0.96
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
%if 0%(perl -e 'print $] < 5.014')
Requires:       perl(Devel::GlobalDestruction)
%endif
%if 0%(perl -e 'print $] >= 5.010')
Requires:       perl(mro)
%else
Requires:       perl(MRO::Compat)
%endif 

# Filter from requires
%if 0%(perl -e 'print $] >= 5.014')
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Devel::GlobalDestruction\\)
%endif

%description
This module offers a minimalist class construction kit in around 120 lines
of code. Here is a list of features:

* defines attributes via import arguments
* generates read-write accessors
* supports lazy attribute defaults
* supports custom accessors
* superclass provides a standard new constructor
* new takes a hash reference or list of key/value pairs
* new has heuristics to catch constructor attribute typos
* new calls BUILD for each class from parent to child
* superclass provides a DESTROY method
* DESTROY calls DEMOLISH for each class from child to parent


%prep
%setup -q -n Class-Tiny-%{version}

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
%license LICENSE
%doc Changes CONTRIBUTING.mkdn README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 1.001-6
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1.001-5
- 为 Magic 3.0 重建

* Wed Sep 16 2015 Liu Di <liudidi@gmail.com> - 1.001-4
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.001-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.001-2
- Perl 5.22 rebuild

* Tue Feb 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.001-1
- 1.001 bump

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.000-2
- Perl 5.20 rebuild

* Tue Jul 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.000-1
- 1.000 bump

* Wed Jul 16 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.015-1
- 0.015 bump

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.014-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Nov 29 2013 Jitka Plesnikova <jplesnik@redhat.com> - 0.014-1
- 0.014 bump

* Thu Nov 28 2013 Jitka Plesnikova <jplesnik@redhat.com> - 0.013-1
- 0.013 bump

* Sun Nov 03 2013 Jitka Plesnikova <jplesnik@redhat.com> - 0.012-1
- 0.012 bump

* Thu Sep 26 2013 Jitka Plesnikova <jplesnik@redhat.com> - 0.011-1
- 0.011 bump

* Thu Sep 19 2013 Jitka Plesnikova <jplesnik@redhat.com> - 0.010-1
- 0.010 bump

* Tue Sep 17 2013 Jitka Plesnikova <jplesnik@redhat.com> - 0.009-1
- 0.009 bump

* Mon Sep 16 2013 Jitka Plesnikova <jplesnik@redhat.com> - 0.008-1
- Specfile autogenerated by cpanspec 1.78.
