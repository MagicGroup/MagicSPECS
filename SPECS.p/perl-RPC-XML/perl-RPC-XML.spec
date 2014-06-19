%global cpan_name RPC-XML

Name:    perl-%{cpan_name}
Version: 0.78
Release: 2%{?dist}
Summary: Set of classes for core data, message and XML handling
Group:   Development/Libraries
License: Artistic 2.0 or LGPLv2
URL:     http://search.cpan.org/dist/%{cpan_name}/
Source0:   http://search.cpan.org/CPAN/authors/id/R/RJ/RJRAY/%{cpan_name}-%{version}.tar.gz
Source1:   README.license
BuildArch: noarch
BuildRequires: perl
BuildRequires: perl(Cwd)
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(File::Spec) >= 0.8
# Run-time without Apache stuff:
BuildRequires: perl(base)
BuildRequires: perl(Carp)
BuildRequires: perl(constant) >= 1.03
BuildRequires: perl(Exporter)
BuildRequires: perl(File::Temp)
BuildRequires: perl(HTTP::Daemon)
BuildRequires: perl(HTTP::Request)
BuildRequires: perl(HTTP::Response)
BuildRequires: perl(HTTP::Status)
BuildRequires: perl(IO::Handle)
BuildRequires: perl(LWP::UserAgent)
BuildRequires: perl(MIME::Base64)
BuildRequires: perl(Module::Load) >= 0.24
BuildRequires: perl(Scalar::Util) >= 1.19
BuildRequires: perl(URI)
BuildRequires: perl(XML::Parser) >= 2.31
# Run-time for Apache stuff:
BuildRequires: perl(Apache)
BuildRequires: perl(Apache::Constants)
BuildRequires: perl(Apache::File)
BuildRequires: perl(CGI)
BuildRequires: perl(Socket)
# Recommended run-time:
# Keep Compress::Raw::Zlib optional
BuildRequires: perl(DateTime) >= 0.70
BuildRequires: perl(DateTime::Format::ISO8601) >= 0.07
BuildRequires: perl(LWP) >= 5.834
BuildRequires: perl(XML::LibXML) >= 1.85
# Tests:
BuildRequires: perl(IO::File)
BuildRequires: perl(IO::Socket)
BuildRequires: perl(Test::More) >= 0.94
# Optional tests:
BuildRequires: perl(Compress::Zlib)
BuildRequires: perl(Digest::MD5)
BuildRequires: perl(Net::Server)

Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(constant) >= 1.03
Requires:       perl(File::Spec) >= 0.8
Requires:       perl(HTTP::Daemon)
Requires:       perl(LWP) >= 5.834
Requires:       perl(MIME::Base64)
Requires:       perl(Module::Load) >= 0.24
Requires:       perl(Scalar::Util) >= 1.19
Requires:       perl(XML::Parser) >= 2.31
# Recommended
# Keep Compress::Raw::Zlib optional
Requires:       perl(DateTime) >= 0.70
Requires:       perl(DateTime::Format::ISO8601) >= 0.07
Requires:       perl(XML::LibXML) >= 1.85

%perl_default_filter
# Remove underspecified symbols
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(constant|File::Spec|Module::Load|Scalar::Util|XML::LibXML|XML::Parser\\)\\s*$

%description
The RPC::XML package is an implementation of XML-RPC. The module provides
classes for sample client and server implementations, a server designed as an
Apache location-handler, and a suite of data-manipulation classes that are
used by them.


%package -n perl-Apache-RPC
Summary: Companion packages for RPC::XML tuned for mod_perl environments
Group:   Development/Libraries
Requires:   perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:   perl(File::Spec) >= 0.8

%description -n perl-Apache-RPC
This package contains Apache::RPC::Server and Apache::RPC::Status, useful for
running RPC::XML under mod_perl.


%prep
%setup -qn %{cpan_name}-%{version}
cp -p %{SOURCE1} .

%build
perl Makefile.PL INSTALLDIRS="vendor" PREFIX="%{_prefix}"
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} %{buildroot}/*

%check
make test

%files
%doc ChangeLog* README etc/*.dtd README.license ex/ methods/
%{_mandir}/man3/RPC*
%{_mandir}/man1/*
%{_bindir}/make_method
%{perl_vendorlib}/RPC

%files -n perl-Apache-RPC
%doc README.apache2 README.license
%{_mandir}/man3/Apache*
%{perl_vendorlib}/Apache

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.78-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Feb 10 2014 Petr Pisar <ppisar@redhat.com> - 0.78-1
- 0.78 bump

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.77-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Aug 01 2013 Petr Pisar <ppisar@redhat.com> - 0.77-3
- Perl 5.18 rebuild
- Adjust tests for perl 5.18 (CPAN RT#86187)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.77-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Sep 04 2012 Petr Pisar <ppisar@redhat.com> - 0.77-1
- 0.77 bump
- Specify all dependencies
- Modernize spec file
- Do not package tests

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.76-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 21 2012 Petr Pisar <ppisar@redhat.com> - 0.76-4
- Perl 5.16 rebuild

* Mon Jan 16 2012 Petr Pisar <ppisar@redhat.com> - 0.76-3
- Require MODULE_COMPAT because this is Perl package.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.76-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 21 2011 Petr Pisar <ppisar@redhat.com> - 0.76-1
- 0.76 bump

* Mon Apr 04 2011 Petr Pisar <ppisar@redhat.com> - 0.74-1
- 0.74 bump

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.69-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.69-3
- 661697 rebuild for fixing problems with vendorach/lib

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.69-2
- Mass rebuild with perl-5.12.0

* Tue Sep 22 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.69-1
- auto-update to 0.69 (by cpan-spec-update 0.01)
- added a new br on perl(File::Spec) (version 0.8)
- altered br on perl(LWP) (0 => 5.801)
- added a new br on perl(Scalar::Util) (version 1.19)
- altered br on perl(XML::Parser) (0 => 2.31)
- added a new br on perl(constant) (version 1.03)
- added a new req on perl(File::Spec) (version 0.8)
- added a new req on perl(LWP) (version 5.801)
- added a new req on perl(Scalar::Util) (version 1.19)
- added a new req on perl(XML::Parser) (version 2.31)
- added a new req on perl(constant) (version 1.03)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.64-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.64-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Oct 23 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.64-1
- update to 0.64-1
- drop tests patch (fixed!)
- add BR on Net::Server

* Mon Sep 08 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.60-3
- bump

* Tue Aug 26 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.60-2
- quiesce offending test

* Sat Aug 23 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.60-1
- even more spec cleanups :-)
- update licensing

* Fri Jul 04 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.60-0.1
- update to 0.60
- spec file cleanups

* Sun Mar 16 2008 Nicholas Boyle <nsboyle@gmail.com> - 0.59-5
- Added BuildRequires for Test::More and XML::Parser

* Sun Mar 16 2008 Nicholas Boyle <nsboyle@gmail.com> - 0.59-4
- Created subpackage perl-Apache-RPC to allow RPC-XML to work without
  requiring mod_perl
- Manpages now installed as regular files, instead of docs
- Removed explicit perl_archlib and perl_vendorarch definitions

* Fri Mar 07 2008 Nicholas Boyle <nsboyle@gmail.com> - 0.59-3
- Added README.license to clarify licensing

* Sat Mar 01 2008 Nicholas Boyle <nsboyle@gmail.com> - 0.59-2
- Initial Fedora packaging

* Mon Sep 18 2006 Dries Verachtert <dries@ulyssis.org> - 0.59-1
- Updated to release 0.59.

* Wed Mar 22 2006 Dries Verachtert <dries@ulyssis.org> - 0.58-1.2
- Rebuild for Fedora Core 5.

* Wed Jun  8 2005 Dries Verachtert <dries@ulyssis.org> - 0.58-1
- Updated to release 0.58.

* Sat Jan  1 2005 Dries Verachtert <dries@ulyssis.org> - 0.57-1
- Initial package.
