Name:           perl-HTML-Encoding
Version:        0.61
Release:        10%{?dist}
Summary:        Determine the encoding of HTML/XML/XHTML documents

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/HTML-Encoding/
Source0:        http://www.cpan.org/authors/id/B/BJ/BJOERN/HTML-Encoding-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(HTML::Parser)
BuildRequires:  perl(HTTP::Headers::Util)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
HTML::Encoding helps to determine the encoding of HTML and XML/XHTML
documents.


%prep
%setup -q -n HTML-Encoding-%{version}
find . -type f | xargs chmod -c -x
find . -type f | xargs %{__perl} -pi -e 's/\r//g'


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



%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/HTML/
%{_mandir}/man3/HTML::Encoding.3*


%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.61-10
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.61-9
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.61-8
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.61-7
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.61-6
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.61-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.61-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.61-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 17 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.61-2
- 661697 rebuild for fixing problems with vendorach/lib

* Sat Sep 25 2010 Ville Skyttä <ville.skytta@iki.fi> - 0.61-1
- Update to 0.61.

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.60-6
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.60-5
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.60-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.60-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.60-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jul  3 2008 Ville Skyttä <ville.skytta@iki.fi> - 0.60-1
- 0.60.

* Thu Apr 10 2008 Ville Skyttä <ville.skytta@iki.fi> - 0.57-1
- 0.57.

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.56-2
- Rebuild for new perl

* Thu Dec  6 2007 Ville Skyttä <ville.skytta@iki.fi> - 0.56-1
- 0.56.

* Wed Dec  5 2007 Ville Skyttä <ville.skytta@iki.fi> - 0.54-1
- 0.54.

* Tue Aug  7 2007 Ville Skyttä <ville.skytta@iki.fi> - 0.53-2
- License: GPL+ or Artistic

* Wed May 23 2007 Ville Skyttä <ville.skytta@iki.fi> - 0.53-1
- 0.53.

* Tue Apr 17 2007 Ville Skyttä <ville.skytta@iki.fi> - 0.52-2
- BuildRequire perl(Test::More).

* Tue Apr  3 2007 Ville Skyttä <ville.skytta@iki.fi> - 0.52-1
- First Fedora build.

* Mon Apr  2 2007 Ville Skyttä <ville.skytta@iki.fi> - 0.52-0.5
- BuildRequire perl(ExtUtils::MakeMaker).

* Sat Sep 30 2006 Ville Skyttä <ville.skytta@iki.fi> - 0.52-0.4
- Fix build dependencies.

* Thu Mar 30 2006 Ville Skyttä <ville.skytta@iki.fi> - 0.52-0.3
- Rebuild, drop extra license texts.

* Tue Aug 30 2005 Ville Skyttä <ville.skytta@iki.fi> - 0.52-0.2
- Include GPL and Artistic license texts.

* Tue Jun 14 2005 Ville Skyttä <ville.skytta@iki.fi> - 0.52-0.1
- 0.52, rebuild for FC4.

* Wed Nov  3 2004 Ville Skyttä <ville.skytta@iki.fi> - 0:0.50-0.fdr.1
- First build.
