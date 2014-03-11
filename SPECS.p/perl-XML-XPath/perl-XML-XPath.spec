Name:           perl-XML-XPath
Version:        1.13
Release:        22%{?dist}

Summary:        XPath parser and evaluator for Perl

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/XML-XPath/
Source0:    http://www.cpan.org/authors/id/M/MS/MSERGEANT/XML-XPath-1.13.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(Test)
BuildRequires:  perl(XML::Parser)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This module aims to comply exactly to the XPath specification at
http://www.w3.org/TR/xpath and yet allow extensions to be added in the
form of functions. Modules such as XSLT and XPointer may need to do
this as they support functionality beyond XPath.


%prep
%setup -q -n XML-XPath-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man1/
cat >> $RPM_BUILD_ROOT/%{_mandir}/man1/xpath.1 << EOF
.so man3/XML::XPath.3pm
EOF

%check



%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README TODO
%{_bindir}/xpath
%{perl_vendorlib}/XML
%{_mandir}/man1/xpath*
%{_mandir}/man3/*.3*


%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.13-22
- 为 Magic 3.0 重建

* Tue Oct 16 2012 Marcela Mašláňová <mmaslano@redhat.com> - 1.13-21
- revert the patch. It breaks backward compatibility for some apps. 
- the xpath has still man page installed.

* Fri Aug 24 2012 Jitka Plesnikova <jplesnik@redhat.com> - 1.13-20
- Specify all dependencies.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 15 2012 Petr Pisar <ppisar@redhat.com> - 1.13-18
- Perl 5.16 rebuild

* Fri Mar 16 2012 Marcela Mašláňová <mmaslano@redhat.com> - 1.13-17
- 680418 - missing man page for xpath
- applied debian patch, which added POD into xpath code, but also fix debian bug(#185292)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 1.13-15
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 23 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.13-13
- 661697 rebuild for fixing problems with vendorach/lib

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.13-12
- Mass rebuild with perl-5.12.0

* Thu Dec 10 2009 Marcela Maslanova <mmaslano@redhat.com> - 1.13-11
- 541668 fix requires for review

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.13-10
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jun 2  2008 Marcela Maslanova <mmaslano@redhat.com> - 1.13-7
- rebuild and remove ||: from check part

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.13-6
- Rebuild for perl 5.10 (again)

* Thu Jan 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.13-5
- rebuild for new perl

* Wed Oct 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.13-4.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Thu Aug 31 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.13-4
- bump for mass rebuild

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sun Jul 11 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.13-2
- Bring up to date with current fedora.us Perl spec template.

* Sun Oct 12 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.13-0.fdr.1
- First build.
