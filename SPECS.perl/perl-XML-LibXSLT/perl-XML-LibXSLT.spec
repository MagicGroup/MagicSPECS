Name:		perl-XML-LibXSLT
# NOTE: also update perl-XML-LibXML to a compatible version.  See below why.
Version:	1.94
Release:	2%{?dist}
Summary:	Perl module for interfacing to GNOME's libxslt
Group:		Development/Libraries
License:	GPL+ or Artistic
URL:		http://search.cpan.org/dist/XML-LibXSLT/
Source0:	http://search.cpan.org/CPAN/authors/id/S/SH/SHLOMIF/XML-LibXSLT-%{version}.tar.gz
BuildRequires:	perl(Carp)
BuildRequires:	perl(DynaLoader)
BuildRequires:	perl(Encode)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(Test::More)
BuildRequires:	libxslt-devel >= 1.1.18, gdbm-devel, libgcrypt-devel, libgpg-error-devel
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
# the package shares code with perl-XML-LibXML, we have to require a compatible version
# see https://bugzilla.redhat.com/show_bug.cgi?id=469480
# for testing is needed the same version of XML::LibXML
# BUT XML::LibXML has new bugfix releases, but XML::LibXSLT not
BuildRequires:	perl(XML::LibXML::Boolean)
BuildRequires:	perl(XML::LibXML::Literal)
BuildRequires:	perl(XML::LibXML::NodeList)
BuildRequires:	perl(XML::LibXML::Number)
BuildRequires:	perl(XML::LibXML) >= %{version}
Requires:	perl(XML::LibXML) >= %{version}

%description
This module is a fast XSLT library, based on the Gnome libxslt engine
that you can find at http://www.xmlsoft.org/XSLT/

%{?perl_default_filter}

%prep
%setup -q -n XML-LibXSLT-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
chmod -R u+w %{buildroot}/*

%check
make test

%files
%doc Changes README benchmark example
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/XML
%{_mandir}/man3/*.3*

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1.94-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.94-1
- 更新到 1.94

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.79-2
- 为 Magic 3.0 重建

* Mon Nov 26 2012 Petr Pisar <ppisar@redhat.com> - 1.79-1
- 1.79 bump

* Fri Sep 14 2012 Jitka Plesnikova <jplesnik@redhat.com> - 1.78-1
- 1.78 bump

* Mon Aug 27 2012 Jitka Plesnikova <jplesnik@redhat.com> - 1.77-4
- Update source link.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.77-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 1.77-2
- Perl 5.16 rebuild

* Mon Feb 27 2012 Petr Šabata <contyk@redhat.com> - 1.77-1
- 1.77 bump
- Remove some ugly macros

* Fri Jan 13 2012 Marcela Mašláňová <mmaslano@redhat.com> - 1.76-1
- 1.76 bump

* Mon Oct 31 2011 Petr Sabata <contyk@redhat.com> - 1.75-1
- 1.75 bump

* Wed Oct 26 2011 Petr Sabata <contyk@redhat.com> - 1.74-1
- 1.74 bump

* Tue Oct 11 2011 Petr Sabata <contyk@redhat.com> - 1.73-1
- 1.73 bump

* Fri Oct 07 2011 Petr Sabata <contyk@redhat.com> - 1.72-1
- 1.72 bump
- benchmark.pl moved to benchmark/

* Mon Sep 19 2011 Petr Sabata <contyk@redhat.com> - 1.71-1
- 1.71 bump
- Remove BuildRoot tag
- Remove useless vendorarch macro definition

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 1.70-8
- Perl mass rebuild

* Fri Jun 24 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.70-7
- clean spec, comment BR on XML::LibXML, use filter on *.so

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.70-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Nov  5 2010 Marcela Mašláňová <mmaslano@redhat.com> - 1.70-5
- add BR

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.70-4
- Mass rebuild with perl-5.12.0

* Thu Mar 11 2010 Paul Howarth <paul@city-fan.org> - 1.70-3
- rebuild for new gdbm

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.70-2
- rebuild against perl 5.10.1

* Fri Nov 20 2009 Marcela Mašláňová <mmaslano@redhat.com> - 1:1.70-1
- update to fix 539102

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.68-4
- rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Mar 18 2009 Stepan Kasal <skasal@redhat.com> - 1.68-3
- patch to fix a refcounting bug leading to segfaults (#490781)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.68-2
- rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Dec 20 2008 Paul Howarth <paul@city-fan.org> - 1.68-1
- update to 1.68
- relax hard version requirement on XML::LibXML, which is at 1.69 upstream
  but 1.67 or above will suffice (care will still have to be taken to keep
  the packages in sync, particularly when XML::LibXML is updated)
- specify $RPM_OPT_FLAGS once rather than twice
- drop historical perl version requirement, which is met even by EL-3
- explicitly buildreq ExtUtils::MakeMaker rather than just perl-devel

* Mon Nov  3 2008 Stepan Kasal <skasal@redhat.com> - 1.66-2
- require XML::LibXML of the same version

* Fri Aug  8 2008 Zing <zing@fastmail.fm> - 1.66-1
- update to 1.66

* Sat May 31 2008 Zing <zing@fastmail.fm> - 1.63-6
- rpm check stage barfs on || :

* Mon Mar  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.63-5
- rebuild for new perl (again)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.63-4
- Autorebuild for GCC 4.3

* Fri Feb  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.63-3
- rebuild for new perl

* Sat Jan 19 2008 Zing <zing@fastmail.fm> - 1.63-2
- build requires gdbm-devel

* Fri Jan 18 2008 Zing <zing@fastmail.fm> - 1.63-1
- update to 1.63

* Sat Aug 11 2007 Zing <zing@fastmail.fm> - 1.62-2
- require perl-devel

* Tue Aug  7 2007 Zing <zing@fastmail.fm> - 1.62-1
- update to 1.62
- Conform to Fedora Licensing Guideline

* Fri Sep  8 2006 Zing <zing@fastmail.fm> - 1.58-3
- rebuild for FE6

* Tue Feb 14 2006 Zing <shishz@hotpop.com> - 1.58-2
- rebuild for FE5

* Wed Aug 17 2005 Zing <shishz@hotpop.com> - 1.58-1
- new upstream
- use dist macro

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sat Mar  5 2005 Ville Skyttä <ville.skytta at iki.fi> - 1.57-3
- Drop pre-FC2 LD_RUN_PATH hack.
- Install benchmark.pl only as %%doc.

* Fri Feb 26 2005 Zing <shishz@hotpop.com> - 1.57-2
- QA from Ville Skyttä
-	BuildRequires XML::LibXML >= 1.57
-	BuildRequires libxslt-devel
-	put benchmark.pl in %%doc

* Fri Feb 25 2005 Zing <shishz@hotpop.com> - 1.57-1
- First build.
