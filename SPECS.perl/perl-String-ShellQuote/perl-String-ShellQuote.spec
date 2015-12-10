Name:           perl-String-ShellQuote
Version:        1.04
Release:        19%{?dist}
Summary:        Perl module for quoting strings for passing through the shell
# shell-quote:  GPLv2+
# rest:         GPL+ or Artistic
License:        (GPL+ or Artistic) and GPLv2+
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/String-ShellQuote/
Source0:        http://www.cpan.org/authors/id/R/RO/ROSCH/String-ShellQuote-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker)
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
# RS::Handy is never used
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(Carp)
Requires:       perl(Getopt::Long)

%description
This package contains a Perl module and a command line utility which
are useful for quoting strings which are going to pass through the
shell or a shell-like object.

%prep
%setup -q -n String-ShellQuote-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes README
%{_bindir}/shell-quote
%{perl_vendorlib}/String
%{_mandir}/man1/shell-quote.1*
%{_mandir}/man3/String::ShellQuote.3*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 1.04-19
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1.04-18
- 为 Magic 3.0 重建

* Thu Sep 17 2015 Liu Di <liudidi@gmail.com> - 1.04-17
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.04-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.04-15
- Perl 5.22 rebuild

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.04-14
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.04-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 1.04-12
- Perl 5.18 rebuild

* Tue Jul 30 2013 Petr Pisar <ppisar@redhat.com> - 1.04-11
- Add GPLv2+ to the license declaration due to shell-quote(1)
- Specify all dependencies

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 1.04-10
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.04-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Aug 17 2012 Petr Pisar <ppisar@redhat.com> - 1.04-8
- Specify all dependencies

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.04-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1.04-6
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.04-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.04-4
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.04-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.04-2
- 661697 rebuild for fixing problems with vendorach/lib

* Sat Dec 18 2010 Steven Pritchard <steve@kspei.com> 1.04-1
- Update to 1.04.

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.03-9
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.03-8
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.03-5
- rebuild for new perl

* Wed Apr 18 2007 Steven Pritchard <steve@kspei.com> 1.03-4
- Reformat to match cpanspec output.
- Use fixperms macro instead of our own chmod incantation.
- BR ExtUtils::MakeMaker.

* Tue Aug 29 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.03-3
- Fix order of arguments to find(1).
- Drop version from perl build dependency.

* Wed May  4 2005 Ville Skyttä <ville.skytta at iki.fi> - 1.03-2
- 1.03.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Thu Dec 16 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.00-8
- Sync with fedora-rpmdevtools' Perl spec template to fix x86_64 build.

* Thu Sep 11 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.00-0.fdr.7
- Specfile cleanup, using INSTALLDIRS=vendor, PERL_INSTALL_ROOT and
  INSTALLARCHLIB.

* Sun Aug 31 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.00-0.fdr.6
- Get rid of perllocal.pod, .packlist and empty *.bs.
  Some of the files don't exist with this package but I want a good template
  %%install section :)

* Sun Aug 31 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.00-0.fdr.5
- Install into vendor dirs.

* Sun Jul 13 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.00-0.fdr.4
- Update description.
- Small spec cleanups.

* Sun May  4 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.00-0.fdr.3
- Own more dirs.

* Sun Apr 13 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.00-0.fdr.2
- Save .spec in UTF-8.

* Sat Mar 22 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.00-0.fdr.1
- Update to current Fedora guidelines.

* Fri Feb  7 2003 Ville Skyttä <ville.skytta at iki.fi> - 1.00-1.fedora.1
- First Fedora release.
