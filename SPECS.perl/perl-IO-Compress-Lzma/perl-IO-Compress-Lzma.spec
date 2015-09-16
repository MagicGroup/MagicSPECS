Name:		perl-IO-Compress-Lzma
Version:	2.068
Release:	1%{?dist}
Summary:	Read and write lzma compressed data
License:	GPL+ or Artistic
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/IO-Compress-Lzma/
Source0:	http://search.cpan.org/CPAN/authors/id/P/PM/PMQS/IO-Compress-Lzma-%{version}.tar.gz
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
BuildArch:	noarch
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(Compress::Raw::Lzma) >= %{version}
BuildRequires:	perl(IO::Compress::Base) >= %{version}
BuildRequires:	perl(IO::String)
BuildRequires:	perl(Test::Pod)
BuildRequires:	xz, xz-lzma-compat
BuildRequires:	/usr/bin/7z

%description
This distribution provides a Perl interface to allow reading and writing of
compressed data created with the lzma library.

%prep
%setup -q -n IO-Compress-Lzma-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} ';' 2>/dev/null
%{_fixperms} %{buildroot}

%check


%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/IO/
%{_mandir}/man3/IO::Compress::Lzma.3pm*
%{_mandir}/man3/IO::Compress::Xz.3pm*
%{_mandir}/man3/IO::Uncompress::UnLzma.3pm*
%{_mandir}/man3/IO::Uncompress::UnXz.3pm*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 2.068-1
- 更新到 2.068

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.045-5
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 2.045-4
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 2.045-3
- 为 Magic 3.0 重建

* Tue Jan 10 2012 Paul Howarth <paul@city-fan.org> - 2.045-2
- Fedora 17 mass rebuild

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
- Resync versioned dependencies on IO::Compress::Base and Compress::Raw::Lzma

* Sat Oct 29 2011 Paul Howarth <paul@city-fan.org> - 2.041-1
- Update to 2.041
  - Remove debugging line in t/001lzma.t that writes to /tmp (CPAN RT#72023)
- Update version requirements for IO::Compress and Compress::Raw::Lzma

* Sat Oct 29 2011 Paul Howarth <paul@city-fan.org> - 2.040-1
- Update to 2.040
  - Fixed uncompression issue in IO::Uncompress::UnLzma (CPAN RT#71114)

* Fri Jun 24 2011 Paul Howarth <paul@city-fan.org> - 2.038-2
- Perl mass rebuild

* Fri Jun 24 2011 Paul Howarth <paul@city-fan.org> - 2.038-1
- Update to 2.038
  - Fixed missing SKIP label in t/050interop-zip-lzma.t
- Hard-code version requirements for IO::Compress and Compress::Raw::Lzma
  until the next synchronized release happens

* Wed Jun 22 2011 Paul Howarth <paul@city-fan.org> - 2.037-2
- Perl mass rebuild

* Wed Jun 22 2011 Paul Howarth <paul@city-fan.org> - 2.037-1
- Update to 2.037
  - Handle "Cannot Allocate Memory" issue with Extreme test in
    t/105oneshot-zip-lzma-only.t

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.036-2
- Perl mass rebuild

* Mon Jun 20 2011 Paul Howarth <paul@city-fan.org> - 2.036-1
- Update to 2.036
  - IO::Compress::Adapter:
    - Added interface to allow creation of LZMA stream for use in a zip file
  - IO::Uncompress::Adapter:
    - Added interface to allow reading of LZMA stream in a zip file
- BR: /usr/bin/7z for additional test coverage

* Sat May  7 2011 Paul Howarth <paul@city-fan.org> - 2.035-1
- Update to 2.035 (fix test failure on Windows - CPAN RT#67931)

* Tue May  3 2011 Paul Howarth <paul@city-fan.org> - 2.034-1
- Update to 2.034 (updates to test harness)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.033-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 11 2011 Paul Howarth <paul@city-fan.org> - 2.033-1
- Update to 2.033 (made 001xz.t more forgiving when the tests run out of memory)

* Fri Jan  7 2011 Paul Howarth <paul@city-fan.org> - 2.032-1
- Update to 2.032 (no changes)

* Fri Dec 17 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.030-2
- Rebuild to fix problems with vendorarch/lib (#661697)

* Mon Jul 26 2010 Paul Howarth <paul@city-fan.org> - 2.030-1
- Update to 2.030 (no changes)

* Tue May 11 2010 Paul Howarth <paul@city-fan.org> - 2.027-2
- Drop redundant buildroot tag

* Thu Apr 29 2010 Paul Howarth <paul@city-fan.org> - 2.027-1
- Initial RPM version
