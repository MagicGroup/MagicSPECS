Name:           perl-Carp-Clan
Version:        6.04
Release:        12%{?dist}
Summary:        Perl module to print improved warning messages

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Carp-Clan/
Source0:        http://www.cpan.org/authors/id/S/ST/STBEY/Carp-Clan-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
%if !%{defined perl_bootstrap}
BuildRequires:  perl(Test::Exception)
BuildRequires:  perl(Object::Deadly)
%endif
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(DB\\)

%description
This module reports errors from the perspective of the caller of a
"clan" of modules, similar to "Carp.pm" itself. But instead of giving
it a number of levels to skip on the calling stack, you give it a
pattern to characterize the package names of the "clan" of modules
which shall never be blamed for any error.


%prep
%setup -q -n Carp-Clan-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*


%check
%if !%{defined perl_bootstrap}

%endif

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README Changes license/Artistic.txt license/GNU_GPL.txt
%{perl_vendorlib}/Carp/
%{_mandir}/man3/*.3*


%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 6.04-12
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 6.04-11
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 6.04-10
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.04-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 6.04-8
- Perl 5.16 re-rebuild of bootstrapped packages

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 6.04-7
- Perl 5.16 rebuild

* Thu May 31 2012 Petr Pisar <ppisar@redhat.com> - 6.04-6
- Do not export private modules

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.04-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 28 2011 Marcela Mašláňová <mmaslano@redhat.com> - 6.04-4
- rebuild with Perl 5.14.1
- use perl_bootstrap macro

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 6.04-3
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 6.04-2
- Mass rebuild with perl-5.12.0

* Wed Jan 27 2010 Stepan Kasal <skasal@redhat.com> - 6.04-1
- new upstream version

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 6.03-2
- rebuild against perl 5.10.1

* Mon Oct 19 2009 Marcela Mašláňová <mmaslano@redhat.com> - 6.031
- update to 6.03

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.00-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Mar 22 2009 Robert Scheck <robert@fedoraproject.org> - 6.00-4
- Really remove the no-prompt patch to avoid RPM rebuild errors

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.00-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.00-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul 22 2008 Marcela Maslanova <mmaslano@redhat.com> - 6.0-1
- update to 6.0

* Tue Feb  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 5.9-5
- rebuild for new perl (normally)

* Sat Feb  2 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 5.9-4.1
- temporarily disable BR on Object::Deadly, tests

* Mon Nov 19 2007 Robin Norwood <rnorwood@redhat.com> - 5.9-4
- Add BR: perl-Object-Deadly now that it is included in Fedora

* Wed Oct 24 2007 Robin Norwood <rnorwood@redhat.com> - 5.9-3
- Fix BuildRequires
- Various specfile cleanups

* Thu Aug 23 2007 Robin Norwood <rnorwood@redhat.com> - 5.9-2
- Update license tag.

* Mon Jun 04 2007 Robin Norwood <rnorwood@redhat.com> - 5.9-1
- Update to latest CPAN version: 5.9
- Upstream Makefile.PL prompts for user input to include
  Object::Deadly as a prerequisite.  We don't ship Object::Deadly, so
  just comment out the prompt.

* Fri Jan 26 2007 Robin Norwood <rnorwood@redhat.com> - 5.8-2
- Resolves: bz#224571 - Remove erroneous rpm 'provides' of perl(DB)

* Sat Dec 02 2006 Robin Norwood <rnorwood@redhat.com> - 5.8-1
- New version

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - sh: line 0: fg: no job control
- rebuild

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 5.3-2
- rebuild for perl-5.8.8

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc

* Sat Apr 02 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 5.3-1
- First build.
