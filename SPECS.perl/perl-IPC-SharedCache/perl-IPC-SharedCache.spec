Name:           perl-IPC-SharedCache
Version:        1.3
Release:        21%{?dist}
Summary:        Perl module to manage a cache in SysV IPC shared memory

Group:          Development/Libraries
License:        GPLv2+
URL:            http://search.cpan.org/dist/IPC-SharedCache/
Source0:        http://www.cpan.org/authors/id/S/SA/SAMTREGAR/IPC-SharedCache-%{version}.tar.gz
Patch0:         IPC-SharedCache-1.3-test.patch

BuildArch:      noarch
BuildRequires:  perl(IPC::ShareLite) >= 0.06
BuildRequires:  perl(ExtUtils::MakeMaker)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This module provides a shared memory cache accessed as a tied hash.
Shared memory is an area of memory that is available to all processes.
It is accessed by choosing a key, the ipc_key argument to tie.  Every
process that accesses shared memory with the same key gets access to
the same region of memory.  In some ways it resembles a file system,
but it is not hierarchical and it is resident in memory.  This makes
it harder to use than a filesystem but much faster.  The data in
shared memory persists until the machine is rebooted or it is
explicitly deleted.


%prep
%setup -q -n IPC-SharedCache-%{version}
%patch0 -p1

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
%doc ANNOUNCE Changes LICENSE README
%{perl_vendorlib}/IPC/
%{_mandir}/man3/*.3pm*


%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.3-21
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.3-20
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.3-19
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.3-17
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.3-15
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Dec 17 2010 Marcela Mašláňová <mmaslano@redhat.com> - 1.3-14
- apply Debian patch for tests, which fix problem of HTML::Template

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.3-13
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.3-12
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.3-8
- rebuild for new perl

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.3-7.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Fri Sep  8 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.3-7
- Rebuild for FC6.

* Thu Feb 16 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.3-6
- Rebuild for FC5 (perl 5.8.8).
- Dist tag and specfile cleanups.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.3-5
- rebuilt

* Sat Jun 26 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.3-0.fdr.4
- Fix license (bug 1783).
- BuildReq perl(Storable) (bug 1783).

* Fri Jun 25 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.3-0.fdr.3
- Bring up to date with current fedora.us perl spec template.

* Mon Apr 26 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.3-0.fdr.2
- Reduce directory ownership bloat.
- Require perl(:MODULE_COMPAT_*).
- BuildArch: noarch.

* Tue Nov 18 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.3-0.fdr.1
- First build.
