Name:		perl-Module-Package-Au
Version:	2
Release:	6%{?dist}
Summary:	Reusable Module::Install bits
Group:		Development/Libraries
License:	CC0
URL:		http://search.cpan.org/dist/Module-Package-Au/
Source0:	http://search.cpan.org/CPAN/authors/id/A/AU/AUDREYT/Module-Package-Au-%{version}.tar.gz
Patch0:		perl-Module-Package-Au-no-bundle.patch
BuildArch:	noarch
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(Module::Install::AuthorTests)
BuildRequires:	perl(Module::Install::GithubMeta)
BuildRequires:	perl(Module::Install::ReadmeFromPod)
BuildRequires:	perl(Module::Install::ReadmeMarkdownFromPod)
BuildRequires:	perl(Module::Install::Repository)
BuildRequires:	perl(Module::Package) >= 0.24
BuildRequires:	perl(Pod::Markdown)
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

# Don't "provide" private Perl libs
%{?perl_default_filter}

%description
This module defines a set of standard configurations for Makefile.PL
files based on Module::Package.

%prep
%setup -q -n Module-Package-Au-%{version}
%patch0 -p1 -b .no-bundle
rm -rf inc/*

# Work around goofy perl versioning mistakes of the past
sed -i 's|1.110730|1.301|g' lib/Module/Package/Au.pm
sed -i 's|1.110730|1.301|g' META.yml

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
%{perl_vendorlib}/Module/Package/
%{_mandir}/man3/Module::Package::Au.3pm*

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 2-6
- 为 Magic 3.0 重建

* Fri Sep 18 2015 Liu Di <liudidi@gmail.com> - 2-5
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2-3
- Perl 5.22 rebuild

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2-2
- Perl 5.20 rebuild

* Tue Jul  8 2014 Tom Callaway <spot@fedoraproject.org> - 2-1
- update to 2

* Tue Dec 11 2012 Tom Callaway <spot@fedoraproject.org> - 0.01-1
- initial package
