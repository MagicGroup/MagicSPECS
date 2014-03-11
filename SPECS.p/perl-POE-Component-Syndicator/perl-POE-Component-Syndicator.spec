Name:           perl-POE-Component-Syndicator
Version:        0.06
Release:        4%{?dist}
Summary:        POE component base class which implements the Observer pattern
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/POE-Component-Syndicator/
Source0:        http://www.cpan.org/authors/id/H/HI/HINRIK/POE-Component-Syndicator-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(constant)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Object::Pluggable) >= 1.29
BuildRequires:  perl(Object::Pluggable::Constants)
BuildRequires:  perl(POE) >= 1.311
# Tests
BuildRequires:  perl(Test::More)
Requires:       perl(Object::Pluggable) >= 1.29
Requires:       perl(POE) >= 1.311
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

# Underspecified dependencies filter
# RPM 4.8 style
%filter_from_requires /^perl(POE)$/d
%filter_from_requires /^perl(Object::Pluggable)$/d
%{?perl_default_filter}
# RPM 4.9 style
%global __requires_exclude %{?__requires_exclude:__requires_exclude|}^perl\\(POE\\)$
%global __requires_exclude %__requires_exclude|^perl\\(Object::Pluggable\\)$

%description
POE::Component::Syndicator is a base class for POE components which need to
handle a persistent resource (e.g. a connection to an IRC server) for one
or more sessions in an extendable way.

%prep
%setup -q -n POE-Component-Syndicator-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;
%{_fixperms} %{buildroot}/*

%check
make test

%files
%doc Changes dist.ini LICENSE META.json README xt
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 0.06-3
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Aug  2 2011 Petr Sabata <contyk@redhat.com> 0.06-1
- Initial package.
