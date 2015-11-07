Name:           perl-GnuPG-Interface
Version:	0.52
Release:	2%{?dist}
Summary:        Perl interface to GnuPG
Group:          Development/Libraries
License:        GPLv2+ or Artistic
URL:            http://search.cpan.org/dist/GnuPG-Interface
Source0:        http://cpan.org/modules/by-module/GnuPG/GnuPG-Interface-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  gpg

BuildRequires:  perl(Carp)
BuildRequires:  perl(Class::Struct)
BuildRequires:  perl(Config)
BuildRequires:  perl(constant)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(English)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Fatal)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(File::Compare)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IO::Seekable)
BuildRequires:  perl(lib)
BuildRequires:  perl(Math::BigInt)
BuildRequires:  perl(Module::Install::Base)
BuildRequires:  perl(Moo)
BuildRequires:  perl(Moo::Role)
BuildRequires:  perl(MooX::HandlesVia)
BuildRequires:  perl(MooX::late)
BuildRequires:  perl(strict)
BuildRequires:  perl(Symbol)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)

Requires:       gpg
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
%{summary}.

%prep
%setup -q -n GnuPG-Interface-%{version}
perldoc -t perlgpl > GPL
perldoc -t perlartistic > Artistic
# gpg as being used by the testsuite requires test to be 0700
chmod 0700 test

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%check
make test

%files
%doc Changes README
%{perl_vendorlib}/GnuPG
%{_mandir}/man3/*.3*


%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.52-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.52-1
- 更新到 0.52

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.50-5
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.50-4
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.50-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Apr 19 2014 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.50-2
- Rework BR:s (RHBZ #1079473).
- Reactivate tests.

* Sun Mar 16 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 0.50-1
- Update to 0.50

* Sun Aug 04 2013 Petr Pisar <ppisar@redhat.com> - 0.46-4
- Perl 5.18 rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.46-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.46-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Oct 28 2012 Emmanuel Seyman <emmanuel@seyman.fr> - 0.46-1
- Update to 0.46

* Sun Sep 30 2012 Emmanuel Seyman <emmanuel@seyman.fr> - 0.45-1
- Update to 0.45
- Remove BuildRoot definition

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.44-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Petr Pisar <ppisar@redhat.com> - 0.44-5
- Perl 5.16 rebuild

* Mon Jan 16 2012 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 0.44-1
- Add Pod::Perldoc (perldoc) as a BR
- Clean up spec file
- Add perl default filter

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.44-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.44-2
- Perl mass rebuild

* Tue May 03 2011 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 0.44-1
- Update to 0.44

* Thu Mar 10 2011 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 0.43-2
- Bump to build the release

* Thu Mar 10 2011 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 0.43-1
- Update to 0.43

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.42-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 17 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.42-5
- 661697 rebuild for fixing problems with vendorach/lib

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.42-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.42-3
- rebuild against perl 5.10.1

* Sun Oct 04 2009 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 0.42-2
- Disable tests because they need /dev/tty to run

* Fri Oct 02 2009 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 0.42-1
- Update to 0.42
- Fix rpmlint errors

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.36-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.36-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Apr 20 2008 Matt Domsch <Matt_Domsch@dell.com> 0.36-1
- new upstream, alreadly includes our patches

* Tue Feb  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.33-10
- rebuild for new perl

* Sun Aug 12 2007 Matt Domsch <Matt_Domsch@dell.com> - 0.33-9
- add BR perl(ExtUtils::MakeMaker)

* Mon Oct 02 2006 Matt Domsch <Matt_Domsch@dell.com> - 0.33-8
- rebuild

* Sat Sep  2 2006 Matt Domsch <Matt_Domsch@dell.com> 0.33-7
- rebuild for FC6

* Mon Feb 13 2006 Matt Domsch <Matt_Domsch@dell.com> 0.33-6
- add 10 years to expiry date of test gpg keys,
  lets 'make test' succeed after 2006-02-05.
- rebuild for FC5

* Thu Oct 06 2005 Ralf Corsepius <rc040203@freenet.de> - 0.33-5
- Requires: perl(Class::MethodMaker) (PR #169976).

* Tue Sep 13 2005 Tom "spot" Callaway <tcallawa@redhat.com> 0.33-4
- FC-3 doesn't use the patch1

* Sun Sep 11 2005 Matt Domsch <matt@domsch.com> 0.33-3
- use perldoc -t and the _smp_mflags macro

* Sun Aug 28 2005 Matt Domsch <matt@domsch.com> 0.33-2
- add Requires: gpg, always apply secret-key-output-1.patch, as it works on
  both gpg 1.4 and gpg2.

* Thu Aug 25 2005 Matt Domsch <matt@domsch.com> 0.33-1
- specfile changes per Paul Howarth's comments
- added GnuPG-Interface-0.33.tru-record-type.txt patch,
  borrowed from Mail-GPG-1.0.1

* Wed Aug 24 2005 Matt Domsch <matt@domsch.com> 0.33-0
- Initial package for Fedora Extras
