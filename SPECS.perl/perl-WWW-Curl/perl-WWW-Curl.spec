Name:           perl-WWW-Curl
Version:	4.17
Release:	3%{?dist}
Summary:        Perl extension interface for libcurl
License:        MPLv1.1 or MIT
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/WWW-Curl/
Source0:        http://search.cpan.org/CPAN/authors/id/S/SZ/SZBALINT/WWW-Curl-%{version}.tar.gz

BuildRequires:  perl(inc::Module::Install)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(XSLoader)
BuildRequires:  libcurl-devel
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
WWW::Curl is a Perl extension interface for libcurl.

%prep
%setup -q -n WWW-Curl-%{version}

# Remove bundled modules
rm -rf inc/*

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -type f -name '*.bs' -size 0 -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
# These tests require network, use "--with network_tests" to execute them
%{?!_with_network_tests: rm t/01basic.t }
%{?!_with_network_tests: rm t/02callbacks.t }
%{?!_with_network_tests: rm t/04abort-test.t }
%{?!_with_network_tests: rm t/05progress.t }
%{?!_with_network_tests: rm t/08ssl.t }
%{?!_with_network_tests: rm t/09times.t }
%{?!_with_network_tests: rm t/14duphandle.t }
%{?!_with_network_tests: rm t/15duphandle-callback.t }
%{?!_with_network_tests: rm t/18twinhandles.t }
%{?!_with_network_tests: rm t/19multi.t }
%{?!_with_network_tests: rm t/21write-to-scalar.t }


%files
%doc Changes LICENSE README
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/WWW*
%{_mandir}/man3/*

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 4.17-3
- 为 Magic 3.0 重建

* Mon Sep 14 2015 Liu Di <liudidi@gmail.com> - 4.17-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 4.17-1
- 更新到 4.17

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 4.15-10
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 4.15-9
- 为 Magic 3.0 重建

* Thu Aug 16 2012 Jitka Plesnikova <jplesnik@redhat.com> - 4.15-8
- Specify all dependencies
- Modernize spec file

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.15-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Petr Pisar <ppisar@redhat.com> - 4.15-6
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jul 24 2011 Iain Arnell <iarnell@gmail.com> 4.15-4
- use perl_default_filter

* Wed Jun 29 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4.15-3
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Nov 30 2010 Nicoleau Fabien <nicoleau.fabien@gmail.com> - 4.15-1
- Update to 4.15
* Thu Oct 28 2010 Nicoleau Fabien <nicoleau.fabien@gmail.com> - 4.14-1
- Update to 4.14
- Add a filter provide to avoid private-shared-object-provides error
* Sun Sep  5 2010 Nicoleau Fabien <nicoleau.fabien@gmail.com> - 4.13-1
- Update to 4.13
* Wed Aug 25 2010 Nicoleau Fabien <nicoleau.fabien@gmail.com> - 4.12-1
- Update to 4.12
* Thu Jun  3 2010 Nicoleau Fabien <nicoleau.fabien@gmail.com> - 4.11-3
- Remove test 19 because it requires network
* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 4.11-2
- Mass rebuild with perl-5.12.0
* Fri Dec 18 2009 Nicoleau Fabien <nicoleau.fabien@gmail.com> - 4.11-1
- Update to 4.11
* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 4.09-3
- rebuild against perl 5.10.1
* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.09-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild
* Sat Jul 11 2009 Nicoleau Fabien <nicoleau.fabien@gmail.com> - 4.09-1
- Rebuild for 4.09
* Mon Jun  1 2009 Nicoleau Fabien <nicoleau.fabien@gmail.com> - 4.07-1
- Rebuild for 4.07
* Sat Apr 18 2009 Nicoleau Fabien <nicoleau.fabien@gmail.com> - 4.06-1
- Step to 4.06
* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.05-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild
* Wed Jan 14 2009 Nicoleau Fabien <nicoleau.fabien@gmail.com> - 4.05-4
- Licence update
* Wed Jan 14 2009 Nicoleau Fabien <nicoleau.fabien@gmail.com> - 4.05-3
- README.Win32 file removed
* Wed Jan 14 2009 Nicoleau Fabien <nicoleau.fabien@gmail.com> - 4.05-2
- Timestamp preserved
- changelog format fix
- README.Win32 file removed
* Thu Dec 11 2008 Nicoleau Fabien <nicoleau.fabien@gmail.com> - 4.05-1
- Initial build with cpan2spec
