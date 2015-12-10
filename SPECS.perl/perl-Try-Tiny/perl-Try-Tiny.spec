Name:		perl-Try-Tiny
Summary:	Minimal try/catch with proper localization of $@
Version:	0.22
Release:	3%{?dist}
License:	MIT
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/Try-Tiny
Source0:	http://search.cpan.org/CPAN/authors/id/D/DO/DOY/Try-Tiny-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
BuildRequires:	perl(Carp)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(Test::More)
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	perl(Exporter)

# obsolete/provide old tests subpackage
# can be removed during F19 development cycle
Obsoletes:	%{name}-tests < 0.11-3
Provides:	%{name}-tests = %{version}-%{release}

%description
This module provides bare bones try/catch statements that are designed to
minimize common mistakes with eval blocks, and NOTHING else.

This is unlike TryCatch, which provides a nice syntax and avoids adding
another call stack layer, and supports calling return from the try block to
return from the parent subroutine. These extra features come at a cost of a
few dependencies, namely Devel::Declare and Scope::Upper that are occasionally
problematic, and the additional catch filtering uses Moose type constraints,
which may not be desirable either.

%prep
%setup -q -n Try-Tiny-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} %{buildroot}

%check


%clean
rm -rf %{buildroot}

%files
%doc Changes t/
%{perl_vendorlib}/Try/
%{_mandir}/man3/Try::Tiny.3pm*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.22-3
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.22-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.22-1
- 更新到 0.22

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.11-9
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.11-8
- 为 Magic 3.0 重建

* Tue Aug 28 2012 Jitka Plesnikova <jplesnik@redhat.com> - 0.11-7
- Add BR/R perl(Exporter).

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 0.11-5
- Perl 5.16 rebuild

* Mon Mar 26 2012 Paul Howarth <paul@city-fan.org> - 0.11-4
- BR: perl(Carp)
- Don't need to remove empty directories from buildroot
- Don't use macros for commands
- Drop redundant %%{?perl_default_filter}
- Enhance %%description
- Reinstate EPEL-5 compatibility:
  - Define buildroot
  - Clean buildroot in %%install and %%clean
- Use tabs

* Sun Jan 22 2012 Iain Arnell <iarnell@gmail.com> - 0.11-3
- Drop tests subpackage; move tests to main package documentation

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct 02 2011 Iain Arnell <iarnell@gmail.com> - 0.11-1
- Update to latest upstream version

* Wed Jun 15 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.09-2
- Perl mass rebuild

* Fri Mar 18 2011 Iain Arnell <iarnell@gmail.com> - 0.09-1
- Update to latest upstream version
- Clean up spec for modern rpmbuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.07-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov  1 2010 Paul Howarth <paul@city-fan.org> - 0.07-1
- Update to 0.07
  - Allow multiple finally blocks
  - Pass the error, if any, to finally blocks when called
  - Documentation fixes and clarifications
- This release by RJBS -> update source URL

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.04-2
- Mass rebuild with perl-5.12.0

* Tue Mar 02 2010 Chris Weyl <cweyl@alumni.drew.edu> - 0.04-1
- Update by Fedora::App::MaintainerTools 0.004
- PERL_INSTALL_ROOT => DESTDIR
- Updating to latest GA CPAN version (0.04)

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.02-2
- Rebuild against perl 5.10.1

* Tue Sep 15 2009 Chris Weyl <cweyl@alumni.drew.edu> - 0.02-1
- Submission

* Tue Sep 15 2009 Chris Weyl <cweyl@alumni.drew.edu> - 0.02-0
- Initial RPM packaging
- Generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.8)
