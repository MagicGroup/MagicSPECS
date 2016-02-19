Name:           perl-TestML
Version:        0.52
Release:        4%{?dist}
Summary:        Generic software Testing Meta Language
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/TestML/
Source0:        http://www.cpan.org/authors/id/I/IN/INGY/TestML-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(File::ShareDir::Install) >= 0.06
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(constant)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Spec)
# Used Pegex::Parser is not versioned, depend on Pegex version
BuildRequires:  perl(Pegex) >= 0.30
BuildRequires:  perl(Pegex::Parser)
BuildRequires:  perl(Test::Builder)
# Text::Diff not used at test-time
# XXX not used at test-time
# Tests:
BuildRequires:  perl(base)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::Builder)
BuildRequires:  perl(Test::More)
# Optional tests:
# t/000-compile-modules.t -> lib/TestML/Base.pm:
# Cwd, IO::All, Template::Toolkit::Simple and YAML::XS
BuildRequires:  perl(Cwd)
BuildRequires:  perl(IO::All)
BuildRequires:  perl(Capture::Tiny)
BuildRequires:  perl(Template::Toolkit::Simple)
BuildRequires:  perl(YAML::XS)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
# Used Pegex::Parser is not versioned, depend on Pegex version
Requires:       perl(Pegex) >= 0.30
Requires:       perl(Text::Diff)
Requires:       perl(XXX)
Requires:       perl(warnings)

%description
TestML <http://www.testml.org/> is a generic, programming language agnostic,
meta language for writing unit tests. The idea is that you can use the same
test files in multiple implementations of a given programming idea. Then you
can be more certain that your application written in, say, Python matches your
Perl implementation.

In a nutshell you write a bunch of data tests that have inputs and expected
results. Using a simple syntax, you specify what functions the data must pass
through to produce the expected results. You use a bridge class to write the
data functions that pass the data through your application.

In Perl 5, TestML module is the evolution of the Test::Base module. It has
a superset of Test:Base's goals. The data markup syntax is currently exactly
the same as Test::Base.


%prep
%setup -q -n TestML-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%license LICENSE
%doc Changes CONTRIBUTING README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.52-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.52-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 08 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.52-2
- Perl 5.22 rebuild

* Mon Jan 05 2015 Petr Pisar <ppisar@redhat.com> - 0.52-1
- 0.52 bump

* Thu Dec 18 2014 Petr Šabata <contyk@redhat.com> - 0.51-1
- 0.51 bump

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.49-2
- Perl 5.20 rebuild

* Mon Aug 18 2014 Petr Pisar <ppisar@redhat.com> - 0.49-1
- 0.49 bump

* Thu Aug 14 2014 Petr Pisar <ppisar@redhat.com> - 0.44-1
- 0.44 bump

* Tue Aug 12 2014 Petr Pisar <ppisar@redhat.com> - 0.43-1
- 0.43 bump

* Thu Aug 07 2014 Petr Pisar <ppisar@redhat.com> - 0.42-1
- 0.42 bump

* Wed Jul 30 2014 Petr Pisar <ppisar@redhat.com> 0.37-1
- Specfile autogenerated by cpanspec 1.78.
