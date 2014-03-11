Name:           perl-GnuPG-Interface
Version:        0.44
Release:        6%{?dist}
Summary:        Perl interface to GnuPG
Group:          Development/Libraries
License:        GPLv2+ or Artistic
URL:            http://search.cpan.org/dist/GnuPG-Interface
Source0:        http://cpan.org/modules/by-module/GnuPG/GnuPG-Interface-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  gpg
BuildRequires:  perl(Any::Moose)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Pod::Perldoc)

Requires:       gpg
Requires:       perl(Any::Moose)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
%{summary}.

%prep
%setup -q -n GnuPG-Interface-%{version}
perldoc -t perlgpl > GPL
perldoc -t perlartistic > Artistic


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%check
chmod 0700 test
# GnuPG-Interface needs to read from /dev/tty to run its tests.
# 

%files
%doc ChangeLog README NEWS THANKS COPYING GPL Artistic
%{perl_vendorlib}/GnuPG
%{_mandir}/man3/*.3*


%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.44-6
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.44-5
- 为 Magic 3.0 重建

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
  lets '' succeed after 2006-02-05.
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
