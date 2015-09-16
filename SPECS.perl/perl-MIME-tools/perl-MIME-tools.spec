Summary:	Modules for parsing and creating MIME entities in Perl
Name:		perl-MIME-tools
Version:	5.506
Release:	1%{?dist}
Group:		Development/Libraries
License:	GPL+ or Artistic
URL:		http://search.cpan.org/dist/MIME-tools/
Source0:	http://search.cpan.org/CPAN/authors/id/D/DS/DSKOLL/MIME-tools-%{version}.tar.gz
Patch0:		MIME-tools-5.502-UTF8.patch
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(File::Path)	>= 1
BuildRequires:	perl(File::Spec)	>= 0.6
BuildRequires:	perl(File::Temp)	>= 0.18
BuildRequires:	perl(IO::File)		>= 1.13
BuildRequires:	perl(IO::Handle)
BuildRequires:	perl(Mail::Field)	>= 1.05
BuildRequires:	perl(Mail::Header)	>= 1.01
BuildRequires:	perl(Mail::Internet)	>= 1.0203
BuildRequires:	perl(MIME::Base64)	>= 3.03
BuildRequires:	perl(MIME::QuotedPrint)
BuildRequires:	perl-MailTools		>= 1.50
BuildRequires:	perl(Test::Deep)
BuildRequires:	perl(Test::More)
BuildRequires:	perl(Test::Pod)
BuildRequires:	perl(Test::Pod::Coverage)
BuildRequires:	perl(Test::Kwalitee)
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
MIME-tools - modules for parsing (and creating!) MIME entities. Modules in this
toolkit: Abstract message holder (file, scalar, etc.), OO interface for
decoding MIME messages, an extracted and decoded MIME entity, Mail::Field
subclasses for parsing fields, a parsed MIME header (Mail::Header subclass),
parser and tool for building your own MIME parser, and utilities.

%prep
%setup -q -n MIME-tools-%{version}

# Fix character encoding
%patch0 -p1

# The more useful examples will go in %%{_bindir}
mkdir useful-examples
mv examples/mime{dump,encode,explode,postcard,send} useful-examples/

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} ';' 2>/dev/null
%{_fixperms} %{buildroot}

# Put the more useful examples in %%{_bindir}
install -d -m 755 %{buildroot}%{_bindir}
install -d -m 755 %{buildroot}%{_mandir}/man1
cd useful-examples
for ex in mime*
do
	install -p -m 755 ${ex} %{buildroot}%{_bindir}/
	pod2man ${ex} > %{buildroot}%{_mandir}/man1/${ex}.1
done
cd -

%check
# POD Coverage test fails due to lots of undocumented routines
TEST_POD_COVERAGE=0 

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README COPYING ChangeLog
# Adding examples introduces additional deps, but these are all satisfied by
# perl, perl-MIME-tools, and perl-MailTools, which are all deps anyway.
%doc examples
%{perl_vendorlib}/MIME/
%{_bindir}/mimedump
%{_bindir}/mimeencode
%{_bindir}/mimeexplode
%{_bindir}/mimepostcard
%{_bindir}/mimesend
%{_mandir}/man1/mimedump.1*
%{_mandir}/man1/mimeencode.1*
%{_mandir}/man1/mimeexplode.1*
%{_mandir}/man1/mimepostcard.1*
%{_mandir}/man1/mimesend.1*
%{_mandir}/man3/MIME::Body.3pm*
%{_mandir}/man3/MIME::Decoder.3pm*
%{_mandir}/man3/MIME::Decoder::Base64.3pm*
%{_mandir}/man3/MIME::Decoder::BinHex.3pm*
%{_mandir}/man3/MIME::Decoder::Binary.3pm*
%{_mandir}/man3/MIME::Decoder::Gzip64.3pm*
%{_mandir}/man3/MIME::Decoder::NBit.3pm*
%{_mandir}/man3/MIME::Decoder::QuotedPrint.3pm*
%{_mandir}/man3/MIME::Decoder::UU.3pm*
%{_mandir}/man3/MIME::Entity.3pm*
%{_mandir}/man3/MIME::Field::ConTraEnc.3pm*
%{_mandir}/man3/MIME::Field::ContDisp.3pm*
%{_mandir}/man3/MIME::Field::ContType.3pm*
%{_mandir}/man3/MIME::Field::ParamVal.3pm*
%{_mandir}/man3/MIME::Head.3pm*
%{_mandir}/man3/MIME::Parser.3pm*
%{_mandir}/man3/MIME::Parser::Filer.3pm*
%{_mandir}/man3/MIME::Parser::Reader.3pm*
%{_mandir}/man3/MIME::Parser::Results.3pm*
%{_mandir}/man3/MIME::Tools.3pm*
%{_mandir}/man3/MIME::WordDecoder.3pm*
%{_mandir}/man3/MIME::Words.3pm*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 5.506-1
- 更新到 5.506

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 5.502-8
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 5.502-7
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 5.502-6
- 为 Magic 3.0 重建

* Thu Jan 12 2012 Paul Howarth <paul@city-fan.org> - 5.502-5
- Fedora 17 mass rebuild

* Wed Oct 26 2011 Paul Howarth <paul@city-fan.org> - 5.502-4
- Use patch rather than scripted iconv to fix character encoding
- Use DESTDIR rather than PERL_INSTALL_ROOT
- Nobody else likes macros for commands
- Use %%{_fixperms} macro rather than our own chmod incantation
- Explicitly specify all manpages in %%files list
- The Makefile.PL --skipdeps option is no longer needed

* Wed Oct 26 2011 Marcela Mašláňová <mmaslano@redhat.com> - 5.502-3
- Own only man pages of this packages (conflict with Perl package)

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 5.502-2
- Perl mass rebuild

* Tue Mar  8 2011 Paul Howarth <paul@city-fan.org> - 5.502-1
- Update to 5.502
  - Fix parsing bug (CPAN RT#66025)
  - Fix typo (CPAN RT#65387)
  - Fix unit tests on Perl 5.8.x (CPAN RT#66188)
  - Fix unit test failure on Win32 (CPAN RT#66286)

* Thu Feb 17 2011 Paul Howarth <paul@city-fan.org> - 5.501-1
- Update to 5.501
  - Add build_requires 'Test::Deep'; to Makefile (CPAN RT#64659)
  - Fix spelling errors (CPAN RT#64610)
  - Fix double-decoding bug when decoding RFC-2231-encoded parameters
    (CPAN RT#65162)
  - Fix inappropriate inclusion of CR characters in parsed headers
    (CPAN RT#65681)
  - Document that MIME::WordDecoder is mostly deprecated
  - Document that MIME::Head->get(...) can include a trailing newline
  - Increase buffer size from 2kB to 8kB in MIME::Entity and MIME::Body
    (part of CPAN RT#65162)
- This release by DSKOLL -> update source URL

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.500-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 10 2011 Paul Howarth <paul@city-fan.org> - 5.500-1
- Update to 5.500
  - cleanup: IO-Stringy is no longer used
  - cleanup: remove auto_install from Makefile.PL
  - RT#22684: fix deadlock in filter() when invoking external programs
    such as gzip
  - RT#60931: if preamble is empty, make sure it's still empty after
    round-tripping through MIME::Entity
  - RT#63739: properly decode RFC2231 encodings in attachment filenames
- New build requirements:
  - perl(IO::Handle)
  - perl(Mail::Field) >= 1.05
  - perl(Mail::Header) >= 1.01
  - perl(Mail::Internet) >= 1.0203
  - perl(Test::Deep)
- Drop buildreq perl(IO::Stringy)

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 5.428-3
- Rebuild to fix problems with vendorarch/lib (#661697)

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 5.428-2
- Mass rebuild with perl-5.12.0

* Thu Apr 22 2010 Paul Howarth <paul@city-fan.org> - 5.428-1
- Update to 5.428
  - RT#56764: build release with a newer Module::Install
  - RT#52924: ensure we add <> around Content-id data
  - RT#48036: make mimesend example script a bit more useful
  - RT#43439: fix for parsing of doubled ; in multipart headers
  - RT#41632: if RFC-2231 and non-RFC-2231 params present, use only RFC-2231
  - RT#40715: reference Encode::MIME::Header in docs
  - RT#39985: correct POD typos
  - Only bind to localhost in smtpsend test, not all interfaces
- Specify --skipdeps in Makefile.PL invocation to prevent use of CPAN module
- Buildreq perl(Test::Kwalitee) for additional test coverage
- Tidy up %%description and other largely cosmetic spec changes

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 5.427-4
- Rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.427-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.427-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul  1 2008 Paul Howarth <paul@city-fan.org> 5.427-1
- Update to 5.427
- Require and BuildRequire perl(IO::File) >= 1.13

* Wed Mar 19 2008 Paul Howarth <paul@city-fan.org> 5.426-1
- Update to 5.426
- Now require File::Temp >= 0.18
- Add POD tests, coverage disabled because of lack of coverage from upstream

* Tue Mar 11 2008 Paul Howarth <paul@city-fan.org> 5.425-1
- Update to 5.425
- Add note about File::Temp requirement
- New upstream maintainer -> updated URL for source
- Given that this package will not build on old distributions, don't cater
  for handling old versions of MIME::QuotedPrint in %%check and buildreq
  perl(MIME::Base64) >= 3.03
- Buildreq perl(File::Path) >= 1, perl(File::Spec) >= 0.6, and
  perl(IO::Stringy) >= 2.110
- Only include README as %%doc, not README*
- Dispense with provides filter, no longer needed

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 5.420-6
- Rebuild for perl 5.10 (again)

* Sun Jan 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> 5.420-5
- rebuild for new perl

* Mon Aug 13 2007 Paul Howarth <paul@city-fan.org> 5.420-4
- Clarify license as GPL v1 or later, or Artistic (same as perl)
- Add buildreq perl(Test::More)

* Tue Apr 17 2007 Paul Howarth <paul@city-fan.org> 5.420-3
- Buildrequire perl(ExtUtils::MakeMaker)
- Fix argument order for find with -depth

* Tue Aug  8 2006 Paul Howarth <paul@city-fan.org> 5.420-2
- Install the more useful examples in %%{_bindir} (#201691)

* Wed Apr 19 2006 Paul Howarth <paul@city-fan.org> - 5.420-1
- 5.420
- Cosmetic changes reflecting new maintainer's preferences
- Examples remain executable since they don't introduce new dependencies
- Simplify provides filter

* Mon Jan 16 2006 Ville Skyttä <ville.skytta at iki.fi> - 5.419-1
- 5.419.
- Don't provide perl(main).

* Tue Oct  4 2005 Paul Howarth <paul@city-fan.org> - 5.418-2
- License is same as perl (GPL or Artistic), not just Artistic

* Mon Oct  3 2005 Ville Skyttä <ville.skytta at iki.fi> - 5.418-1
- 5.418.
- Cosmetic specfile cleanups.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 5.417-2
- rebuilt

* Sat Jan 22 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:5.417-1
- Update to 5.417.

* Wed Jan  5 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:5.416-0.fdr.1
- Update to 5.416.

* Thu Oct 28 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:5.415-0.fdr.1
- Update to 5.415.

* Thu Oct  7 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:5.414-0.fdr.1
- Update to 5.414.

* Wed Sep 15 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:5.413-0.fdr.1
- Update to 5.413, includes the mimedefang patches.
- Bring up to date with current fedora.us Perl spec template.

* Sat Feb  7 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:5.411-0.fdr.6.a
- Install into vendor dirs.
- BuildRequire perl-MailTools (bug 373).

* Sat Aug 16 2003 Dams <anvil[AT]livna.org> 0:5.411-0.fdr.5.a
- Hopefully fixed BuildRequires (for )
- rm-ing perllocal.pod instead of excluding it

* Sat Jul 12 2003 Dams <anvil[AT]livna.org> 0:5.411-0.fdr.4.a
- Package is now noarch

* Fri Jul 11 2003 Dams <anvil[AT]livna.org> 0:5.411-0.fdr.3.a
- Changed Group tag value
-  in build section
- Added missing directory

* Wed Jun 25 2003 Dams <anvil[AT]livna.org> 0:5.411-0.fdr.2.a
- Now using roaringpenguin tarball

* Sun Jun 15 2003 Dams <anvil[AT]livna.org>
- Initial build.
