Name:           perl-Log-Dispatch-Config
Summary:        Log4j for Perl        
Version:	1.04
Release:	2%{?dist}
License:        GPL+ or Artistic        
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/M/MI/MIYAGAWA/Log-Dispatch-Config-%{version}.tar.gz 
URL:            http://search.cpan.org/dist/Log-Dispatch-Config
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:      noarch

BuildRequires:  perl(AppConfig) >= 1.52
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Temp) >= 0.12
BuildRequires:  perl(IO::Scalar)
BuildRequires:  perl(Log::Dispatch) >= 2
BuildRequires:  perl(Test::More) >= 0.32

Requires:       perl(AppConfig) >= 1.52
Requires:       perl(File::Temp) >= 0.12
Requires:       perl(IO::Scalar)
Requires:       perl(Log::Dispatch) >= 2


%{?perl_default_filter}
#{?perl_default_subpackage_tests}

%description
Log::Dispatch::Config is a subclass of Log::Dispatch and provides a way to
configure Log::Dispatch object with configuration file (default, in AppConfig
format).

%prep
%setup -q -n Log-Dispatch-Config-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find %{buildroot} -type d -depth -exec rmdir {} 2>/dev/null ';'
%{_fixperms} %{buildroot}/*


%check



%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*


%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1.04-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.04-1
- 更新到 1.04

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.03-22
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.03-21
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.03-20
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.03-19
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.03-18
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.03-17
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.03-16
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.03-15
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.03-14
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.03-13
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.03-12
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.03-11
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.03-10
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.03-9
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.03-8
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.03-7
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 1.03-5
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.03-3
- 661697 rebuild for fixing problems with vendorach/lib

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.03-2
- Mass rebuild with perl-5.12.0

* Sun Mar 14 2010 Chris Weyl <cweyl@alumni.drew.edu> 1.03-1
- update by Fedora::App::MaintainerTools 0.006
- PERL_INSTALL_ROOT => DESTDIR
- updating to latest GA CPAN version (1.03)
- added a new br on perl(File::Temp) (version 0.12)
- altered br on perl(Log::Dispatch) (2.00 => 2)
- altered br on perl(Test::More) (0 => 0.32)
- added a new req on perl(AppConfig) (version 1.52)
- added a new req on perl(File::Temp) (version 0.12)
- added a new req on perl(IO::Scalar) (version 0)
- added a new req on perl(Log::Dispatch) (version 2)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.02-5
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.02-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.02-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.02-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Oct 25 2008 Chris Weyl <cweyl@alumni.drew.edu> 1.02-1
- update to 1.02

* Thu Mar  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.01-3
- rebuild for new perl

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.01-2.2
- add BR: perl(Test::More)

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.01-2.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Thu Aug 31 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.01-2
- bump for mass rebuild

* Sat Jul  8 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.01-1
- bump for f-e release/build

* Fri Jul 07 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.01-0
- Initial spec file for F-E
