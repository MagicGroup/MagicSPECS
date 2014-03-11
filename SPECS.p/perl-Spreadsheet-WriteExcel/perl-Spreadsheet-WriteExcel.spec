Name:			perl-Spreadsheet-WriteExcel
Version:		2.37
Release:		11%{?dist}
Summary:		Write formatted text and numbers to a cross-platform Excel binary file

Group:			Development/Libraries
License:		GPL+ or Artistic
URL:			http://search.cpan.org/dist/Spreadsheet-WriteExcel
Source0:		http://cpan.org/authors/id/J/JM/JMCNAMARA/Spreadsheet-WriteExcel-%{version}.tar.gz

BuildArch:		noarch
BuildRequires:		perl(ExtUtils::MakeMaker)
BuildRequires:		perl(autouse)
BuildRequires:		perl(Carp)
BuildRequires:		perl(Date::Calc)
BuildRequires:		perl(Date::Manip)
BuildRequires:		perl(Encode)
BuildRequires:		perl(Exporter)
BuildRequires:		perl(File::Temp)
BuildRequires:		perl(OLE::Storage_Lite) >= 0.19
BuildRequires:		perl(Parse::RecDescent)
BuildRequires:		perl(Test::More)
BuildRequires:		perl(Time::Local)
Requires:		perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:		perl(Date::Calc), perl(Date::Manip), perl(Parse::RecDescent)
Requires:		perl(OLE::Storage_Lite) >= 0.19, perl(Encode)

%{?perl_default_filter:
%filter_requires_in %{perl_vendorlib}/Spreadsheet/WriteExcel/Examples.pm
%perl_default_filter
}
%global __requires_exclude_from %{?__requires_exclude_from:%__requires_exclude_from|}Spreadsheet/WriteExcel/Examples\\.pm$


%description
The Spreadsheet::WriteExcel module can be used to create a cross-
platform Excel binary file. Multiple worksheets can be added to a
workbook and formatting can be applied to cells. Text, numbers,
formulas, hyperlinks and images can be written to the cells.

The Excel file produced by this module is compatible with 97,
2000, 2002 and 2003. Generated files are also compatible with the
spreadsheet applications Gnumeric and OpenOffice.org.

This module cannot be used to read an Excel file. See
Spreadsheet::ParseExcel or look at the main documentation for some
suggestions. This module cannot be used to write to an existing
Excel file.


%prep
%setup -q -n Spreadsheet-WriteExcel-%{version} 
%{__perl} -pi -e 's/\r\n/\n/g' Changes README bin/chartex \
     doc/*.html examples/{README,*.{pl,txt}}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%clean 
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes README docs/ examples/
%{_bindir}/chartex
%{perl_vendorlib}/Spreadsheet/
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3*

%changelog
* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.37-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 2.37-10
- Perl 5.16 rebuild
- Specify all dependencies

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.37-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Iain Arnell <iarnell@gmail.com> 2.37-8
- add __requires_exclude_from for rpm 4.9

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.37-7
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.37-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 31 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.37-5
- used new filtering according to guidelines to resolve useless requirement

* Fri Jan 28 2011 Oliver Falk <oliver@linux-kernel.at> - 2.37-4
- Rebuild

* Thu Jan 27 2011 Oliver Falk <oliver@linux-kernel.at> - 2.37-3
- Rebuild with new perl-5.12.3

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.37-2
- 661697 rebuild for fixing problems with vendorach/lib

* Wed Jul 14 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2.37-1
- update to 2.37

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.36-2
- Mass rebuild with perl-5.12.0

* Wed Jan 27 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2.36-1
- update to 2.36

* Fri Jan  8 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2.34-1
- update to 2.34

* Mon Dec  7 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.30-1
- update to 2.30

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 2.25-3
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar 13 2009 Tom "spot" Callaway <tcallawa@redhat.com> 2.25-1
- update to 2.25

* Fri Feb 27 2009 Chris Weyl <cweyl@alumni.drew.edu> 2.21-3
- remove new provides/requires rpm is finding on f11 (RHBZ#473874, also
  visible at http://tinyurl.com/cp75ml koji build log for 2.21-2/f11)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jun  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.21-1
- update to 2.21

* Fri Feb  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.20-2
- rebuild for new perl

* Wed Nov 28 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.20-1
- 2.20

* Sun Aug 26 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.18-1
- 2.18
- license tag fix

* Fri Sep 15 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.17-2
- bump for fc6

* Fri Jul  7 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.17-1
- bump to 2.17

* Fri Mar 31 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.16-1
- bump to 2.16

* Tue Jan 10 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.15-1
- bump to 2.15

* Wed May 11 2005 Oliver Falk <oliver@linux-kernel.at>		- 2.14-1
- Update
- Add a complete URL for Source0
- Beautifying (fix identations and make it look more like the
  spectemplate-perl.spec)

* Tue May 10 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.13-3
- more spec cleanups

* Sun Apr 24 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.13-2
- spec cleanups

* Thu Apr 21 2005 Oliver Falk <oliver@linux-kernel.at> 2.13-1
- Update

* Thu Apr 14 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.12-3
- rework spec to match template
- set to noarch

* Thu Apr 14 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.12-2
- Add MODULE_COMPAT requires line

* Fri Apr 1 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.12-1
- initial package
