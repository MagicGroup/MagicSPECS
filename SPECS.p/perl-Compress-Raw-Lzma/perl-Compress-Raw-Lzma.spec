Name:		perl-Compress-Raw-Lzma
Version:	2.045
Release:	4%{?dist}
Summary:	Low-level interface to lzma compression library
Group:		Development/Libraries
License:	GPL+ or Artistic
URL:		http://search.cpan.org/dist/Compress-Raw-Lzma/
Source0:	http://search.cpan.org/CPAN/authors/id/P/PM/PMQS/Compress-Raw-Lzma-%{version}.tar.gz
BuildRequires:	xz, xz-devel, perl(Carp), perl(ExtUtils::MakeMaker), perl(Test::Pod)
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
# Built-against version is embedded in module, so we have a strict version dependency
Requires:	xz-libs%{?_isa} = %((pkg-config --modversion liblzma 2>/dev/null || echo 0) | tr -dc '[0-9.]')

# Don't "provide" private Perl libs
%{?perl_default_filter}

%description
This module provides a Perl interface to the lzma compression library.
It is used by IO::Compress::Lzma.

%prep
%setup -q -n Compress-Raw-Lzma-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'
%{_fixperms} %{buildroot}

%check


%files
%defattr(-,root,root,-)
%doc Changes
%{perl_vendorarch}/auto/Compress/
%{perl_vendorarch}/Compress/
%{_mandir}/man3/Compress::Raw::Lzma.3pm*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 2.045-4
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 2.045-3
- 为 Magic 3.0 重建

* Tue Jan 10 2012 Paul Howarth <paul@city-fan.org> - 2.045-2
- Rebuild for gcc 4.7 in Rawhide

* Sun Dec  4 2011 Paul Howarth <paul@city-fan.org> - 2.045-1
- Update to 2.045
  - Moved FAQ.pod to IO::Compress

* Sun Dec  4 2011 Paul Howarth <paul@city-fan.org> - 2.044-1
- Update to 2.044
  - Moved FAQ.pod under the lib directory so it can get installed

* Mon Nov 21 2011 Paul Howarth <paul@city-fan.org> - 2.043-1
- Update to 2.043 (no changes)

* Fri Nov 18 2011 Paul Howarth <paul@city-fan.org> - 2.042-1
- Update to 2.042 (no changes)

* Sat Oct 29 2011 Paul Howarth <paul@city-fan.org> - 2.040-1
- Update to 2.040
  - Croak if attempt to freeze/thaw compression object (CPAN RT#69985)
- BR: perl(Carp)

* Sun Oct 16 2011 Jindrich Novy <jnovy@redhat.com> - 2.037-3
- Rebuild against new xz

* Wed Jun 22 2011 Paul Howarth <paul@city-fan.org> - 2.037-2
- Perl mass rebuild

* Wed Jun 22 2011 Paul Howarth <paul@city-fan.org> - 2.037-1
- Update to 2.037 (no changes)

* Mon Jun 20 2011 Paul Howarth <paul@city-fan.org> - 2.036-2
- Perl mass rebuild

* Mon Jun 20 2011 Paul Howarth <paul@city-fan.org> - 2.036-1
- Update to 2.036
  - A number of changes to facilitate adding LZMA support to
    IO::Compress::Zip : IO::Uncompress::Unzip:
    - Added preset filters Lzma::Filter::Lzma1::Preset and
      Lzma::Filter::Lzma2::Preset
   - Added forZip option to Compress::Raw::Lzma::Encoder
   - Added properties option to Compress::Raw::Lzma::RawDecoder

* Sun Jun 19 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.035-3
- Perl mass rebuild

* Mon May 23 2011 Paul Howarth <paul@city-fan.org> - 2.035-2
- Rebuild for xz 5.0.3

* Sat May  7 2011 Paul Howarth <paul@city-fan.org> - 2.035-1
- Update to 2.035 (no changes)

* Tue May  3 2011 Paul Howarth <paul@city-fan.org> - 2.034-1
- Update to 2.034 (document the change of default MemLimit in 2.033)

* Mon Apr  4 2011 Paul Howarth <paul@city-fan.org> - 2.033-4
- Rebuild for xz 5.0.2

* Wed Feb  9 2011 Paul Howarth <paul@city-fan.org> - 2.033-3
- Add explicit version dependency on xz-libs since the version number built
  against is embedded into the module and can cause failures in users of this
  module if they compare build-time and run-time versions of liblzma

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.033-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 11 2011 Paul Howarth <paul@city-fan.org> - 2.033-1
- Update to 2.033 (changed default MemLimit from 128 MB to unlimited)

* Fri Jan  7 2011 Paul Howarth <paul@city-fan.org> - 2.032-1
- Update to 2.032 (no changes)

* Wed Oct 27 2010 Paul Howarth <paul@city-fan.org> - 2.031-1
- Update to 2.031
  - Changed to build with XZ 5.0.0
  - Dropped symbolic constants provided by subblock.h (CPAN RT#62461)
- Drop xz 5.x patch, no longer needed

* Tue Oct 26 2010 Paul Howarth <paul@city-fan.org> - 2.030-2
- Patch out subfilter constants, not supported in xz 5.x (CPAN RT#62461)

* Mon Jul 26 2010 Paul Howarth <paul@city-fan.org> - 2.030-1
- Update to 2.030 (no changes)

* Fri May 14 2010 Paul Howarth <paul@city-fan.org> - 2.029-3
- Rebuild for perl 5.12.0

* Tue May 11 2010 Paul Howarth <paul@city-fan.org> - 2.029-2
- Drop redundant buildroot tag

* Sat May  8 2010 Paul Howarth <paul@city-fan.org> - 2.029-1
- Update to 2.029 (test harness copes with memory shortage)

* Mon May  3 2010 Paul Howarth <paul@city-fan.org> - 2.028-1
- Update to 2.028
  - Remove 'Persistent' option from  Lzma::Filter::Lzma (CPAN RT#57080)
  - Silence a pile of compiler warnings
- Drop patch for CPAN RT#57080, no longer needed

* Thu Apr 29 2010 Paul Howarth <paul@city-fan.org> - 2.027-1
- Initial RPM version
