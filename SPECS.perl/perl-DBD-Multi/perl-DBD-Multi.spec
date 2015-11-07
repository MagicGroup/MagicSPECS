Name:       perl-DBD-Multi 
Version:	0.18
Release:	2%{?dist}
# see Makefile.PL
License:    GPL+ or Artistic 
Group:      Development/Libraries
Summary:    DB Proxy with fail-over and load balancing 
Source:     http://search.cpan.org/CPAN/authors/id/D/DW/DWRIGHT/DBD-Multi-%{version}.tar.gz 
Url:        http://search.cpan.org/dist/DBD-Multi
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 
Requires:   perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:  noarch

BuildRequires: perl(ExtUtils::MakeMaker) 
BuildRequires: perl(Class::Accessor::Fast) >= 0.19
BuildRequires: perl(DBD::SQLite) >= 1.09
BuildRequires: perl(DBI)
BuildRequires: perl(List::Util) >= 1.18
BuildRequires: perl(Pod::Simple)
BuildRequires: perl(Sys::SigAction) >= 0.1
BuildRequires: perl(Test::Exception) >= 0.21
BuildRequires: perl(Test::More)
BuildRequires: perl(Test::Pod) >= 1.14
BuildRequires: perl(Test::Pod::Coverage) >= 1.04

# not picked up due to 'use base'
Requires:      perl(Class::Accessor::Fast) >= 0.19

%description
This software manages multiple database connections for fail-overs and also
simple load balancing. It acts as a proxy between your code and your
database connections, transparently choosing a connection for each query,
based on your preferences and present availability of the DB server.

%prep
%setup -q -n DBD-Multi-%{version}

%{__perl} -pi -e 's|^#!perl|#!%{__perl}|' t/*.t

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'

%{_fixperms} %{buildroot}/*

%check


%clean
rm -rf %{buildroot} 

%files
%defattr(-,root,root,-)
%doc Changes README t/ 
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.18-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.18-1
- 更新到 0.18

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.16-15
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.16-14
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.16-13
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.16-12
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.16-11
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.16-10
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.16-9
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.16-8
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.16-7
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.16-6
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.16-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.16-2
- 661697 rebuild for fixing problems with vendorach/lib

* Wed Sep 08 2010 Petr Pisar <ppisar@redhat.com> - 0.16-1
- 0.16 bump (bug #631224)
- Correct spelling

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.14-6
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.14-5
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Oct 15 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.14-2
- bump

* Sun Oct 05 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.14-1
- initial Fedora packaging
- generated with cpan2dist (CPANPLUS::Dist::Fedora version 0.0.1)

