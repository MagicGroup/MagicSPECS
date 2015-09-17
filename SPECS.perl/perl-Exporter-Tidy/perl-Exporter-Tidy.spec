Name:           perl-Exporter-Tidy
Version:        0.08
Release:        3%{?dist}
Summary:        Another way of exporting symbols
# Generated with licenses.pl
License:        AAL or AFL or AGPLv3 or APSL 2.0 or ASL 2.0 or Artistic 2.0 or BSD or Boost or CATOSL or CDDL or CNRI or CPAL or CeCILL or ECL 2.0 or EFL 2.0 or EPL or EU Datagrid or EUPL 1.1 or Entessa or Fair or GPLv2 or GPLv3 or IBM or IPA or ISC or LGPLv2 or LGPLv3 or LPL or LPPL or MIT or MPLv1.1 or MPLv2.0 or MS-PL or MS-RL or MirOS or Motosoto or NCSA or NGPL or Naumen or Nokia or OFL or OSL 3.0 or PHP or PostgreSQL or Python or QPL or RPSL or SPL or Sleepycat or VSL or W3C or ZPLv2.0 or zlib
URL:            http://search.cpan.org/dist/Exporter-Tidy/
Source0:        http://www.cpan.org/authors/id/J/JU/JUERD/Exporter-Tidy-%{version}.tar.gz
BuildArch:      noarch
# Build
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# Runtime
BuildRequires:  perl(Carp)
# Tests only
BuildRequires:  perl(Config)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(lib)
BuildRequires:  perl(strict)
BuildRequires:  perl(threads)
BuildRequires:  perl(threads::shared)
BuildRequires:  perl(vars)
Requires:       perl(:MODULE_COMPAT_%(eval "$(perl -V:version)"; echo $version))
Requires:       perl(Carp)

%description
This module serves as an easy, clean alternative to Exporter. Unlike
Exporter, it is not subclassed, but it simply exports a custom import()
into your namespace.

%prep
%setup -q -n Exporter-Tidy-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
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
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.08-2
- Perl 5.22 rebuild

* Tue Jan 06 2015 Petr Šabata <contyk@redhat.com> - 0.08-1
- 0.08 bump

* Mon Jan 05 2015 Petr Šabata <contyk@redhat.com> - 0.07-1
- Initial packaging
