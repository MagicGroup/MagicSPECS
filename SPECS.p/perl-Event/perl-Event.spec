Name:		perl-Event
Version:	1.21
Release:	5%{?dist}
Summary:	Event loop processing
Group:		Development/Libraries
License:	GPL+ or Artistic
URL:		http://search.cpan.org/dist/Event/
Source0:	http://search.cpan.org/CPAN/authors/id/J/JP/JPRIT/Event-%{version}.tar.gz
Patch0:		Event-1.19-UTF8.patch
BuildRequires:	perl(Carp)
BuildRequires:	perl(Config)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(Test) >= 1
BuildRequires:	perl(Time::HiRes)
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	perl(Time::HiRes)

%{?perl_default_filter}

%description
The Event module provide a central facility to watch for various types of
events and invoke a callback when these events occur. The idea is to delay the
handling of events so that they may be dispatched in priority order when it is
safe for callbacks to execute.

%prep
%setup -q -n Event-%{version}

# Fix up permissions and shellbangs
find ./ -type f -exec chmod -c -x {} \;
perl -pi -e 's|#!./perl|#!/usr/bin/perl|' demo/*.t t/*.t util/bench.pl
%{_fixperms} demo/ util/

# Fix character encoding
%patch0 -p1

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir --ignore-fail-on-non-empty {} ';'
%{_fixperms} %{buildroot}

%check
make test

%files
%doc ANNOUNCE ChangeLog README README.EV TODO
%doc Tutorial.pdf Tutorial.pdf-errata.txt demo/ t/ util/
%doc %{perl_vendorarch}/Event.pod
%{perl_vendorarch}/auto/Event/
%{perl_vendorarch}/Event.pm
%{perl_vendorarch}/Event/
%{_mandir}/man3/Event.3pm*
%{_mandir}/man3/Event::MakeMaker.3pm*
%{_mandir}/man3/Event::generic.3pm*

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.21-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.21-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.21-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec 17 2012 Paul Howarth <paul@city-fan.org> - 1.21-1
- Update to 1.21:
  - Silence some clang warnings
    (http://www.xray.mpe.mpg.de/mailing-lists/perl5-porters/2012-12/msg00424.html)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 1.20-2
- Perl 5.16 rebuild

* Sun Jan 15 2012 Paul Howarth <paul@city-fan.org> 1.20-1
- update to 1.20 (test suite fixes)
- BR: perl(Carp), perl(Config), perl(Exporter)
- since upstream doesn't ship license files, neither should we
- make %%files list more explicit
- use a patch to fix character encoding rather than scripted iconv
- use DESTDIR rather than PERL_INSTALL_ROOT
- no need for additional filtering on top of %%{?perl_default_filter}
- don't package INSTALL file

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 1.15-3
- rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> 1.15-2
- perl mass rebuild

* Wed May 11 2011 Iain Arnell <iarnell@gmail.com> 1.15-1
- update to latest upstream version
- clean up spec for modern rpmbuild
- filter perl(attrs) from requires

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 1.12-6
- rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> 1.12-5
- rebuild to fix problems with vendorarch/lib (#661697)

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> 1.12-4
- mass rebuild with perl-5.12.0

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> 1.12-3
- mass rebuild with perl-5.12.0

* Mon Dec 07 2009 Stepan Kasal <skasal@redhat.com> 1.12-2
- rebuild against perl 5.10.1

* Tue Sep 01 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.12-1
- add perl_default_filter
- auto-update to 1.12 (by cpan-spec-update 0.01)
- added a new req on perl(Test) (version 1)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 1.11-3
- rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 1.11-2
- rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed May 21 2008 Chris Weyl <cweyl@alumni.drew.edu> 1.11-1
- update to 1.11

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.09-5
- rebuild for perl 5.10 (again)

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> 1.09-4
- autorebuild for GCC 4.3

* Tue Feb 05 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.09-3
- rebuild for new perl

* Tue Aug 21 2007 Chris Weyl <cweyl@alumni.drew.edu> 1.09-2
- bump

* Fri Jun 01 2007 Chris Weyl <cweyl@alumni.drew.edu> 1.09-1
- update to 1.09
- add t/ to doc

* Sat Nov 04 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.08-1
- update to 1.08

* Sun Oct 15 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.07-1
- update to 1.07

* Thu Aug 31 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.06-2
- bump for mass rebuild

* Wed Jun 14 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.06-1
- add explicit provides: perl(Event) = version...  wasn't being picked up
  automagically for some reason
- tweaked summary line
- bumped release

* Thu Jun 08 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.06-0
- initial spec file for F-E
