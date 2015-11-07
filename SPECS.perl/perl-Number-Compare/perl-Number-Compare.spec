Name: 		perl-Number-Compare
Version: 	0.03
Release: 	9%{?dist}
Summary: 	Perl module for numeric comparisons
License: 	GPL+ or Artistic
Group: 		Development/Libraries
URL: 		http://search.cpan.org/dist/Number-Compare/
Source0: 	http://www.cpan.org/authors/id/R/RC/RCLAMP/Number-Compare-%{version}.tar.gz

BuildArch: 	noarch
BuildRequires:	perl(Carp)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(Test::More)
Requires:  	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Number::Compare compiles a simple comparison to an anonymous subroutine,
which you can call with a value to be tested again.

%prep
%setup -q -n Number-Compare-%{version}

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
%{perl_vendorlib}/Number
%{_mandir}/man3/*

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.03-9
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.03-8
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.03-7
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.03-6
- 为 Magic 3.0 重建

* Tue Aug 14 2012 Petr Pisar <ppisar@redhat.com> - 0.03-5
- Specify all dependencies

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.03-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 0.03-3
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.03-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Oct 13 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.03-1
- Upstream update.

* Mon Sep 19 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.02-1
- Upstream update.
- Spec file cleanup.

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.01-16
- 661697 rebuild for fixing problems with vendorach/lib

* Sat Jun 26 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.01-15
- Apply https://rt.cpan.org/Ticket/Attachment/792151/410599/Number-Compare-0.01-uninitialized.patch
  to address https://bugzilla.redhat.com/show_bug.cgi?id=607982.

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.01-14
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.01-13
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.01-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.01-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.01-10
- Rebuild for perl 5.10 (again)

* Fri Jan 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.01-9
- rebuild for new perl

* Fri Aug 17 2007 Ralf Corsépius <rc040203@freenet.de> - 0.01-8
- Update license tag.

* Thu Apr 19 2007 Ralf Corsépius <rc040203@freenet.de> - 0.01-7
- Reflect perl package split.

* Tue Sep 05 2006 Ralf Corsépius <rc040203@freenet.de> - 0.01-6
- Mass rebuild.

* Tue Feb 28 2006 Ralf Corsépius <rc040203@freenet.de> - 0.01-5
- Rebuild for perl-5.8.8.

* Tue Aug 16 2005 Paul Howarth <paul@city-fan.org> - 0.01-4
- BR: perl redundant for Extras.

* Sat Aug 13 2005 Ralf Corsepius <ralf@links2linux.de> - 0.01-3
- Spec cleanup.

* Wed Aug 10 2005 Ralf Corsepius <ralf@links2linux.de> - 0.01-2
- FE re-submission.

* Fri Jul 01 2005 Ralf Corsepius <ralf@links2linux.de> - 0.01-1
- FE submission.
