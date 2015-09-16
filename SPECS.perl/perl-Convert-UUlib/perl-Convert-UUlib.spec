# Filter the Perl extension module
%{?perl_default_filter}

%define pkgname Convert-UUlib

Summary:	Perl interface to the uulib library
Name:		perl-Convert-UUlib
Epoch:		2
Version:	1.5
Release:	1%{?dist}
License:	GPL+ or Artistic
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/%{pkgname}/
Source:		http://search.cpan.org/CPAN/authors/id/M/ML/MLEHMANN/%{pkgname}-%{version}.tar.gz
BuildRequires:	perl(ExtUtils::MakeMaker)
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
A perl interface to the uulib library (a.k.a. uudeview/uuenview).

%prep
%setup -q -n %{pkgname}-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS" < /dev/null
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%check


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes COPYING* README doc/*
%{perl_vendorarch}/Convert
%{perl_vendorarch}/auto/Convert
%{_mandir}/man?/Convert::UUlib*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 2:1.5-1
- 更新到 1.5

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2:1.4-6
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 2:1.4-5
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 2:1.4-4
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 2:1.4-3
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Oct 08 2011 Robert Scheck <robert@fedoraproject.org> 2:1.4-1
- Upgrade to 1.4

* Wed Jun 15 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1:1.34-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.34-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 28 2010 Robert Scheck <robert@fedoraproject.org> 1:1.34-1
- Upgrade to 1.34

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 1:1.33-3
- Rebuild for fixing problems with vendorach/lib (#661697)

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1:1.33-2
- Mass rebuild with perl-5.12.0

* Sun Mar 28 2010 Robert Scheck <robert@fedoraproject.org> 1:1.33-1
- Upgrade to 1.33

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1:1.12-2
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Robert Scheck <robert@fedoraproject.org> 1:1.12-1
- Upgrade to 1.12

* Mon Feb 23 2009 Robert Scheck <robert@fedoraproject.org> 1:1.11-2
- Rebuild against gcc 4.4 and rpm 4.6

* Fri Jul 11 2008 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 1:1.11-1
- Fedora 10 alpha general package cleanup

* Sun May 31 2008 Robert Scheck <robert@fedoraproject.org>
- 1:1.09-5
- Fixed %%check section in order to get the package built

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com>
- 1:1.09-4
- Rebuild for new perl

* Fri Feb 08 2008 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 1:1.09-3
- gcc 4.3 rebuild

* Mon Aug 13 2007 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 1:1.09-2
- Fix License

* Sun Aug 12 2007 Robert Scheck <robert@fedoraproject.org> 1:1.09-1
- Upgrade to 1.09 and rebuilt for EPEL branches (#250865)
- Added build requirement to perl(ExtUtils::MakeMaker)

* Tue Mar 20 2007 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 1:1.08-2
- add perl-devel BR

* Mon Jan 08 2007 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 1.08-1

* Sat Sep 02 2006  Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 1.06-4
- FE6 Rebuild

* Mon Feb 13 2006 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 1.06-3
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 17 2006 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 1.06-2
- bump epoch to force updates

* Mon Jan 16 2006 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 1.06-1
- 1.06 (can't believe I'm still listed as this package owner)

* Thu Jun  2 2005 Paul Howarth <paul@city-fan.org>
- 1.051-2%{?dist}
- add dist tags for ease of syncing with FC-3 & FC-4
- remove redundant perl buildreq
- remove redundant "" from %%build (it's in %%check)
- remove MANIFEST from %%doc

* Sat May 21 2005 Nicolas Mailhot <Nicolas.Mailhot at laPoste.net>
- 1.051-1
- update to 1.051

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Mon Apr 19 2004 Nicolas Mailhot <Nicolas.Mailhot at laPoste.net>
- 0:1.03-0.fdr.1
- Updated to 1.03

* Sun Apr 18 2004 Nicolas Mailhot <Nicolas.Mailhot at laPoste.net>
- 0:1.02-0.fdr.1
- Updated to 1.02

* Sun Apr 18 2004 Nicolas Mailhot <Nicolas.Mailhot at laPoste.net>
- 0:1.01-0.fdr.2
- Merge a few tweaks from 0:0.31-0.fdr.4 (bug #375)

* Sun Apr 18 2004 Nicolas Mailhot <Nicolas.Mailhot at laPoste.net>
- 0:1.01-0.fdr.1
- Fedorization
- Cleanup

* Thu Mar 18 2004 Dag Wieers <dag@wieers.com>
- 1.01-0
- Updated to release 1.01.

* Mon Jul 14 2003 Dag Wieers <dag@wieers.com>
- 0.31-0
- Updated to release 0.31.
- Initial package. (using DAR)
