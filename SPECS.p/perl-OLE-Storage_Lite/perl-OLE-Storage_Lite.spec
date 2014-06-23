Name:		perl-OLE-Storage_Lite
Version:	0.19
Release:	9%{?dist}
Summary:	Simple Class for OLE document interface
Group:		Development/Libraries
License:	GPL+ or Artistic
Source0:	http://search.cpan.org/CPAN/authors/id/J/JM/JMCNAMARA/OLE-Storage_Lite-%{version}.tar.gz
Url: 		http://search.cpan.org/dist/OLE-Storage_Lite/
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch
BuildRequires: 	perl(Test::More)
Requires: 	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:	perl(IO::Scalar)

%description
Simple Class for OLE document interface.

%prep
%setup -q -n OLE-Storage_Lite-%{version} 
%{__perl} -pi -e 's/\r\n/\n/g' Changes README sample/{README,*.pl}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%check
make test

%clean 
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes README sample/
%{perl_vendorlib}/OLE/
%{_mandir}/man3/*.3*

%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.19-9
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 0.19-7
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.19-5
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.19-3
- 661697 rebuild for fixing problems with vendorach/lib

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.19-2
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 0.19-1
- Update to 0.19

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.18-3
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar 13 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 0.18-1
- update to 0.18

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jun  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.17-1
- update to 0.17

* Tue Feb  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.15-2
- rebuild for new perl

* Wed Dec 19 2007 Tom "spot" Callaway <tcallawa@redhat.com> 0.15-1
- 0.15

* Sun Aug 26 2007 Tom "spot" Callaway <tcallawa@redhat.com> 0.14-9
- license tag fix

* Fri Sep 15 2006 Tom "spot" Callaway <tcallawa@redhat.com> 0.14-8
- bump for fc6

* Fri Jul  7 2006 Tom "spot" Callaway <tcallawa@redhat.com> 0.14-7
- bump to fix disttag

* Tue May 10 2005 Tom "spot" Callaway <tcallawa@redhat.com> 0.14-6
- fix defattr order

* Mon May  9 2005 Tom "spot" Callaway <tcallawa@redhat.com> 0.14-5
- fix spec file

* Sun Apr 24 2005 Tom "spot" Callaway <tcallawa@redhat.com> 0.14-4
- spec file cleanup

* Thu Apr 14 2005 Tom "spot" Callaway <tcallawa@redhat.com> 0.14-3
- rework spec to match template
- set to noarch

* Thu Apr 14 2005 Tom "spot" Callaway <tcallawa@redhat.com> 0.14-2
- add MODULE_COMPAT requires

* Fri Apr 1 2005 Tom "spot" Callaway <tcallawa@redhat.com> 0.14-1
- initial package
