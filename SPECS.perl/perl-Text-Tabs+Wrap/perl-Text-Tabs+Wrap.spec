Name:           perl-Text-Tabs+Wrap
Version:        2013.0523
Release:        346%{?dist}
Summary:        Expand tabs and do simple line wrapping
License:        TTWL
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Text-Tabs%2BWrap/
Source0:        http://www.cpan.org/authors/id/M/MU/MUIR/modules/Text-Tabs+Wrap-%{version}.tar.gz
# Work around CPAN RT#103116
Patch0:         Text-Tabs+Wrap-2013.0523-Build-from-lib.patch
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker)
# Run-time:
BuildRequires:  perl(Exporter)
BuildRequires:  perl(re)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings::register)
# Tests:
BuildRequires:  perl(bytes)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(warnings)
# Optional tests:
# Benchmark not used
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
# Sub-packaged from perl.spec, it would conflicted on manual pages
Conflicts:      perl < 4:5.20.2-325

%description
Text::Tabs performs the same job that the UNIX expand(1) and unexpand(1)
commands do: adding or removing tabs from a document.

Text::Wrap::wrap() will reformat lines into paragraphs. All it does is break
up long lines, it will not join short lines together.

%prep
%setup -q -n Text-Tabs+Wrap-%{version}
%patch0 -p1

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
%{_fixperms} %{buildroot}/*

%check
make test

%files
%doc CHANGELOG README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2013.0523-346
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2013.0523-345
- Increase release to favour standalone package

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2013.0523-327
- Perl 5.22 rebuild

* Wed Mar 25 2015 Petr Pisar <ppisar@redhat.com> - 2013.0523-326
- Increase release number to compete with perl's sub-package
- Fix manual pages names

* Wed Feb 13 2013 Petr Pisar <ppisar@redhat.com> - 2013.0523-1
- Version 2013.0523 packaged

