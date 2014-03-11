Name:           perl-Mail-Alias
Version:        1.12
Release:        20%{?dist}
Summary:        Module for manipulating e-mail alias files
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Mail-Alias/
Source0:        http://www.cpan.org/authors/id/Z/ZE/ZELT/Mail-Alias-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This module allows direct manipulation of various types of E-Mail
Alias files. The primary use of Mail::Alias is for manipulating alias
files in the SENDMAIL alias file format. Additionally it is possible
to read some other formats and to convert between various alias file
formats.

%prep
%setup -q -n Mail-Alias-%{version}

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


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.12-20
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.12-19
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.12-17
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 27 2011 Oliver Falk <oliver@linux-kernel.at> - 1.12-15
- Rebuild for new perl-5.12.3

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.12-14
- 661697 rebuild for fixing problems with vendorach/lib

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.12-13
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.12-12
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.12-9
Rebuild for new perl

* Wed Apr 18 2007 Steven Pritchard <steve@kspei.com> 1.12-8
- Remove check macro cruft.
- Reformat to match cpanspec output.
- Fix URL and Source0.
- Use _fixperms macro.
- BR ExtUtils::MakeMaker.

* Tue Sep 26 2006 Steven Pritchard <steve@kspei.com> 1.12-7
- Fix find option order.

* Thu Aug 11 2005 Oliver Falk <oliver@linux-kernel.at>		- 1.12-6
- Fix license

* Thu Aug 11 2005 Oliver Falk <oliver@linux-kernel.at>		- 1.12-5
- Use Fedora perl specfile
- Cleanup
- Took over maintainership

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Thu Oct  2 2003 Michael Schwendt <rh0212ms[AT]arcor.de> 0:1.12-0.fdr.3
- Vendor installation
- noarch build
- Removing some files instead of excluding them

* Fri Jul 11 2003 Dams <anvil[AT]livna.org> 0:1.12-0.fdr.2
- Changed Group tag value
- Added  in build section
- Added missing directory

* Tue Jun 17 2003 Dams <anvil[AT]livna.org>
- Initial build.
