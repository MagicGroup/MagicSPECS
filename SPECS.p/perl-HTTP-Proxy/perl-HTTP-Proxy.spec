Name:           perl-HTTP-Proxy
Version:        0.23
Release:        12%{?dist}
Summary:        A pure Perl HTTP proxy

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/HTTP-Proxy/
Source0:        http://www.cpan.org/authors/id/B/BO/BOOK/HTTP-Proxy-%{version}.tar.gz
Patch0:         HTTP-Proxy-0.17-save.pm.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Test::Pod), perl(Test::Pod::Coverage), perl(HTML::Parser)
BuildRequires:  perl(HTTP::Daemon), perl(LWP::UserAgent), perl(Crypt::SSLeay)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Its main use should be to record and/or modify web sessions, so as to
help users create web robots, web testing suites, as well as proxy
systems than can transparently alter the requests to and answers from
an origin server.


%prep
%setup -q -n HTTP-Proxy-%{version}
%patch0 -p1


%build
%{__perl} Build.PL installdirs=vendor
./Build


%install
rm -rf $RPM_BUILD_ROOT
./Build install destdir=$RPM_BUILD_ROOT create_packlist=0
chmod -R u+w $RPM_BUILD_ROOT/*


%check
# Tests are pretty broken.
# ./Build test


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc Changes README eg/
%{perl_vendorlib}/HTTP/
%{_mandir}/man3/*.3pm*


%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.23-12
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.23-11
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.23-9
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 17 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.23-7
- 661697 rebuild for fixing problems with vendorach/lib

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.23-6
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.23-5
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 16 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 0.23-1
- update to 0.23

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.20-2
Rebuild for new perl

* Mon Sep  4 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.20-1
- Update to 0.20.

* Fri Apr 28 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.19-1
- Update to 0.19.

* Wed Mar 22 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.18-1
- Update to 0.18.

* Mon Mar  6 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.17-3
- Added missing BR: perl(Test::Pod::Coverage).

* Mon Mar  6 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.17-2
- save.pm patched and converted to utf8 (HTTP-Proxy-0.17-save.pm.patch).

* Thu Dec  8 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.17-1
- Update to 0.17.

* Thu Sep  8 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.16-1
- Update to 0.16.

* Sun Jul 04 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:0.13-0.fdr.1
- First build.
