Name:           perl-File-NFSLock
Version:	1.27
Release:	3%{?dist}
Summary:        Perl module to do NFS (or not) locking
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/File-NFSLock
Source0:        http://search.cpan.org/CPAN/authors/id/B/BB/BBB/File-NFSLock-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(base)
BuildRequires:  perl(constant)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Sys::Hostname)
BuildRequires:  perl(Test::More)
Requires:   perl(Exporter)
Requires:   perl(Sys::Hostname)
Requires:   perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Program based of concept of hard linking of files being atomic across NFS. 
This concept was mentioned in Mail::Box::Locker (which was originally 
presented in Mail::Folder::Maildir). Some routine flow is taken from 
there -- particularly the idea of creating a random local file, hard 
linking a common file to the local file, and then checking the nlink 
status. Some ideologies were not complete (uncache mechanism, shared 
locking) and some coding was even incorrect (wrong stat index). 
File::NFSLock was written to be light, generic, and fast.

%prep
%setup -q -n File-NFSLock-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w %{buildroot}/*
chmod a-x examples/lock_test

%check


%files
%doc Changes README examples/
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 1.27-3
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1.27-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.27-1
- 更新到 1.27

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.21-8
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.21-7
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.21-6
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.21-5
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.21-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 1.21-3
- Perl mass rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 1.21-2
- Perl mass rebuild

* Thu Jul 14 2011 Petr Sabata <contyk@redhat.com> - 1.21-1
- 1.21 bump
- Removing now obsolete Buildroot and defattr, general cleanup
- Correcting dependencies

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.20-10
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.20-8
- 661697 rebuild for fixing problems with vendorach/lib

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.20-7
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.20-6
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.20-3
- rebuild for new perl

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.20-2.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Tue Jul 18 2006 Patrice Dumas <pertusus@free.fr> 1.20-2
- add examples/ to %%doc

* Tue Jul 18 2006 Patrice Dumas <pertusus@free.fr> 1.20-1
- Initial packaging
