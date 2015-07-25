Name:           perl-XML-Simple
Version:        2.20
Release:        11%{?dist}
Summary:        Easy API to maintain XML in Perl
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/XML-Simple/
Source0:        http://www.cpan.org/authors/id/G/GR/GRANTM/XML-Simple-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(Storable)
#BuildRequires:  perl(XML::LibXML)
#BuildRequires:  perl(XML::LibXML::Common)
BuildRequires:  perl(XML::NamespaceSupport)
BuildRequires:  perl(XML::Parser)
BuildRequires:  perl(XML::SAX)
# Tests only
BuildRequires:  perl(base)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Tie::IxHash)
BuildRequires:  perl(XML::SAX::Base)
Requires:  perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(File::Spec)
Requires:       perl(IO::Handle)
Requires:       perl(Storable)
Requires:       perl(XML::NamespaceSupport)
Requires:       perl(XML::Parser)
Requires:       perl(XML::SAX)

%description
The XML::Simple module provides a simple API layer on top of an
underlying XML parsing module (either XML::Parser or one of the SAX2
parser modules).

%prep
%setup -q -n XML-Simple-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w %{buildroot}/*

%check


%files
%doc Changes README
%{perl_vendorlib}/XML/
%{_mandir}/man3/*.3*

%changelog
* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 2.20-11
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 2.20-10
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 2.20-9
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.20-8
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.20-7
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.20-6
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 2.20-5
- 为 Magic 3.0 重建

* Fri Aug 24 2012 Jitka Plesnikova <jplesnik@redhat.com> - 2.20-4
- Add test BR perl(XML::SAX::Base)
- Add R perl(IO::Handle), remove duplicate R perl(File::Spec).

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 28 2012 Petr Pisar <ppisar@redhat.com> - 2.20-2
- Perl 5.16 rebuild

* Thu Jun 21 2012 Petr Šabata <contyk@redhat.com> - 2.20-1
- 2.20 bump
- Modernize spec

* Fri Jun 15 2012 Petr Pisar <ppisar@redhat.com> - 2.18-12
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.18-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 2.18-10
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.18-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 23 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.18-8
- 661697 rebuild for fixing problems with vendorach/lib

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.18-7
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 2.18-6
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.18-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.18-3
- Rebuild for perl 5.10 (again)

* Mon Jan 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.18-2
- rebuild for new perl

* Thu Oct 25 2007 Robin Norwood <rnorwood@redhat.com> - 2.18-1
- Update to latest upstream version.

* Tue Oct 23 2007 Robin Norwood <rnorwood@redhat.com> - 2.17-2
- Remove BR: perl

* Mon Aug 13 2007 Robin Norwood <rnorwood@redhat.com> - 2.17-1
- Update to latest CPAN version: 2.17
- Add BuildRequires
- Fix macro-in-changelog rpmlint warning
- Fix license tag

* Tue Dec 05 2006 Robin Norwood <rnorwood@redhat.com> - 2.16-2
- Fix incorrect 'Release' tag - removed extra dot.

* Sat Dec 02 2006 Robin Norwood <rnorwood@redhat.com> - 2.16-1
- Upgrade to latest CPAN version: 2.16

* Wed Jun  7 2006 Jason Vas Dias <jvdias@redhat.com> - 2.14-4
- fix bug 191911:  fails when default Parser is XML::SAX::PurePerl -
                  succeeds when default Parser is XML::LibXML::SAX -
                  +BuildRequires: perl(XML::LibXML) perl(XML::LibXML::Common)

* Wed Jun  7 2006 Matthias Clasen <mclasen@redhat.com> - 2.14-2.2
- Require perl-XML-Parser (#193985)

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 2.14-2.1
- rebuild for new perl-5.8.8

* Tue Jan 17 2006 Matthias Clasen <mclasen@redhat.com> - 2.14-2
- Pull perl-XML-Simple from Extras into Core 
  for dependency reasons

* Fri Sep  9 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.14-1
- Update to 2.14.
- Added the dist tag.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 2.13-2
- rebuilt

* Sat Nov 27 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:2.13-1
- Update to 2.13.

* Wed May 12 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:2.12-0.fdr.4
- Avoid creation of the perllocal.pod file (make pure_install).

* Thu May  6 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:2.12-0.fdr.3
- build requirement for perl < 5.8.0 - perl(Storable)

* Thu May  6 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:2.12-0.fdr.2
- missing $RPM_OPT_FLAGS in the %%build section.
- optional test module as build requirement perl(Tie::IxHash).

* Mon Apr 26 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:2.12-0.fdr.1
- Update to 2.12.
- Require perl(:MODULE_COMPAT_*).

* Sun Mar 14 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:2.11-0.fdr.1
- Update to 2.11.
- Reduce directory ownership bloat.

* Tue Nov 18 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.09-0.fdr.2
- Use INSTALLARCHLIB workaround in %%install.

* Wed Sep 10 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.09-0.fdr.1
- Update to 2.09.

* Wed Sep  3 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.08-0.fdr.1
- First build.
