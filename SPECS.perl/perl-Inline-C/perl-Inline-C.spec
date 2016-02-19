Name:           perl-Inline-C
Version:        0.76
Release:        2%{?dist}
Summary:        Write Perl subroutines in C
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Inline-C/
Source0:        http://search.cpan.org/CPAN/authors/id/I/IN/INGY/Inline-C-%{version}.tar.gz
BuildArch:      noarch
# Build
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker) >= 7.00
BuildRequires:  perl(File::ShareDir::Install)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Runtime
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(constant)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(File::Spec) >= 0.8
BuildRequires:  perl(FindBin)
BuildRequires:  perl(if)
BuildRequires:  perl(Inline) >= 0.58
# Inline::Filters and Inline::Struct are optional and introduce circular deps
BuildRequires:  perl(Parse::RecDescent) >= 1.967009
BuildRequires:  perl(Pegex::Base)
BuildRequires:  perl(Pegex::Parser)
BuildRequires:  perl(Time::HiRes)
# Tests only
BuildRequires:  perl(autodie)
BuildRequires:  perl(base)
BuildRequires:  perl(diagnostics)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Copy::Recursive)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(IO::All)
BuildRequires:  perl(IPC::Cmd)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(Test::Warn) >= 0.23
BuildRequires:  perl(version) >= 0.77
BuildRequires:  perl(YAML::XS)
Requires:       perl(:MODULE_COMPAT_%(eval "$(perl -V:version)"; echo $version))
Requires:       perl(Fcntl)
Requires:       perl(FindBin)
Requires:       perl(File::Spec) >= 0.8
Requires:       perl(Inline) >= 0.58
Requires:       perl(Parse::RecDescent) >= 1.967009
Requires:       perl(Time::HiRes)
# Split from Inline in 0.58
Conflicts:      perl-Inline < 0.58

%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(File::Spec\\)$

%description
Inline::C is a module that allows you to write Perl subroutines in C. Since
version 0.30 the Inline module supports multiple programming languages and
each language has its own support module.

%prep
%setup -q -n Inline-C-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}" NO_PACKLIST=1
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
%{_fixperms} %{buildroot}/*

%check
make test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/auto/*
%{perl_vendorlib}/Inline/*
%{_mandir}/man3/*

%changelog
* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.76-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jul 02 2015 Petr Šabata <contyk@redhat.com> - 0.76-1
- 0.76 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.75-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.75-2
- Perl 5.22 rebuild

* Wed Mar 18 2015 Petr Šabata <contyk@redhat.com> - 0.75-1
- 0.75 bump, documentation fixes

* Wed Feb 18 2015 Petr Šabata <contyk@redhat.com> - 0.74-1
- 0.74 bump, Win32 fixes only

* Thu Jan 08 2015 Petr Šabata <contyk@redhat.com> - 0.73-1
- 0.73 bump

* Wed Nov 26 2014 Petr Šabata <contyk@redhat.com> - 0.67-1
- 0.67 bump

* Wed Nov 05 2014 Petr Šabata <contyk@redhat.com> - 0.64-2
- Backport "PERL IN SPACE" changes from ETJ's 0.65,
  fixing FTBFS with EE::UU 7.00 (#1158390)

* Mon Sep 29 2014 Petr Šabata <contyk@redhat.com> - 0.64-1
- 0.64 bump, include Cookbook.pod again

* Fri Sep 19 2014 Petr Šabata <contyk@redhat.com> - 0.62-1
- 0.62 bump, test suite and documentation changes

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.60-2
- Perl 5.20 rebuild

* Wed Jul 16 2014 Petr Šabata <contyk@redhat.com> 0.60-1
- Initial packaging
