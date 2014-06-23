Name:           perl-IPC-Shareable
Version:        0.60
Release:        25%{?dist}
Summary:        Share Perl variables between processes

Group:          Development/Libraries
License:        GPLv2+
URL:            http://search.cpan.org/dist/IPC-Shareable/
Source0:        http://www.cpan.org/authors/id/B/BS/BSUGARS/IPC-Shareable-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Patch0:         perl-IPC-Shareable-nostrictrefs.patch
Patch1:		perl-IPC-Shareable-fixtest38.patch

BuildArch:      noarch
BuildRequires:  perl(Storable), perl(ExtUtils::MakeMaker)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
IPC::Shareable allows you to tie a variable to shared memory making it
easy to share the contents of that variable with other Perl processes.
Scalars, arrays, and hashes can be tied.  The variable being tied may
contain arbitrarily complex data structures - including references to
arrays, hashes of hashes, etc.


%prep
%setup -q -n IPC-Shareable-%{version}
%patch0 -p1
%patch1 -p1
find eg -type f | xargs chmod -c 644


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*


%check



%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc CHANGES COPYING CREDITS DISCLAIMER README TO_DO eg/
%{perl_vendorlib}/IPC/
%{_mandir}/man3/*.3pm*


%changelog
* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.60-25
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.60-24
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.60-23
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.60-22
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.60-21
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.60-20
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.60-19
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.60-18
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.60-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 14 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.60-16
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.60-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.60-13
- 661697 rebuild for fixing problems with vendorach/lib

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.60-12
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.60-11
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.60-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.60-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.60-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 16 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 0.60-7
- fix missing BuildRequires: perl(ExtUtils::MakeMaker)

* Mon Feb  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.60-6
- fix test38 so it doesn't hang forever
- fix IPC::Shareable STORESIZE

* Sun Feb  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.60-5
- patch for new perl, don't use strict 'refs'

* Sat Feb  2 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.60-4
- rebuild for new perl

* Fri Sep  8 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.60-3
- Rebuild for FC6.

* Mon Feb 20 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.60-2
- Rebuild for FC5 (perl 5.8.8).

* Sat Oct 22 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.60-1
- First build.
