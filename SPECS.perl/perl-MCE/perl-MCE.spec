Name:           perl-MCE
Version:        1.608
Release:        4%{?dist}
Summary:        Many-core Engine for Perl providing parallel processing capabilities
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/MCE/
Source0:        http://www.cpan.org/authors/id/M/MA/MARIOROY/MCE-%{version}.tar.gz
# Fix sharp-bang line
Patch0:         MCE-1.600-Fix-sharp-bang-line.patch
BuildArch:      noarch
# Build
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Runtime
# The bin/mce_grep is not used by tests
BuildRequires:  perl(base)
BuildRequires:  perl(bytes)
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(File::Path)
# Unused BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Socket)
BuildRequires:  perl(Storable) >= 2.04
BuildRequires:  perl(Symbol)
BuildRequires:  perl(Time::HiRes)
# Tests only
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "$(perl -V:version)"; echo $version))
Requires:       perl(IO::Handle)
Requires:       perl(MCE::Candy)
Requires:       perl(MCE::Core::Input::Generator)
Requires:       perl(MCE::Core::Input::Handle)
Requires:       perl(MCE::Core::Input::Iterator)
Requires:       perl(MCE::Core::Input::Request)
Requires:       perl(MCE::Core::Input::Sequence)
Requires:       perl(MCE::Core::Manager)
Requires:       perl(MCE::Core::Validation)
Requires:       perl(MCE::Core::Worker)
Requires:       perl(MCE::Util)
Requires:       perl(Storable) >= 2.04

%{?perl_default_filter}
%global __requires_exclude %{?__requires_exclude|%__requires_exclude|}^perl\\(Storable\\)$
%global __provides_exclude %{?__provides_exclude|%__provides_exclude|}^perl\\(MCE\\)$

%description
Many-core Engine (MCE) for Perl helps enable a new level of performance by
maximizing all available cores. MCE spawns a pool of workers and therefore
does not fork a new process per each element of data. Instead, MCE follows
a bank queuing model. Imagine the line being the data and bank-tellers the
parallel workers. MCE enhances that model by adding the ability to chunk
the next n elements from the input stream to the next available worker.

%package tools
Summary:        Many-core Engine command line tools
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       grep

%description tools
This package delivers command line tools like mce_grep(1) that utilize
the Many-core Engine (MCE) Perl library.


%prep
%setup -q -n MCE-%{version}
%patch0 -p1
chmod -c a-x examples/*pl

%build
MCE_INSTALL_TOOLS=1 perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} +
%{_fixperms} %{buildroot}/*

%check
make test

%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc CHANGES CREDITS README examples
%{perl_vendorlib}/*
%{_mandir}/man3/*

%files tools
%{_bindir}/mce_grep

%changelog
* Wed Sep 16 2015 Liu Di <liudidi@gmail.com> - 1.608-4
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.608-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.608-2
- Perl 5.22 rebuild

* Fri Apr 10 2015 Petr Šabata <contyk@redhat.com> - 1.608-1
- 1.608 bump

* Thu Apr 09 2015 Petr Šabata <contyk@redhat.com> - 1.606-1
- 1.606 bump

* Wed Apr 08 2015 Petr Šabata <contyk@redhat.com> - 1.605-1
- 1.605 bump

* Mon Mar 23 2015 Petr Šabata <contyk@redhat.com> - 1.604-1
- 1.604 bump

* Wed Feb 11 2015 Petr Pisar <ppisar@redhat.com> - 1.600-3
- Move mce_grep tool into a separate sub-package

* Tue Feb 10 2015 Petr Pisar <ppisar@redhat.com> - 1.600-2
- Correct dependencies

* Wed Feb 04 2015 Petr Šabata <contyk@redhat.com> - 1.600-1
- 1.600 bump

* Mon Jan 05 2015 Petr Šabata <contyk@redhat.com> - 1.522-1
- 1.522 bump

* Wed Dec 17 2014 Petr Šabata <contyk@redhat.com> - 1.521-1
- 1.521 bump

* Tue Nov 11 2014 Petr Šabata <contyk@redhat.com> 1.520-1
- Initial packaging
