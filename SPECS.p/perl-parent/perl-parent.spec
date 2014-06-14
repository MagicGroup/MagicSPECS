Name:		perl-parent
Epoch:		1
Version:	0.228
Release:	2%{?dist}
Summary:	Establish an ISA relationship with base classes at compile time
License:	GPL+ or Artistic
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/parent/
Source0:	http://search.cpan.org/CPAN/authors/id/C/CO/CORION/parent-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(lib)
BuildRequires:	perl(Test::More) >= 0.4
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
Allows you to both load one or more modules, while setting up inheritance
from those modules at the same time. Mostly similar in effect to:

	package Baz;

	BEGIN {
		require Foo;
		require Bar;

		push @ISA, qw(Foo Bar);
	}

%prep
%setup -q -n parent-%{version}

# Remove spurious exec permissions
chmod -c -x Changes lib/parent.pm

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
%{_fixperms} %{buildroot}

%check
make test

%clean
rm -rf %{buildroot}

%files
%doc Changes
%{perl_vendorlib}/parent.pm
%{_mandir}/man3/parent.3pm*

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.228-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Sep 17 2013 Paul Howarth <paul@city-fan.org> - 1:0.228-1
- Update to 0.228
  - Install in site/ by default for 5.12+ (CPAN RT#88450)

* Sun Sep  1 2013 Paul Howarth <paul@city-fan.org> - 1:0.227-1
- Update to 0.227
  - Restore tests passing for 5.17.5+ (CPAN RT#88320)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.226-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 29 2013 Paul Howarth <paul@city-fan.org> - 1:0.226-1
- Update to 0.226
  - Fix tests for Perl 5.18 (CPAN RT#86890)

* Mon Jul 15 2013 Petr Pisar <ppisar@redhat.com> - 1:0.225-290
- Increase release to favour standalone package

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 1:0.225-245
- Link minimal build-root packages against libperl.so explicitly

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 1:0.225-244
- Adjust tests to perl-5.18 (CPAN RT#86890)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.225-243
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Aug 25 2012 Paul Howarth <paul@city-fan.org> - 1:0.225-242
- Don't need to remove empty directories from the buildroot
- Drop %%defattr, redundant since rpm 4.4

* Wed Aug 15 2012 Petr Pisar <ppisar@redhat.com> - 1:0.225-241
- Specify all dependencies

* Mon Aug 13 2012 Marcela Mašláňová <mmaslano@redhat.com> - 1:0.225-240
- Bump release to override sub-package from perl.spec

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.225-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 1:0.225-7
- Perl 5.16 rebuild

* Tue Feb  7 2012 Paul Howarth <paul@city-fan.org> - 1:0.225-6
- Reinstate compatibility with old distributions like EL-5
  - Add back buildroot definition and cleaning
- Use DESTDIR rather than PERL_INSTALL_ROOT
- Make %%files list more explicit
- Drop redundant %%{?perl_default_filter}
- Don't use macros for commands
- Use tabs

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.225-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Aug 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1:0.225-4
- Install to vendor directories rather than perl core directories so as to
  avoid conflicts between our debuginfo and the main perl-debuginfo package

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1:0.225-3
- Perl mass rebuild

* Tue Jun 14 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1:0.225-2
- Perl mass rebuild

* Sat May 07 2011 Iain Arnell <iarnell@gmail.com> - 1:0.225-1
- Update to latest upstream version
- Clean up spec for modern rpmbuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.224-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Nov 21 2010 Iain Arnell <iarnell@gmail.com> - 1:0.224-1
- Update to latest upstream version

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 1:0.223-4
- Mass rebuild with perl-5.12.0

* Sat Mar 27 2010 Iain Arnell <iarnell@gmail.com> - 1:0.223-3
- Dual-life module
- Add epoch to match that of parent in core
- Use core macros, not vendor

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.223-2
- Rebuild against perl 5.10.1

* Fri Sep 11 2009 Chris Weyl <cweyl@alumni.drew.edu> - 0.223-1
- Update filtering
- Auto-update to 0.223 (by cpan-spec-update 0.01)
- Altered br on perl(Test::More) (0 => 0.4)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.221-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.221-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jun 19 2008 Chris Weyl <cweyl@alumni.drew.edu> - 0.221-2
- Bump

* Wed May 28 2008 Chris Weyl <cweyl@alumni.drew.edu> - 0.221-1
- Specfile autogenerated by cpanspec 1.75
