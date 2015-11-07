Name:           perl-PAR-Dist
Version:	0.49
Release:	2%{?dist}
Summary:        Toolkit for creating and manipulating Perl PAR distributions
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/PAR-Dist/
Source0:        http://search.cpan.org/CPAN/authors/id/R/RS/RSCHUPP/PAR-Dist-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl(Archive::Zip)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
BuildRequires:  perl(YAML::Tiny)
Requires:       perl(Archive::Zip)
Requires:       perl(YAML::Tiny)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This module creates and manipulates PAR distributions. They are architecture-
specific PAR files, containing everything under blib/ of CPAN distributions
after their make or Build stage, a META.yml describing metadata of the
original CPAN distribution, and a MANIFEST detailing all files within it.
Digitally signed PAR distributions will also contain a SIGNATURE file.

%prep
%setup -q -n PAR-Dist-%{version}

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
 PERL_TEST_POD=1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.49-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.49-1
- 更新到 0.49

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.47-8
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.47-7
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.47-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Petr Pisar <ppisar@redhat.com> - 0.47-5
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.47-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.47-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.47-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Steven Pritchard <steve@kspei.com> 0.47-1
- Update to 0.47.

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.46-4
- 661697 rebuild for fixing problems with vendorach/lib

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.46-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.46-2
- rebuild against perl 5.10.1

* Mon Sep 21 2009 Stepan Kasal <skasal@redhat.com> - 0.46-1
- new upstream version

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.43-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.43-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 02 2009 Steven Pritchard <steve@kspei.com> 0.43-1
- Update to 0.43.
- Explicitly require Archive::Zip and YAML::Tiny.

* Fri Jan 16 2009 Steven Pritchard <steve@kspei.com> 0.42-1
- Update to 0.42.

* Mon Dec 15 2008 Steven Pritchard <steve@kspei.com> 0.40-1
- Update to 0.40.
- BR Archive::Zip and YAML::Tiny for t/03merge_meta.

* Thu Sep 25 2008 Marcela Maslanova <mmaslano@redhat.com> 0.34-2
- forgot apply source

* Thu Sep 25 2008 Marcela Maslanova <mmaslano@redhat.com> 0.34-1
- update to 0.34 -> it was needed for perl-PAR

* Sat May 31 2008 Steven Pritchard <steve@kspei.com> 0.31-1
- Update to 0.31.
- BR Test::Pod and Test::Pod::Coverage.

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.29-2
- Rebuild for perl 5.10 (again)

* Thu Feb 21 2008 Steven Pritchard <steve@kspei.com> 0.29-1
- Update to 0.29.
- Use fixperms macro instead of our own chmod incantation.
- Reformat to match cpanspec output.

* Thu Jan 10 2008 Tom "spot" Callaway <tcallawa@redhat.com>  - 0.25-4
- rebuild (again) for new perl

* Thu Jan 10 2008 Tom "spot" Callaway <tcallawa@redhat.com>  - 0.25-3
- rebuild for new perl

* Mon Aug  6 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.25-2
- License: GPL+ or Artistic

* Mon Jul 30 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.25-1
- 0.25.

* Sun Jul 22 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.24-1
- 0.24.

* Mon Jun 25 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.23-1
- 0.23.

* Sun May  6 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.22-1
- 0.22.

* Tue Apr 17 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.21-2
- BuildRequire perl(ExtUtils::MakeMaker) and perl(Test::More).

* Sun Oct 15 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.21-1
- 0.21.

* Thu Oct 12 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.20-1
- 0.20.

* Sun Sep 17 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.19-1
- 0.19.

* Mon Aug 28 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.18-1
- 0.18.

* Tue Aug 15 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.16-1
- 0.16.

* Sat Jul 29 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.15-1
- 0.15.

* Sun Jul 23 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.14-1
- 0.14.

* Thu Jul 20 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.11-1
- 0.11.
- Fix order of options to find(1) in %%install.

* Thu Jun  8 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.10-1
- 0.10.

* Fri Feb 24 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.08-1
- 0.08.
- Specfile cleanups.

* Thu Mar 17 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.07-3
- Avoid running signature test during build.
- Sync with fedora-rpmdevtools' Perl spec template.

* Sun Apr 25 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.07-0.fdr.2
- Require perl(:MODULE_COMPAT_*).

* Sat Mar 27 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.07-0.fdr.1
- First build.
