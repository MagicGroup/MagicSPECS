Name:       perl-PlRPC 
Version:    0.2020 
Release:    12%{?dist}
License:    GPL+ or Artistic
Group:      Development/Libraries
Summary:    Interface for writing PlRPC clients and servers
Url:        http://search.cpan.org/dist/PlRPC
Source:     http://search.cpan.org/CPAN/authors/id/M/MN/MNOONING/PlRPC/PlRPC-%{version}.tar.gz 
# See <https://rt.cpan.org/Public/Bug/Display.html?id=74430>
Patch0:     %{name}-0.2020-Do-not-use-syslog.patch
BuildArch:  noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
# perldoc utility is called from Makefile
BuildRequires:  perl-Pod-Perldoc
# Run-time
BuildRequires:  perl(Compress::Zlib)
BuildRequires:  perl(IO::Socket)
BuildRequires:  perl(Net::Daemon) >= 0.13
BuildRequires:  perl(Net::Daemon::Log)
BuildRequires:  perl(Net::Daemon::Test)
BuildRequires:  perl(Storable)
# Tests
BuildRequires:  perl(Net::Daemon::Test)
# Optionable tests
BuildRequires:  perl(Crypt::DES)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
# Compress::Zlib is needed for optional compression
Requires:       perl(Compress::Zlib)
Requires:       perl(Net::Daemon) >= 0.13

# Remove undespecified dependencies
%global __requires_exclude %{?__requires_exclude|%__requires_exclude|}^perl\\(Net::Daemon\\)$

%description
PlRPC (Perl RPC) is a package that simplifies the writing of Perl based
client/server applications. RPC::PlServer is the package used on the
server side, and you guess what RPC::PlClient is for.  PlRPC works by 
defining a set of methods that may be executed by the client.

%prep
%setup -q -n PlRPC
%patch0 -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'
%{_fixperms} %{buildroot}/*

%check


%files
%doc ChangeLog README 
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.2020-12
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2020-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.2020-10
- Perl 5.16 rebuild

* Thu Jan 26 2012 Petr Pisar <ppisar@redhat.com> - 0.2020-9
- Modernize spec file
- Enable tests

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2020-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.2020-7
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2020-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.2020-5
- 661697 rebuild for fixing problems with vendorach/lib

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.2020-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.2020-3
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2020-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Apr 01 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.2020-1
- submission

* Thu Mar 19 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.2020-0
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.8)

