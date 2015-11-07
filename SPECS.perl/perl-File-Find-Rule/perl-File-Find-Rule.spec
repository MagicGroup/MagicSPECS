Name: 		perl-File-Find-Rule
Version: 	0.33
Release: 	9%{?dist}
Summary: 	Perl module implementing an alternative interface to File::Find
License: 	GPL+ or Artistic
Group: 		Development/Libraries
URL: 		http://search.cpan.org/dist/File-Find-Rule/
Source0: 	http://www.cpan.org/modules/by-module/File/File-Find-Rule-%{version}.tar.gz

BuildArch: 	noarch
BuildRequires:	perl
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires: 	perl(Number::Compare)
BuildRequires: 	perl(Text::Glob)
BuildRequires:  perl(Test::More)

Requires:  	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
File::Find::Rule is a friendlier interface to File::Find.  It allows
you to build rules which specify the desired files and directories.

%prep
%setup -q -n File-Find-Rule-%{version}

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
%{_bindir}/findrule
%{_mandir}/man1/*
%{perl_vendorlib}/File
%{_mandir}/man3/*

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.33-9
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.33-8
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.33-7
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.33-6
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.33-5
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.33-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 0.33-3
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Oct 13 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.33-1
- Upstream update.
- Modernize spec file.

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.32-6
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.32-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.32-4
- 661697 rebuild for fixing problems with vendorach/lib

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.32-3
- Mass rebuild with perl-5.12.0

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.32-2
- Mass rebuild with perl-5.12.0

* Mon Dec 14 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.32-1
- Upstream update.

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.30-9
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.30-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.30-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.30-6
- Rebuild for perl 5.10 (again)

* Fri Jan 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.30-5
- rebuild for new perl

* Tue Dec 11 2007 Ralf Corsépius <rc040203@freenet.de> - 0.30-4
- Add BR: perl(Test::More) (BZ 419631).

* Mon Sep 03 2007 Ralf Corsépius <rc040203@freenet.de> - 0.30-3
- Update license tag.
- Add BR: perl(ExtUtils::MakeMaker).

* Tue Sep 05 2006 Ralf Corsépius <rc040203@freenet.de> - 0.30-2
- Mass rebuild.

* Mon Jun 05 2006 Ralf Corsépius <rc040203@freenet.de> - 0.30-1
- Upstream update.

* Sun May 21 2006 Ralf Corsépius <rc040203@freenet.de> - 0.29-1
- Upstream update.

* Tue Feb 28 2006 Ralf Corsépius <rc040203@freenet.de> - 0.28-4
- Rebuild for perl-5.8.8.

* Tue Aug 16 2005 Ralf Corsepius <ralf@links2linux.de> - 0.28-3
- Spec cleanup.

* Wed Aug 10 2005 Ralf Corsepius <ralf@links2linux.de> - 0.28-2
- FE re-submission.

* Mon Mar 21 2005 Ralf Corsepius <ralf@links2linux.de> - 0.28-1
- FE submission.
