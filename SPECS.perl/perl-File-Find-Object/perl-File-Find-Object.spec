%global pkgname File-Find-Object

Name:           perl-File-Find-Object
Version:        0.2.13
Release:        4%{?dist}
Summary:        Object oriented File::Find replacement
License:        GPLv2+ or Artistic 2.0
URL:            http://search.cpan.org/dist/File-Find-Object/
Source0:        http://www.cpan.org/authors/id/S/SH/SHLOMIF/%{pkgname}-v%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  perl
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(lib)
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(strict)
# Test::Run::CmdLine::Iface not used
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(Class::XSAccessor)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(integer)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(parent)
# Tests:
BuildRequires:  perl(File::Path)
BuildRequires:  perl(Test::More)
# Optional tests:
BuildRequires:  perl(Test::CPAN::Changes)
BuildRequires:  perl(Test::Pod::Coverage) >= 1.04
BuildRequires:  perl(Test::Pod) >= 1.14
%if !%{defined %perl_bootstrap}
# Break build-time dependency cycle: perl-File-Find-Object
# → perl-Test-TrailingSpace → perl-File-Find-Object-Rule
# → perl-File-Find-Object
BuildRequires:  perl(Test::TrailingSpace)
%endif
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
File::Find::Object does the same job as File::Find but works like an object
and with an iterator. As File::Find is not object oriented, one cannot
perform multiple searches in the same application. The second problem of
File::Find is its file processing: after starting its main loop, one cannot
easily wait for another event and so get the next result.

%prep
%setup -qn %{pkgname}-v%{version}
chmod 644 examples/tree

%build
%{__perl} Build.PL installdirs=vendor
./Build

%install
./Build install destdir=%{buildroot} create_packlist=0
%{_fixperms} %{buildroot}/*

%check
./Build test

%files
%doc Changes README examples rejects scripts
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.2.13-4
- 为 Magic 3.0 重建

* Tue Sep 15 2015 Liu Di <liudidi@gmail.com> - 0.2.13-3
- 为 Magic 3.0 重建

* Tue Sep 15 2015 Liu Di <liudidi@gmail.com> - 0.2.13-2
- 为 Magic 3.0 重建

* Fri Jul 24 2015 Petr Pisar <ppisar@redhat.com> - 0.2.13-1
- 0.2.13 bump
- License changed to (GPLv2+ or Artistic 2.0)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.11-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.2.11-6
- Perl 5.22 re-rebuild of bootstrapped packages

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.2.11-5
- Perl 5.22 rebuild

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.2.11-4
- Perl 5.20 re-rebuild of bootstrapped packages

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.2.11-3
- Perl 5.20 rebuild

* Wed Jul 23 2014 Petr Pisar <ppisar@redhat.com> - 0.2.11-2
- Break dependency cycle perl-File-Find-Object → perl-Test-TrailingSpace →
  perl-File-Find-Object-Rule

* Wed Jun 11 2014 Christopher Meng <rpm@cicku.me> - 0.2.11-1
- Update to 0.2.11

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 21 2013 Petr Pisar <ppisar@redhat.com> - 0.2.7-3
- Perl 5.18 rebuild

* Wed Jul 03 2013 Christopher Meng <rpm@cicku.me> - 0.2.7-2
- Fix the license.
- Fix the files permissions.
- Fill up the BRs.

* Sun May 26 2013 Christopher Meng <rpm@cicku.me> - 0.2.7-1
- Initial Package.
