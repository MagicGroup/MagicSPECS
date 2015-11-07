Summary: 	Tools to test taintedness
Name: 		perl-Test-Taint
Version:	1.06
Release:	2%{?dist}
License: 	GPL+ or Artistic
Group: 		Development/Libraries
URL: 		http://search.cpan.org/dist/Test-Taint/
Source0: 	http://search.cpan.org/CPAN/authors/id/P/PE/PETDANCE/Test-Taint-%{version}.tar.gz

BuildRequires:  perl(ExtUtils::MakeMaker)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

BuildRequires: perl(Test::Pod) >= 1.00
BuildRequires: perl(Test::Pod::Coverage) >= 0.08

%{?perl_default_filter}

%description
Tainted data is data that comes from an unsafe source, such as the command
line, or, in the case of web apps, any GET or POST transactions. Read the 
perlsec man page for details on why tainted data is bad, and how to untaint
the data.

When you're writing unit tests for code that deals with tainted data, you'll
want to have a way to provide tainted data for your routines to handle, and 
easy ways to check and report on the taintedness of your data, in standard 
Test::More style.

%prep
%setup -q -n Test-Taint-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="${RPM_OPT_FLAGS}"
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%check


%files
%defattr(-,root,root,-)
%doc Changes
%{perl_vendorarch}/Test
%{perl_vendorarch}/auto/Test
%{_mandir}/man3/*

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1.06-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.06-1
- 更新到 1.06

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.04-20
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.04-19
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.04-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 1.04-17
- Perl 5.16 rebuild

* Sun Jan 22 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.04-16
- Modernize spec.
- Add %%{perl_default_filter}.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.04-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.04-14
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.04-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.04-12
- 661697 rebuild for fixing problems with vendorach/lib

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.04-11
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1.04-10
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.04-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.04-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.04-7
- Rebuild for perl 5.10 (again)

* Sun Feb 10 2008 Ralf Corsépius <rc040203@freenet.de> - 1.04-6
- Rebuild for gcc43.

* Mon Jan 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.04-5
- rebuild for new perl

* Fri Aug 17 2007 Ralf Corsépius <rc040203@freenet.de> - 1.04-4
- Reflect perl-package split.
- Update license tag.

* Tue Sep 05 2006 Ralf Corsépius <rc040203@freenet.de> - 1.04-3
- Mass rebuild.

* Mon Feb 20 2006 Ralf Corsepius <rc040203@freenet.de> - 1.04-2
- Rebuild.

* Wed Aug 10 2005 Ralf Corsepius <ralf@links2linux.de> - 1.04-1
- FE submission.

* Sun Mar 20 2005 Ralf Corsepius <ralf@links2linux.de> - 1.04-0.pm.2
- Initial version.
