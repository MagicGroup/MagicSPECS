Name:           perl-Text-CSV_XS
Version:        0.91
Release:        3%{?dist}
Summary:        Comma-separated values manipulation routines
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Text-CSV_XS/
Source0:        http://www.cpan.org/authors/id/H/HM/HMBRAND/Text-CSV_XS-%{version}.tgz
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(Test::Harness)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
BuildRequires:  perl(Tie::Scalar)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%{?perl_default_filter}

%description
Text::CSV provides facilities for the composition and decomposition of
comma-separated values.  An instance of the Text::CSV class can combine
fields into a CSV string and parse a CSV string into fields.

%prep
%setup -q -n Text-CSV_XS-%{version}
iconv -f latin1 -t utf8 ChangeLog > ChangeLog.utf8 && mv ChangeLog.utf8 ChangeLog
chmod -c a-x examples/*
# Upstream does this on purpose (2011-03-23):
# "As Text::CSV_XS is so low-level, most of these files are actually *examples*
# and not ready-to-run out-of-the-box scripts that work as expected, though
# I must admit that some have evolved into being like that."
#find . -type f -exec sed -i '1s/pro/usr/' {} \;

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -empty -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w %{buildroot}/*

%check
# TODO: Parallel testing supported since 0.73


%files
%doc ChangeLog README examples/
%{perl_vendorarch}/Text/
%{perl_vendorarch}/auto/Text/
%{_mandir}/man3/*.3pm*

%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.91-3
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.91-2
- 为 Magic 3.0 重建

* Wed Aug 22 2012 Petr Šabata <contyk@redhat.com> - 0.91-1
- 0.91 bump (mostly test-cases updates)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.90-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 28 2012 Petr Pisar <ppisar@redhat.com> - 0.90-2
- Perl 5.16 rebuild

* Tue Jun 19 2012 Petr Šabata <contyk@redhat.com> - 0.90-1
- 0.90 bump

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.88-2
- Perl 5.16 rebuild

* Mon Mar 19 2012 Petr Pisar <ppisar@redhat.com> - 0.88-1
- 0.88 bump
- Fix parsing fields that contain excessive $/

* Wed Mar 14 2012 Petr Šabata <contyk@redhat.com> - 0.87-1
- 0.87 bump
- Remove command macros and defattr

* Tue Jan 24 2012 Marcela Mašláňová <mmaslano@redhat.com> - 0.86-1
- update to 0.86

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.85-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Sep 08 2011 Petr Sabata <contyk@redhat.com> - 0.85-1
- 0.85 bump

* Mon Aug 08 2011 Petr Sabata <contyk@redhat.com> - 0.83a-1
- 0.83a bump

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.82-2
- Perl mass rebuild

* Mon May  9 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.82-1
- update to 0.82

* Wed Mar 23 2011 Petr Sabata <psabata@redhat.com> - 0.81-2
- Revert example scripts interpreter changes

* Wed Mar 23 2011 Petr Sabata <psabata@redhat.com> - 0.81-1
- 0.81 version bump
- Changed script interpreters in various example files
- Convert ChangeLog to proper UTF8
- Removed buildroot garbage

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.80-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan  3 2011 Petr Sabata <psabata@redhat.com> - 0.80-1
- 0.80 version bump

* Thu Dec  2 2010 Petr Sabata <psabata@redhat.com> - 0.79-1
- 0.79 version bump

* Mon Oct 18 2010 Petr Sabata <psabata@redhat.com> - 0.76-1
- 0.76 version bump

* Mon Oct 11 2010 Petr Sabata <psabata@redhat.com> - 0.75-1
- 0.75 version bump

* Mon Oct 04 2010 Petr Pisar <ppisar@redhat.com> - 0.74-1
- 0.74 bump

* Wed Sep 08 2010 Petr Pisar <ppisar@redhat.com> - 0.73-1
- 0.73 bump

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.72-2
- Mass rebuild with perl-5.12.0

* Wed Mar 17 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.72-1
- PERL_INSTALL_ROOT => DESTDIR, add perl_default_filter (XS module)
- auto-update to 0.72 (by cpan-spec-update 0.01) (DBIx::Class needed a newer
  Text::CSV, which in turn can only leverage Text::CSV_XS >= 0.70)
- added a new br on perl(ExtUtils::MakeMaker) (version 0)
- added a new br on perl(IO::Handle) (version 0)
- added a new br on perl(Test::Harness) (version 0)
- added a new br on perl(Test::More) (version 0)
- added a new br on perl(Tie::Scalar) (version 0)

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.69-2
- rebuild against perl 5.10.1

* Mon Nov  2 2009 Stepan Kasal <skasal@redhat.com> - 0.69
- new upstream release

* Wed Oct  7 2009 Marcela Mašláňová <mmaslano@redhat.com> - 0.68-1
- update to new upstream release

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.58-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.58-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Dec 10 2008 Lubomir Rintel <lkundrak@v3.sk> - 0.58-1
- Update to latest upstream
- SvUPGRADE patch upstreamed

* Tue Jul 08 2008 Lubomir Rintel <lkundrak@v3.sk> - 0.52-2
- Actually solving the issue mentioned in previous change

* Tue Jul 08 2008 Lubomir Rintel <lkundrak@v3.sk> - 0.52-1
- Updated to 0.52 to solve an issue with perl 5.10

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.30-5
- Rebuild for perl 5.10 (again)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.30-4
- Autorebuild for GCC 4.3

* Sat Feb  2 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.30-3
- rebuild for new perl

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 0.30-2
- Rebuild for selinux ppc32 issue.

* Sat Jun 23 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.30-1
- Update to 0.30.

* Sat Jun 16 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.29-1
- Update to 0.29.

* Sat Jun 16 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.27-1
- Update to 0.27.
- New upstream maintainer.

* Thu Sep  7 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.23-5
- Rebuild for FC6.

* Wed Feb 22 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.23-4
- Rebuild for FC5 (perl 5.8.8).

* Wed Feb 22 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.23-3
- The wonders of CVS problems (released skipped).

* Thu Jan  5 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.23-2
- Build section: simplified RPM_OPT_FLAGS handling (#175898).

* Sat Nov 05 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.23-1
- First build.
