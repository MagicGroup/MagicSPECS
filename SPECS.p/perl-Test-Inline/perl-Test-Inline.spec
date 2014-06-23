Name: 		perl-Test-Inline
Version: 	2.212
Release: 	15%{?dist}
Summary: 	Test::Inline Perl module
License: 	GPL+ or Artistic
Group: 		Development/Libraries
URL: 		http://search.cpan.org/dist/Test-Inline/
Source0: 	http://search.cpan.org/CPAN/authors/id/A/AD/ADAMK/Test-Inline-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:  	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch: 	noarch

BuildRequires:	perl(Test::More) >= 0.42
BuildRequires:	perl(Test::ClassAPI) >= 1.02
BuildRequires:	perl(File::Spec) >= 0.80
BuildRequires:	perl(List::Util) >= 1.19
BuildRequires:	perl(Getopt::Long) >= 2.34
BuildRequires:	perl(File::chmod) >= 0.31
BuildRequires:	perl(File::Remove) >= 0.37
BuildRequires:	perl(File::Slurp) >= 9999.04
BuildRequires:	perl(File::Find::Rule) >= 0.26
BuildRequires:	perl(Config::Tiny) >= 2.00
BuildRequires:	perl(Params::Util) >= 0.21
BuildRequires:	perl(Class::Autouse) >= 1.29
BuildRequires:	perl(Algorithm::Dependency) >= 1.02
BuildRequires:	perl(File::Flat) >= 1.00
BuildRequires:	perl(Pod::Tests) >= 0.18
BuildRequires:	perl(Test::Script)

# For improved tests
BuildRequires:	perl(Test::Pod) >= 1.00
BuildRequires:  perl(Test::MinimumVersion)
BuildRequires:  perl(Test::CPAN::Meta) >= 0.12
BuildRequires:  perl(Perl::MinimumVersion) >= 1.20

# RPM misses these deps
Requires:	perl(File::Flat)
Requires:	perl(File::Find::Rule)

%description
Test::Inline allows you to inline your tests next to the code being tested.

%prep
%setup -q -n Test-Inline-%{version}

cat << \EOF > %{name}-req
#!/bin/sh
%{__perl_requires} $* |\
    sed -e '/perl(script)/d'
EOF
%define __perl_requires %{_builddir}/Test-Inline-%{version}/%{name}-req
chmod +x %{__perl_requires}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%clean
rm -rf $RPM_BUILD_ROOT

%check
 AUTOMATED_TESTING=1

%files
%defattr(-,root,root,-)
%doc Changes LICENSE
%{_bindir}/*
%{perl_vendorlib}/Test
%{_mandir}/man1/*
%{_mandir}/man3/*

%changelog
* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 2.212-15
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 2.212-14
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 2.212-13
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 2.212-12
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 2.212-11
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.212-10
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.212-9
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.212-8
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 2.212-7
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.212-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 21 2012 Petr Pisar <ppisar@redhat.com> - 2.212-5
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.212-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 2.212-3
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.212-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 06 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.212-1
- Upstream update.

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.211-4
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 2.211-3
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.211-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 20 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.211-1
- Upstream update.

* Wed Jun 17 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.210-1
- Upstream update.

* Fri Feb 27 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.208-5
- Adjust minimum perl version in META.yml (Add Test-Inline-2.208.diff).

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.208-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jun 02 2008 Ralf Corsépius <rc040203@freenet.de> - 2.208-3
- BR: perl(List::Utils) >= 1.19

* Tue Mar 04 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.208-2
- rebuild for new perl

* Wed Jan 02 2008 Ralf Corsépius <rc040203@freenet.de> - 2.208-1
- Upstream update.
- Update build deps.
- Re-enable AUTOMATED_TESTING.

* Wed Sep 19 2007 Ralf Corsépius <rc040203@freenet.de> - 2.207-1
- Upstream update.
- Disable AUTOMATED_TESTING.

* Tue Aug 07 2007 Ralf Corsépius <rc040203@freenet.de> - 2.205-1
- Upstream update.

* Tue Jul 10 2007 Ralf Corsépius <rc040203@freenet.de> - 2.202-1
- Upstream update.

* Wed Jan 18 2007 Ralf Corsépius <rc040203@freenet.de> - 2.201-2
- BR: perl(File::Remove).

* Wed Jan 18 2007 Ralf Corsépius <rc040203@freenet.de> - 2.201-1
- Upstream update.
- Don't chmod -x Changes (Fixed upstream).
- BR: perl(File::Flat) >= 1.00.
- Inline perl-Test-Inline-filter-requires.sh.

* Wed Oct 04 2006 Ralf Corsépius <rc040203@freenet.de> - 2.105-2
- Activate AUTOMATED_TESTING (t/99_author.t).

* Wed Oct 04 2006 Ralf Corsépius <rc040203@freenet.de> - 2.105-1
- Upstream update.

* Tue Sep 05 2006 Ralf Corsépius <rc040203@freenet.de> - 2.103-4
- Mass rebuild.

* Wed Mar 01 2006 Ralf Corsépius <rc040203@freenet.de> - 2.103-3
- Rebuild for perl-5.8.8.

* Fri Oct  7 2005 Paul Howarth <paul@city-fan.org> - 2.103-2
- Minor spec file cleanup
- Add BR: perl(Test::Pod) for extra test coverage

* Thu Sep 29 2005 Ralf Corsepius <ralf@links2linux.de> - 2.103-1
- Upstream update.
- Update BR's.

* Fri Sep 23 2005 Ralf Corsepius <ralf@links2linux.de> - 2.102-1
- Upstream update.

* Tue Sep 14 2005 Ralf Corsepius <ralf@links2linux.de> - 2.101-1
- Upstream update.

* Tue Sep 13 2005 Ralf Corsepius <ralf@links2linux.de> - 2.100-1
- Add filter-requires to filter bogus perl(script).

* Mon Aug 22 2005 Ralf Corsepius <ralf@links2linux.de> - 2.100-0
- Update to 2.100.
