Summary:	Typical installation tasks for system administrators
Name:		perl-Sysadm-Install
Version:	0.44
Release:	2%{?dist}
License:	GPL+ or Artistic
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/Sysadm-Install/
Source0:	http://search.cpan.org/CPAN/authors/id/M/MS/MSCHILLI/Sysadm-Install-%{version}.tar.gz
BuildArch:	noarch
BuildRequires:	perl(Archive::Tar)
BuildRequires:	perl(Config)
BuildRequires:	perl(Cwd)
BuildRequires:	perl(Encode)
BuildRequires:	perl(Expect)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(File::Basename)
BuildRequires:	perl(File::Copy)
BuildRequires:	perl(File::Path)
BuildRequires:	perl(File::Temp) >= 0.16
BuildRequires:	perl(File::Which) >= 1.09
BuildRequires:	perl(HTTP::Request)
BuildRequires:	perl(HTTP::Status)
BuildRequires:	perl(Log::Log4perl) >= 1.00
BuildRequires:	perl(LWP::UserAgent)
BuildRequires:	perl(Term::ReadKey)
# For test suite
BuildRequires:	perl(Test::More)
# Runtime deps not automatically picked up by RPM
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	perl(Archive::Tar)
Requires:	perl(Config)
Requires:	perl(Encode)
Requires:	perl(Expect)
Requires:	perl(HTTP::Request)
Requires:	perl(HTTP::Status)
Requires:	perl(LWP::UserAgent)

%description
"Sysadm::Install" executes shell-like commands performing typical
installation tasks: Copying files, extracting tarballs, calling "make".
It has a "fail once and die" policy, meticulously checking the result of
every operation and calling "die()" immediately if anything fails,
with optional logging of everything.

"Sysadm::Install" also supports a *dry_run* mode, in which it logs
everything, but suppresses any write actions.

%prep
%setup -q -n Sysadm-Install-%{version}

# Fix perl interpreter in eg/mkperl
perl -pi -e 's|/usr/local/bin/perl|/usr/bin/perl|;' eg/mkperl

# Note: not turning off exec bits in examples because they don't
# introduce any unwanted dependencies

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%check
make test TEST_VERBOSE=1

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} %{buildroot}

%files
%doc Changes README eg
# one-liner is an overly-generic name to include in %%{_bindir} and is included
# as %%doc if needed
%exclude %{_bindir}/one-liner
%{perl_vendorlib}/Sysadm/
%{_mandir}/man3/Sysadm::Install.3pm*

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.44-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Paul Howarth <paul@city-fan.org> - 0.44-1
- Update to 0.44
  - Replaced bin_find() implementation by File::Which
  - tap() with raise_error option set now dies with stderr output, because
    $! isn't set on failed close()

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.43-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Aug 01 2013 Petr Pisar <ppisar@redhat.com> - 0.43-2
- Perl 5.18 rebuild

* Tue Mar 19 2013 Paul Howarth <paul@city-fan.org> 0.43-1
- Update to 0.43
  - Using binmode() now for slurp/blurt for compatibility with Win32 systems

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 0.42-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 22 2013 Paul Howarth <paul@city-fan.org> 0.42-1
- Update to 0.42
  - No longer silently remove directories that are in the way before untar()
  - Better error diagnosis on failing untar() tests

* Tue Dec 18 2012 Paul Howarth <paul@city-fan.org> 0.41-1
- Update to 0.41
  - Added home_dir() function returning user's home directory
  - tap() now supports stdout_limit and stderr_limit options to limit log
    verbosity

* Sun Sep 16 2012 Paul Howarth <paul@city-fan.org> 0.40-1
- Update to 0.40
  - Fix Cwd problem on Win32/Mac

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 0.39-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 29 2012 Petr Pisar <ppisar@redhat.com> 0.39-2
- Perl 5.16 rebuild

* Thu May 17 2012 Paul Howarth <paul@city-fan.org> 0.39-1
- Update to 0.39
  - Fixed bin_find to omit directories
  - Added cdback() with reset option

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 0.38-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jul 31 2011 Paul Howarth <paul@city-fan.org> 0.38-1
- Update to 0.38
  - Fixed Win32 test in 012tap.t

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> 0.37-2
- Perl mass rebuild

* Sun Jun 26 2011 Paul Howarth <paul@city-fan.org> 0.37-1
- Update to 0.37
  - Fix for tap's raise_error option and added test case (CPAN RT#68095)
- Drop redundant defattr()

* Mon May  2 2011 Paul Howarth <paul@city-fan.org> 0.36-1
- Update to 0.36
  - Added owner_cp() to copy uid and gid of a file or directory
  - Added raise_error option for tap()
  - snip() now returns original string (with unprintables replaced) if the data
    length is shorter than $maxlen
- Clean up for modern perl and rpmbuild
- Nobody else likes macros for commands

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 0.35-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> 0.35-3
- Rebuild to fix problems with vendorarch/lib (#661697)

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> 0.35-2
- Mass rebuild with perl-5.12.0

* Thu Apr 15 2010 Paul Howarth <paul@city-fan.org> 0.35-1
- Update to 0.35
  - Fix blurt_atomic on Win32 (CPAN RT#54885)
  - Fixed local caller_depth increments
  - Fixed printable() bug masking '-'

* Mon Feb 22 2010 Paul Howarth <paul@city-fan.org> 0.34-1
- Update to 0.34 (documentation update and fixes for Windows)
- BR/R perl(Config), perl(Encode), perl(HTTP::Request), perl(HTTP::Status)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> 0.33-2
- Rebuild against perl 5.10.1

* Mon Sep 14 2009 Paul Howarth <paul@city-fan.org> 0.33-1
- Update to 0.33
  - No longer require perl(Encode)
  - Use perl(LWP::UserAgent) rather than perl(LWP::Simple)

* Tue Sep  1 2009 Paul Howarth <paul@city-fan.org> 0.32-1
- Update to 0.32 (make UTF-8 handling configurable, not automatic)

* Fri Aug 28 2009 Paul Howarth <paul@city-fan.org> 0.31-1
- Update to 0.31 (improved UTF-8 support)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 0.29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul  3 2009 Paul Howarth <paul@city-fan.org> 0.29-1
- Update to 0.29
  - Add proper error handling to print and pipe statements
  - Fix up some "if $dir" cases to protect against a value of "0" in $dir
  - Fix up logcroak calls to use the current logger

* Tue May 12 2009 Paul Howarth <paul@city-fan.org> 0.28-1
- Update to 0.28 (fixed download() with a better check for getstore())

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 0.27-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Oct  9 2008 Paul Howarth <paul@city-fan.org> 0.27-2
- Incorporate comments from package review (#466223)
  - don't include one-liner in %%{_bindir}
  - tighten up %%description

* Thu Oct  9 2008 Paul Howarth <paul@city-fan.org> 0.27-1
- Initial RPM version
