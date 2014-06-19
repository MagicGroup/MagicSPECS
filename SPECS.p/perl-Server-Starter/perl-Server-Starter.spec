Name:           perl-Server-Starter
Version:        0.17
Release:        3%{?dist}
Summary:        Superdaemon for hot-deploying server programs
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Server-Starter/
Source0:        http://www.cpan.org/authors/id/K/KA/KAZUHO/Server-Starter-%{version}.tar.gz
# Fix t/07-envdir.t race, bug #1100158, CPAN RT#73711
Patch0:         Server-Starter-0.17-Synchronize-to-PID-in-t-07-envdir.t.patch
# Fix loading the environment directory, bug #1100158, CPAN RT#73711
Patch1:         Server-Starter-0.17-Fix-loading-envdir.patch
BuildArch:      noarch

BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.42
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(List::MoreUtils)
BuildRequires:  perl(Proc::Wait3)
BuildRequires:  perl(Scope::Guard)
# For the tests
BuildRequires:  perl(Test::TCP) >= 2.00

Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%package start_server
Summary:        perl-Server-Starter start_server script
# FIXME: This doesn't make much sense. If at all, then this should be 
# Requires: perl(Server::Starter) = perl-version(Server::Starter)
Requires:       perl-Server-Starter = %{version}-%{release}

%description
It is often a pain to write a server program that supports graceful
restarts, with no resource leaks. Server::Starter, solves the problem by
splitting the task into two. One is start_server, a script provided as a
part of the module, which works as a superdaemon that binds to zero or
more TCP ports, and repeatedly spawns the server program that actually
handles the necessary tasks (for example, responding to incoming
connections). The spawned server programs under Server::Starter call
accept(2) and handle the requests.

%description start_server
perl-Server-Starter's start_server script.

%prep
%setup -q -n Server-Starter-%{version}
%patch0 -p1
%patch1 -p1

%build
# --skipdeps causes ExtUtils::AutoInstall not to try auto-installing
#   missing modules
%{__perl} Makefile.PL INSTALLDIRS=vendor --skipdeps
make %{?_smp_mflags} 

%install
rm -rf $RPM_BUILD_ROOT

make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%files start_server
%{_bindir}/start_server
%{_mandir}/man1/start_server.*

%changelog
* Tue Jun 17 2014 Petr Pisar <ppisar@redhat.com> - 0.17-3
- Fix races in t/07-envdir.t test (bug #1100158)
- Load the environment directory just before restartin a server (bug #1100158)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Dec 30 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.17-1
- Upstream update.

* Sun Nov 24 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.16-1
- Upstream update.

* Tue Aug 27 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.15-1
- Upstream update.
- Minor spec cleanup.

* Fri Aug 16 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.14-1
- Upstream update.
- BR: perl(Test::TCP) >= 2.00.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 26 2013 Petr Pisar <ppisar@redhat.com> - 0.12-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Sep 26 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.12-1
- Upstream update.
- Modernize spec.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 19 2012 Petr Pisar <ppisar@redhat.com> - 0.11-6
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.11-4
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 24 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 0.11-2
- Add "Requires: perl-Server-Starter = %%{version}-%%{release}"
  per reviewer's demand.

* Thu Jan 20 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 0.11-1
- Upstream update.
- Reflect package review.

* Wed Dec 22 2010 Ralf Corsépius <corsepiu@fedoraproject.org> 0.09-2
- Put start_server into separate subpackage.

* Wed Dec 22 2010 Ralf Corsépius <corsepiu@fedoraproject.org> 0.09-1
- Initial Fedora package.
