Name:           perl-Plack
Version:        1.0004
Release:        1%{?dist}
Summary:        Perl Superglue for Web frameworks and Web Servers (PSGI toolkit)
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Plack/
Source0:        http://www.cpan.org/authors/id/M/MI/MIYAGAWA/Plack-%{version}.tar.gz
BuildArch:      noarch

# Building with apache2 tests enabled works in local mocks, 
# but fails in Fedora's koji.
# Default to not testing apache2.
%bcond_with apache

BuildRequires:  perl(Devel::StackTrace) >= 1.23
BuildRequires:  perl(Devel::StackTrace::AsHTML) >= 0.11
BuildRequires:  perl(Devel::StackTrace::WithLexicals) >= 0.8
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::ShareDir) >= 1.00
BuildRequires:  perl(Filesys::Notify::Simple)
BuildRequires:  perl(Hash::MultiValue) >= 0.05
BuildRequires:  perl(HTTP::Body) >= 1.06
BuildRequires:  perl(LWP) >= 5.814
BuildRequires:  perl(LWP::Protocol::http10)
BuildRequires:  perl(parent)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(Test::Requires)
BuildRequires:  perl(Test::TCP) >= 0.11
BuildRequires:  perl(Try::Tiny)
BuildRequires:  perl(URI) >= 1.59

# for improved tests
BuildRequires:  perl(Authen::Simple::Adapter)
BuildRequires:  perl(Authen::Simple::Passwd)
BuildRequires:  perl(CGI)
BuildRequires:  perl(CGI::Compile)
BuildRequires:  perl(CGI::Emulate::PSGI)
BuildRequires:  perl(Class::Data::Inheritable)
BuildRequires:  perl(FCGI)
BuildRequires:  perl(FCGI::Client)
BuildRequires:  perl(FCGI::ProcManager)
BuildRequires:  perl(HTTP::Request::AsCGI)
BuildRequires:  perl(HTTP::Server::Simple::PSGI)
BuildRequires:  perl(IO::Handle::Util)
BuildRequires:  perl(Log::Dispatch::Array)
BuildRequires:  perl(Log::Log4perl)
BuildRequires:  perl(MIME::Types)
BuildRequires:  perl(Module::Refresh)

# For mod_perl.so
BuildRequires:  mod_perl >= 2

# For httpd tests
BuildRequires:  /usr/sbin/httpd

# For t/Plack-Middleware/cgibin_exec.t
BuildRequires:  /usr/bin/python

# For lighttpd tests
BuildRequires:  /usr/sbin/lighttpd
BuildRequires:  lighttpd-fastcgi

Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Plack is a set of tools for using the PSGI stack. It contains middleware
components, a reference server and utilities for Web application
frameworks. Plack is like Ruby's Rack or Python's Paste for WSGI.

%prep
%setup -q -n Plack-%{version}

# Fedora's mod_perl.so is under modules/
sed -i -e 's,libexec/apache2/mod_perl.so,modules/mod_perl.so,' \
t/Plack-Handler/apache2.t t/Plack-Handler/apache2-registry.t

%build
# --skipdeps causes ExtUtils::AutoInstall not to try auto-installing
# missing modules
%{__perl} Makefile.PL INSTALLDIRS=vendor --skipdeps
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test %{?_with_apache:TEST_APACHE2=1 TEST_FCGI_CLIENT=1}

%files
%defattr(-,root,root,-)
%doc Changes README
%{_bindir}/plackup
%{_mandir}/man1/plackup.*
%{perl_vendorlib}/Plack
%{perl_vendorlib}/Plack.pm
%{perl_vendorlib}/HTTP
# Used by Plack/Test
%{perl_vendorlib}/auto/*
%exclude %{perl_vendorlib}/auto/share/dist/Plack/#foo
# Abandoned/Unsupported in Fedora: Apache1
%exclude %{perl_vendorlib}/Plack/Server/Apache1.pm
%exclude %{perl_vendorlib}/Plack/Handler/Apache1.pm

%{_mandir}/man3/*

%changelog
* Mon Sep 24 2012 Ralf Corsépius <corsepiu@fedoraproject.org> 1.0004-1
- Upstream update.

* Sun Sep 16 2012 Ralf Corsépius <corsepiu@fedoraproject.org> 1.0003-1
- Upstream update.

* Thu Aug 16 2012 Ralf Corsépius <corsepiu@fedoraproject.org> 1.0002-1
- Upstream update.

* Mon Jul 30 2012 Ralf Corsépius <corsepiu@fedoraproject.org> 1.0001-1
- Upstream update.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9989-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 29 2012 Petr Pisar <ppisar@redhat.com> - 0.9989-2
- Perl 5.16 rebuild

* Wed Jun 27 2012 Ralf Corsépius <corsepiu@fedoraproject.org> 0.9989-1
- Upstream update.

* Mon May 21 2012 Ralf Corsépius <corsepiu@fedoraproject.org> 0.9988-1
- Upstream update.

* Mon Mar 19 2012 Ralf Corsépius <corsepiu@fedoraproject.org> 0.9986-1
- Upstream update.

* Wed Jan 18 2012 Ralf Corsépius <corsepiu@fedoraproject.org> 0.9985-3
- Activate optional BR: perl(Devel::StackTrace::WithLexicals).
- Activate optional BR: perl(LWP::Protocol::http10).

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9985-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Nov 26 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 0.9985-1
- Upstream update.

* Thu Oct 14 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 0.9984-2
- Add %%bcond_with apache to work around building failures in koji.

* Thu Oct 13 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 0.9984-1
- Upstream update.

* Fri Aug 19 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 0.9982-1
- Upstream update.

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.9980-2
- Perl mass rebuild

* Wed Jun 08 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 0.9980-1
- Upstream update.

* Thu May 19 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 0.9979-1
- Upstream update.
- Activate lighttpd and lighttpd-fcgi tests.

* Wed May 11 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 0.9978-1
- Upstream update.

* Mon May 02 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 0.9977-1
- Upstream update.

* Sun Apr 17 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 0.9976-1
- Upstream update.

* Mon Mar 14 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 0.9974-2
- Reflect HTTP-Server-Simple-PSGI having entered Fedora
  (Add BR: perl(HTTP::Server::Simple::PSGI)).

* Mon Mar 14 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 0.9974-1
- Upstream update.

* Thu Mar 03 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 0.9973-1
- Upstream update.
- Reflect upstream not shipping Plack/Handler/Net/FastCGI.pm anymore.
- Spec file cleanup.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9967-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 26 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 0.9967-1
- Upstream update.

* Tue Jan 25 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 0.9964-1
- Upstream update.

* Tue Jan 18 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 0.9963-1
- Upstream update.
- Hack around incorrect hard-coded path to mod_perl.so.
- Activate Apache2 test.

* Mon Jan 03 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 0.9960-1
- Upstream update.

* Wed Dec 22 2010 Ralf Corsépius <corsepiu@fedoraproject.org> 0.9959-2
- Re-add %%{perl_vendorlib}/auto/*jpg (Used by Plack/Test).
- Add BR: perl(Authen::Simple::Passwd).
- Add BR: perl(CGI::Emulate::PSGI).

* Wed Dec 22 2010 Ralf Corsépius <corsepiu@fedoraproject.org> 0.9959-1
- Update to 0.9959.

* Tue Dec 21 2010 Ralf Corsépius <corsepiu@fedoraproject.org> 0.9958-1
- Initial Fedora package.
