Name:           perl-Coro
Version:        6.39
Release:        6%{?dist}
Summary:        The only real threads in perl
# Coro/libcoro:    GPLv2 or BSD
# Rest of package: GPL+ or Artistic
License:        (GPL+ or Artistic) and (GPLv2 or BSD)
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Coro/
Source0:        http://search.cpan.org/CPAN/authors/id/M/ML/MLEHMANN/Coro-%{version}.tar.gz
Patch0:         %{name}-5.25-ucontext-default.patch
BuildRequires:  libecb
BuildRequires:  perl
BuildRequires:  perl(Config)
BuildRequires:  perl(EV) >= 4
BuildRequires:  perl(EV::MakeMaker)
BuildRequires:  perl(Event) >= 1.08
BuildRequires:  perl(Event::MakeMaker)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(strict)
# Run-time:
BuildRequires:  perl(AnyEvent) >= 7
# AnyEvent::AIO >= 1 not used at tests
# AnyEvent::BDB >= 1 not used at tests
# AnyEvent::DNS not used at tests
BuildRequires:  perl(AnyEvent::Socket)
BuildRequires:  perl(AnyEvent::Util)
BuildRequires:  perl(base)
# BDB not used at tests
BuildRequires:  perl(Carp)
BuildRequires:  perl(common::sense)
BuildRequires:  perl(Errno)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Guard) >= 0.5
# IO::AIO >= 3.1 not used at tests
BuildRequires:  perl(IO::Socket::INET)
# Net::Config not used at tests
# Net::FTP not used at tests
# Net::HTTP not used at tests
# Net::NNTP not used at tests
BuildRequires:  perl(overload)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Socket)
BuildRequires:  perl(Storable) >= 2.15
BuildRequires:  perl(warnings)
BuildRequires:  perl(XSLoader)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
# Export correct required versions
Requires:       perl(AnyEvent) >= 7
Requires:       perl(AnyEvent::AIO) >= 1
Requires:       perl(AnyEvent::BDB) >= 1
Requires:       perl(EV) >= 4
Requires:       perl(Event) >= 1.08
Requires:       perl(Guard) >= 0.5
Requires:       perl(Storable) >= 2.15
Requires:       perl(warnings)

%if 0%{?rhel} && 0%{?rhel} < 7
# RPM 4.8 style:
# Filter underspecified dependencies
%filter_from_requires /^perl(AnyEvent)$/d
%filter_from_requires /^perl(AnyEvent) >= 4.800001$/d
%filter_from_requires /^perl(AnyEvent::AIO)$/d
%filter_from_requires /^perl(AnyEvent::BDB)$/d
%filter_from_requires /^perl(EV)$/d
%filter_from_requires /^perl(Event)$/d
%filter_from_requires /^perl(Guard)$/d
%filter_from_requires /^perl(Storable)$/d
# Version unversioned Provides
%filter_from_provides s/^\(perl(Coro\>[^=]*\)$/\1 = %{version}/

%{?perl_default_filter}
%else
%{?perl_default_filter}

# RPM 4.9 style:
# Filter underspecified dependencies
%global __requires_exclude %{?__requires_exclude:__requires_exclude|}^perl\\(AnyEvent\\)$
%global __requires_exclude %__requires_exclude|^perl\\(AnyEvent\\) >= 4.800001$
%global __requires_exclude %__requires_exclude|^perl\\(AnyEvent::AIO\\)$
%global __requires_exclude %__requires_exclude|^perl\\(AnyEvent::BDB\\)$
%global __requires_exclude %__requires_exclude|^perl\\(EV\\)$
%global __requires_exclude %__requires_exclude|^perl\\(Event\\)$
%global __requires_exclude %__requires_exclude|^perl\\(Guard\\)$
%global __requires_exclude %__requires_exclude|^perl\\(Storable\\)$
%global __provides_exclude %{?__provides_exclude:__provides_exclude|}^perl\\(Coro\\)$
%endif


%description
This module collection manages continuations in general, most often in the
form of cooperative threads (also called coros, or simply "coro" in the
documentation). They are similar to kernel threads but don't (in general) run
in parallel at the same time even on SMP machines. The specific flavor of
thread offered by this module also guarantees you that it will not switch
between threads unless necessary, at easily-identified points in your
program, so locking and parallel access are rarely an issue, making thread
programming much safer and easier than using other thread models.


%prep
%setup -q -n Coro-%{version}
# Unbundle libecb
rm Coro/ecb.h
sed -i '/^Coro\/ecb\.h$/d' MANIFEST
sed -i 's/ecb\.h//' Coro/Makefile.PL

# use ucontext backend on non-x86 (setjmp didn't work on s390(x))
%ifnarch %{ix86} x86_64 %{arm}
%patch0 -p1 -b .ucontext-default
%endif

for F in Coro/jit-*.pl; do
    sed -i -e '/^#!/d' "$F"
    chmod -x "$F"
done

%global wrong_shbangs eg/myhttpd
%if %{defined fix_shbang_line}
%fix_shbang_line %wrong_shbangs
%else
# at least EL6 doesn't have the %%fix_shbang_line macro
sed -i -e '/^#!/ s|.*|#!%{__perl}|' %wrong_shbangs
%endif


%build
# Disable FORTIFY_SOURCE on ARM as it breaks setjmp - RHBZ 750805
%ifarch %{arm}
RPM_OPT_FLAGS=$(echo "${RPM_OPT_FLAGS}" | sed -e 's/-Wp,-D_FORTIFY_SOURCE=2/-D_FORTIFY_SOURCE=0/g')
%endif

# Interractive configuration. Use default values.
perl Makefile.PL INSTALLDIRS=perl OPTIMIZE="$RPM_OPT_FLAGS" </dev/null
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -type f -name '*.bs' -size 0 -exec rm -f {} \;
%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%doc Changes COPYING README README.linux-glibc
%doc doc/* eg
%{perl_archlib}/auto/*
%{perl_archlib}/Coro*
%{_mandir}/man3/*

%changelog
* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 6.39-6
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 6.39-5
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 6.39-4
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 6.39-3
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.39-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jun 02 2014 Petr Pisar <ppisar@redhat.com> - 6.39-1
- 6.39 bump

* Wed Mar 05 2014 Petr Pisar <ppisar@redhat.com> - 6.37-1
- 6.37 bump

* Tue Nov 19 2013 Petr Pisar <ppisar@redhat.com> - 6.33-1
- 6.33 bump

* Wed Nov 06 2013 Petr Pisar <ppisar@redhat.com> - 6.32-1
- 6.32 bump

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.31-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Petr Pisar <ppisar@redhat.com> - 6.31-2
- Perl 5.18 rebuild

* Mon May 13 2013 Petr Pisar <ppisar@redhat.com> - 6.31-1
- 6.31 bump

* Thu May 09 2013 Petr Pisar <ppisar@redhat.com> - 6.29-1
- 6.29 bump

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec 10 2012 Petr Pisar <ppisar@redhat.com> - 6.23-1
- 6.23 bump

* Mon Oct 22 2012 Petr Pisar <ppisar@redhat.com> - 6.10-3
- Do not mark this package as bundling libecb

* Mon Oct 22 2012 Petr Pisar <ppisar@redhat.com> - 6.10-2
- Unbundle libecb (bug #863988)

* Fri Oct 12 2012 Petr Pisar <ppisar@redhat.com> - 6.10-1
- 6.10 bump

* Mon Oct 08 2012 Petr Pisar <ppisar@redhat.com> - 6.09-2
- Fix building on big endian system (bug #863991)

* Sun Oct 07 2012 Nicolas Chauvet <kwizart@gmail.com> - 6.09-1
- Update to 4.09

* Fri Aug  3 2012 Jitka Plesnikova <jplesnik@redhat.com> - 6.08-4
- Update BR

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.08-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 15 2012 Petr Pisar <ppisar@redhat.com> - 6.08-2
- Perl 5.16 rebuild

* Mon Apr 16 2012 Petr Pisar <ppisar@redhat.com> - 6.08-1
- 6.08 bump

* Tue Feb 21 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 6.07-3
- Add patch to fix build on ARM. RHBZ 750805

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.07-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 09 2011 Petr Pisar <ppisar@redhat.com> - 6.07-1
- 6.07 bump

* Thu Nov 03 2011 Nicolas Chauvet <kwizart@gmail.com> - 6.06-2
- Fix ucontext on ARM - rhbz750805

* Fri Aug 12 2011 Petr Sabata <contyk@redhat.com> - 6.06-1
- 6.06 bump

* Fri Aug 05 2011 Petr Sabata <contyk@redhat.com> - 6.05-1
- 6.05 bump

* Thu Aug 04 2011 Petr Sabata <contyk@redhat.com> - 6.04-1
- 6.04 bump

* Fri Jul 29 2011 Petr Pisar <ppisar@redhat.com> - 6.02-1
- 6.02 bump
- Major version 6 breaks compatibility: Unreferenced coro objects will now be
  destroyed and cleaned up automatically (e.g. async { schedule }).

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 5.372-4
- Perl mass rebuild

* Fri Apr 08 2011 Mathieu Bridon <bochecha@fedoraproject.org> - 5.372-3
- Added explicit versionned Requires: on perl(EV)
- Removed automatically added unversionned Requires: on perl(EV)

* Thu Apr 07 2011 Mathieu Bridon <bochecha@fedoraproject.org> - 5.372-2
- Rebuild with EV support.

* Mon Mar 07 2011 Petr Pisar <ppisar@redhat.com> - 5.372-1
- 5.372 bump

* Mon Feb 21 2011 Petr Pisar <ppisar@redhat.com> - 5.37-1
- 5.37 bump
- Fix State.xs syntax (RT#65991)
- Version unversioned Provides

* Mon Feb 14 2011 Petr Pisar <ppisar@redhat.com> - 5.26-1
- 5.26 bump

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.25-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 21 2011 Mathieu Bridon <bochecha@fedoraproject.org> 5.25-3
- Allow building on systems without %%fix_shbang_line macro (needed for EL6)

* Mon Jan 10 2011 Dan Horák <dan[at]danny.cz> 5.25-2
- use ucontext backend on non-x86

* Tue Jan 04 2011 Petr Pisar <ppisar@redhat.com> 5.25-1
- 5.25 import
- Disable perl(EV) support as it's not packaged yet
