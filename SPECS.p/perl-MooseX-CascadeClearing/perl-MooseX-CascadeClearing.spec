Name:           perl-MooseX-CascadeClearing
Version:        0.05
Release:        4%{?dist}
Summary:        Cascade clearer actions across attributes
License:        LGPLv2+
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/MooseX-CascadeClearing/
Source0:        http://www.cpan.org/authors/id/R/RS/RSRCHBOY/MooseX-CascadeClearing-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(Carp)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(lib)
BuildRequires:  perl(Moose)
BuildRequires:  perl(Moose::Exporter)
BuildRequires:  perl(Moose::Role)
BuildRequires:  perl(Moose::Util::MetaRole)
BuildRequires:  perl(namespace::autoclean)
BuildRequires:  perl(Test::More) >= 0.88
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
MooseX::CascadeClearing does the necessary meta class fiddling to allow an
clearing one attribute to be cascaded through to other attributes as well,
calling their clear accessors.

%prep
%setup -q -n MooseX-CascadeClearing-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 0.05-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Sep 17 2012 Jitka Plesnikova <jplesnik@redhat.com> - 0.05-1
- 0.05 bump
- Update dependencies.
- Modernize spec and drop command macros. 
- Remove unnecessary patch and filter. 

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Petr Pisar <ppisar@redhat.com> - 0.04-5
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 21 2011 Iain Arnell <iarnell@gmail.com> 0.04-3
- update filtering for rpm 4.9

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.04-2
- Perl mass rebuild

* Mon Apr 04 2011 Petr Pisar <ppisar@redhat.com> - 0.04-1
- 0.04 bump

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.03-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.03-2
- 661697 rebuild for fixing problems with vendorach/lib

* Thu Sep 16 2010 Petr Pisar <ppisar@redhat.com> - 0.03-1
- 0.03 bump
- Correct description spelling
- Remove unversioned Requires

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.02-3
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.02-2
- rebuild against perl 5.10.1

* Tue Oct 20 2009 Marcela Mašláňová <mmaslano@redhat.com> 0.02-1
- Specfile autogenerated by cpanspec 1.78.
