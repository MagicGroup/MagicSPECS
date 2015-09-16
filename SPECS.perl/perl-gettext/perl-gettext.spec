Name:           perl-gettext
Version:        1.05
Release:        35%{?dist}
Summary:        Interface to gettext family of functions

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/gettext/
Source0:        http://search.cpan.org/CPAN/authors/id/P/PV/PVANDRY/gettext-%{version}.tar.gz
Patch0:         http://patch-tracking.debian.net/patch/series/view/liblocale-gettext-perl/1.05-4/compatibility-with-POSIX-module.diff

BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	gettext
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
# Encode is optional
# Tests:
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Test)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

Obsoletes:	perl-Locale-gettext <= 1.05

%{?perl_default_filter}

%description
The gettext module permits access from perl to the gettext() family of 
functions for retrieving message strings from databases constructed to
internationalize software.

%prep
%setup -q -n gettext-%{version}
%patch0 -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}


%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*


%check
unset LC_MESSAGES
case "$LANG" in
''|'C'|'POSIX' ) 
  export LANG=en_US.UTF-8;;
esac
make test


%files
%defattr(-,root,root,-)
%doc README
%{perl_vendorarch}/auto/Locale
%{perl_vendorarch}/Locale
%{_mandir}/man3/*.3*


%changelog
* Wed Sep 16 2015 Liu Di <liudidi@gmail.com> - 1.05-35
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.05-33
- Perl 5.22 rebuild

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.05-32
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.05-28
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 07 2012 Petr Pisar <ppisar@redhat.com> - 1.05-25
- Perl 5.16 rebuild
- Specify all dependencies

* Sun Jan 22 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.05-24
- Add %%{?perl_default_filter}.
- Modernize spec.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.05-22
- Perl mass rebuild

* Thu Jun 09 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.05-21
- Perl 5.14 mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.05-19
- 661697 rebuild for fixing problems with vendorach/lib

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.05-18
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.05-17
- rebuild against perl 5.10.1

* Mon Jul 27 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.05-16
- Adopt Debian's compatibility-with-POSIX-module.diff (RH BZ#447859).

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Mar 05 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.05-13
- rebuild for new perl

* Sun Feb 10 2008 Ralf Corsépius <rc040203@freenet.de> - 1.05-12
- Rebuild for gcc43.

* Fri Aug 17 2007 Ralf Corsépius <rc040203@freenet.de> - 1.05-11
- Update license tag.

* Thu Apr 19 2007 Ralf Corsépius <rc040203@freenet.de> - 1.05-10
- Reflect perl package split.

* Tue Sep 05 2006 Ralf Corsépius <rc040203@freenet.de> - 1.05-9
- Mass rebuild.

* Mon Feb 20 2006 Ralf Corsépius <rc040203@freenet.de> - 1.05-8
- Rebuild.

* Wed Nov 02 2005 Ralf Corsepius <rc040203@freenet.de> - 1.05-7
- Work-around to "make test" not supporting LC_MESSAGES=POSIX.

* Wed Nov 02 2005 Ralf Corsepius <rc040203@freenet.de> - 1.05-6
- Obsoletes: perl-Locale-gettext <= 1.05.
- Fix minor spec file typos.

* Tue Nov 01 2005 Ralf Corsepius <rc040203@freenet.de> - 1.05-5
- FE import.
- Add Obsoletes: perl-Locale-gettext.

* Tue Nov 01 2005 Ralf Corsepius <rc040203@freenet.de> - 1.05-4
- Rename package to perl-gettext.
- Remove "Require: perl".

* Mon Aug 20 2005 Ralf Corsepius <ralf@links2linux.de> - 1.05-3
- Add Provides: perl-gettext (RH bugzilla PR 165885).

* Tue Aug 09 2005 Ralf Corsepius <ralf@links2linux.de> - 1.05-2
- Add BuildRequires: gettext.

* Sun Aug 07 2005 Ralf Corsepius <ralf@links2linux.de> - 1.05-1
- FE submission.

* Thu Aug 04 2005 Ralf Corsepius <ralf@links2linux.de> - 1.05-0
- Initial rpm.
