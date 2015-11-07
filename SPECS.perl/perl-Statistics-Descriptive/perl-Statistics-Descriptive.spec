Name:           perl-Statistics-Descriptive
Version:	3.0609
Release:	2%{?dist}
Summary:        Perl module of basic descriptive statistical functions
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Statistics-Descriptive/
Source0:        http://www.cpan.org/authors/id/S/SH/SHLOMIF/Statistics-Descriptive-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
This module provides basic functions used in descriptive statistics. It has
an object oriented design and supports two different types of data storage
and calculation objects: sparse and full. With the sparse method, none of
the data is stored and only a few statistical measures are available. Using
the full method, the entire data set is retained and additional functions
are available.

%prep
%setup -q -n Statistics-Descriptive-%{version}

%build
%{__perl} Build.PL installdirs=vendor
./Build

%install
./Build install destdir=$RPM_BUILD_ROOT create_packlist=0

%{_fixperms} $RPM_BUILD_ROOT/*

%check
./Build test

%files
%doc Changes examples README UserSurvey.txt
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 3.0609-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 3.0609-1
- 更新到 3.0609

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 3.0604-7
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 3.0604-6
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 3.0604-5
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 3.0604-4
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 3.0604-3
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 3.0604-2
- 为 Magic 3.0 重建

* Sun Jul 29 2012 Iain Arnell <iarnell@gmail.com> 3.0604-1
- update to latest upstream version

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0603-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 3.0603-2
- Perl 5.16 rebuild

* Fri May 18 2012 Iain Arnell <iarnell@gmail.com> 3.0603-1
- update to latest upstream version

* Fri Mar 02 2012 Iain Arnell <iarnell@gmail.com> 3.0400-1
- update to latest upstream version

* Tue Feb 21 2012 Iain Arnell <iarnell@gmail.com> 3.0300-1
- update to latest upstream version

* Fri Jan 06 2012 Iain Arnell <iarnell@gmail.com> 3.0203-1
- update to latest upstream version

* Tue Jul 26 2011 Iain Arnell <iarnell@gmail.com> 3.0202-1
- update to latest upstream

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 3.0201-3
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0201-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 03 2010 Iain Arnell <iarnell@gmail.com> 3.0201-1
- update to latest upstream
- clean up spec for modern rpmbuild

* Wed Jun 23 2010 Iain Arnell <iarnell@gmail.com> 3.0200-1
- update to latest upstream

* Wed Jun 16 2010 Iain Arnell <iarnell@gmail.com> 3.0101-1
- update to latest upstream

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 3.0100-2
- Mass rebuild with perl-5.12.0

* Sat May 01 2010 Iain Arnell <iarnell@gmail.com> 3.0100-1
- update to latest upstream

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 2.6-6
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.6-3
- rebuild for new perl

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 2.6-2.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Tue Aug 29 2006 Patrice Dumas <pertusus at free.fr> - 2.6-2
- Rebuild for FC6

* Fri Jul 14 2006 Patrice Dumas <pertusus at free.fr> - 2.6-1
- Submit to Fedora Extras.

* Mon Mar 27 2006 Ville Skyttä <ville.skytta at iki.fi> - 2.6-0.2
- Rebuild.

* Fri Jun  3 2005 Ville Skyttä <ville.skytta at iki.fi> - 2.6-0.1
- Rebuild for FC4.

* Sat Jun 12 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:2.6-0.fdr.2
- Bring up to date with current fedora.us Perl spec template.

* Mon Oct 13 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.6-0.fdr.1
- First build.
