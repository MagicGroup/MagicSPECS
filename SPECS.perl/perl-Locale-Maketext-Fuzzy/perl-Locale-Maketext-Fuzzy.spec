Name:           perl-Locale-Maketext-Fuzzy
Version:	0.11
Release:	2%{?dist}
Summary:        Maketext from already interpolated strings

Group:          Development/Libraries
License:        MIT
URL:            http://search.cpan.org/dist/Locale-Maketext-Fuzzy/
Source0:        http://www.cpan.org/modules/by-module/Locale/Locale-Maketext-Fuzzy-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This module is a subclass of Locale::Maketext, with additional
support for localizing messages that already contains interpolated
variables.  This is most useful when the messages are returned by
external modules -- for example, to match "dir: command not foundr"
against "[_1]: command not found".


%prep
%setup -q -n Locale-Maketext-Fuzzy-%{version}


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
%{perl_vendorlib}/Locale/
%{_mandir}/man3/*.3pm*


%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.11-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.11-1
- 更新到 0.11

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.10-14
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.10-13
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.10-12
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jun 15 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.10-10
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.10-8
- 661697 rebuild for fixing problems with vendorach/lib

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.10-7
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.10-6
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.10-2
Rebuild for new perl

* Wed Dec 05 2007 Ralf Corsépius <rc040203@freenet.de> - 0.10-1
- Upstream update.
- Change Source0: to using "by-module".
- Reflect upstream license change.

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.02-4.2
- add BR: perl(Test::More)

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.02-4.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Thu Sep  7 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.02-4
- Rebuild for FC6.

* Fri Feb 17 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.02-3
- Rebuild for FC5 (perl 5.8.8).

* Fri Sep  9 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.02-2
- Comment about license files location.

* Thu Aug 11 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.02-1
- Update to Fedora Extras template.

* Sun Oct 31 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:0.02-0.fdr.1
- First build.
