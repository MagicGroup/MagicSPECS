Name:      perl-POE
Version:	1.367
Release:	2%{?dist}
Summary:   POE - portable multitasking and networking framework for Perl

Group:     Development/Libraries
License:   GPL+ or Artistic
URL:       http://search.cpan.org/dist/POE/
Source0:   http://search.cpan.org/CPAN/authors/id/R/RC/RCAPUTO/POE-%{version}.tar.gz
BuildArch: noarch
Requires:  perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Compress::Zlib) >= 1.33
BuildRequires:  perl(Curses) >= 1.08
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Errno) >= 1.09
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Spec) >= 0.87
BuildRequires:  perl(IO) >= 1.24
BuildRequires:  perl(IO::Handle) >= 1.27
BuildRequires:  perl(IO::Poll) >= 0.01
BuildRequires:  perl(IO::Pty) >= 1.02
BuildRequires:  perl(IO::Socket)
BuildRequires:  perl(IO::Tty) >= 1.08
BuildRequires:  perl(HTTP::Date)
BuildRequires:  perl(HTTP::Request)
BuildRequires:  perl(HTTP::Response)
BuildRequires:  perl(HTTP::Status)
# POE::Test::Loops unsurprisingly requires POE
%if 0%{!?perl_bootstrap:1}
BuildRequires:  perl(POE::Test::Loops) >= 1.351
%endif
BuildRequires:  perl(Socket) >= 1.7
BuildRequires:  perl(Socket6) >= 0.14
BuildRequires:  perl(Storable) >= 2.16
BuildRequires:  perl(Term::Cap) >= 1.09
BuildRequires:  perl(Term::ReadKey) >= 2.21
BuildRequires:  perl(Time::HiRes) >= 1.59
BuildRequires:  perl(URI) >= 1.30
# test
BuildRequires:  perl(Test::Harness) >= 2.26
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod) >= 1.00
BuildRequires:  perl(Test::Pod::Coverage) >= 1.08

Requires:       perl(Compress::Zlib)
Requires:       perl(Data::Dumper)
Requires:       perl(Errno) >= 1.09
Requires:       perl(Exporter)
Requires:       perl(File::Spec) >= 0.87
Requires:       perl(IO::Handle) >= 1.27
Requires:       perl(IO::Pty)
Requires:       perl(IO::Tty) >= 1.08
Requires:       perl(POSIX) >= 1.02
Requires:       perl(Socket) >= 1.7
Requires:       perl(Socket6) >= 0.14
Requires:       perl(Storable) >= 2.16
Requires:       perl(Time::HiRes) >= 1.59

%{?perl_default_filter}

%global __requires_exclude %{?__requires_exclude:__requires_exclude|}perl\\(Errno\\)
%global __requires_exclude %__requires_exclude|perl\\(File::Spec\\)
%global __requires_exclude %__requires_exclude|perl\\(IO::Handle\\)
%global __requires_exclude %__requires_exclude|perl\\(IO::Tty\\)
%global __requires_exclude %__requires_exclude|perl\\(POE::Test::Loops\\)
%global __requires_exclude %__requires_exclude|perl\\(POSIX\\)
%global __requires_exclude %__requires_exclude|perl\\(Socket\\)
%global __requires_exclude %__requires_exclude|perl\\(Socket6\\)
%global __requires_exclude %__requires_exclude|perl\\(Storable\\)
%global __requires_exclude %__requires_exclude|perl\\(Time::HiRes\\)

%description
POE is a framework for cooperative, event driven multitasking in Perl.
Other languages have similar frameworks. Python has Twisted. TCL has "the
event loop".

POE originally was developed as the core of a persistent object server and
runtime environment. It has evolved into a general purpose multitasking
and networking framework, encompassing and providing a consistent interface
to other event loops such as Event and the Tk and Gtk toolkits.

POE is written in layers, each building upon the previous. It's therefore
possible to use POE at varying levels of abstraction.


%prep
%setup -q -n POE-%{version}
# make rpmlint happy...
chmod -c -x examples/*
find t/ -type f -exec chmod -c -x {} +
find t/ -type f -name '*.t' -exec perl -pi -e 's|^#!perl|#!%{__perl}|' {} +

%build
perl Makefile.PL INSTALLDIRS=vendor --default
# yah.  don't do the network tests
%{?!_with_network_tests: rm run_network_tests }
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} +
find %{buildroot} -type d -depth -exec rmdir {} 2>/dev/null ';'
%{_fixperms} %{buildroot}/*

%check
# enable POD tests
#export POE_TEST_POD=1
# note that there are currently a number of tests that throw errors, but do
# not fail nor cause the build/suite to fail.  For now just please be aware
# that there will be some noisy output as the tests are run.
# Reported upstream at http://rt.cpan.org/Public/Bug/Display.html?id=19878


%files
%doc CHANGES HISTORY README examples/ TODO t/
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1.367-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.367-1
- 更新到 1.367

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.354-14
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.354-13
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.354-12
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.354-11
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.354-10
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.354-9
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.354-8
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.354-7
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.354-6
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.354-5
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.354-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 1.354-3
- Perl 5.16 re-rebuild of bootstrapped packages

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 1.354-2
- Perl 5.16 rebuild

* Wed May 16 2012 Petr Šabata <contyk@redhat.com> - 1.354-1
- 1.354 bump

* Fri May 11 2012 Petr Šabata <contyk@redhat.com> - 1.353-1
- 1.353 bump

* Thu Apr 05 2012 Petr Šabata <contyk@redhat.com> - 1.352-2
- Remove POE::Test::Loops circular buildtime and runtime dependency
  (thanks, Paul; #810234)

* Wed Mar 28 2012 Petr Šabata <contyk@redhat.com> - 1.352-1
- 1.352 bump
- Filter underspecified dependencies

* Wed Mar 14 2012 Petr Šabata <contyk@redhat.com> - 1.351-1
- 1.351 bump
- Remove command macros

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.350-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 21 2011 Petr Šabata <contyk@redhat.com> - 1.350-1
- 1.350 bump
- Remove Buildroot and defattr

* Mon Aug 01 2011 Petr Sabata <contyk@redhat.com> - 1.312-1
- 1.312 bump
- Deps updated

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 1.289-5
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.289-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.289-3
- 661697 rebuild for fixing problems with vendorach/lib

* Sun Sep 12 2010 Iain Arnell <iarnell@gmail.com> 1.289-2
- doesn't require POE::Test::Loops (RHBZ#632855)

* Tue Jun  8 2010 Petr Pisar <ppisar@redhat.com> - 1.289-1
- 1.289 bump
- Reenable t/90_regression/rt1648-tied-stderr.t test

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.269-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.269-2
- rebuild against perl 5.10.1

* Sun Sep 27 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.269-1
- update filtering...
- auto-update to 1.269 (by cpan-spec-update 0.01)
- added a new br on perl(Module::Build)
- altered br on perl(POE::Test::Loops) (1.021 => 1.022)
- altered req on perl(POE::Test::Loops) (1.021 => 1.022)

* Tue Aug 25 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.007-1
- auto-update to 1.007 (by cpan-spec-update 0.01)

* Tue Aug 11 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.007-1
- auto-update to 1.007 (by cpan-spec-update 0.01)
- altered br on perl(POE::Test::Loops) (1.004 => 1.021)
- added a new req on perl(Carp) (version 0)
- added a new req on perl(Errno) (version 1.09)
- added a new req on perl(Exporter) (version 0)
- added a new req on perl(File::Spec) (version 0.87)
- added a new req on perl(IO::Handle) (version 1.27)
- added a new req on perl(IO::Tty) (version 1.08)
- added a new req on perl(POE::Test::Loops) (version 1.021)
- added a new req on perl(POSIX) (version 1.02)
- added a new req on perl(Socket) (version 1.7)
- added a new req on perl(Storable) (version 2.16)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.006-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 02 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.006-1
- auto-update to 1.006 (by cpan-spec-update 0.01)

* Sun May 17 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.005-1
- auto-update to 1.005 (by cpan-spec-update 0.01)
- added a new br on perl(Storable) (version 2.16)
- added a new br on perl(Errno) (version 1.09)
- added a new br on perl(IO::Handle) (version 1.27)
- added a new br on perl(Socket) (version 1.7)
- added a new br on perl(IO::Tty) (version 1.08)
- added a new br on perl(POE::Test::Loops) (version 1.004)
- added a new br on perl(POSIX) (version 1.02)
- added a new br on perl(File::Spec) (version 0.87)
- added a new br on perl(Exporter) (version 0)
- added a new br on perl(Test::Harness) (version 2.26)
- added a new br on perl(Carp) (version 0)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.003-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Sep 07 2008 Chris Weyl <cweyl@alumni.drew.edu> 1.003-1
- update to 1.003
- filter provides, too

* Mon Jun 16 2008 Chris Weyl <cweyl@alumni.drew.edu> 1.0002-1
- update to 1.0002

* Tue Mar  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.9999-1
- update to 0.9999
- don't filter out POE::Kernel, POE::Loop::Tk (it actually is provided)

* Tue Mar  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.9989-2
- rebuild for new perl

* Sat May 19 2007 Chris Weyl <cweyl@alumni.drew.edu>
- spec cleanups, tweaks
- add t/ to doc
- move away from macroized versioning system
- no rebuild at this point

* Fri Mar 23 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.9989-1
- update to 0.9989

* Wed Mar 21 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.9917-1
- update to 0.9917.  0.3800-1, below, was never built/released to the wild.

* Mon Sep 25 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.3800-1
- update to 0.38.  0.37-1, below, was never built/released to the wild.

* Mon Sep 11 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.3700-1
- update to 0.37
- samples/ is now examples/
- add additional br's: perl(IO::Pty), perl(Test::Pod),
  perl(Test::Pod::Coverage)

* Thu Aug 31 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.3601-2
- bump for mass rebuild

* Sun Aug 13 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.3601-1
- update to cpan ver 0.3601

* Thu Aug 10 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.3600-1
- update to cpan ver 0.36

* Tue Jun 20 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.3502-1
- filter errant provides.  Also translate POE::Provides::foo modules to
  POE::Provide::foo
- Bump to latest version released

* Thu Jun 15 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.3501-2
- Nix test that was causing build to fail in plague

* Wed Jun 14 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.3501-1
- bump release, minor cleanups per review.

* Fri Jun 09 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.3501-0
- Initial spec file for F-E
