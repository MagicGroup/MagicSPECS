Name:           perl-Cache-FastMmap
Version:        1.40
Release:        6%{?dist}
Summary:        Uses an mmap'ed file to act as a shared memory interprocess cache
Summary(zh_CN.UTF-8): 使用 mmap 文件做为共享内存间的缓存
License:        GPL+ or Artistic
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
URL:            http://search.cpan.org/dist/Cache-FastMmap/
Source0:        http://www.cpan.org/authors/id/R/RO/ROBM/Cache-FastMmap-%{version}.tar.gz
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(GTop)
BuildRequires:  perl(Compress::Zlib)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
In multi-process environments (eg mod_perl, forking daemons, etc),
it's common to want to cache information, but have that cache shared
between processes. Many solutions already exist, and may suit your
situation better.

%description -l zh_CN.UTF-8
使用 mmap 文件做为共享内存间的缓存。

%prep
%setup -q -n Cache-FastMmap-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -type f -name '*.bs' -size 0 -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*
magic_rpm_clean.sh

%check


%files
%doc Changes README
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Cache*
%{_mandir}/man3/*

%changelog
* Fri May 08 2015 Liu Di <liudidi@gmail.com> - 1.40-6
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.40-5
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.40-4
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.40-3
- 为 Magic 3.0 重建

* Sat Jan 28 2012 Liu Di <liudidi@gmail.com> - 1.40-2
- 为 Magic 3.0 重建

* Thu Jan 05 2012 Iain Arnell <iarnell@gmail.com> 1.40-1
- update to latest upstream version

* Tue Jul 26 2011 Iain Arnell <iarnell@gmail.com> 1.39-1
- update to latest upstream
- clean up spec for modern rpmbuild
- re-enable leak test t/6.t

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.36-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.36-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Oct 02 2010 Iain Arnell <iarnell@gmail.com> 1.36-1
- update to latest upstream
- re-enable leak test

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.35-2
- Mass rebuild with perl-5.12.0

* Sat Feb 20 2010 Iain Arnell <iarnell@gmail.com> 1.35-1
- update to latest upstream version

* Fri Feb 12 2010 Iain Arnell <iarnell@gmail.com> 1.34-5
- use perl_default_filter

* Tue Dec 08 2009 Iain Arnell <iarnell@gmail.com> 1.34-4
- drop failing leak test (rt #39342)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.34-3
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.34-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jun 21 2009 Iain Arnell <iarnell@gmail.com> 1.34-1
- update to latest upstream version

* Thu May 14 2009 Iain Arnell <iarnell@gmail.com> 1.30-1
- update to latest upstream version

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.28-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Sep 15 2008 Iain Arnell <iarnell@gmail.com> 1.28-2
- BR perl(GTop) and perl(Compress::Zlib) to enable optional tests

* Sun Sep 14 2008 Iain Arnell <iarnell@gmail.com> 1.28-1
- Specfile autogenerated by cpanspec 1.77.