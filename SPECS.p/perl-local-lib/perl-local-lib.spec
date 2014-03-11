Name:       perl-local-lib
Version:    1.008004
Release:    5%{?dist}
# lib/local/lib.pm -> GPL+ or Artistic
License:    GPL+ or Artistic
Group:      Development/Libraries
Summary:    Create and use a local lib/ for perl modules
Source:     http://search.cpan.org/CPAN/authors/id/A/AP/APEIRON/local-lib-%{version}.tar.gz
Url:        http://search.cpan.org/dist/local-lib
Requires:   perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:  noarch

Source10:   perl-homedir.sh
Source11:   perl-homedir.csh

BuildRequires: perl(ExtUtils::MakeMaker) >= 6.42
BuildRequires: perl(CPAN) >= 1.82
BuildRequires: perl(Module::Build) >= 0.3600
# testing...
BuildRequires: perl(Capture::Tiny)
BuildRequires: perl(Test::More)

### auto-added reqs!
Requires:       perl(CPAN) >= 1.82
Requires:       perl(ExtUtils::Install) >= 1.43
Requires:       perl(ExtUtils::MakeMaker) >= 6.31
Requires:       perl(Module::Build) >= 0.3600

### auto-added brs!
BuildRequires:  perl(ExtUtils::Install) >= 1.43

%{?perl_default_filter}

%description
This module provides a quick, convenient way of bootstrapping a user-
local Perl module library located within the user's home directory. It
also constructs and prints out for the user the list of environment
variables using the syntax appropriate for the user's current shell (as
specified by the 'SHELL' environment variable), suitable for directly
adding to one's shell configuration file.

More generally, local::lib allows for the bootstrapping and usage of a
directory containing Perl modules outside of Perl's '@INC'. This makes
it easier to ship an application with an app-specific copy of a Perl module,
or collection of modules. Useful in cases like when an upstream maintainer
hasn't applied a patch to a module of theirs that you need for your
application.

%package -n perl-homedir
License:    GPL+ or Artistic
Group:      Development/Libraries
Summary:    Per-user Perl local::lib setup
Requires:   %{name} = %{version}-%{release}
Requires:   /usr/bin/cpan

%description -n perl-homedir
perl-homedir configures the system to automatically create a ~/perl5
directory in each user's $HOME on user login.  This allows each user to
install and CPAN packages via the CPAN to their $HOME, with no additional
configuration or privileges, and without installing them system-wide.

If you want your users to be able to install and use their own Perl modules,
install this package.

%prep
%setup -q -n local-lib-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'

%{_fixperms} %{buildroot}/*

mkdir -p %{buildroot}%{_sysconfdir}/profile.d
cp %{SOURCE10} %{buildroot}%{_sysconfdir}/profile.d/
cp %{SOURCE11} %{buildroot}%{_sysconfdir}/profile.d/

%check


%files
%defattr(-,root,root,-)
%doc Changes
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%files -n perl-homedir
%defattr(-,root,root,-)
%{_sysconfdir}/profile.d/*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.008004-5
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.008004-4
- 为 Magic 3.0 重建

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.008004-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.008004-2
- Perl mass rebuild

* Wed Mar 16 2011 Iain Arnell <iarnell@gmail.com> 1.008004-1
- update to latest upstream version

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.008001-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 23 2011 Iain Arnell <iarnell@gmail.com> 1.008001-2
- update requires perl(Module::Build) >= 0.3600

* Sun Jan 23 2011 Iain Arnell <iarnell@gmail.com> 1.008001-1
- update to latest upstream version
- drop R/BR perl(ExtUtils::CBuilder) and perl(ExtUtils::ParseXS)

* Fri Dec 17 2010 Iain Arnell <iarnell@gmail.com> 1.007000-1
- update to latest upstream version
- fix typo in description

* Sun Nov 21 2010 Iain Arnell <iarnell@gmail.com> 1.006007-1
- update to latest upstream version
- clean up spec for modern rpmbuild
- BR perl(Capture::Tiny)

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.004009-3
- Mass rebuild with perl-5.12.0

* Tue Jan 05 2010 Chris Weyl <cweyl@alumni.drew.edu> 1.004009-2
- add perl-homedir subpackage

* Tue Jan 05 2010 Chris Weyl <cweyl@alumni.drew.edu> 1.004009-1
- add perl_default_filter
- auto-update to 1.004009 (by cpan-spec-update 0.01)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.004007-2
- rebuild against perl 5.10.1

* Sat Sep 19 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.004007-1
- auto-update to 1.004007 (by cpan-spec-update 0.01)

* Sat Aug 29 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.004006-1
- auto-update to 1.004006 (by cpan-spec-update 0.01)

* Tue Aug 25 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.004005-1
- auto-update to 1.004005 (by cpan-spec-update 0.01)

* Tue Aug 11 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.004004-1
- auto-update to 1.004004 (by cpan-spec-update 0.01)
- added a new br on perl(ExtUtils::Install) (version 1.43)
- added a new req on perl(CPAN) (version 1.80)
- added a new req on perl(ExtUtils::CBuilder) (version 0)
- added a new req on perl(ExtUtils::Install) (version 1.43)
- added a new req on perl(ExtUtils::MakeMaker) (version 6.31)
- added a new req on perl(ExtUtils::ParseXS) (version 0)
- added a new req on perl(Module::Build) (version 0.28)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.004001-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 03 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.004001-1
- auto-update to 1.004001 (by cpan-spec-update 0.01)

* Tue May 19 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.004000-1
- auto-update to 1.004000 (by cpan-spec-update 0.01)
- altered br on perl(ExtUtils::MakeMaker) (6.31 => 6.42)

* Sun Mar 08 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.003002-1
- submission

* Sun Mar 08 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.003002-0
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.8)
