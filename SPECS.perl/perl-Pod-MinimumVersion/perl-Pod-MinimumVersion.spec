Name:           perl-Pod-MinimumVersion
Version:        50
Release:        14%{?dist}
Summary:        Perl version for POD directives used
License:        GPLv3+
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Pod-MinimumVersion/
Source0:        http://www.cpan.org/authors/id/K/KR/KRYDE/Pod-MinimumVersion-%{version}.tar.gz
BuildArch:      noarch
# See Makefile.PL for dependencies; META.yml is out-dated.
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(IO::String) >= 1.02
BuildRequires:  perl(List::Util)
BuildRequires:  perl(Pod::Parser)
BuildRequires:  perl(version)
# Tests only
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Test)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(IO::String) >= 1.02
# This module has been divided from perl-Perl-Critic-Pulp
Conflicts:      perl-Perl-Critic-Pulp < 49

%description
Pod::MinimumVersion parses the POD in a Perl script, module, or document,
and reports what version of Perl is required to process the directives in
it with pod2man etc.

%prep
%setup -q -n Pod-MinimumVersion-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;
%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%defattr(-,root,root,-)
%doc Changes COPYING
%{perl_vendorlib}/*
%{_bindir}/*
%{_mandir}/man3/*
%{_mandir}/man1/*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 50-14
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 50-13
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 50-12
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 50-11
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 50-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 50-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 50-8
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 50-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 50-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 50-5
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 50-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 50-3
- Perl mass rebuild

* Thu Apr 21 2011 Petr Pisar <ppisar@redhat.com> - 50-2
- Splitted from perl-Perl-Critic-Pulp, conficts with old perl-Perl-Critic-Pulp
  versions

* Wed Apr 06 2011 Petr Pisar <ppisar@redhat.com> 50-1
- Specfile autogenerated by cpanspec 1.78.
- Remove BuildRoot stuff
