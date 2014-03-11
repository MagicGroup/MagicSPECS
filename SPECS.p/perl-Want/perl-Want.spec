Name: 		perl-Want
Version: 	0.21
Release: 	4%{?dist}
Summary: 	Perl module implementing a generalisation of wantarray
License: 	GPL+ or Artistic
Group: 		Development/Libraries
URL: 		http://search.cpan.org/dist/Want/
Source0: 	http://search.cpan.org/CPAN/authors/id/R/RO/ROBIN/Want-%{version}.tar.gz

Requires:  	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(Test::More)

%{?perl_default_filter}

%description
This module generalises the mechanism of the wantarray
function, allowing a function to determine in some detail
how its return value is going to be immediately used.

%prep
%setup -q -n Want-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="${RPM_OPT_FLAGS}"
make %{?_smp_mflags}

%install
make install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%check
make test

%files
%doc Changes README
%{perl_vendorarch}/Want*
%{perl_vendorarch}/auto/Want*
%{_mandir}/man3/*

%changelog
* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 10 2012 Petr Pisar <ppisar@redhat.com> - 0.21-3
- Perl 5.16 rebuild

* Mon Mar 05 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.21-2
- More *.spec typo fixes.

* Sun Mar 04 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.21-1
- Upstream update.
- Fix *.spec typo.

* Mon Feb 06 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.20-1
- Upstream update.
- Modernize spec.

* Sun Jan 22 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.18-11
- Add %%{?perl_default_filter}.
- Modernize spec.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.18-9
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 23 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.18-7
- 661697 rebuild for fixing problems with vendorach/lib

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.18-6
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.18-5
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Mar 04 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.18-2
- rebuild for new perl

* Wed Feb 06 2008 Ralf Corsépius <rc040203@freenet.de> - 0.18-1
- Upstream update.

* Wed Jan 02 2008 Ralf Corsépius <rc040203@freenet.de> - 0.16-1
- Upstream update.

* Fri Aug 17 2007 Ralf Corsépius <rc040203@freenet.de> - 0.15-2
- Update license tag.

* Thu Jul 26 2007 Ralf Corsépius <rc040203@freenet.de> - 0.15-1
- Upstream update.

* Mon May 07 2007 Ralf Corsépius <rc040203@freenet.de> - 0.14-1
- Upstream update.

* Thu Apr 19 2007 Ralf Corsépius <rc040203@freenet.de> - 0.12-2
- Reflect perl package split.

* Mon Sep 04 2006 Ralf Corsépius <rc040203@freenet.de> - 0.12-1
- Upstream update.

* Tue Apr 04 2006 Ralf Corsépius <rc040203@freenet.de> - 0.10-1
- Upstream update.

* Mon Feb 20 2006 Ralf Corsépius <rc040203@freenet.de> - 0.09-3
- Rebuild.

* Sat Aug 13 2005 Ralf Corsepius <ralf@links2linux.de> - 0.09-2
- Streamline with FE spec-template.

* Sat Jul 02 2005 Ralf Corsepius <ralf@links2linux.de> - 0.09-1
- Upstream update to 0.09.
