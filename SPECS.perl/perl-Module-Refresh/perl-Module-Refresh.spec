Name: 		perl-Module-Refresh
Version: 	0.17
Release: 	9%{?dist}
Summary: 	Refresh %INC files when updated on disk
License: 	GPL+ or Artistic
Group: 		Development/Libraries
URL: 		http://search.cpan.org/dist/Module-Refresh/
Source0: 	http://www.cpan.org/modules/by-module/Module/Module-Refresh-%{version}.tar.gz

BuildRequires:	perl(Cwd)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(ExtUtils::MM_Unix)
# Tests:
BuildRequires:	perl(File::Temp) >= 0.19
BuildRequires:	perl(Path::Class)
BuildRequires:	perl(Test::More)
Requires:  	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch: 	noarch

%description
This module is a generalization of the functionality provided by 
Apache::StatINC. It's designed to make it easy to do simple iterative
development when working in a persistent environment.

%prep
%setup -q -n Module-Refresh-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%check


%files
%defattr(-,root,root,-)
%doc Changes
%{perl_vendorlib}/Module
%{_mandir}/man3/*

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.17-9
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.17-8
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.17-7
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.17-6
- 为 Magic 3.0 重建

* Thu Aug 09 2012 Petr Pisar <ppisar@redhat.com> - 0.17-5
- Specify all dependencies

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Petr Pisar <ppisar@redhat.com> - 0.17-3
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 25 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.17-1
- Upstream update.

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.16-2
- Perl mass rebuild

* Sat Apr 30 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.16-1
- Upstream update.
- Spec file cleanup.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.13-8
- 661697 rebuild for fixing problems with vendorach/lib

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.13-7
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.13-6
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Mar 04 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.13-3
- rebuild for new perl

* Thu Sep 06 2007 Ralf Corsépius <rc040203@freenet.de> - 0.13-2
- Update license tag.

* Tue May 08 2007 Ralf Corsépius <rc040203@freenet.de> - 0.13-1
- Upstream update.

* Wed Apr 25 2007 Ralf Corsépius <rc040203@freenet.de> - 0.11-1
- Upstream update.

* Tue Sep 05 2006 Ralf Corsépius <rc040203@freenet.de> - 0.09-3
- Mass rebuild.

* Wed Mar 01 2006 Ralf Corsépius <rc040203@freenet.de> - 0.09-2
- Rebuild for perl-5.8.8.

* Sat Jan 14 2006 Ralf Corsépius <rc040203@freenet.de> - 0.09-1
- Upstream update.

* Wed Nov 02 2005 Ralf Corsepius <rc040203@freenet.de> - 0.08-1
- Upstream update.
