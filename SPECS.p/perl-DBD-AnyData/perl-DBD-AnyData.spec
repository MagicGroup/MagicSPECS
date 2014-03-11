Name:           perl-DBD-AnyData
Summary:        DBI access to XML, CSV and other formats 
Version:        0.110
Release:        7%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/R/RE/REHSACK/DBD-AnyData-%{version}.tar.gz 
URL:            http://search.cpan.org/dist/DBD-AnyData
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:      noarch

BuildRequires:  perl(AnyData) >= 0.07
BuildRequires:  perl(DBI) >= 1.611
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Module::Build) >= 0.36
BuildRequires:  perl(Params::Util) >= 1.00
BuildRequires:  perl(SQL::Statement) >= 1.27
BuildRequires:  perl(Test::More) >= 0.9

Requires:       perl(AnyData) >= 0.07
Requires:       perl(DBI) >= 1.611_93
Requires:       perl(Params::Util) >= 1.00
Requires:       perl(SQL::Statement) >= 1.27


%{?perl_default_filter}
%{?perl_default_subpackage_tests}

%description
The DBD::AnyData module provides a DBI (Perl Database Interface) and SQL 
(Structured Query Language) interface to data in many formats and from many 
sources.

%prep
%setup -q -n DBD-AnyData-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%check


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/DBD/*
%{_mandir}/man3/*.3*


%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.110-7
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.110-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 18 2012 Petr Pisar <ppisar@redhat.com> - 0.110-5
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.110-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.110-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.110-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 17 2010 Marcela Mašláňová <mmaslano@redhat.com> 0.110-1
- update by Fedora::App::MaintainerTools 0.006
- updating to latest GA CPAN version (0.110)
- added a new br on perl(AnyData) (version 0.07)
- added a new br on perl(DBI) (version 1.611_93)
- added a new br on perl(Module::Build) (version 0.36)
- added a new br on perl(Params::Util) (version 1.00)
- added a new br on perl(SQL::Statement) (version 1.27_02)
- altered br on perl(Test::More) (0 => 0.9)
- force-adding ExtUtils::MakeMaker as a BR
- dropped old BR on perl(DBI),
- added a new req on perl(AnyData) (version 0.07)
- added a new req on perl(DBI) (version 1.611_93)
- added a new req on perl(Params::Util) (version 1.00)
- added a new req on perl(SQL::Statement) (version 1.27_02)

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.09-8
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.09-7
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.09-6
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.09-3
- Rebuild for perl 5.10 (again)

* Mon Jan 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.09-2
- rebuild for new perl

* Fri Aug 24 2007 Tom "spot" Callaway <tcallawa@redhat.com> 0.09-1
- bump to 0.09
- license fix

* Fri Sep 15 2006 Tom "spot" Callaway <tcallawa@redhat.com> 0.08-3
- bump for fc6

* Fri Mar 31 2006 Tom "spot" Callaway <tcallawa@redhat.com> 0.08-2
- minor cleanups

* Fri Jan  6 2006 Tom "spot" Callaway <tcallawa@redhat.com> 0.08-1
- Initial package for Fedora Extras
