# the debuginfo package is empty
%define debug_package %{nil}

# Avoid Epoch inflation
%define module_version 0.59

Name:           perl-Spreadsheet-ParseExcel
Version:        0.5900
Release:        4%{?dist}
Summary:        Extract information from an Excel file
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Spreadsheet-ParseExcel/
Source0:        http://www.cpan.org/authors/id/J/JM/JMCNAMARA/Spreadsheet-ParseExcel-%{module_version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  perl(Crypt::RC4)
BuildRequires:  perl(Digest::Perl::MD5)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(IO::Scalar)
BuildRequires:  perl(Jcode)
BuildRequires:  perl(OLE::Storage_Lite) >= 0.19
BuildRequires:  perl(Proc::ProcessTable)
BuildRequires:  perl(Spreadsheet::WriteExcel)
BuildRequires:  perl(Test::CPAN::Meta)
BuildRequires:  perl(Test::MinimumVersion)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Unicode::Map)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
The Spreadsheet::ParseExcel module can be used to read information from an
Excel 95-2003 file.

%prep
%setup -q -n Spreadsheet-ParseExcel-%{module_version}

# Fix line-endings of sample files
for file in README sample/* ; do
    [ -f "$file" ] && %{__perl} -pi -e 's/\r\n/\n/' "$file"
done

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type d -depth -exec rmdir {} 2>/dev/null ';'
%{_fixperms} %{buildroot}

# For Spreadsheet::ParseExcel::FmtJapan2; see README for details
install -D -m 644 -p CP932Excel.map \
    %{buildroot}%{perl_vendorarch}/Unicode/Map/MS/WIN/CP932Excel.map

%check
make test AUTOMATED_TESTING=1

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes README README_Japan.htm examples/ sample/
%{perl_vendorarch}/Unicode/
%{perl_vendorlib}/Spreadsheet/
%{_mandir}/man3/Spreadsheet::ParseExcel.3pm*
%{_mandir}/man3/Spreadsheet::ParseExcel::Cell.3pm*
%{_mandir}/man3/Spreadsheet::ParseExcel::Dump.3pm*
%{_mandir}/man3/Spreadsheet::ParseExcel::FmtDefault.3pm*
%{_mandir}/man3/Spreadsheet::ParseExcel::FmtJapan.3pm*
%{_mandir}/man3/Spreadsheet::ParseExcel::FmtJapan2.3pm*
%{_mandir}/man3/Spreadsheet::ParseExcel::FmtUnicode.3pm*
%{_mandir}/man3/Spreadsheet::ParseExcel::Font.3pm*
%{_mandir}/man3/Spreadsheet::ParseExcel::Format.3pm*
%{_mandir}/man3/Spreadsheet::ParseExcel::SaveParser.3pm*
%{_mandir}/man3/Spreadsheet::ParseExcel::SaveParser::Workbook.3pm*
%{_mandir}/man3/Spreadsheet::ParseExcel::SaveParser::Worksheet.3pm*
%{_mandir}/man3/Spreadsheet::ParseExcel::Utility.3pm*
%{_mandir}/man3/Spreadsheet::ParseExcel::Workbook.3pm*
%{_mandir}/man3/Spreadsheet::ParseExcel::Worksheet.3pm*

%changelog
* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5900-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 21 2012 Petr Pisar <ppisar@redhat.com> - 0.5900-3
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5900-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Aug 22 2011 Paul Howarth <paul@city-fan.org> - 0.5900-1
- Update to 0.59 (#731907)
  - Patch for decryption of default encrypted workbooks from Alexey Mazurin
  - Fix for invalid formatting of text cells that are numeric (CPAN RT#62073)
- BR: perl(Crypt::RC4) and perl(Digest::Perl::MD5)
- Drop conditionals for EPEL-5 support since Crypt::RC4 isn't available there

* Mon Aug 22 2011 Paul Howarth <paul@city-fan.org> - 0.5800-1
- Update to 0.58
  - Fix for text cells formatted with a leading apostrophe (CPAN RT#61299)
  - Documentation fixes (CPAN RT#61320)
  - Fix for currency locales in format strings (CPAN RT#60547)
  - Fix for incomplete SETUP records

* Mon Aug 22 2011 Paul Howarth <paul@city-fan.org> - 0.5700-1
- Update to 0.57
  - Added fix for reading formatted data from Excel 4 files
  - Added example programs, a_simple_parser.pl and display_text_table.pl
  - Removed Build.PL from README (CPAN RT#52670)
- Package examples as %%doc
- Drop note about sample files not being UTF-8 encoded; no longer applicable

* Mon Aug 22 2011 Paul Howarth <paul@city-fan.org> - 0.5600-1
- Update to 0.56
  - Added error() and error_code() error handling routines, which allows
    encrypted files to be ignored; added t/10_error_codes.t for these methods
    (CPAN RT#47978, CPAN RT#51033)
  - Made version 0.19 of OLE::Storage_Lite a prerequisite to avoid issues when
    writing OLE header in SaveParser
  - Changed Parse() method name to parse() for consistency with the rest of the
    API; the older method name is still supported but not documented
- Bump version requirement for perl(OLE::Storage_Lite) to 0.19
- No longer need to fix line-endings of Changes file

* Mon Aug 22 2011 Paul Howarth <paul@city-fan.org> - 0.5500-1
- Update to 0.55
  - Refactored Worksheet interface and documentation, adding 04_regression.t
    and 05_regression.t to test changes
  - Fixed column units conversion, adding 24_row_col_sizes.t as check
  - Fixed RK number conversion, which was the source of several RT bugs and
    portability issues; added 25_decode_rk_numbers.t test case
  - Added fix for incorrectly skipped charts (CPAN RT#44009)
  - Added fix for locale [$-ddd] strings in number formats (CPAN RT#43638)
  - Added fix for multiple dots in number formats (CPAN RT#45502)
  - Added fix to make half way rounding behave like Excel (CPAN RT#45626)
  - Added checks for valid dates in Utility::ExcelFmt (CPAN RT#48831)
  - Added new FmtJapan module and tests written by Goro Fuji
  - Fixed bug in ExcelFmt() date handling where conversion to weekday and month
    names wasn't handled correctly, adding extra tests to
    21_number_format_user.t
  - Fixed bug when checking $Config{useperlio} (CPAN RT#28861)
  - Fixed bug where CellHandler variables weren't scoped to package
    (CPAN RT#43250)
  - Added tests for ExcelLocaltime() and LocaltimeExcel(),
    26_localtime2excel.t and 27_localtime2excel.t
  - Refactored SaveParser docs
  - Made perl 5.8.0 a requirement for proper Unicode handling
  - Fixed minor int2col() bug, adding 28_int2col.t test (CPAN RT#48967)
  - Refactored Workbook API and docs
  - Fix for height/width of hidden rows/columns with additional tests in
    05_regression.t (CPAN RT#48450)
  - Fix for malformed Print_Title Name block
  - Refactored Cell.pm documentation and method names and added regression
    suite, t/06_regression.t
  - Added float comparison test to avoid false failing tests on 64-bit systems
- Drop perl(Test::More) and perl(Test::Pod) version requirements
- BR: perl(Test::CPAN::Meta) and perl(Test::MinimumVersion), and enable
  AUTOMATED_TESTING
- Fix line-endings of Changes file

* Mon Aug 22 2011 Paul Howarth <paul@city-fan.org> - 0.4900-10
- Revert to ExtUtils::MakeMaker flow preferred by upstream
- Make %%files list more explicit
- Add note about encoding of sample files

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 0.4900-9
- Perl mass rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.4900-8
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4900-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.4900-6
- Rebuild to fix problems with vendorarch/lib (#661697)

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.4900-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.4900-4
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4900-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4900-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 02 2009 Steven Pritchard <steve@kspei.com> 0.4900-1
- Update to 0.49.

* Thu Jan 22 2009 Steven Pritchard <steve@kspei.com> 0.4700-1
- Update to 0.47.

* Sat Jan 17 2009 Steven Pritchard <steve@kspei.com> 0.4500-1
- Update to 0.45.
- s/Get/Extract/ in Summary.
- Update Source0 URL.
- Update description.
- Fix line endings in README and samples.

* Thu Dec 11 2008 Steven Pritchard <steve@kspei.com> 0.3300-1
- Update to 0.33.
- Make Test::More dep versioned.
- BR Test::Pod.

* Mon Mar  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.3200-5
- rebuild for new perl (again)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.3200-4
- Autorebuild for GCC 4.3

* Fri Feb  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.3200-3
- rebuild for new perl

* Thu Jan 10 2008 Ralf Corsépius <rc040203@freenet.de> 0.3200-2
- Update License-tag.
- BR perl(Test::More) (BZ 419631).
- Let package own %%{perl_vendorarch}/Unicode.

* Sat May 19 2007 Steven Pritchard <steve@kspei.com> 0.3200-1
- Update to 0.32.

* Fri Apr 06 2007 Steven Pritchard <steve@kspei.com> 0.3000-1
- Update to 0.30.
- BR Proc::ProcessTable for better test coverage.

* Wed Jan 17 2007 Steven Pritchard <steve@kspei.com> 0.2800-1
- Update to 0.28.
- Drop typo fix.
- BR: Spreadsheet::WriteExcel (for tests).

* Wed Jan 17 2007 Steven Pritchard <steve@kspei.com> 0.2700-2
- Fix typo in Spreadsheet::ParseExcel::FmtUnicode.

* Tue Jan 16 2007 Steven Pritchard <steve@kspei.com> 0.2700-1
- Update to 0.27.
- Cleanup to more closely match cpanspec output.
- Switch to Module::Build-based build.
- BR: IO::Scalar, Unicode::Map, and Jcode.

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 0.2603-3
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 26 2006 Steven Pritchard <steve@kspei.com> 0.2603-2
- Fix find option order.

* Sun May 14 2006 Michael A. Peters <mpeters@mac.com> - 0.2603-1
- Install the CP932Excel.map file
- makes package arch dependent

* Wed May 10 2006 Michael A. Peters <mpeters@mac.com> - 0.2603-0.2
- Changed license to GPL or Artistic per the ParseExcel.pm file

* Wed May 10 2006 Michael A. Peters <mpeters@mac.com> - 0.2603-0.1
- Initial packaging
