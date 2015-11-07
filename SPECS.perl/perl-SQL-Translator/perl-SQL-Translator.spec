Name:           perl-SQL-Translator
Summary:        Manipulate structured data definitions (SQL and more)
Version:	0.11021_01
Release:	2%{?dist}
License:        GPLv2
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/I/IL/ILMARI/SQL-Translator-%{version}.tar.gz
URL:            http://search.cpan.org/dist/SQL-Translator/
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:      noarch

BuildRequires:  perl(Carp::Clan)
BuildRequires:  perl(Class::Base)
BuildRequires:  perl(Class::Data::Inheritable) >= 0.02
BuildRequires:  perl(Class::MakeMethods)
BuildRequires:  perl(CPAN)
BuildRequires:  perl(DBI)
BuildRequires:  perl(Digest::SHA)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.42
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::ShareDir) >= 1.0
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(GD)
BuildRequires:  perl(Graph::Directed)
BuildRequires:  perl(GraphViz)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(IO::Scalar) >= 2.110
BuildRequires:  perl(Log::Log4perl)
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Moo) >= 0.009007
BuildRequires:  perl(Parse::RecDescent) >= 1.967009
BuildRequires:  perl(Pod::Usage)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Spreadsheet::ParseExcel)
BuildRequires:  perl(Template)
BuildRequires:  perl(Test::Differences)
BuildRequires:  perl(Test::Exception) >= 0.31
BuildRequires:  perl(Test::More) >= 0.6
BuildRequires:  perl(Text::RecordParser)
BuildRequires:  perl(XML::LibXML)
BuildRequires:  perl(XML::Parser)
BuildRequires:  perl(XML::Writer) >= 0.500
BuildRequires:  perl(XML::XPath)
BuildRequires:  perl(YAML) >= 0.66
BuildRequires:  perl(Package::Variant)

Requires:       perl(Class::Data::Inheritable) >= 0.02
Requires:       perl(File::ShareDir) >= 1.0
Requires:       perl(IO::Scalar) >= 2.110
Requires:       perl(Parse::RecDescent) >= 1.967009
Requires:       perl(XML::Writer) >= 0.500

# obsolete/provide old tests subpackage
# can be removed during F19 development cycle
Obsoletes:      %{name}-tests < 0.11010-3
Provides:       %{name}-tests = %{version}-%{release}

# hidden from PAUSE
Provides:       perl(SQL::Translator::Schema::Graph::Port)
Provides:       perl(SQL::Translator::Schema::Graph::Node)
Provides:       perl(SQL::Translator::Schema::Graph::HyperEdge)
Provides:       perl(SQL::Translator::Schema::Graph::Edge)
Provides:       perl(SQL::Translator::Schema::Graph::CompoundEdge)

%?perl_default_filter
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}perl\\(:\\)

%description
SQL::Translator is a group of Perl modules that converts vendor-specific
SQL table definitions into other formats, such as other vendor-specific
SQL, ER diagrams, documentation (POD and HTML), XML, and Class::DBI
classes.  The main focus of SQL::Translator is SQL, but parsers exist
for other structured data formats, including Excel spreadsheets and
arbitrarily delimited text files.  Through the separation of the code into
parsers and producers with an object model in between, it’s possible to
combine any parser with any producer, to plug in custom parsers or
producers, or to manipulate the parsed data via the built-in object model.
Presently only the definition parts of SQL are handled (CREATE, ALTER),
not the manipulation of data (INSERT, UPDATE, DELETE).

%prep
%setup -q -n SQL-Translator-%{version}

find . -type f -exec chmod -c -x {} +
perl -pi -e 's|^#!/usr/local/bin/perl|#!%{__perl}|' t/*.t

%build
%{?!with_local_perl:unset PERL_MM_OPT MODULEBUILDRC PERL5LIB}
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} +
find %{buildroot} -type f -name '*.bs' -size 0 -exec rm -f {} +
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} %{buildroot}/*

%check
make test

%files
%doc Changes README t/
%{_bindir}/*
%{perl_vendorlib}/*
%{_mandir}/man[13]/*

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.11021_01-2
- 更新到 0.11021_01

* Mon Sep 14 2015 Liu Di <liudidi@gmail.com> - 0.11021-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.11021-1
- 更新到 0.11021

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.11012-10
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.11012-9
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.11012-8
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.11012-7
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.11012-6
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.11012-5
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.11012-4
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.11012-3
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.11012-2
- 为 Magic 3.0 重建

* Sun Jul 29 2012 Iain Arnell <iarnell@gmail.com> 0.11012-1
- update to latest upstream version

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11011-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 29 2012 Petr Pisar <ppisar@redhat.com> - 0.11011-3
- Perl 5.16 rebuild

* Tue May 15 2012 Iain Arnell <iarnell@gmail.com> 0.11011-2
- add provides for SQL::Translator::Schema::Graph::*

* Sun May 13 2012 Iain Arnell <iarnell@gmail.com> 0.11011-1
- update to latest upstream version

* Sun Jan 22 2012 Iain Arnell <iarnell@gmail.com> 0.11010-3
- drop tests subpackage; move tests to main package documentation
- drop old-style filtering

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11010-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 12 2011 Iain Arnell <iarnell@gmail.com> 0.11010-1
- update to latest upstream version
- clean up spec for modern rpmbuild
- remove unnecessary explicit requires

* Thu Jul 21 2011 Iain Arnell <iarnell@gmail.com> 0.11006-6
- update filtering for rpm 4.9

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 0.11006-5
- Perl mass rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.11006-4
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11006-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.11006-2
- 661697 rebuild for fixing problems with vendorach/lib

* Thu Sep 02 2010 Iain Arnell <iarnell@gmail.com> 0.11006-1
- update to latest upstream version

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.11005-3
- Mass rebuild with perl-5.12.0

* Tue Mar 16 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.11005-2
- fix deps on perl(Parse::RecDescent)... again :\

* Sat Mar 13 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.11005-1
- update by Fedora::App::MaintainerTools 0.006
- updating to latest GA CPAN version (0.11005)
- altered br on perl(Parse::RecDescent) (1.963 => 1.962002)
- added manual BR on perl(Template) (or override to 0)
- added manual BR on perl(Text::RecordParser) (or override to 0)
- added manual BR on perl(XML::XPath) (or override to 0)
- altered req on perl(Parse::RecDescent) (1.963 => 1.962002)

* Wed Feb 10 2010 Paul Howarth <paul@city-fan.org> 0.11003-3
- fix broken deps for perl(Parse::RecDescent)
- altered br on perl(Parse::RecDescent) (1.962002 => 1.963)
- altered req on perl(Parse::RecDescent) (1.962002 => 1.963)

* Fri Feb 05 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.11003-2
- PERL_INSTALL_ROOT => DESTDIR
- add perl_default_subpackage_tests

* Sat Jan 16 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.11003-1
- add br on XML::LibXML
- auto-update to 0.11003 (by cpan-spec-update 0.01)

* Sun Sep 27 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.11002-1
- auto-update to 0.11002 (by cpan-spec-update 0.01)
- altered br on perl(Parse::RecDescent) (1.096 => 1.962002)
- altered req on perl(Parse::RecDescent) (1.096 => 1.962002)

* Mon Aug 24 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.11001-1
- auto-update to 0.11001 (by cpan-spec-update 0.01)
- added a new br on perl(Carp::Clan) (version 0)
- altered br on perl(Digest::SHA1) (2.00 => 2)
- added a new br on perl(ExtUtils::MakeMaker) (version 6.42)
- added a new br on perl(File::ShareDir) (version 1)
- altered br on perl(IO::Scalar) (0 => 2.11)
- altered br on perl(Parse::RecDescent) (1.94 => 1.096)
- altered br on perl(YAML) (0.39 => 0.66)
- added a new br on CPAN (inc::Module::AutoInstall found)
- added a new req on perl(Carp::Clan) (version 0)
- added a new req on perl(Class::Base) (version 0)
- altered req on perl(Class::Data::Inheritable) (0 => 0.02)
- added a new req on perl(Class::MakeMethods) (version 0)
- added a new req on perl(DBI) (version 0)
- added a new req on perl(Digest::SHA1) (version 2)
- added a new req on perl(File::ShareDir) (version 1)
- added a new req on perl(File::Spec) (version 0)
- added a new req on perl(IO::Dir) (version 0)
- added a new req on perl(IO::Scalar) (version 2.11)
- added a new req on perl(Parse::RecDescent) (version 1.096)
- added a new req on perl(Pod::Usage) (version 0)
- added a new req on perl(XML::Writer) (version 0.5)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09004-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed May 27 2009 Iain Arnell <iarnell@gmail.com> 0.09004-2
- add missing requires Class::Accessor::Fast and Class::Data::Inheritable

* Sun Mar 08 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.09004-1
- update to 0.09004

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09002-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 03 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.09002-1
- update to 0.09002

* Sun Sep 07 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.9001-1
- update to 0.9001
- add new BR: perl(Digest::SHA1) >= 2.00

* Wed Mar 19 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.09000-1
- update to 0.09000
- expose more core BR's
- additional br's now required

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.08001-3
- Rebuild for new perl

* Wed Oct 24 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.08001-2
- bump

* Sun Oct 14 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.08001-1
- updated to 0.08001
- update license tag
- nix errant perl(Producer::BaseTest) provides
- make description useful :)
- we now skip Template::Toolkit tests correctly, so stop disabling them

* Mon May 14 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.08-1
- Specfile autogenerated by cpanspec 1.71.
