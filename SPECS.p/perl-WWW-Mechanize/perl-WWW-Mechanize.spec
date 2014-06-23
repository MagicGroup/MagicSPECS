#
# Rebuild switches:
#  --with localtests         enable local tests
%bcond_with localtests
#  --with livetests          enable live tests
%bcond_with livetests

Name:           perl-WWW-Mechanize
Version:        1.73
Release:        3%{?dist}
Summary:        Automates web page form & link interaction
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/WWW-Mechanize/
Source0:        http://search.cpan.org/CPAN/authors/id/E/ET/ETHER/WWW-Mechanize-%{version}.tar.gz
BuildArch:      noarch
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
# HTML::Status is not used anymore probably
#Requires:       perl(HTTP::Status)
# LWP is not run-time dependecy probably
#Requires:       perl(LWP) >= 5.829
BuildRequires:  perl(Carp)
BuildRequires:  perl(CGI)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(HTML::Form) >= 1.038
BuildRequires:  perl(HTML::HeadParser)
# HTML::Parser is not used anymore probably
#BuildRequires:  perl(HTML::Parser) >= 3.33
BuildRequires:  perl(HTTP::Request) >= 1.3
# HTTP::Response::Encoding is not used anymore probably
BuildRequires:  perl(HTTP::Response::Encoding) >= 0.05
BuildRequires:  perl(HTML::TreeBuilder)
# HTML::Status is not used anymore probably
#BuildRequires:  perl(HTTP::Status)
BuildRequires:  perl(HTML::TokeParser) >= 2.28
BuildRequires:  perl(IO::Socket::SSL)
BuildRequires:  perl(LWP) >= 5.829
BuildRequires:  perl(LWP::UserAgent) >= 5.829
BuildRequires:  perl(Pod::Usage)
BuildRequires:  perl(Test::More) >= 0.34
BuildRequires:  perl(URI::file)
BuildRequires:  perl(URI::URL)
# For %%check only:
# HTTP::Server::Simple is not used anymore probably
BuildRequires:  perl(HTTP::Server::Simple) >= 0.35
BuildRequires:  perl(HTTP::Server::Simple::CGI)
BuildRequires:  perl(Test::Exception)
BuildRequires:  perl(Test::Memory::Cycle)
BuildRequires:  perl(Test::NoWarnings)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
BuildRequires:  perl(Test::Taint)
BuildRequires:  perl(Test::Warn) >= 0.11
BuildRequires:  perl(URI) >= 1.36
%if %{with localtests}
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(HTTP::Daemon)
BuildRequires:  perl(HTTP::Response)
%endif

%description
"WWW::Mechanize", or Mech for short, helps you automate interaction
with a website.  It supports performing a sequence of page fetches
including following links and submitting forms. Each fetched page is
parsed and its links and forms are extracted. A link or a form can be
selected, form fields can be filled and the next page can be fetched.
Mech also stores a history of the URLs you've visited, which can be
queried and revisited.

%prep
%setup -q -n WWW-Mechanize-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor \
%if %{with localtests}
    --local \
%else
    --nolocal \
%endif
%if %{with livetests}
    --live
%else
    --nolive
%endif
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} +
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'

%{_fixperms} %{buildroot}/*
for F in Changes; do
    iconv -f iso8859-1 -t utf-8 "$F" > "${F}.utf8" && \
        touch -r "$F" "${F}.utf8" && mv "${F}.utf8" "$F"
done;

%check
make test

%files
%doc Changes etc/www-mechanize-logo.png
%{_bindir}/mech-dump
%{perl_vendorlib}/*
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3pm*

%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.73-3
- 为 Magic 3.0 重建

* Tue May 06 2014 Liu Di <liudidi@gmail.com> - 1.73-2
- 为 Magic 3.0 重建

* Sun Aug 25 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 1.73-1
- Update to 1.73

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.72-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Petr Pisar <ppisar@redhat.com> - 1.72-5
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.72-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.72-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 15 2012 Petr Pisar <ppisar@redhat.com> - 1.72-2
- Perl 5.16 rebuild

* Fri Feb 03 2012 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 1.72-1
- Update to 1.72

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.71-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 28 2011 Petr Šabata <contyk@redhat.com> - 1.71-1
- 1.71 bump
- Remove defattr
- Correct Source URL

* Sat Aug 27 2011 Petr Sabata <contyk@redhat.com> - 1.70-1
- 1.70 bump (live tests won't run by default now)

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 1.68-2
- Perl mass rebuild

* Tue Apr 26 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.68-1
- update to 1.68
- add BR HTML::TreeBuilder, remove duplicated requires

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.66-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 08 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.66-2
- Add BR: perl(CGI) (Fix FTBS: BZ 661086).

* Sun Nov 21 2010 Iain Arnell <iarnell@gmail.com> 1.66-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.62-2
- Mass rebuild with perl-5.12.0

* Wed Apr 21 2010 Petr Pisar <ppisar@redhat.com> 1.62-1
- version bump
- clean dependecies up

* Sun Aug 23 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.60-1
- auto-update to 1.60 (by cpan-spec-update 0.01)
- added a new br on perl(Carp) (version 0)
- added a new br on perl(File::Temp) (version 0)
- added a new br on perl(FindBin) (version 0)
- added a new br on perl(Getopt::Long) (version 0)
- added a new br on perl(HTML::Form) (version 1.038)
- added a new br on perl(HTML::HeadParser) (version 0)
- added a new br on perl(HTML::Parser) (version 3.33)
- altered br on perl(HTML::TokeParser) (0 => 2.28)
- added a new br on perl(HTTP::Daemon) (version 0)
- added a new br on perl(HTTP::Request) (version 1.3)
- altered br on perl(HTTP::Server::Simple) (0 => 0.35)
- added a new br on perl(HTTP::Server::Simple::CGI) (version 0)
- added a new br on perl(HTTP::Status) (version 0)
- added a new br on perl(LWP) (version 5.829)
- altered br on perl(LWP::UserAgent) (0 => 5.829)
- added a new br on perl(Pod::Usage) (version 0)
- altered br on perl(Test::More) (0 => 0.34)
- altered br on perl(Test::Warn) (0 => 0.11)
- added a new br on perl(URI::file) (version 0)
- added a new req on perl(Carp) (version 0)
- added a new req on perl(File::Temp) (version 0)
- added a new req on perl(FindBin) (version 0)
- added a new req on perl(Getopt::Long) (version 0)
- added a new req on perl(HTML::Form) (version 1.038)
- added a new req on perl(HTML::HeadParser) (version 0)
- added a new req on perl(HTML::Parser) (version 3.33)
- added a new req on perl(HTML::TokeParser) (version 2.28)
- added a new req on perl(HTTP::Daemon) (version 0)
- added a new req on perl(HTTP::Request) (version 1.3)
- added a new req on perl(HTTP::Server::Simple) (version 0.35)
- added a new req on perl(HTTP::Server::Simple::CGI) (version 0)
- added a new req on perl(HTTP::Status) (version 0)
- added a new req on perl(LWP) (version 5.829)
- added a new req on perl(LWP::UserAgent) (version 5.829)
- added a new req on perl(Pod::Usage) (version 0)
- added a new req on perl(URI) (version 1.36)
- added a new req on perl(URI::URL) (version 0)
- added a new req on perl(URI::file) (version 0)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.54-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.54-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb 21 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.54-1
- Upstream update.
- Add BR: perl(URI), perl(HTTP::Server::Simple),
  perl(HTTP::Response::Encoding).
- Use %%bcond_with and %%with to process build options.

* Wed May 28 2008 Chris Weyl <cweyl@alumni.drew.edu> 1.34-1
- update to 1.34

* Tue Feb 05 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.32-2
- rebuild for new perl

* Fri Dec 07 2007 Chris Weyl <cweyl@alumni.drew.edu> - 1.32-1
- update to 1.32

* Thu Jun  7 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.30-2
- New rebuild option: "--with livetests".

* Thu Jun  7 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.30-1
- Update to 1.30.
- The Makefile.PL --mech-dump option is now deprecated.

* Thu Jun  7 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.24-1
- Update to 1.24.

* Sun Mar 18 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.22-2
- New BR: perl(IO::Socket::SSL).

* Sun Mar 18 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.22-1
- Update to 1.22.

* Tue Sep  5 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.20-1
- Update to 1.20.
- Live tests have been dropped.

* Tue Feb 28 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.18-2
- Re-enable test suite but without local and live tests.
  One local test fails in mock (see #165650 comment 4).
- New rebuild option: "--with localtests".

* Thu Feb  2 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.18-1
- Update to 1.18.

* Thu Nov 10 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.16-1
- Update to 1.16.

* Wed Aug 31 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.14-2
- Added Test::LongString to the live tests build requirements.

* Wed Aug 31 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.14-1
- Update to 1.14.

* Fri Aug 26 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.12-4
- Added Test::Pod::Coverage to the BR list in order to improve test coverage.
- Disabled test suite as it fails in mock (see #165650 comment 4).

* Thu Aug 25 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.12-3
- Conditional rebuild switch to enable live tests (RFE in #165650).

* Fri Jul  1 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.12-2
- Dist tag.

* Sat Feb 26 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.12-0.fdr.1
- Update to 1.12.

* Mon Feb 14 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.10-0.fdr.1
- Update to 1.10.

* Sat Dec 25 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.08-0.fdr.1
- Update to 1.08.

* Sun Jul 04 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.02-0.fdr.1
- First build.
