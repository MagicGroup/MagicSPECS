Name:           perl-XML-Parser
Version:        2.41
Release:        7%{?dist}
Summary:        Perl module for parsing XML files

Group:          Development/Libraries
License:        GPL+ or Artistic
Url:            http://search.cpan.org/dist/XML-Parser/
Source0:        http://search.cpan.org/CPAN/authors/id/C/CH/CHORNY/XML-Parser-%{version}.tar.gz

BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  expat-devel
# The script LWPExternEnt.pl is loaded by Parser.pm
BuildRequires:  perl(LWP), perl(URI)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(LWP), perl(URI)

%{?filter_setup:
%filter_from_provides /perl(XML::Parser)$/d
%?perl_default_filter
}
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}perl\\(XML::Parser\\)$

%description
This module provides ways to parse XML documents. It is built on top
of XML::Parser::Expat, which is a lower level interface to James
Clark's expat library. Each call to one of the parsing methods creates
a new instance of XML::Parser::Expat which is then used to parse the
document. Expat options may be provided when the XML::Parser object is
created. These options are then passed on to the Expat object on each
parse call. They can also be given as extra arguments to the parse
methods, in which case they override options given at XML::Parser
creation time.

%prep
%setup -q -n XML-Parser-%{version} 
chmod 644 samples/{canonical,xml*}
%{__perl} -pi -e 's|^#!/usr/local/bin/perl\b|#!%{__perl}|' samples/{canonical,xml*}

%build
CFLAGS="$RPM_OPT_FLAGS" %{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags} OPTIMIZE="$RPM_OPT_FLAGS"

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

for file in samples/REC-xml-19980210.xml; do
  iconv -f iso-8859-1 -t utf-8 < "$file" > "${file}_"
  mv -f "${file}_" "$file"
done

magic_rpm_clean.sh

%check


%files
%doc README Changes samples/
%{perl_vendorarch}/XML/
%{perl_vendorarch}/auto/XML/
%{_mandir}/man3/*.3*


%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.41-7
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 2.41-6
- 为 Magic 3.0 重建

* Wed Oct 10 2012 Liu Di <liudidi@gmail.com> - 2.41-5
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.41-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jul 24 2011 Iain Arnell <iarnell@gmail.com> 2.41-3
- update filtering for rpm 4.9

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 2.41-2
- Perl mass rebuild

* Fri Jun  3 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.41-1
- update 2.41
- clean spec from rm, clean, deffattr

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.40-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 jkeating - 2.40-2
- Rebuilt for gcc bug 634757

* Tue Sep 21 2010 Marcela Mašláňová <mmaslano@redhat.com> - 2.40-1
- update 

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.36-9
- Mass rebuild with perl-5.12.0

* Tue Feb  9 2010 Marcela Mašláňová <mmaslano@redhat.com> - 2.36-8
- rebuild with expat-2.0.1-10 which should fix tests part #549216, #555457

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 2.36-7
- rebuild against perl 5.10.1

* Mon Aug 24 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.36-6
- rebuild against perl without DEBUGGING defined

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.36-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.36-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.36-3
- Rebuild for perl 5.10 (again)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.36-2
- Autorebuild for GCC 4.3

* Sun Jan 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.36-1
- bump to 2.36

* Thu Jan 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.34-11
- rebuild for new perl

* Thu Oct 25 2007 Robin Norwood <rnorwood@redhat.com> - 2.34-10
- Add dist tag to release field
- Fix previous changelog

* Tue Oct 23 2007 Robin Norwood <rnorwood@redhat.com> - 2.34-9
- Remove BR: perl
- fix utf-8 rpmlint warning

* Tue Aug 28 2007 Robin Norwood <rnorwood@redhat.com> - 2.34-8
- Update license tag
- Add README Changes samples/ to %%doc section

* Thu Aug  9 2007 Joe Orton <jorton@redhat.com> - 2.34-7
- BuildRequire perl(ExtUtils::MakeMaker)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.34-6.1.2.2.1
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.34-6.1.2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.34-6.1.2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 2.34-6-1.2
- rebuild for new perl-5.8.8

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Thu Apr 21 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.34-6
- #155619
- Bring up to date with current Fedora.Extras perl spec template.

* Sun Aug 08 2004 Alan Cox <alan@redhat.com> 2.34-5
- runtime requires expat

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Apr 16 2004 Warren Togami <wtogami@redhat.com> 2.34-3
- #110597 BR expat-devel

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Chip Turner <cturner@redhat.com> 2.34-1
- update to 2.34

* Mon Jan 26 2004 Jeremy Katz <katzj@redhat.com> 2.31-17
- more rebuilding

* Mon Jan 19 2004 Chip Turner <cturner@redhat.com> 2.31-16
- rebuild for newer perl

* Mon Jan 27 2003 Chip Turner <cturner@redhat.com>
- version bump and rebuild

* Tue Aug  6 2002 Chip Turner <cturner@redhat.com>
- automated release bump and build

* Thu Jun 27 2002 Chip Turner <cturner@redhat.com>
- description update

* Tue Jun  4 2002 Chip Turner <cturner@redhat.com>
- properly claim directories owned by package so they are removed when
  package is removed

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Dec 7 2001 root <root@redhat.com>
- Spec file was autogenerated. 
