#global subver 1

# A noarch-turned-arch package should not have debuginfo
%global debug_package %{nil}

Name:           perl-AnyEvent
Version:        7.02
Release:        2%{?dist}
Summary:        Framework for multiple event loops
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/AnyEvent/
Source0:        http://search.cpan.org/CPAN/authors/id/M/ML/MLEHMANN/AnyEvent-%{version}%{?subver}.tar.gz

# Build requirements
BuildRequires:  perl(ExtUtils::MakeMaker)

# Module requirements
BuildRequires:  perl >= 3:5.8.1
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Socket)
BuildRequires:  perl(Task::Weaken)
BuildRequires:  perl(Time::HiRes)

# Test suite requirements
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Net::SSLeay)
BuildRequires:  perl(Test::More)

# Event loop testing
#
# Many of these modules require or build-require AnyEvent themselves,
# so don't do event loop testing when bootstrapping
#
# Cocoa and FLTK are not in Fedora/EPEL
# Version of IO::Async::Loop in Fedora is too old
# TODO: BuildRequires: perl(IO::Async::Loop) >= 0.33
# Test suite does not currently test the Qt event loop
%if 0%{!?perl_bootstrap:1}
BuildRequires:  perl(AnyEvent::AIO)
BuildRequires:  perl(EV)
BuildRequires:  perl(Event)
BuildRequires:  perl(Event::Lib)
BuildRequires:  perl(Glib) >= 1.210
BuildRequires:  perl(IO::AIO) >= 4.13
BuildRequires:  perl(POE) >= 1.312
BuildRequires:  perl(Tk)
%endif

# Runtime requires
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
# Optional but recommended
Requires:       perl(Task::Weaken)

# Optional dependencies we don't want to require
%global optional_deps                  AnyEvent::AIO
%global optional_deps %{optional_deps}|Cocoa::EventLoop
%global optional_deps %{optional_deps}|EV
%global optional_deps %{optional_deps}|Event
%global optional_deps %{optional_deps}|Event::Lib
%global optional_deps %{optional_deps}|EventLoop
%global optional_deps %{optional_deps}|FLTK
%global optional_deps %{optional_deps}|Glib
%global optional_deps %{optional_deps}|IO::AIO
%global optional_deps %{optional_deps}|IO::Async::Loop
%global optional_deps %{optional_deps}|Irssi
%global optional_deps %{optional_deps}|POE
%global optional_deps %{optional_deps}|Qt
%global optional_deps %{optional_deps}|Qt::isa
%global optional_deps %{optional_deps}|Qt::slots
%global optional_deps %{optional_deps}|Tk

# Don't include optional dependencies
%global __requires_exclude ^perl[(](%{optional_deps})[)]

# Filter unversioned and bogus provides
# AnyEvent::Impl::Cocoa and AnyEvent::Impl::FLTK are filtered as the required
# underlying modules are not currently available in Fedora
%global __provides_exclude ^perl[(](AnyEvent(::Impl::(Cocoa|FLTK))?|DB)[)]$


%description
AnyEvent provides an identical interface to multiple event loops. This allows
module authors to utilize an event loop without forcing module users to use the
same event loop (as multiple event loops cannot coexist peacefully at any one
time).


%prep
%setup -q -n AnyEvent-%{version}%{?subver}


%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'


%check
# PERL_ANYEVENT_NET_TESTS shouldn't be set to avoid network tests
# on our builder.
export PERL_ANYEVENT_LOOP_TESTS=1



%files
%doc Changes COPYING README
%{perl_vendorarch}/AE.pm
%{perl_vendorarch}/AnyEvent.pm
%{perl_vendorarch}/AnyEvent/
%{_mandir}/man3/AE.3pm*
%{_mandir}/man3/AnyEvent.3pm*
%{_mandir}/man3/AnyEvent::DNS.3pm*
%{_mandir}/man3/AnyEvent::Debug.3pm*
%{_mandir}/man3/AnyEvent::FAQ.3pm*
%{_mandir}/man3/AnyEvent::Handle.3pm*
%{_mandir}/man3/AnyEvent::Impl::Cocoa.3pm*
%{_mandir}/man3/AnyEvent::Impl::EV.3pm*
%{_mandir}/man3/AnyEvent::Impl::Event.3pm*
%{_mandir}/man3/AnyEvent::Impl::EventLib.3pm*
%{_mandir}/man3/AnyEvent::Impl::FLTK.3pm*
%{_mandir}/man3/AnyEvent::Impl::Glib.3pm*
%{_mandir}/man3/AnyEvent::Impl::IOAsync.3pm*
%{_mandir}/man3/AnyEvent::Impl::Irssi.3pm*
%{_mandir}/man3/AnyEvent::Impl::POE.3pm*
%{_mandir}/man3/AnyEvent::Impl::Perl.3pm*
%{_mandir}/man3/AnyEvent::Impl::Qt.3pm*
%{_mandir}/man3/AnyEvent::Impl::Tk.3pm*
%{_mandir}/man3/AnyEvent::Intro.3pm*
%{_mandir}/man3/AnyEvent::IO.3pm*
%{_mandir}/man3/AnyEvent::IO::IOAIO.3pm*
%{_mandir}/man3/AnyEvent::IO::Perl.3pm*
%{_mandir}/man3/AnyEvent::Log.3pm*
%{_mandir}/man3/AnyEvent::Loop.3pm*
%{_mandir}/man3/AnyEvent::Socket.3pm*
%{_mandir}/man3/AnyEvent::Strict.3pm*
%{_mandir}/man3/AnyEvent::TLS.3pm*
%{_mandir}/man3/AnyEvent::Util.3pm*


%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 7.02-2
- 为 Magic 3.0 重建

* Tue Aug 21 2012 Paul Howarth <paul@city-fan.org> - 7.02-1
- Update to 7.02:
  - AnyEvent::Util::run_cmd could block indefinitely
  - Verified that AnyEvent::Socket follows RFC5952
  - Try to parse "ADDR#PORT" in addition to "ADDR PORT"
- Make %%files list more explicit

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.01-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 7.01-3
- Perl 5.16 re-rebuild of bootstrapped packages

* Thu Jun 14 2012 Petr Pisar <ppisar@redhat.com> - 7.01-2
- Perl 5.16 rebuild

* Sun May 13 2012 Paul Howarth <paul@city-fan.org> - 7.01-1
- Update to 7.01:
  - Fail with EPROTO in AnyEvent::Handle when TLS is requested but not
    available, instead of throwing an exception
  - Use File::Spec to get the tmpdir in t/*, to avoid needless failures on
    (most, not mine :) windows boxes
  - New handle read types: tls_detect and tls_autostart
- BR: perl(File::Spec)

* Thu Apr 26 2012 Paul Howarth <paul@city-fan.org> - 7.0-1
- Update to 7.0
- Package generates no debuginfo, so avoid creation of debuginfo sub-package
- Add explicit build requirements for the module's needs
- Add build requirements for as much event loop testing as is possible in
  Fedora, breaking potential build dependency cycles by use of the
  %%{perl_bootstrap} macro
- Clean up spec for modern rpmbuild:
  - Drop %%defattr, redundant since rpm 4.4
  - Use DESTDIR rather than PERL_INSTALL_ROOT
  - Drop buildroot definition and cleaning
  - Drop requires/provides filters for rpm versions prior to 4.9
- Simplify requires/provides filtering
- Explicitly require perl(Task::Weaken) as per upstream recommendation

* Mon Apr 23 2012 Nicolas Chauvet <kwizart@gmail.com> - 6.14-2
- Filter requires perl(FLTK) perl(Cocoa) - rhbz#815496
- Filter perl(IO::Async::Loop) to reintroduce later.
- Remove filter on perl(AnyEvent::Impl::Qt) since there is perl(Qt)

* Sun Apr 22 2012 Nicolas Chauvet <kwizart@gmail.com> - 6.14-1
- Update to 6.14
- Make the package arch specific

* Mon Jan 16 2012 Nicolas Chauvet <kwizart@gmail.com> - 6.13-1
- Update to 6.13

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.27-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Jul 23 2011 Nicolas Chauvet <kwizart@gmail.com> - 5.34-1
- Update to 5.34

* Fri Jul 22 2011 Petr Pisar <ppisar@redhat.com> - 5.27-6
- RPM 4.9 dependency filtering added

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 5.27-5
- Perl mass rebuild

* Thu Feb 10 2011 Nicolas Chauvet <kwizart@gmail.com> - 5.27-4
- Rewritten to new filtering rules
 http://fedoraproject.org/wiki/Packaging:AutoProvidesAndRequiresFiltering#Perl

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.27-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 14 2010 Marcela Maslanova <mmaslano@redhat.com> - 5.27-2
- 661697 rebuild for fixing problems with vendorach/lib

* Sun Aug 22 2010 Nicolas Chauvet <kwizart@gmail.com> - 5.27-1
- Update to 5.271 (rpm version : 5.27)

* Thu Apr 29 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 5.26-1
- Update to 5.261 (rpm version : 5.26)

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 5.24-2
- Mass rebuild with perl-5.12.0

* Tue Jan 19 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 5.24-1
- Update to 5.24  (rpm version : 5.24)

* Mon Dec 7 2009 Nicolas Chauvet <kwizart@fedoraproject.org> - 5.22-1
- Update to 5.22  (rpm version : 5.22)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 5.11-3
- rebuild against perl 5.10.1

* Mon Aug 31 2009 kwizart < kwizart at gmail.com > - 5.11-2
- Update to 5.112   (rpm version : 5.11 )

* Mon Jul 27 2009 kwizart < kwizart at gmail.com > - 4.870-1
- Update to 4.87   (rpm version : 4.870 )
- Add more filter requires to workaround rhbz#512553

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.820-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 15 2009 kwizart < kwizart at gmail.com > - 4.820-1
- Update to 4.82   (rpm version : 4.820 )

* Fri May 29 2009 kwizart < kwizart at gmail.com > - 4.410-1
- Update to 4.41   (rpm version : 4.41 )

* Wed Apr 22 2009 kwizart < kwizart at gmail.com > - 4.352-1
- Update to 4.352   (rpm version : same )

* Fri Apr  3 2009 kwizart < kwizart at gmail.com > - 4.350-1
- Update to 4.35   (rpm version : 4.350 )

* Thu Mar  5 2009 kwizart < kwizart at gmail.com > - 4.340-1
- Update to 4.34   (rpm version : 4.340 )

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.331-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 12 2009 kwizart < kwizart at gmail.com > - 4.331-1
- Update to 4.331   (rpm version : same )

* Fri Oct 17 2008 kwizart < kwizart at gmail.com > - 4.300-1
- Update to 4.3   (rpm version : 4.300 )

* Tue Oct 14 2008 kwizart < kwizart at gmail.com > - 4.3-1
- Update to 4.3 

* Mon Aug  4 2008 kwizart < kwizart at gmail.com > - 4.231-1
- Update to 4.231 (rpm version : match )

* Fri Jul 18 2008 kwizart < kwizart at gmail.com > - 4.220-1
- Update to 4.22 (rpm version : 4.220 )

* Fri Jul 18 2008 kwizart < kwizart at gmail.com > - 4.21-1
- Update to 4.21

* Fri Jul  4 2008 kwizart < kwizart at gmail.com > - 4.161-1
- Update to 4.161

* Mon Jun 23 2008 kwizart < kwizart at gmail.com > - 4.152-1
- Update to 4.152

* Mon Jun  9 2008 kwizart < kwizart at gmail.com > - 4.151-1
- Update to 4.151

* Thu Jun  5 2008 kwizart < kwizart at gmail.com > - 4.13-1
- Update to 4.13

* Tue Jun  3 2008 kwizart < kwizart at gmail.com > - 4.12-1
- Update to 4.12

* Thu May 29 2008 kwizart < kwizart at gmail.com > - 4.1-1
- Update to 4.1

* Tue May 27 2008 kwizart < kwizart at gmail.com > - 3.5-1
- Update to 3.5

* Wed Apr 30 2008 kwizart < kwizart at gmail.com > - 3.3-1
- Initial package for Fedora

