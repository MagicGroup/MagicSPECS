Name:           perl-XML-XQL
Version:        0.68
Release:        20%{?dist}
Summary:        Perl module for querying XML tree structures with XQL
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/XML-XQL/
Source0:        http://www.cpan.org/authors/id/T/TJ/TJMATHER/XML-XQL-%{version}.tar.gz
Patch0:         %{name}-tput-147465.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Date::Manip) >= 5.33
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(fields)
BuildRequires:  perl(LWP::UserAgent)
BuildRequires:  perl(Parse::Yapp)
BuildRequires:  perl(XML::DOM) >= 1.29
BuildRequires:  perl(XML::Parser) >= 2.30
BuildRequires:  perl(XML::RegExp)
Requires:       perl(XML::DOM)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%global __provides_exclude ^perl\\(XML::\(DOM::.+\|XQL)\\)\\s*$

%description
This is a Perl extension that allows you to perform XQL queries on XML
object trees. Currently only the XML::DOM module is supported, but
other implementations, like XML::Grove, may soon follow.

%prep
%setup -q -n XML-XQL-%{version}
%patch0 -p0

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*
magic_rpm_clean.sh

%check


%clean
rm -rf $RPM_BUILD_ROOT %{__perl_provides}

%files
%defattr(-,root,root,-)
%doc Changes README
%{_bindir}/xql.pl
%{perl_vendorlib}/XML/
%{_mandir}/man3/XML::XQL*.3*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.68-20
- 为 Magic 3.0 重建

* Tue Aug 21 2012 Jitka Plesnikova <jplesnik@redhat.com> - 0.68-19
- Use macro __provides_exclude for filtering of Provides instead of running
  script.

* Fri Aug 17 2012 Jitka Plesnikova <jplesnik@redhat.com> - 0.68-18
- Specify all dependencies.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.68-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Petr Pisar <ppisar@redhat.com> - 0.68-16
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.68-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 0.68-14
- Perl mass rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.68-13
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.68-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 23 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.68-11
- 661697 rebuild for fixing problems with vendorach/lib

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.68-10
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.68-9
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.68-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.68-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.68-6
- Rebuild for perl 5.10 (again)

* Mon Jan 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.68-5
- rebuild for new perl

* Wed Apr 18 2007 Steven Pritchard <steve@kspei.com> 0.68-4
- Reformat to match cpanspec output.
- Fix find option order.
- Use fixperms macro instead of our own chmod incantation.
- BR ExtUtils::MakeMaker.

* Mon Aug 27 2006 Michael J. Knox <michael[AT]knox.net.nz> - 0.68-3
- Rebuild for FC6

* Thu Jun 08 2006 Michael J. Knox <michael[AT]knox.net.nz> - 0.68-2
- rebuilt and spec clean.
 
* Sun Nov  6 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.68-1
- First Fedora Extras release.

* Thu Nov  3 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.68-0.3
- Add minimum version to XML::DOM build dependency, filter out
  versionless perl(XML::DOM) provision (#172332, Ralf Corsepius).

* Thu Nov  3 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.68-0.2
- Fix insecure $PATH error in taint mode (#147465).
- Avoid warnings with empty (but defined) $TERM (#147465).

* Thu Oct 27 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.68-0.1
- First build (#128879).
