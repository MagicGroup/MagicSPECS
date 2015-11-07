# RPM version needs 4 digits after the decimal to preserve upgrade path
%global module_version 0.500
%global RPM_version %(echo %{module_version} | %{__perl} -pi -e 's/(.*)/sprintf("%.4f", $1)/e')

Name:           perl-Test-Differences
Version:	0.63
Release:	2%{?dist}
Summary:        Test strings and data structures and show differences if not OK

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Test-Differences/
Source0:        http://search.cpan.org/CPAN/authors/id/O/OV/OVID/Test-Differences-%{module_version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
# Run-time
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Text::Diff) >= 0.35
# Tests
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::More)
# Optional tests
BuildRequires:  perl(Test::Pod) >= 1.08
BuildRequires:  perl(Test::Pod::Coverage) >= 0.18
# not detected
Requires:       perl(Carp)
Requires:       perl(Data::Dumper)
Requires:       perl(Text::Diff) >= 0.35
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
When the code you're testing returns multiple lines, records or data
structures and they're just plain wrong, an equivalent to the Unix
diff utility may be just what's needed.


%prep
%setup -q -n Test-Differences-%{module_version}


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



%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/Test/
%{_mandir}/man3/Test::Differences.3pm*


%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.63-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.63-1
- 更新到 0.63

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.5000-10
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.5000-9
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5000-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 0.5000-7
- Perl 5.16 rebuild
- Specify all dependencies

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5000-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.5000-5
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5000-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.5000-3
- 661697 rebuild for fixing problems with vendorach/lib

* Thu Jul 08 2010 Iain Arnell <iarnell@gmail.com> 0.500-2
- explicitly require perl(Text::Diff)

* Tue Jun 29 2010 Paul Howarth <paul@city-fan.org> - 0.5000-1
- Update to 0.500
  - Add support for all diff styles supplied by Text::Diff (CPAN RT#23579)
  - Add Build.PL
  - Convert to universally use Test::More instead of Test
  - Convert to modern Perl distribution.
  - Applied doc suggestion from CPAN RT#24297
  - Fix the { a => 1 } versus { a => '1' } bug (CPAN RT#3029)
- Upstream dropped eg/ docs
- Bump perl(Text::Diff) requirement to 0.35
- BR: perl(Test::Pod) and perl(Test::Pod::Coverage) for extra test cover

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.4801-5
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.4801-4
- rebuild against perl 5.10.1

* Wed Aug 19 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 0.4801-3
- fix source url

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4801-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar 13 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 0.4801-1
- update to 0.4801

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.47-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.47-4
- Rebuild for perl 5.10 (again)

* Thu Jan 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.47-3
- rebuild for new perl

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.47-2.2
- add BR: perl(Test::More)

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.47-2.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Sun May 14 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.47-2
- Bumping release (repodata checksum inconsistency for previous release).

* Mon May 01 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.47-1
- First build.
