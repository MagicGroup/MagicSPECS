Name:       perl-Module-Install-GithubMeta 
Version:	0.30
Release:	1%{?dist}
# lib/Module/Install/GithubMeta.pm -> GPL+ or Artistic
License:    GPL+ or Artistic 
Group:      Development/Libraries
Summary:    A Module::Install extension to include GitHub meta information in META.yml 
Source:     http://search.cpan.org/CPAN/authors/id/B/BI/BINGOS/Module-Install-GithubMeta-%{version}.tar.gz 
Url:        http://search.cpan.org/dist/Module-Install-GithubMeta
Requires:   perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:  noarch

BuildRequires: perl(Capture::Tiny) >= 0.05
BuildRequires: perl(ExtUtils::MakeMaker) >= 6.42
BuildRequires: perl(Module::Install) >= 0.85
BuildRequires: perl(Test::More) >= 0.47
BuildRequires: perl(Test::Pod)

Requires:      perl(Module::Install) >= 0.85

%{?perl_default_filter}

%description
Module::Install::GithubMeta is a Module::Install extension
to include GitHub (http://github.com) meta information in
'META.yml'.  It automatically detects if the distribution 
directory is under 'git' version control and whether the 
'origin' is a GitHub repository; if so, it will set the
'repository' and 'homepage' meta in 'META.yml' to the 
appropriate URLs for GitHub.


%prep
%setup -q -n Module-Install-GithubMeta-%{version}

cat README | iconv -f `file --mime-encoding --brief README` -t UTF-8 > x
mv x README

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'

%{_fixperms} %{buildroot}/*

%check


%files
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.30-1
- 更新到 0.30

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.16-5
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.16-4
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Petr Pisar <ppisar@redhat.com> - 0.16-2
- Perl 5.16 rebuild

* Fri Jan 27 2012 Marcela Mašláňová <mmaslano@redhat.com> - 0.16-1
- update to 0.16

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct 16 2011 Iain Arnell <iarnell@gmail.com> 0.14-1
- update to latest upstream version
- clean up spec for modern rpmbuild
- use DESTDIR, not PERL_INSTALL_ROOT

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.10-6
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.10-4
- 661697 rebuild for fixing problems with vendorach/lib

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.10-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.10-2
- rebuild against perl 5.10.1

* Fri Sep 11 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.10-1
- submission

* Fri Sep 11 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.10-0
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.8)

