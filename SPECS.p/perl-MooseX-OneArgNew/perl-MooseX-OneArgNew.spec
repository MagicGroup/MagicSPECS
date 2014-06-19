Name:           perl-MooseX-OneArgNew
Version:        0.002
Release:        8%{?dist}
Summary:        Teach ->new to accept single, non-hashref arguments
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/MooseX-OneArgNew/
Source0:        http://www.cpan.org/authors/id/R/RJ/RJBS/MooseX-OneArgNew-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Moose)
BuildRequires:  perl(Moose::Util::TypeConstraints)
BuildRequires:  perl(MooseX::Role::Parameterized)
BuildRequires:  perl(namespace::autoclean)
BuildRequires:  perl(strict)
BuildRequires:  perl(Test::More) >= 0.96
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(warnings)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
MooseX::OneArgNew lets your constructor take a single argument, which will
be translated into the value for a one-entry hashref. It is a parameterized
role with two parameters:

%prep
%setup -q -n MooseX-OneArgNew-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%doc LICENSE README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.002-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 0.002-7
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.002-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.002-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Petr Pisar <ppisar@redhat.com> - 0.002-4
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.002-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.002-2
- Perl mass rebuild

* Sat Jun 25 2011 Iain Arnell <iarnell@gmail.com> 0.002-1
- update to latest upstream version

* Thu Feb 17 2011 Iain Arnell <iarnell@gmail.com> 0.001-1
- Specfile autogenerated by cpanspec 1.79.
