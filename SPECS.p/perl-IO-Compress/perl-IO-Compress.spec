%bcond_without long_tests
%{?perl_default_filter}

Name:           perl-IO-Compress
Version:        2.046
Release:        3%{?dist}
Summary:        Read and write compressed data
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/IO-Compress/
Source0:        http://www.cpan.org/authors/id/P/PM/PMQS/IO-Compress-%{version}.tar.gz
BuildArch:      noarch
Requires:       perl(Exporter)
BuildRequires:  perl(bytes)
BuildRequires:  perl(constant)
BuildRequires:  perl(Compress::Raw::Bzip2) >= 2.045
BuildRequires:  perl(Compress::Raw::Zlib) >= 2.045
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::GlobMapper)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IO::Seekable)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Symbol)
BuildRequires:  perl(Test::Pod) >= 1.00, perl(Test::NoWarnings)
BuildRequires:  perl(Test::Builder), perl(Test::More), perl(Config)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
# this is wrapper for different Compress modules
Provides:       perl-Compress-Zlib = %{version}-%{release}
Obsoletes:      perl-Compress-Zlib < %{version}-%{release}
Provides:       perl-IO-Compress-Base = %{version}-%{release}
Obsoletes:      perl-IO-Compress-Base < %{version}-%{release}
Provides:       perl-IO-Compress-Bzip2 = %{version}-%{release}
Obsoletes:      perl-IO-Compress-Bzip2 < %{version}-%{release}
Obsoletes:      perl-IO-Compress-Zlib < %{version}-%{release}
Provides:       perl-IO-Compress-Zlib = %{version}-%{release}

%description
This distribution provides a Perl interface to allow reading and writing of
compressed data created with the zlib and bzip2 libraries.

IO-Compress supports reading and writing of bzip2, RFC 1950, RFC 1951,
RFC 1952 (i.e. gzip) and zip files/buffers.

The following modules used to be distributed separately, but are now
included with the IO-Compress distribution:

* Compress-Zlib
* IO-Compress-Zlib
* IO-Compress-Bzip2
* IO-Compress-Base

%prep
%setup -q -n IO-Compress-%{version}

# Remove spurious exec permissions
chmod -x lib/IO/Uncompress/{Adapter/Identity,RawInflate}.pm
find examples -type f -exec chmod -x {} +
# Fix shellbangs in examples
%{__perl} -pi -e 's|^#!/usr/local/bin/perl\b|#!%{__perl}|' examples/io/anycat \
        examples/io/bzip2/* examples/io/gzip/* examples/compress-zlib/*

%build
%{__perl} Makefile.PL
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} \; 2>/dev/null
%{_fixperms} %{buildroot}

%check
# Build using "--without long_tests" to avoid very long tests
# (full suite can take nearly an hour on an i7)
 %{?with_long_tests:COMPRESS_ZLIB_RUN_ALL=1}

%files
%doc Changes README examples/*
%{_bindir}/zipdetails
%{perl_privlib}/Compress/
%{perl_privlib}/File/
%dir %{perl_privlib}/IO/
%dir %{perl_privlib}/IO/Compress/
%doc %{perl_privlib}/IO/Compress/FAQ.pod
%{perl_privlib}/IO/Compress/Adapter/
%{perl_privlib}/IO/Compress/Base/
%{perl_privlib}/IO/Compress/Base.pm
%{perl_privlib}/IO/Compress/Bzip2.pm
%{perl_privlib}/IO/Compress/Deflate.pm
%{perl_privlib}/IO/Compress/Gzip/
%{perl_privlib}/IO/Compress/Gzip.pm
%{perl_privlib}/IO/Compress/RawDeflate.pm
%{perl_privlib}/IO/Compress/Zip/
%{perl_privlib}/IO/Compress/Zip.pm
%{perl_privlib}/IO/Compress/Zlib/
%{perl_privlib}/IO/Uncompress/
%{_mandir}/man1/zipdetails.1*
%{_mandir}/man3/Compress::Zlib.3pm*
%{_mandir}/man3/File::GlobMapper.3pm*
%{_mandir}/man3/IO::Compress::*.3pm*
%{_mandir}/man3/IO::Uncompress::*.3pm*

%changelog
* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 2.046-3
- 为 Magic 3.0 重建

* Tue Jan 10 2012 Paul Howarth <paul@city-fan.org> - 2.046-2
- Fedora 17 mass rebuild

* Mon Dec 19 2011 Paul Howarth <paul@city-fan.org> - 2.046-1
- Update to 2.046
  - Minor update to bin/zipdetails
  - Typo in name of IO::Compress::FAQ.pod
  - IO::Uncompress::Unzip:
    - Example for walking a zip file used eof to control the outer loop; this
      is wrong
  - IO::Compress::Zip:
    - Change default for CanonicalName to false (CPAN RT#72974)
- Freeze Compress::Raw::* dependency versions until next synchronized release

* Sun Dec  4 2011 Paul Howarth <paul@city-fan.org> - 2.045-1
- Update to 2.045
  - Restructured IO::Compress::FAQ.pod

* Sun Dec  4 2011 Paul Howarth <paul@city-fan.org> - 2.044-1
- Update to 2.044
  - Moved FAQ.pod under the lib directory so it can get installed
  - Added bin/zipdetails
  - In IO::Compress::Zip, in one-shot mode, enable Zip64 mode if the input
    file/buffer ≥ 0xFFFFFFFF bytes
  - Update IO::Compress::FAQ

* Mon Nov 21 2011 Paul Howarth <paul@city-fan.org> - 2.043-1
- Update to 2.043
  - IO::Compress::Base:
    - Fixed issue that with handling of Zip files with two (or more) entries
      that were STORED; symptom is the first is uncompressed ok but the next
      will terminate early if the size of the file is greater than BlockSize
      (CPAN RT#72548)

* Fri Nov 18 2011 Paul Howarth <paul@city-fan.org> - 2.042-1
- Update to 2.042
  - IO::Compress::Zip:
    - Added exUnixN option to allow creation of the "ux" extra field, which
      allows 32-bit UID/GID to be stored
    - In one-shot mode use exUnixN rather than exUnix2 for the UID/GID
  - IO::Compress::Zlib::Extra::parseExtraField:
    - Fixed bad test for length of ID field (CPAN RT#72329, CPAN RT#72505)

* Sat Oct 29 2011 Paul Howarth <paul@city-fan.org> - 2.040-1
- Update to 2.040
  - IO::Compress::Zip:
    - Added CanonicalName option (note this option is set to true by default)
    - Added FilterName option
    - ExtAttr now populates MSDOS attributes
  - IO::Uncompress::Base:
    - Fixed issue where setting $\ would corrupt the uncompressed data
  - t/050interop-*.t:
    - Handle case when external command contains a whitespace (CPAN RT#71335)
  - t/105oneshot-zip-only.t:
    - CanonicalName test failure on Windows (CPAN RT#68926)

* Wed Jun 22 2011 Paul Howarth <paul@city-fan.org> - 2.037-2
- Perl mass rebuild

* Wed Jun 22 2011 Paul Howarth <paul@city-fan.org> - 2.037-1
- Update to 2.037 (support streamed stored content in IO::Uncompress::Unzip)

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.036-2
- Perl mass rebuild

* Mon Jun 20 2011 Petr Sabata <contyk@redhat.com> - 2.036-1
- 2.036 bump (Zip/Unzip enhancements)

* Sat May  7 2011 Paul Howarth <paul@city-fan.org> - 2.035-1
- Update to 2.035 (fix test failure on Windows - CPAN RT#67931)

* Tue May  3 2011 Petr Sabata <psabata@redhat.com> - 2.034-1
- 2.034 bump
- Buildroot and defattr cleanup
- Correcting BRs/Rs

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.033-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 13 2011 Paul Howarth <paul@city-fan.org> - 2.033-1
- Update to 2.033 (fixed typos and spelling errors - Perl RT#81816)
- Use more explicit %%files list
- Simplify inclusion of IO::Compress::FAQ
- Drop redundant explicit requires of Compress::Raw::{Bzip2,Zlib}
- Drop installdirs patch, not needed with perl 5.12
- Default installdirs are perl, so no need to specify it explicitly
- Make %%summary less generic

* Fri Jan 07 2011 Petr Pisar <ppisar@redhat.com> - 2.032-1
- 2.032 bump
- Small improvements in spec file

* Fri Dec 17 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.030-4
- 661697 rebuild for fixing problems with vendorach/lib

* Tue Sep 21 2010 Paul Howarth <paul@city-fan.org> 2.030-3
- Turn long-running tests back on and support build --without long_tests
  to skip them

* Thu Sep 16 2010 Ville Skyttä <ville.skytta@iki.fi> - 2.030-2
- Install IO::Compress::FAQ into usual POD and man dirs (#634722)

* Mon Jul 26 2010 Petr Sabata <psabata@redhat.com> 2.030-1
- 2.030 version bump

* Thu May 06 2010 Marcela Mašláňová <mmaslano@redhat.com> 2.027-1
- update

* Mon Apr 12 2010 Marcela Mašláňová <mmaslano@redhat.com> 2.024-3
- few fixes in specfile 573932

* Tue Mar 16 2010 Marcela Mašláňová <mmaslano@redhat.com> 2.024-2
- Specfile autogenerated by cpanspec 1.78.
- thanks with fixes of specfile to Paul Howarth

