Name:           perl-Cache-Memcached
Version:	1.30
Release:	1%{?dist}
Summary:        Perl client for memcached
Summary(zh_CN.UTF-8): memcached 的 Perl 客户端

Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Cache-Memcached/
Source0:        http://search.cpan.org/CPAN/authors/id/D/DO/DORMANDO/Cache-Memcached-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker) perl(Storable) perl(Time::HiRes) perl(String::CRC32) perl(Test::More)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Cache::Memcached - client library for memcached (memory cache daemon)

%description -l zh_CN.UTF-8
memcached 的 Perl 客户端。

%prep
%setup -q -n Cache-Memcached-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w %{buildroot}/*
magic_rpm_clean.sh

#%check
# This requires a running memcached on the local host, which isn't very
# convenient or suitable. YMMV. BR's are there if we REALLY want this.
#


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc README ChangeLog
%dir %{perl_vendorlib}/Cache/
%dir %{perl_vendorlib}/Cache/Memcached/
%{perl_vendorlib}/Cache/Memcached.pm
%{perl_vendorlib}/Cache/Memcached/GetParser.pm
%{_mandir}/man3/Cache::Memcached.3*


%changelog
* Fri May 08 2015 Liu Di <liudidi@gmail.com> - 1.30-1
- 更新到 1.30

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.29-14
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.29-13
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.29-12
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.29-11
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.29-10
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.29-9
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.29-8
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.29-7
- 为 Magic 3.0 重建

* Sat Jan 28 2012 Liu Di <liudidi@gmail.com> - 1.29-6
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.29-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jun 19 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.29-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.29-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.29-2
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Aug 27 2010 Michael Fleming <mfleming+rpm@thatfleminggent.com> - 1.29-1
- New upstream release (makes local sockets users happy)

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.28-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.28-2
- rebuild against perl 5.10.1

* Mon Nov  2 2009 Stepan Kasal <skasal@redhat.com> - 1.28-1
- new upstream version

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.26-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 9 2009 Michael Fleming <mfleming+rpm@thatfleminggent.com> - 1.2.6-3
- More cleanups
- Change license

* Sat Jun 6 2009 Michael Fleming <mfleming+rpm@thatfleminggent.com> - 1.2.6-2
- Cleaned up for Fedora review

* Sat Jun 6 2009 Michael Fleming <mfleming+rpm@thatfleminggent.com> - 1.2.6-1.mf
- Initial Revision
