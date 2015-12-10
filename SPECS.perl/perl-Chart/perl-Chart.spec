Name:           perl-Chart
Version:	2.4.10
Release:	3%{?dist}
Summary:        Series of charting modules
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Chart/
Source0:        http://www.cpan.org/authors/id/C/CH/CHARTGRP/Chart-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(GD)
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This module is an attempt to build a general purpose graphing module that
is easily modified and expanded.  Chart uses Lincoln Stein's GD module for
all of its graphics primitives calls.

%prep
%setup -q -n Chart-%{version}
chmod -c 644 Chart/*.pm TODO Documentation.pdf
rm -f pm_to_blib

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
rm -rf t/{mountain.t,mountain_2.t}


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README TODO Documentation.pdf
%{perl_vendorlib}/Chart*
%{_mandir}/man3/Chart.3*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 2.4.10-3
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 2.4.10-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 2.4.10-1
- 更新到 2.4.10

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.4.2-11
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.4.2-10
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 2.4.2-9
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 2.4.2-8
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 2.4.2-7
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 2.4.2-6
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.4.2-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.4.2-2
- 661697 rebuild for fixing problems with vendorach/lib

* Sun Dec 12 2010 Steven Pritchard <steve@kspei.com> 2.4.2-1
- Update to 2.4.2.
- Improve Summary and description.
- Use PERL_INSTALL_ROOT instead of DESTDIR while installing.

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.4.1-10
- Mass rebuild with perl-5.12.0
- remove two tests failing

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 2.4.1-9
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.4.1-6
- Rebuild for new perl

* Mon Apr 09 2007 Steven Pritchard <steve@kspei.com> 2.4.1-5
- Fix find option order.
- Use fixperms macro instead of our own chmod incantation.
- BR ExtUtils::MakeMaker.
- Minor spec cleanup to more closely resemble cpanspec output.

* Mon Aug 27 2006 Michael J. Knox <michael[AT]knox.net.nz> - 2.4.1-4
- Rebuild for FC6

* Mon May 29 2006 Michael J. Knox <michael[AT]knox.net.nz> - 2.4.1-3
- rebuilt and reimported in to devel

* Wed Jan 25 2006 Ville Skyttä <ville.skytta at iki.fi> - 2.4.1-1
- 2.4.1.
- Don't ship rgb.txt in docs.
- Specfile cleanups.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 2.3-3
- rebuilt

* Sun Jul 11 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:2.3-2
- Bring up to date with current fedora.us Perl Spec template.

* Thu Jan 15 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:2.3-0.fdr.1
- Update to 2.3.
- Fix file permissions.

* Sat Oct 11 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.2-0.fdr.1
- First build.
