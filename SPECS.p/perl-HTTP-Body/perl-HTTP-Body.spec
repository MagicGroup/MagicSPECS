Name:           perl-HTTP-Body
Summary:        HTTP Body Parser
Version:        1.07
Release:        9%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/M/MR/MRAMBERG/HTTP-Body-%{version}.tar.gz 
URL:            http://search.cpan.org/dist/HTTP-Body
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:      noarch

BuildRequires:  perl(Carp)
BuildRequires:  perl(Digest::MD5)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.42
BuildRequires:  perl(File::Temp) >= 0.14
BuildRequires:  perl(HTTP::Headers)
BuildRequires:  perl(IO::File) >= 1.14
BuildRequires:  perl(Test::Deep)
BuildRequires:  perl(Test::More) >= 0.86
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)

Requires:       perl(File::Temp) >= 0.14
Requires:       perl(IO::File) >= 1.14

%{?perl_default_filter}

%description
A perl module for parsing the MultiPart, OctetStream, and UrlEncoded 
parts of an HTTP Body.

%prep
%setup -q -n HTTP-Body-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
%{_fixperms} $RPM_BUILD_ROOT/*

%check
 TEST_POD=1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/HTTP/
%{_mandir}/man3/*.3*


%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.07-9
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.07-8
- 为 Magic 3.0 重建

* Tue Jan 17 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.07-7
- Add BR: perl(Digest::MD5) (Fix mass rebuild FTBFS).

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.07-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.07-5
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.07-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 17 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.07-3
- 661697 rebuild for fixing problems with vendorach/lib

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.07-2
- Mass rebuild with perl-5.12.0

* Wed Mar 03 2010 Chris Weyl <cweyl@alumni.drew.edu> 1.07-1
- Plack requires >= 1.06 of this package
- update by Fedora::App::MaintainerTools 0.004
- updating to latest GA CPAN version (1.07)
- PERL_INSTALL_ROOT => DESTDIR
- added a new br on perl(ExtUtils::MakeMaker) (version 6.42)
- added a new br on perl(HTTP::Headers) (version 0)
- altered br on perl(IO::File) (0 => 1.14)
- added a new br on perl(Test::Deep) (version 0)
- altered br on perl(Test::More) (0 => 0.86)
- dropped old BR on perl(YAML)
- added a new req on perl(File::Temp) (version 0.14)
- added a new req on perl(IO::File) (version 1.14)
- dropped old requires on perl(YAML)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.05-5
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 06 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.05-1
- update to 1.05

* Thu Nov 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.04-1
- update to 1.04

* Sun Feb  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.9-4
- disable tests due to wacky ppc builders

* Sat Feb  2 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.9-3
- rebuild for new perl

* Sun Aug 26 2007 Tom "spot" Callaway <tcallawa@redhat.com> 0.9-2
- license tag fix

* Sun Apr 29 2007 Tom "spot" Callaway <tcallawa@redhat.com> 0.9-1
- bump to 0.9

* Thu Sep 14 2006 Tom "spot" Callaway <tcallawa@redhat.com> 0.6-3
- add TEST_POD=1 to 

* Mon Sep 11 2006 Tom "spot" Callaway <tcallawa@redhat.com> 0.6-2
- enhance description
- add missing BR
- remove unnecessary Requires

* Thu Aug  3 2006 Tom "spot" Callaway <tcallawa@redhat.com> 0.6-1
- initial package for Fedora Extras
