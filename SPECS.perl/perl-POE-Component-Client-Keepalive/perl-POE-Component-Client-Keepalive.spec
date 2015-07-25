Name:           perl-POE-Component-Client-Keepalive
%define real_ver 0.271
# Keep four digits to stay above the unfortunate 0.0901,
# so that epoch need not be changed.
Version:        %{real_ver}0
Release:        13%{?dist}
Summary:        Manages and keeps alive client connections
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/POE-Component-Client-Keepalive
Source0:        http://search.cpan.org/CPAN/authors/id/R/RC/RCAPUTO/POE-Component-Client-Keepalive-%{real_ver}.tar.gz
BuildArch:      noarch
# core
BuildRequires:  perl(constant)
BuildRequires:  perl(Carp)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(IO::Socket::INET)
BuildRequires:  perl(Net::IP::Minimal) >= 0.02
BuildRequires:  perl(POE) >= 1.311
BuildRequires:  perl(POE::Component::Resolver) >= 0.917
BuildRequires:  perl(POE::Component::Server::TCP)
BuildRequires:  perl(POE::Component::SSLify)
BuildRequires:  perl(POE::Wheel::ReadWrite)
BuildRequires:  perl(POE::Wheel::SocketFactory)
BuildRequires:  perl(Socket)
BuildRequires:  perl(Test::More)
Requires:       perl(Net::IP::Minimal) >= 0.02
Requires:       perl(POE) >= 1.311
Requires:       perl(POE::Component::Resolver) >= 0.917
Requires:  perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
# Satisfy automaticly generated requires that want this module >= 0.0901
# (So the package has this provide in two versions, oh well.)
Provides:       perl(POE::Component::Client::Keepalive) = %{version}

%{?perl_default_filter}
%global __requires_exclude %{?__requires_exclude:__requires_exclude|}perl\\(Net::IP::Minimal\\)
%global __requires_exclude %__requires_exclude|perl\\(POE\\)
%global __requires_exclude %__requires_exclude|perl\\(POE::Component::Resolver\\)

%description
POE::Component::Client::Keepalive creates and manages connections for other
components. It maintains a cache of kept-alive connections for quick reuse. It
is written specifically for clients that can benefit from kept-alive
connections, such as HTTP clients. Using it for one-shot connections would
probably be silly.

%prep
%setup -q -n POE-Component-Client-Keepalive-%{real_ver}
chmod -c -x mylib/* t/*
for test in t/release-pod-syntax.t \
            t/release-pod-coverage.t \
            t/000-report-versions.t; do
    sed -i 's/#!perl/#!\/usr\/bin\/perl/' ${test}
done

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type d -depth -exec rmdir {} 2>/dev/null ';'
%{_fixperms} %{buildroot}/*

%check
# I'm leaving all tests active for now, even though 09_timeout.t runs a test
# which is _supposed_ to timeout against google.com.  This may or may not
# work inside the buildsys; if it doesn't the cure should be as easy as nixing
# this one test.


%files
%doc CHANGES README mylib/ t/
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.2710-13
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.2710-12
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.2710-11
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.2710-10
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.2710-9
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.2710-8
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.2710-7
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.2710-6
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.2710-5
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2710-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 15 2012 Petr Pisar <ppisar@redhat.com> - 0.2710-3
- Perl 5.16 rebuild

* Tue May 15 2012 Petr Šabata <contyk@redhat.com> - 0.2710-2
- Fix the Resolver runtime dependency

* Tue May 15 2012 Petr Šabata <contyk@redhat.com> - 0.2710-1
- 0.271 bump

* Tue Mar 27 2012 Petr Šabata <contyk@redhat.com> - 0.2690-1
- 0.269 bump
- Drop command macros

* Thu Jan 19 2012 Petr Šabata <contyk@redhat.com> - 0.2680-1
- 0.268 bump
- Spec cleanup

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2620-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.2620-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2620-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.2620-2
- 661697 rebuild for fixing problems with vendorach/lib

* Tue Jun  8 2010 Petr Pisar <ppisar@redhat.com> - 0.2620-1
- 0.262 bump
- Escape per-cent sign in spec changelog

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.2600-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.2600-4
- rebuild against perl 5.10.1

* Wed Sep 30 2009 Stepan Kasal <skasal@redhat.com> 0.2600-3
- keep the version aligned to 0.xxxx to maintain upgrade path

* Tue Sep 29 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.260-2
- fix provides version (for perl-POE-Component-Client-HTTP)

* Sun Sep 27 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.260-1
- update filtering
- auto-update to 0.260 (by cpan-spec-update 0.01)
- added a new br on perl(Net::IP) (version 1.25)
- altered br on perl(POE) (0.31 => 1.007)
- altered br on perl(POE::Component::Client::DNS) (1.01 => 1.04)
- added a new req on perl(Net::IP) (version 1.25)
- added a new req on perl(POE) (version 1.007)
- added a new req on perl(POE::Component::Client::DNS) (version 1.04)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2500-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 15 2009 Stepan Kasal <skasal@redhat.com> 0.2500-2
- add an explicite perl(POE::Component::Client::Keepalive) = 0.25, sigh

* Sat Jun 13 2009 Stepan Kasal <skasal@redhat.com> 0.2500-1
- work around the broken versioning

* Thu May 21 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.25-1
- auto-update to 0.25 (by cpan-spec-update 0.01)
- altered br on perl(POE::Component::Client::DNS) (0 => 1.01)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1000-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Mar  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.1000-2
- rebuild for new perl

* Sun May 13 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.1000-1
- update to 0.1000
- add t/ to %doc
- perl splittage BR tweaks

* Tue Oct 03 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.0901-1
- update to 0.0901
- minor spec tweaks

* Thu Aug 31 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.0801-3
- bump for mass rebuild

* Tue Jul 25 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.0801-2
- import, bump & build for devel

* Thu Jul 20 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.0801-1
- bits snipped

* Fri Jul 14 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.0801-0
- Initial spec file for F-E
