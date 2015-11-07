Name:           perl-Config-IniFiles
Version:	2.88
Release:	2%{?dist}
Summary:        A module for reading .ini-style configuration files

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Config-IniFiles/
Source0:        http://www.cpan.org/authors/id/S/SH/SHLOMIF/Config-IniFiles-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  perl(Module::Build::Compat)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
BuildArch:      noarch
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Config::IniFiles provides a way to have readable configuration files
outside your Perl script. Configurations can be imported (inherited,
stacked,...), sections can be grouped, and settings can be accessed
from a tied hash.


%prep
%setup -q -n Config-IniFiles-%{version}

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
%doc README Changes
%{perl_vendorlib}/Config/
%{_mandir}/man3/*.3pm*


%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 2.88-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 2.88-1
- 更新到 2.88

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 2.68-12
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 2.68-11
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.68-10
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.68-9
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.68-8
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.68-7
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 2.68-6
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 2.68-5
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 2.68-4
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 2.68-3
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.68-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Aug 23 2011 Tom Callaway <spot@fedoraproject.org> - 2.68-1
- update to 2.68

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.58-5
- Perl mass rebuild

* Thu Jun 09 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.58-4
- Perl 5.14 mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.58-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.58-2
- 661697 rebuild for fixing problems with vendorach/lib

* Mon Jun 28 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2.58-1
- update to 2.58

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.47-5
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 2.47-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.47-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.47-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 12 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.47-1
- Upstream update.
- Add Changes to %%doc.

* Thu Nov 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.40-0.1.20081120svn88
- Update to svn checkout, since 2.39 doesn't appear to be accurate.

* Sat Feb  2 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.39-6
- rebuild for new perl

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 2.39-5.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Fri Sep  8 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.39-5
- Rebuild for FC6.
- Convert man page to utf8.

* Wed Feb 15 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.39-4
- Rebuild for FC5 (perl 5.8.8).

* Sat May 14 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.39-3
- Add dist tag.

* Fri Apr 29 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.39-2
- Update to 2.39.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Tue May 25 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.38-2
- Patch URI generated from the RT entry as suggested (bug 1625)

* Thu May 20 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:2.38-0.fdr.1
- Patch: http://rt.cpan.org/NoAuth/Bug.html?id=2584
- First build.
