Name: 		perl-Sort-Versions
Version:	1.61
Release:	3%{?dist}
Summary: 	Perl module for sorting of revision-like numbers 
License: 	GPL+ or Artistic
Group: 		Development/Libraries
URL: 		http://search.cpan.org/dist/Sort-Versions/
Source0: 	http://www.cpan.org/modules/by-module/Sort/Sort-Versions-%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildArch: 	noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:	perl(Test::More)
Requires:  	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
A perl 5 module for sorting of revision-like numbers 

Sort::Versions allows easy sorting of mixed non-numeric and numeric strings,
like the 'version numbers' that many shared library systems and revision
control packages use. This is quite useful if you are trying to deal with
shared libraries. It can also be applied to applications that intersperse
variable-width numeric fields within text. Other applications can
undoubtedly be found.

%prep
%setup -q -n Sort-Versions-%{version}
for f in Changes Versions.pm; do
	iconv -f iso-8859-1 -t utf-8 <$f >${f}_ &&
	touch -r $f ${f}_ &&
	mv ${f}_ $f
done

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -depth \
	-type f -name .packlist -exec rm -f {} ';' -o \
	-type d -empty -exec rmdir {} ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%clean
rm -rf $RPM_BUILD_ROOT

%check


%files
%defattr(-,root,root,-)
%doc Changes
%{perl_vendorlib}/Sort
%{_mandir}/man3/*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 1.61-3
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1.61-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.61-1
- 更新到 1.61

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.5-22
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.5-21
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 1.5-19
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.5-17
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.5-15
- 661697 rebuild for fixing problems with vendorach/lib

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.5-14
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.5-13
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Mar 19 2009 Stepan Kasal <skasal@redhat.com> - 1.5-11
- fix timestamps of the recoded text files

* Mon Mar 16 2009 Stepan Kasal <skasal@redhat.com> - 1.5-10
- Recode as UTF-8, fix argument order find with -depth (both by Paul Howarth)
- Other minor cleanups

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.5-8
- rebuild for new perl

* Fri Aug 17 2007 Ralf Corsépius <rc040203@freenet.de> - 1.5-7
- Add BR: perl(Test::More).

* Fri Aug 17 2007 Ralf Corsépius <rc040203@freenet.de> - 1.5-6
- Update license tag.
- Reflect perl split.

* Tue Sep 05 2006 Ralf Corsépius <rc040203@freenet.de> - 1.5-5
- Mass rebuild.

* Tue Feb 28 2006 Ralf Corsépius <rc040203@freenet.de> - 1.5-4
- Rebuild for perl-5.8.8.

* Wed Aug 17 2005 Ralf Corsepius <ralf@links2linux.de> - 1.5-3
- Spec cleanup.

* Wed Aug 10 2005 Ralf Corsepius <ralf@links2linux.de> - 1.5-2
- FE re-submission.

* Fri Jul 01 2005 Ralf Corsepius <ralf@links2linux.de> - 1.5-1
- FE submission.
