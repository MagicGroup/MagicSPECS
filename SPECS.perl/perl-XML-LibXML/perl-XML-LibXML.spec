Name:           perl-XML-LibXML
# NOTE: also update perl-XML-LibXSLT to a compatible version, see
# https://bugzilla.redhat.com/show_bug.cgi?id=469480
# it might not be needed anymore
# this module is maintained, the other is not
Version:	2.0122
Release:	2%{?dist}
Epoch:          1
Summary:        Perl interface to the libxml2 library

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/XML-LibXML/
Source0:        http://search.cpan.org/CPAN/authors/id/S/SH/SHLOMIF/XML-LibXML-%{version}.tar.gz 

BuildRequires:  libxml2-devel
BuildRequires:  perl(Devel::CheckLib)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec)
# Run-time
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(Encode)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Tie::Hash)
BuildRequires:  perl(XML::NamespaceSupport)
BuildRequires:  perl(XML::SAX::Base)
BuildRequires:  perl(XML::SAX::DocumentLocator)
BuildRequires:  perl(XML::SAX::Exception)
# Tests
# Optional Test::Differences has a fall-back
BuildRequires:  perl(Errno)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(XML::SAX)
# Optional tests
BuildRequires:  perl(Test::Pod) >= 1.14
BuildRequires:  perl(threads)
BuildRequires:  perl(threads::shared)
BuildRequires:  perl(URI::file)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
# threads and threads::shared are optional
Provides:       perl-XML-LibXML-Common = %{version}
Obsoletes:      perl-XML-LibXML-Common <= 0.13

%{?perl_default_filter}

%description
This module implements a Perl interface to the GNOME libxml2 library
which provides interfaces for parsing and manipulating XML files. This
module allows Perl programmers to make use of the highly capable
validating XML parser and the high performance DOM implementation.

%prep
%setup -q -n XML-LibXML-%{version}
chmod -x *.c
for i in Changes; do
  /usr/bin/iconv -f iso8859-1 -t utf-8 $i > $i.conv && /bin/mv -f $i.conv $i
done
# Remove bundled modules
rm -r inc/*
sed -i -e '/^inc\// d' MANIFEST

%build
perl Makefile.PL SKIP_SAX_INSTALL=1 INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -empty -exec rm -f {} ';'
find %{buildroot} -type d -depth -exec rmdir {} ';' 2>/dev/null
chmod -R u+w %{buildroot}/*

%check
THREAD_TEST=1 

%triggerin -- perl-XML-SAX
for p in XML::LibXML::SAX::Parser XML::LibXML::SAX ; do
  perl -MXML::SAX -e "XML::SAX->add_parser(q($p))->save_parsers()" \
    2>/dev/null || :
done

%preun
if [ $1 -eq 0 ] ; then
  for p in XML::LibXML::SAX::Parser XML::LibXML::SAX ; do
    perl -MXML::SAX -e "XML::SAX->remove_parser(q($p))->save_parsers()" \
      2>/dev/null || :
  done
fi

%files
%doc Changes HACKING.txt LICENSE README TODO
%{perl_vendorarch}/auto/XML
%{perl_vendorarch}/XML
%{_mandir}/man3/*.3*

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1:2.0122-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1:2.0122-1
- 更新到 2.0122

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1:2.0006-5
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1:2.0006-4
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1:2.0006-3
- 为 Magic 3.0 重建

* Mon Oct 15 2012 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0006-1
- 2.0006 bump
- Remove bundled library and add BR perl(Devel::CheckLib).

* Mon Aug 27 2012 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0004-2
- Rebuild for the latest libxml2.

* Thu Aug 09 2012 Petr Šabata <contyk@redhat.com> - 1:2.0004-1
- 2.0004 bump

* Fri Aug 03 2012 Petr Pisar <ppisar@redhat.com> - 1:2.0003-2
- Re-enable 12html test as the bug has been fixed (bug #769537)

* Mon Jul 30 2012 Petr Šabata <contyk@redhat.com> - 1:2.0003-1
- 2.0003 bump

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.0002-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 11 2012 Petr Pisar <ppisar@redhat.com> - 1:2.0002-2
- Perl 5.16 rebuild

* Tue Jul 10 2012 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.0002-1
- 2.0002 bump

* Thu Jun 28 2012 Petr Pisar <ppisar@redhat.com> - 1:2.0001-2
- Perl 5.16 rebuild

* Thu Jun 21 2012 Petr Šabata <contyk@redhat.com> - 1:2.0001-1
- 2.0001 bump

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 1:1.99-2
- Perl 5.16 rebuild

* Mon Jun 04 2012 Petr Šabata <contyk@redhat.com> - 1:1.99-1
- 1.99 bump, test updates

* Mon May 28 2012 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.98-1
- 1.98 bump

* Wed May 02 2012 Petr Šabata <contyk@redhat.com> - 1:1.97-1
- 1.97 bump

* Mon Mar 19 2012 Marcela Mašláňová <mmaslano@redhat.com> - 1:1.96-1
- 1.96 bump

* Wed Mar 14 2012 Petr Šabata <contyk@redhat.com> - 1:1.95-1
- 1.95 bump, tests bugfixes

* Mon Feb 27 2012 Petr Šabata <contyk@redhat.com> - 1:1.93-1
- 1.93 bumpity, minor bugfix

* Thu Feb 23 2012 Petr Pisar <ppisar@redhat.com> - 1:1.92-1
- 1.92 bump
- Declare all dependencies
- Enable thread tests

* Wed Jan 10 2012 Marcela Mašláňová <mmaslano@redhat.com> - 1:1.90-1
- update to 1.90

* Wed Dec 21 2011 Dan Horák <dan[at]danny.cz> - 1:1.88-3
- use better workaround until rhbz#769537 is resolved

* Tue Dec 20 2011 Karsten Hopp <karsten@redhat.com> - 1:1.88-2
- disable tests on ppc as most ppc buildmachines have only 2Gb 
  and the tests run out of memory

* Sun Oct  2 2011 Tom Callaway <spot@fedoraproject.org> - 1:1.88-1
- update to 1.88

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 1:1.74-2
- Perl mass rebuild

* Fri Jun 24 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1:1.74-1
- update to 1.74

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.70-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Nov  5 2010 Paul Howarth <paul@city-fan.org> - 1:1.70-6
- Rebuild for libxml2 2.7.8 in Rawhide
- Move recoding of documentation from %%install to %%prep
- Use %%{?perl_default_filter}
- Use standard %%install idiom

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 1:1.70-5
- Mass rebuild with perl-5.12.0

* Fri Jan  8 2010 Marcela Mašláňová <mmaslano@redhat.com> - 1:1.70-4
- remove BR XML::LibXML::Common

* Mon Nov 30 2009 Marcela Mašláňová <mmaslano@redhat.com> - 1:1.70-3
- corrected version of obsoletes

* Thu Nov 26 2009 Marcela Mašláňová <mmaslano@redhat.com> - 1:1.70-2
- 541605 this package now contains XML::LibXML::Common

* Fri Nov 20 2009 Marcela Mašláňová <mmaslano@redhat.com> - 1:1.70-1
- update to fix 539102

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.69-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.69-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec 11 2008 Marcela Mašláňová <mmaslano@redhat.com> - 1:1.69-1
- update to 1.69

* Fri Aug 01 2008 Lubomir Rintel <lkundrak@v3.sk> - 1:1.66-2
- Supress warning about nonexistent file in perl-XML-SAX install trigger

* Mon Jun 23 2008 Marcela Maslanova <mmaslano@redhat.com> - 1:1.66-1
- upgrade to 1.66

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1:1.65-5
- Rebuild for perl 5.10 (again)

* Mon Feb 11 2008 Robin Norwood <rnorwood@redhat.com> - 1:1.65-4
- Build for new perl

* Mon Feb 11 2008 Robin Norwood <rnorwood@redhat.com> - 1:1.65-3
- Resolves: bz#432442
- Use epoch to permit upgrade from 1.62001 -> 1.65

* Mon Jan 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.65-2
- disable hacks, build normally

* Thu Jan 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.65-1.1
- rebuild for new perl, first pass, temporarily disable BR: XML::Sax, tests

* Wed Oct 24 2007 Robin Norwood <rnorwood@redhat.com> - 1.65-1
- Update to latest CPAN release: 1.65
- patch0 no longer needed
- various spec file cleanups

* Wed Oct 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.62001-2.3
- fix stupid test

* Wed Oct 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.62001-2.2
- add BR: perl(Test::More)

* Wed Oct 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.62001-2.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Thu Dec 07 2006 Robin Norwood <rnorwood@redhat.com> - 1.62001-2
- Rebuild

* Sat Dec 02 2006 Robin Norwood <rnorwood@redhat.com> - 1.62001
- Build latest version from CPAN: 1.62001

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.58-2.2.2.1
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.58-2.2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.58-2.2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 1.58-2.2
- rebuild for new perl-5.8.8

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Sat Mar 19 2005 Joe Orton <jorton@redhat.com> 1.58-2
- rebuild

* Sun Apr 18 2004 Ville Skyttä <ville.skytta at iki.fi> - 1.58-1
- #121168
- Update to 1.58.
- Require perl(:MODULE_COMPAT_*).
- Handle ParserDetails.ini parser registration.
- BuildRequires libxml2-devel.
- Own installed directories.

* Fri Feb 27 2004 Chip Turner <cturner@redhat.com> - 1.56-1
- Specfile autogenerated.
