Name:           perl-File-MMagic
Version:	1.30
Release:	3%{?dist}
Summary:        A Perl module emulating the file(1) command
Group:          Development/Libraries
License:        ASL 1.0 and BSD
URL:            http://search.cpan.org/dist/File-MMagic/
Source0:        http://www.cpan.org/authors/id/K/KN/KNOK/File-MMagic-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(base)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
This module attempts to guess a file's type from its contents like the file(1)
command.

%prep
%setup -q -n File-MMagic-%{version}
iconv -f ISO-2022-JP -t utf8 README.ja > README.ja.utf8 && mv README.ja.utf8 README.ja

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} %{buildroot}

%check


%files
%doc ChangeLog COPYING README.en README.ja
%{perl_vendorlib}/File/
%{_mandir}/man3/File::MMagic.3pm*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 1.30-3
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1.30-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.30-1
- 更新到 1.30

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.29-5
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.29-4
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.29-3
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul 12 2012 Paul Howarth <paul@city-fan.org> - 1.29-1
- Update to 1.29
  - MMagic.pm (checktype_contents): fix infinite loop bug (CPAN RT#77836)
- BR: perl(base) and perl(Test::More)
- Use DESTDIR rather than PERL_INSTALL_ROOT
- Use %%{_fixperms} macro rather than our own chmod incantation
- Don't need to remove empty directories from the buildroot
- Make %%files list more explicit
- Tweak %%description

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1.28-2
- Perl 5.16 rebuild

* Tue Jun 05 2012 Petr Šabata <contyk@redhat.com> - 1.28-1
- 1.28 bump
- Modernizing spec (removing buildroot, defattr, and command macros)
- Removing trailing whitespace
- Packaging README.ja

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.27-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.27-12
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.27-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.27-10
- 661697 rebuild for fixing problems with vendorach/lib

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.27-9
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.27-8
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.27-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.27-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb  2 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.27-5
- rebuild for new perl

* Fri Oct 26 2007 Robin Norwood <rnorwood@redhat.com> - 1.27-4
- Remove BR: perl for package review
- Resolves: bz#226257

* Wed Aug 29 2007 Robin Norwood <rnorwood@redhat.com> - 1.27-3
- Update license tag
- Add BuildRequires: perl(ExtUtils::MakeMaker)

* Fri Jul 20 2007 Robin Norwood <rnorwood@redhat.com> - 1.27-2.fc8
- Add fixes from EPEL branch
- Fix minor specfile issues

* Mon Jun 05 2006 Jason Vas Dias <jvdias@redhat.com> - 1.27-1
- Upgrade to 1.27

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 1.26-1
- Upgrade to 1.26
- rebuild for new perl-5.8.8

* Tue Jan 10 2006 Jason Vas Dias <jvdias@redhat.com> - 1.25-1
- fix bug 176717: upgrade to 1.25

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc

* Sat Apr 02 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.22-1
- Update to 1.22
- Spec cleanup (#153204)

* Wed Sep 22 2004 Chip Turner <cturner@redhat.com> 1.21-2
- rebuild

* Fri Feb 13 2004 Chip Turner <cturner@redhat.com> 1.21-1
- move to 1.21

* Tue Dec 10 2002 Chip Turner <cturner@redhat.com>
- update to latest version from CPAN

* Tue Aug  6 2002 Chip Turner <cturner@redhat.com>
- automated release bump and build

* Tue Aug  6 2002 Chip Turner <cturner@localhost.localdomain>
- update to 1.15

* Fri Dec 7 2001 root <root@redhat.com>
- Spec file was autogenerated.
