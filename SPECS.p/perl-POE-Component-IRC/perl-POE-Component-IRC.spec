# Note:  The tests for this perl dist. are disabled by default, as they
# require network access and would thus fail in the buildsys' mock
# environments.  To build locally while enabling tests, either:
#
#   rpmbuild ... --define '_with_network_tests 1' ...
#   rpmbuild ... --with network_tests ...
#   define _with_network_tests 1 in your ~/.rpmmacros
#
# Note that right now, the only way to run tests locally from a cvs sandbox
# "make noarch" type scenario is the third one.

Name:           perl-POE-Component-IRC
Summary:        A POE component for building IRC clients
Version:        6.81
Release:        3%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/B/BI/BINGOS/POE-Component-IRC-%{version}.tar.gz 
URL:            http://search.cpan.org/dist/POE-Component-IRC
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
BuildArch:      noarch
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Digest::MD5)
BuildRequires:  perl(Encode::Guess)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.31
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(IO::Handle)
BuildRequires:	perl(IRC::Utils) >= 0.11
BuildRequires:  perl(lib)
BuildRequires:  perl(List::MoreUtils)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(Object::Pluggable)
BuildRequires:  perl(POE) >= 1.287
BuildRequires:  perl(POE::Component::Client::DNS)
BuildRequires:  perl(POE::Component::Syndicator)
BuildRequires:  perl(POE::Driver::SysRW)
BuildRequires:  perl(POE::Filter)
BuildRequires:  perl(POE::Filter::IRCD) >= 2.42
BuildRequires:  perl(POE::Filter::Line)
BuildRequires:  perl(POE::Filter::Stackable)
BuildRequires:  perl(POE::Filter::Stream)
BuildRequires:  perl(POE::Filter::Zlib::Stream)
BuildRequires:  perl(POE::Session)
BuildRequires:  perl(POE::Wheel::FollowTail)
BuildRequires:  perl(POE::Wheel::ReadWrite)
BuildRequires:  perl(POE::Wheel::SocketFactory)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Socket)
BuildRequires:  perl(Socket6)
BuildRequires:  perl(Test::Differences)
BuildRequires:  perl(Test::More) >= 0.47
Requires:       perl(Object::Pluggable)
Requires:       perl(POE) >= 1.311
Requires:       perl(POE::Driver::SysRW)
Requires:       perl(POE::Filter::IRCD) >= 2.42
Requires:       perl(POE::Filter::Line)
Requires:       perl(POE::Filter::Stream)
Requires:       perl(POE::Session)
Requires:       perl(POE::Wheel::ReadWrite)
Requires:       perl(POE::Wheel::SocketFactory)
# Added during f19 development cycle
Obsoletes:      %{name}-tests <= 6.81

%{?perl_default_filter}

%description
POE::Component::IRC is a POE component (who'd have guessed?) which acts as an
easily controllable IRC client for your other POE components and sessions. You
create an IRC component and tell it what events your session cares about and
where to connect to, and it sends back interesting IRC events when they
happen. You make the client do things by sending it events. That's all there
is to it. Cool, no?

%prep
%setup -q -n POE-Component-IRC-%{version}
# Funky permissions...
%{_fixperms} *
chmod -c -x Changes README examples/*

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} %{buildroot}/*
# remove errant execute bit from the .pm's
find %{buildroot} -type f -name '*.pm' -exec chmod -x {} 2>/dev/null ';'

%check
# tests require network access, disabled by default
%{?_with_network_tests: make test}

%files
%doc Changes README* docs/ examples/
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Mon Nov 26 2012 Petr Šabata <contyk@redhat.com> - 6.81-3
- Correct the Obsoletes tests version to 6.81, thanks to Ralf Corsepius

* Mon Nov 26 2012 Petr Šabata <contyk@redhat.com> - 6.81-2
- Obsolete tests < v2.81 to be more future-proof

* Mon Nov 26 2012 Petr Šabata <contyk@redhat.com> - 6.81-1
- 6.81 bump
- Drop command macros
- Drop the tests subpackage

* Thu Sep 20 2012 Petr Pisar <ppisar@redhat.com> - 6.80-1
- 6.80 bump

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.78-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 6.78-3
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.78-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 08 2011 Petr Šabata <contyk@redhat.com> - 6.78-1
- 6.78 bump (just tests)

* Mon Dec 05 2011 Petr Šabata <contyk@redhat.com> - 6.77-1
- 6.77 bump

* Tue Nov 29 2011 Petr Šabata <contyk@redhat.com> - 6.76-1
- 6.76 bump

* Mon Nov 14 2011 Petr Šabata <contyk@redhat.com> - 6.75-1
- 6.75 bump

* Mon Oct 10 2011 Petr Sabata <contyk@redhat.com> - 6.74-1
- 6.74 bump

* Mon Sep 19 2011 Petr Sabata <contyk@redhat.com> - 6.71-1
- 6.71 bump

* Tue Aug  4 2011 Petr Sabata <contyk@redhat.com> - 6.68-1
- 6.70 bump
- Remove defattr and some forgotten buildroot stuff

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 6.52-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.52-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Nov 09 2010 Marcela Mašláňová <mmaslano@redhat.com> 6.52-2
- update by Fedora::App::MaintainerTools 0.006
- PERL_INSTALL_ROOT => DESTDIR
- altered br on perl(ExtUtils::MakeMaker) (6.42 => 6.31)
- added a new br on perl(Object::Pluggable) (version 0)
- altered br on perl(POE) (0.3202 => 1.287)
- altered br on perl(POE::Filter::IRCD) (1.7 => 2.42)
- added a new br on perl(POE::Session) (version 0)
- dropped old BR on perl(Encode)
- dropped old BR on perl(Encode::Guess)
- dropped old BR on perl(POE::Component::Client::DNS)
- dropped old BR on perl(POE::Component::Pluggable)
- dropped old BR on perl(POE::Filter::Zlib::Stream)
- dropped old BR on perl(Socket6)
- dropped old BR on perl(Test::Pod)
- dropped old BR on perl(Test::Pod::Coverage)
- added a new req on perl(Object::Pluggable) (version 0)
- altered req on perl(POE) (0.3202 => 1.287)
- altered req on perl(POE::Filter::IRCD) (1.7 => 2.42)
- added a new req on perl(POE::Session) (version 0)
- dropped old requires on perl(Encode)
- dropped old requires on perl(Encode::Guess)
- dropped old requires on perl(POE::Component::Pluggable)

* Thu May 20 2010 Iain Arnell <iarnell@gmail.com> 6.14-4
- apply patch for rhbz#591215

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 6.14-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 6.14-2
- rebuild against perl 5.10.1

* Sun Sep 27 2009 Chris Weyl <cweyl@alumni.drew.edu> 6.14-1
- auto-update to 6.14 (by cpan-spec-update 0.01)
- altered br on perl(POE::Component::Pluggable) (1.12 => 1.24)
- altered req on perl(POE::Component::Pluggable) (1.12 => 1.24)

* Wed Aug 26 2009 Chris Weyl <cweyl@alumni.drew.edu> 6.10-1
- auto-update to 6.10 (by cpan-spec-update 0.01)
- altered br on perl(ExtUtils::MakeMaker) (0 => 6.42)
- added a new req on perl(Encode) (version 0)
- added a new req on perl(Encode::Guess) (version 0)
- added a new req on perl(POE) (version 0.3202)
- added a new req on perl(POE::Component::Pluggable) (version 1.12)
- added a new req on perl(POE::Driver::SysRW) (version 0)
- added a new req on perl(POE::Filter::IRCD) (version 1.7)
- added a new req on perl(POE::Filter::Line) (version 0)
- added a new req on perl(POE::Filter::Stackable) (version 0)
- added a new req on perl(POE::Filter::Stream) (version 0)
- added a new req on perl(POE::Wheel::ReadWrite) (version 0)
- added a new req on perl(POE::Wheel::SocketFactory) (version 0)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.06-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu May 21 2009 Chris Weyl <cweyl@alumni.drew.edu> 6.06-1
- auto-update to 6.06 (by cpan-spec-update 0.01)
- added a new br on perl(Encode) (version 0)
- added a new br on perl(POE::Component::Pluggable) (version 1.12)
- added a new br on perl(POE::Filter::Stream) (version 0)
- added a new br on perl(POE::Filter::Stackable) (version 0)
- added a new br on perl(POE::Wheel::ReadWrite) (version 0)
- added a new br on perl(POE::Wheel::SocketFactory) (version 0)
- altered br on perl(POE::Filter::IRCD) (0 => 1.7)
- altered br on perl(POE) (0 => 0.3202)
- added a new br on perl(POE::Driver::SysRW) (version 0)
- altered br on perl(Test::More) (0 => 0.47)
- added a new br on perl(POE::Filter::Line) (version 0)
- added a new br on perl(Encode::Guess) (version 0)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.88-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Oct 26 2008 Chris Weyl <cweyl@alumni.drew.edu> 5.88-1
- update to 5.88

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 5.29-2
Rebuild for new perl

* Sat May 05 2007 Chris Weyl <cweyl@alumni.drew.edu> 5.29-1
- update to 5.29

* Wed May 02 2007 Chris Weyl <cweyl@alumni.drew.edu> 5.28-1
- update to 5.28

* Mon Apr 30 2007 Chris Weyl <cweyl@alumni.drew.edu> 5.26-1
- update to 5.26
- include t/ in %%doc

* Sat Apr 21 2007 Chris Weyl <cweyl@alumni.drew.edu> 5.24-1
- update to 5.24
- additional splittage BR's
- Additional BR's to handle new tests, ipv6 functionality, etc

* Thu Jan 04 2007 Chris Weyl <cweyl@alumni.drew.edu> 5.18-1
- update to 5.18

* Fri Dec 15 2006 Chris Weyl <cweyl@alumni.drew.edu> 5.17-1
- update to 5.17

* Tue Dec 05 2006 Chris Weyl <cweyl@alumni.drew.edu> 5.14-1
- update to 5.14

* Sun Oct 22 2006 Chris Weyl <cweyl@alumni.drew.edu> 5.07-1
- update to 5.07

* Tue Oct 10 2006 Chris Weyl <cweyl@alumni.drew.edu> 5.05-1
- update to 5.05
- scratched head in confusion at versions in the last few changelogs

* Fri Sep 29 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.54-1
- update to 0.54

* Sun Sep 17 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.53-1
- update to 0.53
- add br: perl(POE::Filter::Zlib::Stream)

* Sun Sep 10 2006 Chris Weyl <cweyl@alumni.drew.edu> 5.02-1
- update to 5.02

* Fri Sep 01 2006 Chris Weyl <cweyl@alumni.drew.edu> 5.00-1
- update to 5.00
- add br on Test::Pod, Test::Pod::Coverage, which are now used
- minor spec tweaks, mostly cosmetic

* Thu Aug 31 2006 Chris Weyl <cweyl@alumni.drew.edu> 4.99-1
- rebuild per mass rebuild
- update to 4.99

* Tue Aug 22 2006 Chris Weyl <cweyl@alumni.drew.edu> 4.98-1
- update to 4.98

* Tue Jul 25 2006 Chris Weyl <cweyl@alumni.drew.edu> 4.97-1
- update to 4.97

* Sat Jul 22 2006 Chris Weyl <cweyl@alumni.drew.edu> 4.96-3
- Fix typo, add more verbage

* Fri Jul 21 2006 Chris Weyl <cweyl@alumni.drew.edu> 4.96-2
- bump for f-e build
- rework conditionals around testing to... well, work :)

* Thu Jul 20 2006 Chris Weyl <cweyl@alumni.drew.edu> 4.96-1
- snip lines

* Mon Jul 17 2006 Chris Weyl <cweyl@alumni.drew.edu> 4.96-0
- updated to version 4.96
- Dropped the licensing conversation as the documentation (README, pods) were
  updated to include it
- Added optional framework around test suite, rather than just disabling

* Thu Jul 13 2006 Chris Weyl <cweyl@alumni.drew.edu> 4.95-0
- Initial spec file for F-E
