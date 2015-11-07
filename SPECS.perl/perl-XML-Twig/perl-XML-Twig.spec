Name:           perl-XML-Twig
Version:	3.49
Release:	2%{?dist}
Summary:        Perl module for processing huge XML documents in tree mode
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/XML-Twig/
Source0:        http://www.cpan.org/authors/id/M/MI/MIROD/XML-Twig-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  expat >= 2.0.1
BuildRequires:  perl(base)
BuildRequires:  perl(bytes)
BuildRequires:  perl(lib)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Encode)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(HTML::TreeBuilder) >= 4.00
BuildRequires:  perl(HTML::Entities::Numbered)
BuildRequires:  perl(HTML::Tidy)
BuildRequires:  perl(HTML::Entities)
BuildRequires:  perl(IO::Scalar)
BuildRequires:  perl(IO::String)
BuildRequires:  perl(LWP)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(strict)
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
BuildRequires:  perl(Text::Iconv)
BuildRequires:  perl(Tie::IxHash)
#BuildRequires:  perl(Tree::XPathEngine) # not available in Fedora yet
BuildRequires:  perl(Test)
%if 0%{!?perl_bootstrap:1}
%if 0%{?fedora}  || 0%{?rhel} < 7
BuildRequires:  perl(Test::Kwalitee)
%endif
%endif
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
BuildRequires:  perl(Text::Wrap)
BuildRequires:  perl(Text::Iconv)
BuildRequires:  perl(Unicode::Map8)
BuildRequires:  perl(Unicode::String)
BuildRequires:  perl(utf8)
BuildRequires:  perl(warnings)
BuildRequires:  perl(XML::Filter::BufferText)
BuildRequires:  perl(XML::Handler::YAWriter)
BuildRequires:  perl(XML::Parser) >= 2.34
BuildRequires:  perl(XML::SAX::Writer)
BuildRequires:  perl(XML::Simple)
BuildRequires:  perl(XML::XPathEngine)
BuildRequires:  perl(XML::XPath)
Requires:       perl(XML::Parser) >= 2.34
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%{?perl_default_filter}

%{?filter_setup:
%filter_from_provides /perl(XML::XPathEngine::NodeSet)/d
%filter_from_requires /perl(XML::XPath)/d
%filter_from_requires /perl(xml_split::state)/d
%?perl_default_filter
}
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}perl\\(XML::XPathEngine::NodeSet\\)
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}perl\\(XML::XPath\\)
%global __requires_exclude %__requires_exclude|perl\\(xml_split::state\\)

%description
This module provides a way to process XML documents. It is build on
top of XML::Parser.  XML::Twig offers a tree interface to the
document, while allowing you to output the parts of it that have been
completely processed.  It allows minimal resource (CPU and memory)
usage by building the tree only for the parts of the documents that
need actual processing, through the use of the twig_roots and
twig_print_outside_roots options.

%prep
%setup -q -n XML-Twig-%{version}

%build
perl Makefile.PL -y INSTALLDIRS=perl
make %{?_smp_mflags}
cp Changes Changes.orig
iconv -f iso88591 -t utf8 < Changes.orig > Changes

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;
%{_fixperms} %{buildroot}/*

%check


%files
%doc Changes README 
%{perl_privlib}/*
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man3/*

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 3.49-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 3.49-1
- 更新到 3.49

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 3.41-8
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 3.41-7
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 3.41-6
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 3.41-5
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 3.41-4
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 3.41-3
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 3.41-2
- 为 Magic 3.0 重建

* Tue Aug 14 2012 Petr Šabata <contyk@redhat.com> - 3.41-1
- 3.41 bump

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.40-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 3.40-3
- Perl 5.16 re-rebuild of bootstrapped packages

* Mon Jun 18 2012 Petr Pisar <ppisar@redhat.com> - 3.40-2
- Perl 5.16 rebuild

* Fri May 11 2012 Petr Šabata <contyk@redhat.com> - 3.40-1
- 3.40 bump
- Dropping defattr and perl command macros

* Thu Apr 19 2012 Marcela Mašláňová <mmaslano@redhat.com> - 3.39-4
- make module Kwalitee conditional

* Tue Apr 10 2012 Marcela Mašláňová <mmaslano@redhat.com> - 3.39-3
- remove cyclic dependency added by mistake  810563 
  XML::Twig::Elt, XML::Twig::XPath

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.39-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Sep 22 2011 Petr Sabata <contyk@redhat.com> - 3.39-1
- 3.39 bump

* Sun Jul 24 2011 Iain Arnell <iarnell@gmail.com> 3.38-4
- update filtering for rpm 4.9

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 3.38-3
- Perl mass rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 3.38-2
- Perl mass rebuild

* Wed Mar 23 2011 Marcela Mašláňová <mmaslano@redhat.com> 3.38-1
- update to 3.38
- BR organize according to cpanspec list

* Mon Feb 14 2011 Marcela Mašláňová <mmaslano@redhat.com> 3.37-3
- 677179 filter internal xml_split::state from requires and call filter properly
- add new BR, which is now in Fedora

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.37-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Oct 18 2010 Marcela Mašláňová <mmaslano@redhat.com> 3.37-1
- update, fix BR, R

* Tue Sep 21 2010 Marcela Mašláňová <mmaslano@redhat.com> 3.35-1
- update

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 3.34-2
- Mass rebuild with perl-5.12.0

* Tue Jan 19 2010 Chris Weyl <cweyl@alumni.drew.edu> 3.34-1
- update prov/dep filtering to current guidelines
- auto-update to 3.34 (by cpan-spec-update 0.01)
- added a new br on perl(ExtUtils::MakeMaker) (version 0)
- altered br on perl(XML::Parser) (0 => 2.23)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 3.33-2
- rebuild against perl 5.10.1

* Mon Oct 19 2009 Marcela Mašláňová <mmaslano@redhat.com> - 3.33-1
- new development release which should fix various bug reports e.g. 529220

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.32-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.32-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Mar  2 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 3.32-1
- update to 3.32

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 3.29-6
- Rebuild for perl 5.10 (again)

* Mon Jan 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 3.29-5
- rebuild for new perl

* Sun Jul 08 2007 Robin Norwood <rnorwood@redhat.com> - 3.29-4
- Resolves: rhbz#247247
- Remove bogus Provides: perl(XML::XPathEngine::NodeSet), and move
  Requires filter into spec file.

* Thu Jun 28 2007 Robin Norwood <rnorwood@redhat.com> - 3.29-3
- Add several buildrequires for tests and optional features

* Sat Feb 17 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 3.29-2
- Minor cleanups.

* Tue Feb 13 2007 Robin Norwood <rnorwood@redhat.com> - 3.29-1
- New version: 3.29

* Mon Jul 17 2006 Jason Vas Dias <jvdias@redhat.com> - 3.26-1
- Upgrade to 3.26

* Mon Jun 05 2006 Jason Vas Dias <jvdias@redhat.com> - 3.25-1
- Upgrade to 3.25

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 3.22-1.1
- Update to 3.23
- rebuild for new perl-5.8.8

* Mon Dec 19 2005 Jason Vas Dias<jvdias@redhat.com> - 3.22-1
- Update to 3.22

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc

* Sun Apr 17 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 3.17-1
- Update to 3.17.
- Specfile cleanup. (#155168)

* Wed Sep 22 2004 Chip Turner <cturner@redhat.com> 3.13-6
- rebuild

* Mon May  3 2004 Chip Turner <cturner@redhat.com> 3.13-5
- bugzilla 122079, add dep filter to remove bad dependency

* Fri Apr 23 2004 Chip Turner <cturner@redhat.com> 3.13-4
- remove Packager tag

* Fri Apr 23 2004 Chip Turner <cturner@redhat.com> 3.13-2
- bump

* Fri Feb 13 2004 Chip Turner <cturner@redhat.com> 3.13-1
- update to 3.13

* Tue Dec 10 2002 Chip Turner <cturner@redhat.com>
- update to latest version from CPAN

* Mon Aug 26 2002 Chip Turner <cturner@redhat.com>
- rebuild for build failure

* Tue Aug  6 2002 Chip Turner <cturner@redhat.com>
- automated release bump and build

* Wed May 29 2002 cturner@redhat.com
- Specfile autogenerated
