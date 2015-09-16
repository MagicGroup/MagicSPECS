Name:           perl-Class-MethodMaker
Version:	2.24
Release:	1%{?dist}
Summary:        Perl module for creating generic object-oriented methods

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/~schwigon/Class-MethodMaker/
Source0:        http://search.cpan.org/CPAN/authors/id/S/SC/SCHWIGON/class-methodmaker/Class-MethodMaker-%{version}.tar.gz

BuildRequires:  perl(ExtUtils::MakeMaker)
# Required by the tests
BuildRequires:  perl(IPC::Run)

Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
Class::MethodMaker solves the problem of having to continually write accessor
methods for your objects that perform standard tasks.

%prep
%setup -q -T -c
%setup -q -T -D -a0

%build
cd Class-MethodMaker-%{version}
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}
cd ..

%install
cd Class-MethodMaker-%{version}
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
cd ..
find $RPM_BUILD_ROOT -type f -a \( -name .packlist \
  -o \( -name '*.bs' -a -empty \) \) -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%check
cd Class-MethodMaker-%{version}

cd ..

%files
%defattr(-,root,root,-)
%doc Class-MethodMaker-%{version}/Changes Class-MethodMaker-%{version}/README Class-MethodMaker-%{version}/TODO
%{perl_vendorarch}/Class/
%{perl_vendorarch}/auto/*
%{_mandir}/man3/*.3*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 2.24-1
- 更新到 2.24

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 2.18-17
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 2.18-16
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 2.18-15
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 2.18-14
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 2.18-13
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 2.18-12
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.18-11
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.18-10
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.18-9
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.18-8
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 2.18-7
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 2.18-6
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 2.18-5
- 为 Magic 3.0 重建

* Sun Jan 22 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.18-4
- Add %%{perl_default_filter}.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 24 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.18-2
- Perl mass rebuild

* Sun Apr 17 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.18-1
- Upstream update.

* Mon Mar 28 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.17-1
- Upstream update.
- Spec file cleanup.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.16-3
- 661697 rebuild for fixing problems with vendorach/lib

* Tue May 18 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.16-2
- Rebuild with perl-5.12.0.

* Tue May 18 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.16-1
- Upstream update.

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.15-4
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 2.15-3
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Mar 01 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.15-1
- Upstream update.
- Build in subdir to work-around rpm breaking the testsuite.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Dec 20 2008 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.13-1
- Upstream update.

* Fri Sep  5 2008 Daniel P. Berrange <berrange@redhat.com> - 2.12-1
- Update to new release for rhbz #461285

* Fri Jul 18 2008 Ralf Corsépius <rc040203@freenet.de> - 2.11-1
- Upstream update.

* Fri Jul 18 2008 Ralf Corsépius <rc040203@freenet.de> - 2.10-4
- Remove %%clean ||: (BZ 449442, FTBFS).
- Use %%version in Source0-URL.
- Don't skip 0-signature.t.
- Misc. minor spec-file overhaul.

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.10-3
- Rebuild for perl 5.10 (again)

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.10-2
- Autorebuild for GCC 4.3

* Tue Jan 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.10-1
- fix compile bug by going to 2.10 (CPAN says it is unauthorized, 
  but the copyright holder says it is ok)

* Mon Jan 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.08-5
- rebuild for new perl

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 2.08-4.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Fri Feb 17 2006 Dennis Gregorovic <dgregor@redhat.com> - 2.08-4
- Rebuild for FC6

* Fri Feb 17 2006 Dennis Gregorovic <dgregor@redhat.com> - 2.08-3
- Appended the dist tag to the Release number

* Fri Feb 17 2006 Dennis Gregorovic <dgregor@redhat.com> - 2.08-2
- Rebuild for FC5 (perl 5.8.8)

* Sat Feb 11 2006 Dennis Gregorovic <dgregor@redhat.com> - 2.08-1
- Rebuilt for version 2.08 of source

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 2.06-3
- rebuild on all arches

* Mon Mar 21 2005 Dennis Gregorovic <dgregor@redhat.com> - 2.06-2
- Rebuilt for version 2.06 of source

* Thu Feb 24 2005 Dennis Gregorovic <dgregor@redhat.com> - 2.05-2
- Incorporated feedback from Jose Pedro Oliveira. (#149637)

* Fri Feb  4 2005 Dennis Gregorovic <dgregor@redhat.com> - 2.05-1
- First build.
