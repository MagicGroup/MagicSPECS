Name:		perl-Test-NoTabs
Version:	1.4
Release:	3%{?dist}
Summary:	Check the presence of tabs in your project
Group:		Development/Libraries
License:	GPL+ or Artistic
URL:		http://search.cpan.org/dist/Test-NoTabs/
Source0:	http://search.cpan.org/CPAN/authors/id/B/BO/BOBTFISH/Test-NoTabs-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
BuildRequires:	perl(Cwd)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(File::Temp)
BuildRequires:	perl(Test::Builder)
BuildRequires:	perl(Test::More)
BuildRequires:	perl(Test::Pod)
BuildRequires:	perl(Test::Pod::Coverage)
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
This module scans your project/distribution for any perl files (scripts,
modules, etc.) for the presence of tabs.

%prep
%setup -q -n Test-NoTabs-%{version}

%build
perl Makefile.PL --skip INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
%{_fixperms} %{buildroot}

%check


%clean
rm -rf %{buildroot}

%files
%doc Changes README
%{perl_vendorlib}/Test/
%{_mandir}/man3/Test::NoTabs.3pm*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 1.4-3
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1.4-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.4-1
- 更新到 1.4

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.3-5
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.3-4
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 28 2012 Petr Pisar <ppisar@redhat.com> - 1.3-2
- Perl 5.16 rebuild

* Tue Jun 26 2012 Paul Howarth <paul@city-fan.org> - 1.3-1
- Update to 1.3
  - Fix regex to ignore '.svn', but not 'Xsvn' - unescaped

* Sun Jun 17 2012  Paul Howarth <paul@city-fan.org> - 1.2-1
- Update to 1.2
  - Fix to ignore inc/ for Module::Install
- BR: perl(Cwd), perl(ExtUtils::MakeMaker), perl(File::Spec), perl(File::Temp)
  and perl(Test::Builder)
- Don't need to remove empty directories from the buildroot
- Use DESTDIR rather than PERL_INSTALL_ROOT
- Drop %%defattr, redundant since rpm 4.4

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 1.1-4
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.1-2
- Perl mass rebuild

* Fri Apr 29 2011 Paul Howarth <paul@city-fan.org> 1.1-1
- Update to 1.1
  - Fix test fails if cwd or perl has a space in its path (CPAN RT#67376)
- Remove remaining uses of macros for commands

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> 1.0-4
- Rebuild to fix problems with vendorarch/lib (#661697)

* Wed Jun 16 2010 Paul Howarth <paul@city-fan.org> 1.0-3
- Clean up for Fedora submission

* Mon May 17 2010 Paul Howarth <paul@city-fan.org> 1.0-2
- Fix dist tag for RHEL-6 Beta

* Thu Feb 11 2010 Paul Howarth <paul@city-fan.org> 1.0-1
- Update to 1.0 (patches upstreamed)

* Wed Feb 10 2010 Paul Howarth <paul@city-fan.org> 0.9-2
- Add patch and test case for CPAN RT#53727 (broken POD breaks tab detection)
- Fix a `Parentheses missing around "my" list' warning in old Perls (RT#54477)

* Mon Feb  1 2010 Paul Howarth <paul@city-fan.org> 0.9-1
- Initial RPM version
