Name:           perl-Log-Dispatch
Version:        2.29
Release:        4%{?dist}
Summary:        Dispatches messages to one or more outputs
Group:          Development/Libraries
License:        Artistic 2.0
URL:            http://search.cpan.org/dist/Log-Dispatch/
Source0:        http://www.cpan.org/authors/id/D/DR/DROLSKY/Log-Dispatch-%{version}.tar.gz

# Hacks to make spell checking tests work with hunspell
Patch0:         Log-Dispatch-2.29.diff
BuildArch:      noarch
BuildRequires:  perl(Apache2::Log)
BuildRequires:  perl(Mail::Send), perl(Mail::Sender)
BuildRequires:  perl(Mail::Sendmail), perl(MIME::Lite)
BuildRequires:  perl(Params::Validate) >= 0.15
BuildRequires:  perl(Sys::Syslog) >= 0.25

# testsuite
BuildRequires:  perl(Test::More) >= 0.88

# for improved tests
BuildRequires:  perl(Test::EOL)
BuildRequires:  perl(Test::NoTabs)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
BuildRequires:  perl(Test::Spelling)
BuildRequires:  hunspell-en
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Log::Dispatch is a suite of OO modules for logging messages to
multiple outputs, each of which can have a minimum and maximum log
level.  It is designed to be easily subclassed, both for creating a
new dispatcher object and particularly for creating new outputs.

%prep
%setup -q -n Log-Dispatch-%{version}
%patch0 -p1
sed -i -e "s,set_spell_cmd(.*),set_spell_cmd(\'hunspell -l\')," t/release-pod-spell.t

%build
%{__perl} Makefile.PL installdirs=vendor
make

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*
magic_rpm_clean.sh

%check
RELEASE_TESTING=1 LOG_DISPATCH_TEST_EMAIL="root@localhost.localdomain" \


%files
%defattr(-,root,root,-)
%doc Changes LICENSE README
%{perl_vendorlib}/Log/
%{_mandir}/man3/*.3pm*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 2.29-4
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.29-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 29 2012 Petr Pisar <ppisar@redhat.com> - 2.29-2
- Perl 5.16 rebuild

* Mon Feb 06 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.29-1
- Upstream update.
- Remove --with mailtests build option (unnecessary).
- Remove Log-Dispatch-2.11-enable-mail-tests.patch (rotten, obsolete).
- Rework spec.
- Enable release tests.
- Make hunspell checks working.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 2.27-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 03 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2.27-1
- update to 2.27

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.22-6
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 2.22-5
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.22-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.22-2
- BR: perl(Test::Kwalitee).

* Wed Nov 26 2008 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.22-1
- Upstream update.

* Fri Mar 14 2008 Ralf Corsépius <rc040203@freenet.de> - 2.21-1
- Upstream update.
- BR: perl(Apache2::Log) instead of mod_perl.
- Add BR: Test::Pod::Coverage, activate IS_MAINTAINER checks.

* Sat Feb  2 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.20-2
- rebuild for new perl

* Wed Dec 19 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 2.20-1
- bump to 2.20

* Sat Jun  9 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.18-1
- Update to 2.18.

* Wed Dec 20 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.16-1
- Update to 2.16.
- Removed perl(IO::String) from the BR list (no longer needed).

* Sat Dec 16 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.15-2
- New build requirement: perl(IO::String).

* Sat Dec 16 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.15-1
- Update to 2.15.

* Sat Nov 25 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.14-2
- Log-Dispatch-2.11-mod_perl2.patch no longer needed.

* Sat Nov 25 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.14-1
- Update to 2.14.

* Tue Sep 26 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.13-1
- Update to 2.13.

* Wed Aug  9 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.12-1
- Update to 2.12.

* Wed Feb 22 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.11-4
- Rebuild for FC5 (perl 5.8.8).

* Thu Sep 22 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.11-3
- Exclude mod_perl from the requirements list
  (overkill for most applications using Log::Dispatch).

* Mon Sep 12 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.11-2
- Better mod_perl handling.

* Fri Sep 09 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.11-1
- First build.
