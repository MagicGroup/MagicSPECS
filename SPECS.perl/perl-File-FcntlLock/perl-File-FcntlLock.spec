Name:		perl-File-FcntlLock
Version:	0.22
Release:	3%{?dist}
Summary:	Perl module for file locking with fcntl
Group:		Development/Libraries
License:	GPL+ or Artistic
URL:		http://search.cpan.org/dist/File-FcntlLock/
Source0:	http://search.cpan.org/CPAN/authors/id/J/JT/JTT/File-FcntlLock-%{version}.tar.gz
BuildRequires:	perl(POSIX), perl(Errno), perl(Carp), perl(Exporter), perl(DynaLoader)
BuildRequires:	perl(ExtUtils::MakeMaker), perl(Config)
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
FcntlLock is a module to do file locking in an object oriented
fashion using the fcntl(2) system call. This allows locks on parts
of a file as well as on the whole file and overcomes some known
problems with flock(2), on which Perl's flock() function is based.

%prep
%setup -q -n File-FcntlLock-%{version}

%build
CFLAGS="$RPM_OPT_FLAGS" %{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w %{buildroot}/*

%check


%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/File/
%{_mandir}/man3/*.3pm*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.22-3
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.22-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.22-1
- 更新到 0.22

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.12-9
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.12-8
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.12-7
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.12-6
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.12-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.12-2
- 661697 rebuild for fixing problems with vendorach/lib

* Tue Jul 13 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 0.12-1
- initial package
