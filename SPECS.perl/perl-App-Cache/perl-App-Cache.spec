Name:           perl-App-Cache
Summary:        Easy application-level caching
Summary(zh_CN.UTF-8): 易用的应用程序级别缓存
Version:        0.37
Release:        18%{?dist}
License:        GPL+ or Artistic

Source0:        http://search.cpan.org/CPAN/authors/id/L/LB/LBROCARD/App-Cache-%{version}.tar.gz 
URL:            http://search.cpan.org/dist/App-Cache

Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:      noarch

BuildRequires:  perl(Class::Accessor::Chained::Fast)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Find::Rule)
BuildRequires:  perl(File::HomeDir)
BuildRequires:  perl(File::stat)
BuildRequires:  perl(HTTP::Cookies)
BuildRequires:  perl(LWP::UserAgent)
BuildRequires:  perl(Path::Class)
BuildRequires:  perl(Storable)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)

Requires:       perl(Class::Accessor::Chained::Fast)
Requires:       perl(File::Find::Rule)
Requires:       perl(File::HomeDir)
Requires:       perl(File::stat)
Requires:       perl(HTTP::Cookies)
Requires:       perl(LWP::UserAgent)
Requires:       perl(Path::Class)
Requires:       perl(Storable)


%{?perl_default_filter}
#{?perl_default_subpackage_tests}

%description
The App::Cache module lets an application cache data locally. There are a
few times an application would need to cache data: when it is retrieving
information from the network or when it has to complete a large calculation.
For example, the Parse::BACKPAN::Packages module downloads a file off the
net and parses it, creating a data structure. Only then can it actually
provide any useful information for the programmer. Parse::BACKPAN::Packages
uses App::Cache to cache both the file download and data structures,
providing much faster use when the data is cached. This module stores data
in the home directory of the user, in a dot directory. For example, the
Parse::BACKPAN::Packages cache is actually stored underneath
"~/.parse_backpan_packages/cache/". This is so that permissions are not a
problem -- it is a per-user, per-application cache.

%description -l zh_CN.UTF-8
易用的应用程序级别缓存。

%prep
%setup -q -n App-Cache-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'

%{_fixperms} %{buildroot}/*
magic_rpm_clean.sh

%check
make test

%files
%doc CHANGES README
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.37-18
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.37-17
- 为 Magic 3.0 重建

* Thu Apr 23 2015 Liu Di <liudidi@gmail.com> - 0.37-16
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.37-15
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.37-14
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.37-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.37-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 31 2013 Petr Pisar <ppisar@redhat.com> - 0.37-11
- Perl 5.18 rebuild

* Sun Feb 24 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 0.37-10
- Remove no-longer-needed macros
- Fix a spelling mistake in the package description

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.37-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.37-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Petr Pisar <ppisar@redhat.com> - 0.37-7
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.37-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.37-5
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.37-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.37-3
- 661697 rebuild for fixing problems with vendorach/lib

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.37-2
- Mass rebuild with perl-5.12.0

* Sat Feb 27 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.37-1
- update by Fedora::App::MaintainerTools 0.004
- PERL_INSTALL_ROOT => DESTDIR
- dropped old BR on perl(Test::Pod::Coverage)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.36-2
- rebuild against perl 5.10.1

* Sat Aug 08 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.36-1
- auto-update to 0.36 (by cpan-spec-update 0.01)
- added a new req on perl(File::Find::Rule) (version 0)
- added a new req on perl(File::HomeDir) (version 0)
- added a new req on perl(File::stat) (version 0)
- added a new req on perl(HTTP::Cookies) (version 0)
- added a new req on perl(LWP::UserAgent) (version 0)
- added a new req on perl(Path::Class) (version 0)
- added a new req on perl(Storable) (version 0)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.35-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Mar 05 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.35-1
- submission

* Thu Mar 05 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.35-0
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.8)
