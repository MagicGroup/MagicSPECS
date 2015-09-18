Name:		perl-Unicode-EastAsianWidth
Version:	1.33
Release:	6%{?dist}
Summary:	East Asian Width properties
Group:		Development/Libraries
License:	CC0
URL:		http://search.cpan.org/dist/Unicode-EastAsianWidth/
Source0:	http://search.cpan.org/CPAN/authors/id/A/AU/AUDREYT/Unicode-EastAsianWidth-%{version}.tar.gz
Patch0:		perl-Unicode-EastAsianWidth-no-inc.patch
BuildArch:	noarch
BuildRequires:	perl(base)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(Test)
BuildRequires:	perl(Module::Package)
BuildRequires:	perl(Pod::Markdown)
BuildRequires:	perl(Module::Package::Au)
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

# Don't "provide" private Perl libs
%{?perl_default_filter}

%description
This module provide user-defined Unicode properties that deal with width
status of East Asian characters, as specified in
<http://www.unicode.org/unicode/reports/tr11/>.

%prep
%setup -q -n Unicode-EastAsianWidth-%{version}
%patch0 -p1 -b .noinc
rm -rf inc/*

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -empty -exec rm -f {} ';'
%{_fixperms} %{buildroot}

%check
make test

%files
%doc Changes README
%{perl_vendorlib}/Unicode/
%{_mandir}/man3/Unicode::EastAsianWidth.3pm*

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.33-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.33-5
- Perl 5.22 rebuild

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.33-4
- Perl 5.20 rebuild

* Tue Jul  8 2014 Tom Callaway <spot@fedoraproject.org> - 1.33-3
- fix MANIFEST to not include inc/ bits

* Tue Dec 11 2012 Tom Callaway <spot@fedoraproject.org> - 1.33-2
- update BuildRequires
- do not manually delete empty dirs
- delete bundled items in inc/

* Thu Nov  8 2012 Tom Callaway <spot@fedoraproject.org> - 1.33-1
- initial package
