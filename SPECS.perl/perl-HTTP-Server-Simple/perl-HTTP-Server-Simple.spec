Name:           perl-HTTP-Server-Simple
Version:	0.51
Release:	3%{?dist}
Summary:        Very simple standalone HTTP daemon

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/HTTP-Server-Simple/
Source0:        http://search.cpan.org/CPAN/authors/id/B/BP/BPS/HTTP-Server-Simple-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  perl(CGI)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod), perl(Test::Pod::Coverage)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
# Not autodetected
Requires:       perl(CGI)

%description
HTTP::Server::Simple is a very simple standalone HTTP daemon with no non-core
module dependencies.  It's ideal for building a standalone http-based UI to
your existing tools.


%prep
%setup -q -n HTTP-Server-Simple-%{version}
chmod -c a-x lib/HTTP/Server/*.pm
%{__perl} -pi -e 's|^#!perl\b|#!%{__perl}|' ex/sample_server


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*


%check



%files
%doc Changes README ex/
%{perl_vendorlib}/HTTP/
%{_mandir}/man3/*.3pm*


%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.51-3
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.51-2
- 更新到 0.51

* Mon Sep 14 2015 Liu Di <liudidi@gmail.com> - 0.50-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.50-1
- 更新到 0.50

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.44-6
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.44-5
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.44-4
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.44-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jul 18 2011 Petr Sabata <contyk@redhat.com> - 0.44-2
- Perl mass rebuild

* Tue Jul  5 2011 Tom Callaway <spot@fedoraproject.org> - 0.44-1
- update to 0.44
- add explicit Requires for perl(CGI), since it is not autodetected (bz719048)

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.43-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.43-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 17 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.43-2
- 661697 rebuild for fixing problems with vendorach/lib

* Wed Jun 23 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.43-1
- Upstream update.

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.42-2
- Mass rebuild with perl-5.12.0

* Tue Mar 02 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.42-1
- Upstream update.
- Abandon BR: perl(URI::Escape).

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.41-2
- rebuild against perl 5.10.1

* Tue Oct 13 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.41-1
- Upstream update.

* Tue Sep 08 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.40-1
- Upstream update.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.38-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Feb 28 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.38-1
- Upstream update.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.34-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Aug 26 2008 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.34-1
- Upstream update (Required by rt >= 3.8.0).

* Wed Mar  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.27-2
- rebuild for new perl

* Sat Jan 20 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.27-1
- Update to 0.27.

* Fri Dec  1 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.26-1
- Update to 0.26.

* Wed Nov 22 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.24-1
- Update to 0.24.

* Mon Oct 23 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.23-1
- Update to 0.23.

* Tue Jun 20 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.20-1
- Update to 0.20.

* Fri Feb 24 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.18-2
- Rebuild for FC5 (perl 5.8.8).

* Thu Feb  9 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.18-1
- Update to 0.18.

* Mon Jan 23 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.17-1
- Update to 0.17.

* Tue Nov  8 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.16-1
- Update to 0.16.

* Tue Oct 11 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.15-1
- Update to 0.15.

* Thu Aug 11 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.13-1
- First build.
