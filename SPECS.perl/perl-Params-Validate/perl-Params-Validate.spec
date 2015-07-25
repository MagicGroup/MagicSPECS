Summary: 	Params-Validate Perl module
Name: 		perl-Params-Validate
Version: 	1.06
Release: 	12%{?dist}
License: 	Artistic2.0
Group: 		Development/Libraries
URL: 		http://search.cpan.org/dist/Params-Validate/
Source0: 	http://search.cpan.org/CPAN/authors/id/D/DR/DROLSKY/Params-Validate-%{version}.tar.gz

# Hacks to make spell checking tests work with hunspell
Patch0:         Params-Validate-0.99.diff

Requires:  	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

BuildRequires:  perl(Carp)
BuildRequires:  perl(Module::Implementation) >= 0.04
BuildRequires:  perl(Module::Build) >= 0.37

# Run-time:
BuildRequires:  perl(Attribute::Handlers) >= 0.79
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Scalar::Util) >= 1.10
BuildRequires:  perl(XSLoader)

# Required by the tests
BuildRequires:  perl(base)
BuildRequires:  perl(Devel::Peek)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::Fatal)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(Test::Taint) >= 0.02
BuildRequires:  perl(Tie::Array)
BuildRequires:  perl(Tie::Hash)
BuildRequires:  perl(Readonly)
BuildRequires:  perl(Readonly::XS)

# For release testing tests
BuildRequires:	perl(Test::CPAN::Changes)
BuildRequires:	perl(Test::EOL)
BuildRequires:	perl(Test::NoTabs)
BuildRequires:	perl(Test::Pod) >= 1.41
BuildRequires:	perl(Test::Pod::Coverage) >= 1.04
# Optional, not (yet) in Fedora: BuildRequires:  perl(Test::Pod::LinkCheck)
# Optional, not (yet) in Fedora: BuildRequires:  perl(Test::Pod::No404s)
BuildRequires:	perl(Test::Spelling)
BuildRequires:  hunspell-en

%{?perl_default_filter}

%description
The Params::Validate module allows you to validate method or function
call parameters to an arbitrary level of specificity. At the simplest
level, it is capable of validating the required parameters were given
and that no unspecified additional parameters were passed in. It is
also capable of determining that a parameter is of a specific type,
that it is an object of a certain class hierarchy, that it possesses
certain methods, or applying validation callbacks to arguments.

%prep
%setup -q -n Params-Validate-%{version}
%patch0 -p1
sed -i -e "s,set_spell_cmd(.*),set_spell_cmd(\'hunspell -l\')," t/release-pod-spell.t

%build
%{__perl} Build.PL installdirs=vendor optimize="$RPM_OPT_FLAGS"
./Build

%install
./Build install destdir=$RPM_BUILD_ROOT create_packlist=0
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'

%{_fixperms} $RPM_BUILD_ROOT/*

%check
RELEASE_TESTING=1 ./Build test

%files
%defattr(-,root,root,-)
%doc Changes LICENSE README TODO
%{perl_vendorarch}/Params
%{perl_vendorarch}/auto/Params
%{perl_vendorarch}/Attribute
%{_mandir}/man3/*

%changelog
* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.06-12
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.06-11
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.06-10
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.06-9
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.06-8
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.06-7
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.06-6
- 为 Magic 3.0 重建

* Tue Aug 14 2012 Petr Pisar <ppisar@redhat.com> - 1.06-5
- Specify all dependencies

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.06-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 1.06-3
- Perl 5.16 rebuild

* Thu May 31 2012 Petr Pisar <ppisar@redhat.com> - 1.06-2
- Round Module::Build version to 2 digits

* Mon Mar 19 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.06-1
- Upstream update.

* Wed Feb 09 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.05-1
- Upstream update.

* Mon Feb 06 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.01-1
- Upstream update.
- Drop Params-Validate-1.00-no-pod-coverage.patch.
- Spec file cleanup.

* Sun Jan 22 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.00-5
- Add %%{perl_default_filter}.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.00-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 1.00-3
- Perl mass rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 1.00-2
- Perl mass rebuild

* Thu Jun 30 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.00-1
- Upstream update.
- Deactivate t/release-pod-coverage.t 
  (Add Params-Validate-1.00-no-pod-coverage.patch).

* Thu Jun 30 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.99-3
- Fix up bogus Tue Jun 28 2011 changelog entry.
- Fix License (Artistic2.0).
- Add BR: perl(Test::CPAN:Changes).

* Tue Jun 28 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.99-2
- Perl mass rebuild
- remove unneeded Pod::Man 

* Tue May 31 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.99-1
- Upstream update.
- Rebase patch (Params-Validate-0.99.diff).

* Sat Apr 30 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.98-1
- Upstream update.
- Spec cleanup.
- Rework BR's.
- Reflect upstream having abandoned AUTHOR_TESTING.
- Make spell-checking tests working/work-around aspell/hunspell/perl(Test::Spelling)
  issues (add Params-Validate-0.98.diff).

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.95-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.95-3
- 661697 rebuild for fixing problems with vendorach/lib

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.95-2
- Mass rebuild with perl-5.12.0

* Wed Mar 03 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.95-1
- Upstream update.

* Thu Dec 15 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.94-1
- Upstream update.
- Reflect upstream having reworked author tests to using AUTHOR_TESTING=1.

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.92-2
- rebuild against perl 5.10.1

* Mon Nov 23 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.92-1
- Upstream update.
- Switch to Build.PL.
- Disable IS_MAINTAINER test.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jun 10 2008 Ralf Corsépius <rc040203@freenet.de> - 0.91-1
- Upstream update.
- Conditionally activate IS_MAINTAINER tests.

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.89-4
- Rebuild for perl 5.10 (again)

* Sun Feb 10 2008 Ralf Corsépius <rc040203@freenet.de> - 0.89-3
- Rebuild for gcc43.

* Tue Jan 15 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.89-2
- rebuild for new perl

* Tue Nov 13 2007 Ralf Corsépius <rc040203@freenet.de> - 0.89-1
- Upstream update.

* Thu Sep 06 2007 Ralf Corsépius <rc040203@freenet.de> - 0.88-3
- Update license tag.

* Wed Aug 22 2007 Ralf Corsépius <rc040203@freenet.de> - 0.88-2
- Mass rebuild.

* Mon Mar 12 2007 Ralf Corsépius <rc040203@freenet.de> - 0.88-1
- BR: perl(ExtUtils::MakeMaker).
- Upstream update.

* Sat Jan 20 2007 Ralf Corsépius <rc040203@freenet.de> - 0.87-1
- Upstream update.

* Tue Sep 05 2006 Ralf Corsépius <rc040203@freenet.de> - 0.86-2
- Mass rebuild.

* Sun Aug 13 2006 Ralf Corsépius <rc040203@freenet.de> - 0.86-1
- Upstream update.

* Mon Jun 28 2006 Ralf Corsépius <rc040203@freenet.de> - 0.85-1
- Upstream update.

* Mon Jun 05 2006 Ralf Corsépius <rc040203@freenet.de> - 0.84-1
- Upstream update.

* Sun May 21 2006 Ralf Corsépius <rc040203@freenet.de> - 0.82-1
- Upstream update.

* Wed Apr 04 2006 Ralf Corsépius <rc040203@freenet.de> - 0.81-1
- Upstream update.

* Wed Feb 20 2006 Ralf Corsépius <rc040203@freenet.de> - 0.80-2
- Rebuild.

* Wed Feb 01 2006 Ralf Corsépius <rc040203@freenet.de> - 0.80-1
- Upstream update.

* Sat Jan 14 2006 Ralf Corsépius <rc040203@freenet.de> - 0.79-1
- Upstream update.
- BR perl(Readonly), perl(Readonly::XS).

* Sun Aug 14 2005 Ralf Corsepius <ralf@links2linux.de> - 0.78-2
- Spec file cleanup.

* Wed Aug 10 2005 Ralf Corsepius <ralf@links2linux.de> - 0.78-1
- FE submission.
