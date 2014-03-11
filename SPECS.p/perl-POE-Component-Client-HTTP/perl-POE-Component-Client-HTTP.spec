# Note:  The tests for this perl dist. are disabled by default, as they
# require network access and would thus fail in the buildsys' mock
# environments.  To build locally while enabling tests, either:
#
#   rpmbuild ... --define '_with_network_tests 1' ...
#   rpmbuild ... --with network_tests ...
#   define _with_network_tests 1 in your ~/.rpmmacros

Name:           perl-POE-Component-Client-HTTP
Version:        0.947
Release:        4%{?dist}
Summary:        A non-blocking/parallel web requests engine for POE
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/POE-Component-Client-HTTP
Source0:        http://search.cpan.org/CPAN/authors/id/R/RC/RCAPUTO/POE-Component-Client-HTTP-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(base)
BuildRequires:  perl(constant)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(HTTP::Headers) >= 5.810
BuildRequires:  perl(HTTP::Request) >= 5.811
BuildRequires:  perl(HTTP::Request::Common) >= 5.811
BuildRequires:  perl(HTTP::Response) >= 5.813
BuildRequires:  perl(HTTP::Status) >= 5.811
BuildRequires:  perl(IO::File)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IO::Socket::INET)
BuildRequires:  perl(Net::HTTP::Methods) >= 5.812
BuildRequires:  perl(POE) >= 1.312
# Original perl(POE::Component::Client::Keepalive) >= 0.271 rounded to
# 4 digit precision
BuildRequires:  perl(POE::Component::Client::Keepalive) >= 0.2710
BuildRequires:  perl(POE::Driver::SysRW)
BuildRequires:  perl(POE::Filter)
BuildRequires:  perl(POE::Filter::Line)
BuildRequires:  perl(POE::Filter::Stackable)
BuildRequires:  perl(POE::Filter::Stream)
BuildRequires:  perl(POE::Session)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Socket) >= 2.001
BuildRequires:  perl(URI) >= 1.37
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
BuildRequires:  perl(Test::POE::Server::TCP) >= 1.14
BuildRequires:  perl(Test::More) > 0.96
BuildRequires:  perl(Time::HiRes)
Requires:       perl(HTTP::Headers) >= 5.810
Requires:       perl(HTTP::Request) >= 5.811
Requires:       perl(HTTP::Request::Common) >= 5.811
Requires:       perl(HTTP::Response) >= 5.813
Requires:       perl(HTTP::Status) >= 5.811
Requires:       perl(Net::HTTP::Methods) >= 5.812
Requires:       perl(POE) >= 1.312
# Original perl(POE::Component::Client::Keepalive) >= 0.271 rounded to
# 4 digit precision
Requires:       perl(POE::Component::Client::Keepalive) >= 0.2710
Requires:       perl(Socket) >= 2.001
Requires:       perl(URI) >= 1.37
Requires:  perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%{?perl_default_filter}

%description
POE::Component::Client::HTTP is an HTTP user-agent for POE. It lets other
sessions run while HTTP transactions are being processed, and it lets several
HTTP transactions be processed in parallel.

%prep
%setup -q -n POE-Component-Client-HTTP-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type d -depth -exec rmdir {} 2>/dev/null ';'
%{_fixperms} %{buildroot}/*
cd examples
sed -i '/#!perl/d;s/\r//' pcchget.perl

%check
# we don't have network access during the builds; fortunately these look to be
# the only tests requiring it.  Failing that, the entire suite can be
# disabled.
%{?!_with_network_tests:rm t/01* t/02*}


%files
%doc CHANGES* README examples/
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.947-4
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.947-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 15 2012 Petr Pisar <ppisar@redhat.com> - 0.947-2
- Perl 5.16 rebuild

* Tue Jun 05 2012 Petr Šabata <contyk@redhat.com> - 0.947-1
- 0.947 bump

* Tue May 15 2012 Petr Šabata <contyk@redhat.com> - 0.946-1
- 0.946 bump

* Thu Apr 19 2012 Petr Šabata <contyk@redhat.com> - 0.945-2
- Removing erroneous build dependencies on self (#810738)

* Tue Mar 27 2012 Petr Šabata <contyk@redhat.com> - 0.945-1
- 0.945 bump

* Thu Jan 19 2012 Petr Šabata <contyk@redhat.com> - 0.944-1
- 0.944 bump
- Spec cleanup

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.895-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.895-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.895-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.895-2
- 661697 rebuild for fixing problems with vendorach/lib

* Mon Jun  7 2010 Petr Pisar <ppisar@redhat.com> - 0.895-1
- 0.895 bump (bug #600022)
- Delete removal of missing tests

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.890-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.890-3
- rebuild against perl 5.10.1

* Wed Sep 30 2009 Stepan Kasal <skasal@redhat.com> 0.890-2
- fix the perl(POE::Component::Client::Keepalive) require
  to match our numbering

* Tue Aug 25 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.890-1
- auto-update to 0.890 (by cpan-spec-update 0.01)
- altered br on perl(POE) (0.3202 => 1.007)
- altered br on perl(POE::Component::Client::Keepalive) (0.25 => 0.26)
- added a new req on perl(HTTP::Request) (version 1.3)
- added a new req on perl(HTTP::Response) (version 1.37)
- added a new req on perl(Net::HTTP::Methods) (version 0.02)
- added a new req on perl(POE) (version 1.007)
- altered req on perl(POE::Component::Client::Keepalive) (0.0901 => 0.26)
- added a new req on perl(URI) (version 1.24)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.88-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu May 21 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.88-1
- auto-update to 0.88 (by cpan-spec-update 0.01)
- altered br on perl(POE::Component::Client::Keepalive) (0.0901 => 0.25)
- altered br on perl(POE) (0.31 => 0.3202)
- altered br on perl(HTTP::Request) (1.30 => 1.3)
- added a new br on perl(Test::POE::Server::TCP) (version 0)
- added a new br on perl(Net::HTTP::Methods) (version 0.02)

* Sun Mar 22 2009 Robert Scheck <robert@fedoraproject.org> 0.85-3
- Disabled the network requiring test t/59_andy_one_keepalive.t

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.85-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Oct 26 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.85-1
- update to 0.85

* Tue Mar  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.82-2
- rebuild for new perl

* Sat Apr 21 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.82-1
- update to 0.82
- additional BR's for perl splittage
- nix dos2unix BR

* Thu Jan 04 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.80-2
- nix another text when not performing network-enabled tests

* Thu Jan 04 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.80-1
- update to 0.80

* Sun Oct 22 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.79-1
- update to 0.79-1
- add pod test modules to BR

* Tue Oct 03 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.78-1
- update to 0.78
- minor spec tweaks
- bump version BR on PoCo::Client::Keepalive to 0.0901 (tests fail otherwise)
- ...and add explicit requires on the above (the way POE loads its PoCo's irks
  me sometimes...)

* Thu Aug 31 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.77-3
- bump for mass rebuild

* Wed Aug 16 2006 Chris Weyl <cweyl@alumni.drew.edu>
- nixed t/10* due to mock build issues with reduced buildroot.  see BZ#202602.
  This fix does not warrant a rebuild.

* Thu Jul 27 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.77-2
- bump for build

* Thu Jul 27 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.77-1
- switched to the same _with_network_tests test as perl-POE-Component-IRC
- updated to 0.77

* Thu Jul 20 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.76-1
- bits snipped

* Thu Jul 13 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.76-0
- Initial spec file for F-E
