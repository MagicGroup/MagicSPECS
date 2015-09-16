Name:		perltidy
Version:	20150815
Release:	1%{?dist}
Summary:	Tool for indenting and re-formatting Perl scripts
License:	GPLv2+
URL:		http://perltidy.sourceforge.net/
Source0:	http://www.cpan.org/modules/by-module/Perl/Perl-Tidy-%{version}.tar.gz
Patch0:		Perl-Tidy-utf8.patch
BuildArch:	noarch
# Module Build
BuildRequires:	perl
BuildRequires:	perl(ExtUtils::MakeMaker)
# Module Runtime
BuildRequires:	perl(Carp)
BuildRequires:	perl(constant)
BuildRequires:	perl(Cwd)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(File::Basename)
BuildRequires:	perl(File::Copy)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(File::Temp)
BuildRequires:	perl(Getopt::Long)
BuildRequires:	perl(IO::File)
BuildRequires:	perl(strict)
BuildRequires:	perl(vars)
# Test Suite
BuildRequires:	perl(Test)
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	perl(File::Spec)
Provides:	perl-Perl-Tidy = %{version}-%{release}

%description
Perltidy is a Perl script that indents and re-formats Perl scripts to
make them easier to read. If you write Perl scripts, or spend much
time reading them, you will probably find it useful. The formatting
can be controlled with command line parameters. The default parameter
settings approximately follow the suggestions in the Perl Style Guide.
Perltidy can also output HTML of both POD and source code. Besides
re-formatting scripts, Perltidy can be a great help in tracking down
errors with missing or extra braces, parentheses, and square brackets
because it is very good at localizing errors.

%prep
%setup -q -n Perl-Tidy-%{version}

# Re-format documentation as UTF-8
%patch0

# Don't need Windows batch file
rm examples/pt.bat

# We'll ship the perltidy manpage in %%{_mandir} so we don't need another copy
rm docs/perltidy.1

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} %{buildroot}

%check
make test

%files
%doc BUGS CHANGES COPYING README TODO docs/ examples/
%{_bindir}/perltidy
%{perl_vendorlib}/Perl/
%{_mandir}/man1/perltidy.1*
%{_mandir}/man3/Perl::Tidy.3*

%changelog
* Wed Sep 16 2015 Liu Di <liudidi@gmail.com> - 20150815-1
- 更新到 20150815

* Wed Sep 16 2015 Liu Di <liudidi@gmail.com> - 20140328-4
- 为 Magic 3.0 重建

* Tue Jun 17 2014 Liu Di <liudidi@gmail.com> - 20140328-3
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20140328-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Paul Howarth <paul@city-fan.org> - 20140328-1
- Update to 20140328
  - Fixed CPAN RT#94190 and debian Bug #742004: perltidy.LOG file left behind;
    the problem was caused by the memoization speedup patch in version
    20121207: an unwanted flag was being set, which caused a LOG to be written
    if perltidy was called multiple times
  - New default behavior for LOG files: if the source is from an array or
    string (through a call to the perltidy module) then a LOG output is only
    possible if a logfile stream is specified; this is to prevent unexpected
    perltidy.LOG files
  - Fixed debian Bug #740670, insecure temporary file usage; File::Temp is now
    used to get a temporary file (CVE-2014-2277)
  - Any -b (--backup-and-modify-in-place) flag is silently ignored when a
    source stream, destination stream, or standard output is used; this is
    because the -b flag may have been in a .perltidyrc file and warnings break
    Test::NoWarnings
- Drop upstreamed patch for CVE-2014-2277
- Classify buildreqs by usage

* Tue Mar 25 2014 Paul Howarth <paul@city-fan.org> - 20130922-2
- Cosmetic spec changes:
  - Use tabs
  - Comment patch applications
  - Don't use macros for commands
  - Use %%{buildroot} rather than $RPM_BUILD_ROOT
- Provide perl-Perl-Tidy for benefit of people looking for CPAN module
- Use a patch rather than scripted iconv run to fix character encoding
- BR: perl(Getopt::Long)
- Don't need to remove empty directories from the buildroot
- Use DESTDIR rather than PERL_INSTALL_ROOT

* Wed Mar 12 2014 Ville Skyttä <ville.skytta@iki.fi> - 20130922-1
- Update to 20130922.
- Fix for CVE-2014-2277 from Debian (#1074721) + related man page fix.
- Fix bogus date in %%changelog.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20121207-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 20121207-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20121207-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Dec 11 2012 Ville Skyttä <ville.skytta@iki.fi> - 20121207-1
- Update to 20121207.

* Wed Aug 15 2012 Jitka Plesnikova <jplesnik@redhat.com> - 20120714-3
- Specify all dependencies.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20120714-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Ville Skyttä <ville.skytta@iki.fi> - 20120714-1
- Update to 20120714.

* Mon Jul 09 2012 Petr Pisar <ppisar@redhat.com> - 20120701-2
- Perl 5.16 rebuild

* Sat Jul  7 2012 Ville Skyttä <ville.skytta@iki.fi> - 20120701-1
- Update to 20120701.

* Thu Jun 28 2012 Petr Pisar <ppisar@redhat.com> - 20120619-2
- Perl 5.16 rebuild

* Wed Jun 20 2012 Ville Skyttä <ville.skytta@iki.fi> - 20120619-1
- Update to 20120619.
- Clean up specfile constructs no longer needed in Fedora or EL6+.

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 20101217-5
- Perl 5.16 rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20101217-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 20101217-3
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20101217-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Dec 26 2010 Ville Skyttä <ville.skytta@iki.fi> - 20101217-1
- Update to 20101217.

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 20090616-4
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 20090616-3
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20090616-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 18 2009 Ville Skyttä <ville.skytta@iki.fi> - 20090616-1
- Update to 20090616.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20071205-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 20071205-3
- Rebuild for perl 5.10 (again)

* Sun Jan 13 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 20071205-2
- rebuild for new perl

* Thu Dec  6 2007 Ville Skyttä <ville.skytta@iki.fi> - 20071205-1
- 20071205.
- Convert docs to UTF-8.

* Wed Aug  1 2007 Ville Skyttä <ville.skytta@iki.fi> - 20070801-1
- 20070801.

* Wed May  9 2007 Ville Skyttä <ville.skytta@iki.fi> - 20070508-1
- 20070508.

* Sat May  5 2007 Ville Skyttä <ville.skytta@iki.fi> - 20070504-1
- 20070504.

* Tue Apr 24 2007 Ville Skyttä <ville.skytta@iki.fi> - 20070424-1
- 20070424.

* Tue Apr 17 2007 Ville Skyttä <ville.skytta@iki.fi> - 20060719-3
- BuildRequire perl(ExtUtils::MakeMaker).

* Fri Sep 15 2006 Ville Skyttä <ville.skytta@iki.fi> - 20060719-2
- Rebuild.

* Thu Jul 20 2006 Ville Skyttä <ville.skytta@iki.fi> - 20060719-1
- 20060719.
- Fix order of options to find(1) in %%install.

* Thu Jun 15 2006 Ville Skyttä <ville.skytta@iki.fi> - 20060614-1
- 20060614, specfile cleanups, include examples in docs.

* Wed Apr  6 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Thu Dec 16 2004 Ville Skyttä <ville.skytta@iki.fi> - 0:20031021-1
- Sync with fedora-rpmdevtools' Perl spec template to fix x86_64 build.
- Move version to the version field.

* Wed Oct 22 2003 Ville Skyttä <ville.skytta@iki.fi> 0:0.0-0.fdr.3.20031021
- Update to 20031021.

* Sat Oct 11 2003 Ville Skyttä <ville.skytta@iki.fi> 0:0.0-0.fdr.3.20030726
- Install into vendor dirs.
- Spec cleanups.

* Tue Jul 29 2003 Ville Skyttä <ville.skytta@iki.fi> 0:0.0-0.fdr.2.20030726
- Update to 20030726.
- Use fedora-rpm-helper.

* Mon Jun 23 2003 Ville Skyttä <ville.skytta@iki.fi> 0:0.0-0.fdr.2.20021130
- Address issues in #194:
- Patch to get rid of a warning on startup.
- Do defattr before doc.

* Fri May 30 2003 Ville Skyttä <ville.skytta@iki.fi> 0:0.0-0.fdr.1.20021130
- Fix release naming scheme (this is snapshot-only).

* Wed May  7 2003 Ville Skyttä <ville.skytta@iki.fi> 0:0.0-0.fdr.0.2.20021130
- Own dirs.
- Save .spec in UTF-8.

* Mon Apr 21 2003 Ville Skyttä <ville.skytta@iki.fi> 0:0.0-0.fdr.0.1.20021130
- First Fedora release, based on Simon Perreault's work.

* Mon Mar 10 2003 Simon Perreault <nomis80@nomis80.org> 20021130-2
- Changed architecture from i386 to noarch
- Added my name as packager
- Bumped up release number, which was forgotten by Anthony Rumble

* Sun Mar 09 2003 Anthony Rumble <anthony@linuxhelp.com.au>
- Tidied up RPM Source

* Sun Dec  1 2002 Simon Perreault <nomis80@linuxquebec.com>
- Update to 20021130

* Sat Nov  9 2002 Simon Perreault <nomis80@linuxquebec.com>
- Update to 20021106

* Mon Sep 23 2002 Simon Perreault <nomis80@linuxquebec.com>
- Update to 20020922

* Wed Aug 28 2002 Simon Perreault <nomis80@linuxquebec.com>
- Update to 20020826

* Tue May 7 2002 Simon Perreault <nomis80@linuxquebec.com>
- Require 5.6.1 because Tidy.pm is placed in a directory dependant on perl
  version.

* Sat Apr 27 2002 Simon Perreault <nomis80@linuxquebec.com>
- Update to 20020425.

* Wed Apr 17 2002 Simon Perreault <nomis80@linuxquebec.com>
- Generalized spec file. Added some documentation.

* Wed Apr 17 2002 Simon Perreault <nomis80@linuxquebec.com>
- Upgraded to version 20020416

* Mon Feb 25 2002 Simon Perreault <nomis80@linuxquebec.com>
- Spec file was created on release of 20020225
