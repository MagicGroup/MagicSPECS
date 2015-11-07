Name:           perl-ExtUtils-PkgConfig
Version:	1.15
Release:	2%{?dist}
Summary:        Simplistic interface to pkg-config

Group:          Development/Libraries
License:        LGPLv2+
URL:            http://search.cpan.org/dist/ExtUtils-PkgConfig/
Source0:        http://search.cpan.org/CPAN/authors/id/X/XA/XAOC/ExtUtils-PkgConfig-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  pkgconfig
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       pkgconfig

%description
The pkg-config program retrieves information about installed libraries,
usually for the purposes of compiling against and linking to them.

ExtUtils::PkgConfig is a very simplistic interface to this utility,
intended for use in the Makefile.PL of perl extensions which bind
libraries that pkg-config knows. It is really just boilerplate code
that you would've written yourself.


%prep
%setup -q -n ExtUtils-PkgConfig-%{version}


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
%{perl_vendorlib}/ExtUtils/
%{_mandir}/man3/*.3pm*


%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1.15-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.15-1
- 更新到 1.15

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.12-16
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.12-15
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.12-14
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 1.12-12
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.12-10
- Perl mass rebuild

* Thu Jun 09 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.12-9
- Perl 5.14 mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.12-7
- 661697 rebuild for fixing problems with vendorach/lib

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.12-6
- Mass rebuild with perl-5.12.0

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.12-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.12-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 19 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.12-1
- Upstream update.

* Wed Jul 09 2008 Ralf Corsépius <rc040203@freenet.de> - 1.11-1
- Upstream update.
- Reflect Source0-URL having changed.

* Sat Feb  2 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.08-2
- rebuild for new perl

* Fri Nov 30 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.08-1
- 1.08

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.07-5.2
- add BR: perl(Test::More)

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.07-5.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Sat Sep  9 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.07-5
- Rebuild for FC6.

* Fri Feb 17 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.07-4
- Rebuild for FC5 (perl 5.8.8).

* Thu Dec 29 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.07-3
- Dist tag.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.07-2
- rebuilt

* Tue Feb 15 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.07-1
- Update to 1.07.

* Sun Oct  3 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.06-0.fdr.1
- Update to 1.06.

* Sun Jul 18 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.05-0.fdr.1
- First build.
