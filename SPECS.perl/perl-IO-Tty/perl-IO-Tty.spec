Name:           perl-IO-Tty
Version:	1.13_01
Release:	2%{?dist}
Summary:        Perl interface to pseudo tty's

License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/IO-Tty/
Source0:        http://www.cpan.org/authors/id/T/TO/TODDR/IO-Tty-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

# don't "provide" private Perl libs
%global _use_internal_dependency_generator 0
%global __deploop() while read FILE; do /usr/lib/rpm/rpmdeps -%{1} ${FILE}; done | /bin/sort -u
%global __find_provides /bin/sh -c "%{__grep} -v '%_docdir' | %{__grep} -v '%{perl_vendorarch}/.*\\.so$' | %{__deploop P}"
%global __find_requires /bin/sh -c "%{__grep} -v '%_docdir' | %{__deploop R}"

%description
IO::Tty and IO::Pty provide an interface to pseudo tty's.


%prep
%setup -q -n IO-Tty-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
%{_fixperms} $RPM_BUILD_ROOT/*


%check
##


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc ChangeLog README
%{perl_vendorarch}/auto/IO/
%{perl_vendorarch}/IO/
%{_mandir}/man3/*.3pm*


%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1.13_01-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.13_01-1
- 更新到 1.13_01

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.10-9
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.10-8
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 1.10-6
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.10-4
- Perl mass rebuild

* Thu Jun 09 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.10-3
- Perl 5.14 mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 28 2010 Steven Pritchard <steve@kspei.com> 1.10-1
- Update to 1.10.
- Use fixperms macro instead of our own chmod incantation.
- Update Source0 URL.
- BR Test::More.

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.08-6
- 661697 rebuild for fixing problems with vendorach/lib

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.08-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.08-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.08-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 16 2009 Chris Weyl <cweyl@alumni.drew.edu> - 1.08-2
- filter out private Perl .so provides

* Wed Feb 25 2009 Paul Howarth <paul@city-fan.org> - 1.08-1
- Update to 1.08 (add support for posix_openpt())
- Fix argument order for find with -depth

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.07-5
- Rebuild for perl 5.10 (again)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.07-4
- Autorebuild for GCC 4.3

* Mon Jan 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.07-3
- rebuild for new perl

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.07-2.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Sun Sep 10 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.07-2
- Rebuild for FC6.

* Fri Jul 21 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.07-1
- Update to 1.07.

* Tue Jul 18 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.06-1
- Update to 1.06.

* Sat Jun 10 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.05-1
- Update to 1.05.

* Wed May 31 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.04-1
- Update to 1.04.

* Tue May  9 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.03-1
- Update to 1.03.
- Taking maintainership.

* Tue Feb 14 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.02-5
- Rebuild.

* Tue Jan 17 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.02-4
- Rebuild, cosmetic cleanups.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.02-3
- rebuilt

* Sun Feb  1 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.02-0.fdr.2
- Reduce directory ownership bloat.

* Fri Nov 21 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.02-0.fdr.1
- First build.
