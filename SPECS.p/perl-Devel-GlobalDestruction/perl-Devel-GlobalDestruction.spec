# Package is noarch from perl 5.13.7
%global noarch_package %(perl -e 'print (($] >= 5.013007) ? 1 : 0);')

Name:		perl-Devel-GlobalDestruction
Version:	0.09
Release:	2%{?dist}
License:	GPL+ or Artistic
Group:		Development/Libraries
Summary:	Expose PL_dirty, the flag that marks global destruction
Url:		http://search.cpan.org/dist/Devel-GlobalDestruction
Source:		http://search.cpan.org/CPAN/authors/id/R/RI/RIBASUSHI/Devel-GlobalDestruction-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
%if %{noarch_package}
BuildArch:	noarch
%else
BuildRequires:	perl(ExtUtils::CBuilder) >= 0.27
BuildRequires:	perl(XSLoader)
Requires:	perl(XSLoader)
%endif
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(File::Temp)
BuildRequires:	perl(Sub::Exporter::Progressive) >= 0.001002
BuildRequires:	perl(threads)
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	perl(Carp)

# Don't "provide" private Perl libs
%{?perl_default_filter}

%description
Perl's global destruction is a little tricky to deal with with respect to
finalizers because it's not ordered and objects can sometimes disappear.

Writing defensive destructors is hard and annoying, and usually if global
destruction is happening you only need the destructors that free up non
process local resources to actually execute.

For these constructors you can avoid the mess by simply bailing out if
global destruction is in effect.

%prep
%setup -q -n Devel-GlobalDestruction-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
%{_fixperms} %{buildroot}

%check


%clean
rm -rf %{buildroot}

%files
%doc Changes t/
%if %{noarch_package}
%{perl_vendorlib}/Devel/
%else
%{perl_vendorarch}/auto/Devel/
%{perl_vendorarch}/Devel/
%endif
%{_mandir}/man3/Devel::GlobalDestruction.3pm*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.09-2
- 为 Magic 3.0 重建

* Thu Aug  9 2012 Paul Howarth <paul@city-fan.org> - 0.09-1
- Update to 0.09
  - Rewrite completely broken pure-perl GD detection under threads
  - Fix pure-perl implementation incorrectly reporting GD during END phase
- This release by RIBASUSHI -> update source URL

* Wed Aug  1 2012 Paul Howarth <paul@city-fan.org> - 0.08-1
- Update to 0.08
  - Switch to Sub::Exporter::Progressive
- BR: perl(Sub::Exporter::Progressive) ≥ 0.001002 rather than plain
  perl(Sub::Exporter)

* Thu Jul 26 2012 Paul Howarth <paul@city-fan.org> - 0.07-1
- Update to 0.07
  - Actually detect errors in pure-perl test
  - Add prototype to pure-perl pre-5.14 version
- This release by FLORA -> update source URL
- BR: perl(File::Spec), perl(File::Temp) and perl(threads)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 28 2012 Petr Pisar <ppisar@redhat.com> - 0.06-2
- Perl 5.16 rebuild

* Thu Jun 14 2012 Paul Howarth <paul@city-fan.org> - 0.06-1
- Update to 0.06
  - De-retardize XS-less behavior under SpeedyCGI
  - Test suite now works from within space-containing paths
- This release by RIBASUSHI -> update source URL

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 0.05-2
- Perl 5.16 rebuild

* Fri Apr 27 2012 Paul Howarth <paul@city-fan.org> - 0.05-1
- Update to 0.05
  - Add pure-perl implementation for situations where neither ${^GLOBAL_PHASE}
    nor XS are available
- This release by DOY -> update source URL
- BR: perl(XSLoader) only if we're doing an XS build, and in that case add a
  runtime dependency on it and BR: perl(ExtUtils::CBuilder) ≥ 0.27 too
- Add runtime dependency on perl(Carp)
- Drop %%defattr, redundant since rpm 4.4

* Fri Jan 13 2012 Paul Howarth <paul@city-fan.org> - 0.04-1
- Update to 0.04
  - To detect a perl with ${^GLOBAL_PHASE}, check for the feature itself
    instead of a specific perl version
  - Update the documentation to reflect the use of ${^GLOBAL_PHASE} if available
  - Stop depending on Scope::Guard for the tests
  - Upgrade ppport.h from version 3.13 to 3.19
- Drop no-longer-necessary buildreq perl(Scope::Guard)
- Use DESTDIR rather than PERL_INSTALL_ROOT
- BR: perl(XSLoader)

* Wed Jan 11 2012 Paul Howarth <paul@city-fan.org> - 0.03-3
- Fedora 17 mass rebuild

* Wed Jun 29 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.03-2
- Perl mass rebuild

* Fri Jun 24 2011 Paul Howarth <paul@city-fan.org> - 0.03-1
- Update to 0.03
  - Drop the XS code on perl versions recent enough to have ${^GLOBAL_PHASE}
    (5.13.7 onwards)
  - Require at least Perl 5.6
    - Use XSLoader without a fallback to DynaLoader
    - Use our instead of use vars
- This release by FLORA -> update source URL
- Package is noarch from perl 5.13.7
- Package Changes file
- Use %%{?perl_default_filter}

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.02-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.02-11
- Rebuild to fix problems with vendorarch/lib (#661697)

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.02-10
- Mass rebuild with perl-5.12.0

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.02-9
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.02-8
- rebuild against perl 5.10.1

* Sun Aug 23 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.02-7
- bump

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.02-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Chris Weyl <cweyl@alumni.drew.edu> - 0.02-5
- Stripping bad provides of private Perl extension libs

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.02-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Nov 03 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.02-3
- bump

* Sat Nov 01 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.02-2
- tweak summary

* Sun Oct 26 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.02-1
- clean up for review submission

* Sun Oct 19 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.02-0.1
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.5)

