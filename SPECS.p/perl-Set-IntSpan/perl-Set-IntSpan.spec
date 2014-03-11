Name:           perl-Set-IntSpan
Version:        1.16
Release:        6%{?dist}
Summary:        Perl module for managing sets of integers

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Set-IntSpan/
Source0:        http://www.cpan.org/authors/id/S/SW/SWMCD/Set-IntSpan-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Set::IntSpan manages sets of integers. It is optimized for sets that
have long runs of consecutive integers.


%prep
%setup -q -n Set-IntSpan-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*


%check
make test


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/Set/
%{_mandir}/man3/Set::IntSpan.3*


%changelog
* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1.16-5
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.16-3
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 06 2010 Ralf Corsépius <rc040203@freenet.de>  - 1.16-1
- Upstream update.

* Tue Jul 20 2010 Ralf Corsépius <rc040203@freenet.de>  - 1.14-1
- Upstream update.

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.13-6
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.13-5
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.13-2
- rebuild for new perl

* Tue Oct 30 2007 Ralf Corsépius <rc040203@freenet.de>  - 1.13.1
- Upstream update.

* Mon Sep 10 2007 Ralf Corsépius <rc040203@freenet.de>  - 1.12.1
- Upstream update.

* Mon Aug  6 2007 Ville Skyttä <ville.skytta at iki.fi> - 1.11-2
- License: GPL+ or Artistic

* Sun Mar 25 2007 Ville Skyttä <ville.skytta at iki.fi> - 1.11-1
- 1.11.

* Sun Mar 11 2007 Ville Skyttä <ville.skytta at iki.fi> - 1.10-2
- BuildRequire perl(ExtUtils::MakeMaker).

* Sun Mar  4 2007 Ville Skyttä <ville.skytta at iki.fi> - 1.10-1
- 1.10.

* Mon Aug 28 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.09-2
- Fix order of arguments to find(1).

* Wed Dec 14 2005 Ville Skyttä <ville.skytta at iki.fi> - 1.09-1
- 1.09.

* Sun Oct 16 2005 Ville Skyttä <ville.skytta at iki.fi> - 1.08-1
- 1.08 (#170944).
- Specfile cleanups.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.07-6
- rebuilt

* Sun May  9 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.07-0.fdr.5
- BuildRequire perl >= 1:5.6.1-34.99.6 for support for vendor installdirs.
- Use pure_install to avoid perllocal.pod workarounds.

* Sun Apr 25 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.07-0.fdr.4
- Require perl(:MODULE_COMPAT_*).

* Mon Feb  2 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.07-0.fdr.3
- Reduce directory ownership bloat.

* Tue Dec  2 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.07-0.fdr.2
- Install into vendor dirs.
- Remove #---- section markers.

* Wed May  7 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.07-0.fdr.1
- First Fedora release.

* Thu Oct  3 2002 Ville Skyttä <ville.skytta at iki.fi> 1.07-2cr
- Rebuild for Red Hat 8.0.

* Sat Jul  6 2002 Ville Skyttä <ville.skytta@iki.fi> 1.07-1cr
- Initial build.
