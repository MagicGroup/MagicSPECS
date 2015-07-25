Name:		perl-List-MoreUtils
Version:	0.33
Release:	14%{?dist}
Summary:	Provide the stuff missing in List::Util
Group:		Development/Libraries
License:	GPL+ or Artistic
URL:		http://search.cpan.org/dist/List-MoreUtils/
Source0:	http://search.cpan.org/CPAN/authors/id/A/AD/ADAMK/List-MoreUtils-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildRequires:	perl(Carp)
BuildRequires:	perl(constant)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(ExtUtils::CBuilder)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(Pod::Simple)
BuildRequires:	perl(Test::CPAN::Meta)
# For EL-7 onwards, this package is imported to RHEL, where Test::LeakTrace in EPEL isn't available
%if 0%{?rhel} < 7
BuildRequires:	perl(Test::LeakTrace)
%endif
# Test::MinimumVersion -> Perl::MinimumVersion -> PPI -> List::MoreUtils
%if 0%{!?perl_bootstrap:1}
BuildRequires:	perl(Test::MinimumVersion)
%endif
BuildRequires:	perl(Test::More) >= 0.42
BuildRequires:	perl(Test::Pod)
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	perl(Carp)

# Don't "provide" private Perl libs
%if 0%{?rhel}%{?fedora} < 6
%global _use_internal_dependency_generator 0
%global __deploop() while read FILE; do /usr/lib/rpm/rpmdeps -%{1} ${FILE}; done | sort -u
%global __find_provides /bin/sh -c "grep -v '%{perl_vendorarch}/.*\\.so$' | %{__deploop P}"
%global __find_requires /bin/sh -c "%{__deploop R}"
%else
%{?perl_default_filter}
%endif

%description
List::MoreUtils provides some trivial but commonly needed functionality
on lists that is not going to go into List::Util.

%prep
%setup -q -n List-MoreUtils-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -empty -exec rm -f {} ';'
%{_fixperms} %{buildroot}

%check

 TEST_FILES="xt/*.t" AUTOMATED_TESTING=1

%clean
rm -rf %{buildroot}

%files
%doc Changes README LICENSE
%{perl_vendorarch}/List/
%{perl_vendorarch}/auto/List/
%{_mandir}/man3/List::MoreUtils.3pm*

%changelog
* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.33-14
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.33-13
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.33-12
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.33-11
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.33-10
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.33-9
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.33-8
- 为 Magic 3.0 重建

* Wed Oct 17 2012 Paul Howarth <paul@city-fan.org> - 0.33-7
- BR:/R: perl(Carp)
- BR: perl(constant), perl(Exporter) and perl(ExtUtils::CBuilder)
- Add commentary regarding non-use of Test::LeakTrace for EL-7 builds
- Use Test::LeakTrace for EL-5 builds
- Drop support for EL-4 builds since it was EOL-ed ages ago
- Drop %%defattr, redundant since rpm 4.4
- Don't need to remove empty directories from the buildroot
- Remove more command macros

* Mon Oct 15 2012 Petr Pisar <ppisar@redhat.com> - 0.33-6
- Do not build-require Test::LeakTrace on RHEL 7

* Fri Jul 27 2012 Tom Callaway <spot@fedoraproject.org> - 0.33-5
- Add epel filtering mechanism

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.33-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 0.33-3
- Perl 5.16 re-rebuild of bootstrapped packages

* Tue Jun 19 2012 Petr Pisar <ppisar@redhat.com> - 0.33-2
- Perl 5.16 rebuild

* Tue Jan 24 2012 Paul Howarth <paul@city-fan.org> - 0.33-1
- Update to 0.33
  - Updated can_xs to fix a bug in it
- Reinstate compatibility with old distributions like EL-5
- Drop Test::More version requirement to 0.42
- BR: perl(ExtUtils::MakeMaker)
- BR: perl(Test::LeakTrace) except on EL-4/EL-5 where it's not available
- BR: perl(Pod::Simple), perl(Test::CPAN::Meta), perl(Test::MinimumVersion)
  (if we're not bootstrapping) and perl(Test::Pod), and run the developer tests
  too
- Don't use macros for commands
- Use %%{_fixperms} macro rather than our own chmod incantation
- Make %%files list more specific
- Use tabs

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.32-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jul 18 2011 Petr Sabata <contyk@redhat.com> - 0.32-3
- Perl mass rebuild

* Tue Jul 12 2011 Tom Callaway <spot@fedoraproject.org> - 0.32-2
- Rebuild to fix broken rawhide deps

* Sat Jul 02 2011 Iain Arnell <iarnell@gmail.com> - 0.32-1
- Update to latest upstream version

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.30-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.30-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 03 2011 Iain Arnell <iarnell@gmail.com> - 0.30-1
- Update to latest upstream version
- Clean up spec for modern rpmbuild
- Use perl_default_filter
- Remove unnecessary buildrequires

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.22-12
- Rebuild to fix problems with vendorarch/lib (#661697)

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.22-11
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.22-10
- Rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.22-6
- Rebuild normally, second pass

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.22-5
- Rebuild for perl 5.10 (again), tests disabled for first pass

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.22-4
- Autorebuild for GCC 4.3

* Mon Jan 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.22-3
- Rebuild normally, second pass

* Fri Jan 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.22-2.1
- Rebuild for new perl, first pass, disable TPC and tests

* Sun Sep 10 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.22-2
- Rebuild for FC6

* Mon Jul  3 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.22-1
- Update to 0.22

* Mon Jun 19 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.21-1
- Update to 0.21

* Sat Jun 10 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.20-1
- Update to 0.20

* Sat Apr 22 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.19-1
- First build
