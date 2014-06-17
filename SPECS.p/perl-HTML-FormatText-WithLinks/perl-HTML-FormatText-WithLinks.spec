Name:           perl-HTML-FormatText-WithLinks
Version:        0.14
Release:        7%{?dist}
Summary:        HTML to text conversion with links as footnotes

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/HTML-FormatText-WithLinks
Source0:        http://search.cpan.org/CPAN/authors/id/S/ST/STRUAN/HTML-FormatText-WithLinks-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(HTML::FormatText) perl(HTML::TreeBuilder)
BuildRequires:  perl(URI::WithBase)
BuildRequires:  perl(Test::MockObject) perl(Test::Pod::Coverage) 
BuildRequires:  perl(Test::Pod) perl(Test::More)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
# not picked up automatically since it is called through SUPER
Requires:  perl(HTML::FormatText) >= 2

%description
HTML::FormatText::WithLinks takes HTML and turns it into plain text but 
prints all the links in the HTML as footnotes. By default, it attempts 
to mimic the format of the lynx text based web browser's --dump option.

%prep
%setup -q -n HTML-FormatText-WithLinks-%{version}


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



%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*


%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.14-7
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.14-6
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.14-5
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.14-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 13 2010 Petr Sabata <psabata@redhat.com> - 0.14-1
- 0.14 bump

* Thu Dec  2 2010 Petr Sabata <psabata@redhat.com> - 0.12-1
- 0.12 bump

* Wed Sep 15 2010 Petr Pisar <ppisar@redhat.com> - 0.11-1
- 0.11 bump

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.09-8
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.09-7
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jul 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.09-3
- fix license tag (it may be correct, but its flagging as a false positive on checks)

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.09-2
- Rebuild for new perl

* Wed Aug  8 2007 Patrice Dumas <pertusus@free.fr> 0.09-1
- update to 0.09

* Sun Sep 17 2006 Patrice Dumas <pertusus@free.fr> 0.07-1
- update to 0.07

* Fri Sep 15 2006 Patrice Dumas <pertusus@free.fr> 0.06-3
- add Requires for perl(HTML::FormatText), fix #206729

* Tue Aug 29 2006 Patrice Dumas <pertusus@free.fr> 0.06-2
- added BuildRequires for tests

* Tue Jul 18 2006 Patrice Dumas <pertusus@free.fr> 0.06-1
- Initial packaging
