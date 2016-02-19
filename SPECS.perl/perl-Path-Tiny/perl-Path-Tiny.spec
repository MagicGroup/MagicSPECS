Name:		perl-Path-Tiny
Version:	0.076
Release:	1%{?dist}
Summary:	File path utility
Group:		Development/Libraries
License:	ASL 2.0
URL:		http://search.cpan.org/dist/Path-Tiny/
Source0:	http://search.cpan.org/CPAN/authors/id/D/DA/DAGOLDEN/Path-Tiny-%{version}.tar.gz
BuildArch:	noarch
# Module Build
BuildRequires:	perl
BuildRequires:	perl(ExtUtils::MakeMaker) >= 6.17
# Module Runtime
BuildRequires:	perl(Carp)
BuildRequires:	perl(Config)
BuildRequires:	perl(constant)
BuildRequires:	perl(Cwd)
BuildRequires:	perl(Digest) >= 1.03
BuildRequires:	perl(Digest::MD5)
BuildRequires:	perl(Digest::SHA) >= 5.45
BuildRequires:	perl(Exporter) >= 5.57
BuildRequires:	perl(Fcntl)
BuildRequires:	perl(File::Copy)
BuildRequires:	perl(File::Path) >= 2.07
BuildRequires:	perl(File::Spec) >= 3.40
BuildRequires:	perl(File::stat)
BuildRequires:	perl(File::Temp) >= 0.19
BuildRequires:	perl(if)
BuildRequires:	perl(overload)
BuildRequires:	perl(strict)
BuildRequires:	perl(threads)
BuildRequires:	perl(warnings)
# Test Suite
BuildRequires:	perl(blib)
BuildRequires:	perl(CPAN::Meta)
BuildRequires:	perl(CPAN::Meta::Requirements) >= 2.120900
BuildRequires:	perl(File::Basename)
BuildRequires:	perl(File::Spec::Functions)
BuildRequires:	perl(File::Spec::Unix)
BuildRequires:	perl(File::Temp) >= 0.19
BuildRequires:	perl(lib)
BuildRequires:	perl(List::Util)
BuildRequires:	perl(open)
BuildRequires:	perl(Test::FailWarnings)
BuildRequires:	perl(Test::More) >= 0.96
BuildRequires:	perl(version)
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	perl(Cwd)
Requires:	perl(Digest) >= 1.03
Requires:	perl(Digest::MD5)
Requires:	perl(Digest::SHA) >= 5.45
Requires:	perl(Fcntl)
Requires:	perl(File::Copy)
Requires:	perl(File::Path) >= 2.07
Requires:	perl(File::stat)
Requires:	perl(File::Temp) >= 0.18
Requires:	perl(threads)

# For performance and consistency
BuildRequires:	perl(Unicode::UTF8) >= 0.58
Requires:	perl(Unicode::UTF8) >= 0.58

%description
This module attempts to provide a small, fast utility for working with file
paths. It is friendlier to use than File::Spec and provides easy access to
functions from several other core file handling modules.

It doesn't attempt to be as full-featured as IO::All or Path::Class, nor does
it try to work for anything except Unix-like and Win32 platforms. Even then, it
might break if you try something particularly obscure or tortuous.

All paths are forced to have Unix-style forward slashes. Stringifying the
object gives you back the path (after some clean up).

File input/output methods flock handles before reading or writing, as
appropriate.

The *_utf8 methods (slurp_utf8, lines_utf8, etc.) operate in raw mode without
CRLF translation.

%prep
%setup -q -n Path-Tiny-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
%{_fixperms} %{buildroot}

%check
make test

%files
%{perl_vendorlib}/Path/
%{_mandir}/man3/Path::Tiny.3pm*

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com>
- 更新到 0.073-TRIAL

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.072-1
- 更新到 0.072

* Thu Jun 19 2014 Liu Di <liudidi@gmail.com> - 0.054-3
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.054-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May  6 2014 Paul Howarth <paul@city-fan.org> - 0.054-1
- Update to 0.054
  - The 'is_file' method now does -e && ! -d and not -f because -f is often
    more restrictive than people intend or expect
  - Added 'chmod' method with symbolic chmod support ("a=r,u+rx")
  - The 'basename' method now takes a list of suffixes to remove before
    returning the name
  - Added FREEZE/THAW/TO_JSON serialization helpers
  - When constructing a Path::Tiny object from another, the original is
    returned unless it's a temp dir/file, which significantly speeds up calling
    path($path) if $path is already a Path::Tiny object
  - Constructing any path - e.g. with child() - with undef or zero-length
    parts throws an error instead of constructing an invalid path

* Wed Jan 15 2014 Paul Howarth <paul@city-fan.org> - 0.052-1
- Update to 0.052
  - Backslash-to-slash conversion now only happens on Windows (since backslash
    is legal on Unix, we must allow it)

* Sat Dec 21 2013 Paul Howarth <paul@city-fan.org> - 0.051-1
- Update to 0.051
  - Recursive iteration won't throw an exception if a directory is removed or
    unreadable during iteration

* Thu Dec 12 2013 Paul Howarth <paul@city-fan.org> - 0.049-1
- Update to 0.049
  - Added 'subsumes' method
  - The 'chomp' option for 'lines' will remove any end-of-line sequences fully
    instead of just chomping the last character
  - Fixed locking test on AIX
  - Revised locking tests for portability again: locks are now tested from a
    separate process
  - The 'flock' package will no longer indexed by PAUSE
  - Hides warnings and fixes possible fatal errors from pure-perl Cwd,
    particularly on MSWin32
  - Generates filename for atomic writes independent of thread-ID, which fixes
    crashing bug on Win32 when fork() is called

* Fri Oct 18 2013 Paul Howarth <paul@city-fan.org> - 0.044-1
- Update to 0.044
  - Fixed child path construction against the root path
  - Fixed path construction when a relative volume is provided as the first
    argument on Windows; e.g. path("C:", "lib") must be like path("C:lib"),
    not path("C:/lib")
  - On AIX, shared locking is replaced by exclusive locking on a R/W
    filehandle, as locking read handles is not supported

* Mon Oct 14 2013 Paul Howarth <paul@city-fan.org> - 0.043-1
- Update to 0.043
  - Calling 'absolute' on Windows will add the volume if it is missing (e.g.
    "/foo" will become "C:/foo"); this matches the behavior of
    File::Spec->rel2abs
  - Fixed t/00-report-prereqs.t for use with older versions of
    CPAN::Meta::Requirements

* Sun Oct 13 2013 Paul Howarth <paul@city-fan.org> - 0.042-1
- Update to 0.042
  - When 'realpath' can't be resolved (because intermediate directories don't
    exist), the exception now explains the error clearly instead of complaining
    about path() needing a defined, positive-length argument
  - On Windows, fixed resolution of relative paths with a volume, e.g. "C:foo"
    is now correctly translated into getdcwd on "C:" plus "foo"

* Fri Oct 11 2013 Paul Howarth <paul@city-fan.org> - 0.041-1
- Update to 0.041
  - Remove duplicate test dependency on File::Spec that triggers a CPAN.pm bug

* Wed Oct  9 2013 Paul Howarth <paul@city-fan.org> - 0.040-1
- Update to 0.040
  - The 'filehandle' method now offers an option to return locked handles
    based on the file mode
  - The 'filehandle' method now respects default encoding set by the caller's
    open pragma

* Wed Oct  2 2013 Paul Howarth <paul@city-fan.org> - 0.038-1
- Update to 0.038
  - Added 'is_rootdir' method to simplify testing if a path is the root
    directory

* Thu Sep 26 2013 Paul Howarth <paul@city-fan.org> - 0.037-1
- Update to 0.037
  - No longer lists 'threads' as a prerequisite; if you have a threaded perl,
    you have it and if you've not, Path::Tiny doesn't care
  - Fixed for v5.8

* Tue Sep 24 2013 Paul Howarth <paul@city-fan.org> - 0.035-1
- Update to 0.035
  - Fixed flock warning on BSD that was broken with the autodie removal; now
    also applies to all BSD flavors

* Tue Sep 24 2013 Paul Howarth <paul@city-fan.org> - 0.034-1
- Update to 0.034
  - Exceptions are now Path::Tiny::Error objects, not autodie exceptions; this
    removes the last dependency on autodie, which allows us to support Perls as
    far back as v5.8.1
  - BSD/NFS flock fix was not backwards compatible before v5.14; this fixes it
    harder
  - Lowered ExtUtils::MakeMaker configure_requires version to 6.17

* Thu Sep 12 2013 Paul Howarth <paul@city-fan.org> - 0.033-1
- Update to 0.033
  - Perl on BSD may not support locking on an NFS filesystem: if this is
    detected, Path::Tiny warns and continues in an unsafe mode (the 'flock'
    warning category may be fatalized to die instead)
  - Added 'iterator' example showing defaults

* Fri Sep  6 2013 Paul Howarth <paul@city-fan.org> - 0.032-1
- Update to 0.032
  - Removed several test dependencies; Path::Tiny now only needs core modules,
    though some must be upgraded on old Perls

* Tue Sep  3 2013 Paul Howarth <paul@city-fan.org> - 0.031-3
- BR: perl(Config) for the test suite (#1003660)

* Mon Sep  2 2013 Paul Howarth <paul@city-fan.org> - 0.031-2
- Sanitize for Fedora submission

* Mon Sep  2 2013 Paul Howarth <paul@city-fan.org> - 0.031-1
- Initial RPM version
