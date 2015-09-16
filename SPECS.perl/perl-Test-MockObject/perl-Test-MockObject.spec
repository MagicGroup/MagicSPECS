Name:           perl-Test-MockObject
Version:	1.20150527
Release:	1%{?dist}
Summary:        Perl extension for emulating troublesome interfaces

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Test-MockObject/
Source0:        http://www.cpan.org/authors/id/C/CH/CHROMATIC/Test-MockObject-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(CGI)
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Test::Exception)
BuildRequires:  perl(Test::Pod), perl(Test::Pod::Coverage)
BuildRequires:  perl(UNIVERSAL::can) >= 1.11
BuildRequires:  perl(UNIVERSAL::isa) >= 0.06
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Test::MockObject is a highly polymorphic testing object, capable of
looking like all sorts of objects.  This makes white-box testing much
easier, as you can concentrate on what the code being tested sends to
and receives from the mocked object, instead of worrying about faking
up your own data.  (Another option is not to test difficult things.
Now you have no excuse.)

%prep
%setup -q -n Test-MockObject-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} ';' 2>/dev/null
%{_fixperms} %{buildroot}

%check
PERL_RUN_ALL_TESTS=1 make test

%files
%doc Changes README
%{perl_vendorlib}/Test/
%{_mandir}/man3/*.3pm*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.20150527-1
- 更新到 1.20150527

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.09-20
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.09-19
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.09-18
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.09-17
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.09-16
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.09-15
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.09-14
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.09-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 14 2012 Petr Pisar <ppisar@redhat.com> - 1.09-12
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.09-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.09-10
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.09-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.09-8
- 661697 rebuild for fixing problems with vendorach/lib

* Thu Dec 09 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.09-7
- Add BR: perl(CGI) (Fix FTBFS: BZ 660972).

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.09-6
- Mass rebuild with perl-5.12.0

* Thu Feb  4 2010 Marcela Mašláňová <mmaslano@redhat.com> - 1.09-5
- 552253 merge review

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1.09-4
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.09-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.09-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Nov 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.09-1
- update to 1.09

* Wed Mar 05 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.08-2
- rebuild for new perl

* Fri Jun 29 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.08-1
- Update to 1.08.

* Thu Oct  5 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.07-1
- Update to 1.07.

* Fri Apr 21 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.06-1
- Update to 1.06.

* Tue Apr 11 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.05-1
- Update to 1.05.

* Thu Mar 30 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.04-1
- Update to 1.04.
- Makefile.PL -> Build.PL.

* Mon Mar 13 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.03-1
- Update to 1.03.

* Tue Feb 28 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.02-1
- Update to 1.02.

* Fri Jul 15 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.00-1
- Update to 1.00.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0:0.15-3
- rebuilt

* Tue Dec 28 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:0.15-2
- Build requires Test::Simple >= 0.44 (bug 2324).

* Wed Dec 01 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:0.15-0.fdr.1
- Update to 0.15.

* Tue May 25 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:0.14-0.fdr.1
- Update to 0.14.
- Require perl >= 1:5.6.1 for vendor install dir support.
- Use pure_install to avoid perllocal.pod workarounds.
- Moved  to section %%check.

* Wed Nov 19 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.12-0.fdr.1
- First build.
