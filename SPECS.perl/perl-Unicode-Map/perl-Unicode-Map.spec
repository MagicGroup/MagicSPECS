%{!?perl_vendorarch: %define perl_vendorarch %(eval "`%{__perl} -V:installvendorarch`"; echo $installvendorarch)}

Name:           perl-Unicode-Map
Version:        0.112
Release:        27%{?dist}

Summary:        Perl module for mapping charsets from and to utf16 unicode

License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Unicode-Map/
Source0:        http://www.cpan.org/authors/id/M/MS/MSCHWARTZ/Unicode-Map-0.112.tar.gz

BuildRequires:  perl(ExtUtils::MakeMaker) 
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
This module converts strings from and to 2-byte Unicode UCS2
format. All mappings happen via 2 byte UTF16 encodings, not via 1 byte
UTF8 encoding. To convert between UTF8 and UTF16 use Unicode::String.
For historical reasons this module coexists with Unicode::Map8.
Please use Unicode::Map8 unless you need to care for >1 byte character
sets, e.g. chinese GB2312. Anyway, if you stick to the basic
functionality (see documentation) you can use both modules
equivalently.
Practically this module will disappear from earth sooner or later as
Unicode mapping support needs somehow to get into perl's core. If you
like to work on this field please don't hesitate contacting Gisle Aas
and check out the mailing list perl-unicode!


%prep
%setup -q -n Unicode-Map-%{version}
# See bug 191387
echo '
# Add support for perl-Spreadsheet-ParseExcel
name:    CP932Excel
srcURL:  $SrcUnicode/VENDORS/MICSFT/WINDOWS/CP932.TXT
src:     $DestUnicode/VENDORS/MICSFT/WINDOWS/CP932.TXT
map:     $DestMap/MS/WIN/CP932Excel.map
' >> Map/REGISTRY


%build
CFLAGS="$RPM_OPT_FLAGS" %{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags} OPTIMIZE="$RPM_OPT_FLAGS"


%install
make install \
  PERL_INSTALL_ROOT=$RPM_BUILD_ROOT \
  INSTALLARCHLIB=$RPM_BUILD_ROOT%{perl_archlib}
find $RPM_BUILD_ROOT -type f -a \( -name perllocal.pod -o -name .packlist \
  -o \( -name '*.bs' -a -empty \) \) -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*


%check
make test


%files
%doc COPYING Changes README
%{_bindir}/m*
%{perl_vendorarch}/auto/Unicode
%{perl_vendorarch}/Unicode
%{_mandir}/man[13]/*.[13]*


%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.112-27
- 为 Magic 3.0 重建

* Sun Dec 02 2012 Emmanuel Seyman <emmanuel@seyman.fr> - 0.112-26
- Add perl default filter
- Remove no-longer-used macros

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.112-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 0.112-24
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.112-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.112-22
- Perl mass rebuild

* Fri Jul  8 2011 Paul Howarth <paul@city-fan.org> - 0.112-21
- Add perl(:MODULE_COMPAT_*) dependency

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.112-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 23 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.112-19
- Rebuild to fix problems with vendorarch/lib (#661697)

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.112-18
- Mass rebuild with perl-5.12.0

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.112-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.112-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jun 05 2008 Aurelien Bompard <abompard@fedoraproject.org> 0.112-15
- fix build

* Mon Mar  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.112-14
- rebuild for new perl (again)

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.112-13
- Autorebuild for GCC 4.3

* Fri Feb  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.112-12
- rebuild for new perl

* Thu Sep 27 2007 Aurelien Bompard <abompard@fedoraproject.org> 0.112-11
- fix license tag (thanks Tom)

* Sun Aug 26 2007 Aurelien Bompard <abompard@fedoraproject.org> 0.112-10
- rebuild for BuildID
- fix license tag (like perl itself)

* Mon Aug 13 2007 Aurelien Bompard <abompard@fedoraproject.org> 0.112-9
- BR: perl-devel

* Wed Aug 30 2006 Aurelien Bompard <abompard@fedoraproject.org> 0.112-8
- Add support for perl-Spreadsheet-ParseExcel (bug 191387)

* Tue Feb 21 2006 Aurelien Bompard <gauret[AT]free.fr> 0.112-7
- rebuild for FC5

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Mon Feb  2 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.112-0.fdr.5
- Reduce directory ownership bloat.

* Sat Oct 11 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.112-0.fdr.4
- Install into vendor dirs.
- Specfile cleanup.

* Mon Jul  7 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.112-0.fdr.3
- Regenerate %%install section with cpanflute2.
- Improve %%description.

* Sun May  4 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.112-0.fdr.2
- Own more dirs.

* Fri Mar 21 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.112-0.fdr.1
- Update to current Fedora guidelines.

* Sun Mar  2 2003 Ville Skyttä <ville.skytta at iki.fi> - 0.112-1.fedora.1
- First Fedora release.
