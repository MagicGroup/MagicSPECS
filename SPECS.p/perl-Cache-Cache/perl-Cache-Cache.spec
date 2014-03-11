Name:           perl-Cache-Cache
Version:        1.06
Release:        11%{?dist}
Summary:        Generic cache interface and implementations
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Cache-Cache/
Source0:        http://www.cpan.org/authors/id/J/JS/JSWARTZ/Cache-Cache-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl(Digest::SHA1) >= 2.02
BuildRequires:  perl(Error) >= 0.15
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(IPC::ShareLite)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
The Cache modules are designed to assist a developer in persisting data for a
specified period of time.  Often these modules are used in web applications to
store data locally to save repeated and redundant expensive calls to remote
machines or databases.  People have also been known to use Cache::Cache for
its straightforward interface in sharing data between runs of an application
or invocations of a CGI-style script or simply as an easy to use abstraction
of the filesystem or shared memory.

%prep
%setup -q -n Cache-Cache-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc CHANGES COPYING CREDITS DISCLAIMER README STYLE
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.06-11
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.06-10
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.06-9
- 为 Magic 3.0 重建

* Sat Jan 28 2012 Liu Di <liudidi@gmail.com> - 1.06-8
- 为 Magic 3.0 重建

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.06-7
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.06-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.06-5
- 661697 rebuild for fixing problems with vendorach/lib

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.06-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.06-3
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.06-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed May 13 2009 Steven Pritchard <steve@kspei.com> 1.06-1
- Update to 1.06.
- Reformat to match cpanspec output.
- Fix find option order.
- Use fixperms macro instead of our own chmod incantation.
- Drop explicit perl build dependency.
- Update Source0 URL.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.05-2
- rebuild for new perl

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.05-1.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Mon May 29 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.05-1
- Update to 1.05.

* Mon Feb 20 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.04-4
- Rebuild for FC5 (perl 5.8.8).

* Thu Dec 29 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.04-3
- Dist tag.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.04-2
- rebuilt

* Fri Mar 18 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.04-1
- Update to 1.04.

* Mon Feb 28 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.03-2
- Bring up to date with current fedora.extras perl spec template.

* Tue Feb  1 2005 Matthias Saou <http://freshrpms.net/> 1.03-1
- Merge in changes from Jose Pedro Oliveira's fedora.us package : #146741.
- Update to 1.03.

* Tue Nov 16 2004 Matthias Saou <http://freshrpms.net/> 1.02-4
- Bump release to provide Extras upgrade path.

* Wed May 26 2004 Matthias Saou <http://freshrpms.net/> 1.02-3
- Rebuilt for Fedora Core 2.

* Fri Apr  2 2004 Matthias Saou <http://freshrpms.net/> 1.02-2
- Change the explicit package deps to perl package style ones to fix the
  perl-Storable obsoletes problem.

* Fri Mar 19 2004 Matthias Saou <http://freshrpms.net/> 1.02-1
- Initial RPM release.

