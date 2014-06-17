Name:           perl-Net-Server
Version:        2.006
Release:        2%{?dist}
Summary:        Extensible, general Perl server engine
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Net-Server/
Source0:        http://www.cpan.org/modules/by-module/Net/Net-Server-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Socket)
Requires:       perl(Socket)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
# IO::Multiplex support is optional, but since it's in Fedora and not
# including it causes build problems in some packages…
Requires: perl(IO::Multiplex)

%description
An extensible, class oriented module written in perl and intended to
be the back end layer of internet protocol servers.

%prep
%setup -q -n Net-Server-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}
# Do not want to pull in any packaging deps here.
chmod 644 examples/*

%install
rm -rf $RPM_BUILD_ROOT

make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes README examples
%{perl_vendorlib}/*
%{_mandir}/man3/*
%{_bindir}/net-server
%{_mandir}/man1/net-server.1*

%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.006-2
- 为 Magic 3.0 重建

* Sat Aug 25 2012 Kevin Fenzi <kevin@scrye.com> 2.006-1
- Update to 2.006 upstream release
- Redo spec with current guidelines. 

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.97-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 0.97-14
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.97-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.97-12
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.97-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.97-10
- 661697 rebuild for fixing problems with vendorach/lib

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.97-9
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.97-8
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.97-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.97-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jul 11 2008 <nicolas.mailhot at laposte.net>
- 0.97-5
⌖ Fedora 10 alpha general package cleanup

* Mon Jun 02 2008 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 0.97-3
⋰ remove old %%check Dag leftover rpmbuild does not like anymore

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com>
- 0.97-2
Rebuild for new perl

* Sun Aug 12 2007 Nicolas Mailhot <nicolas.mailhot at laposte.net>
⍟ 0.97-1

* Fri May 18 2007 Nicolas Mailhot <nicolas.mailhot at laposte.net>
⍟ 0.96-2
- more build checks
⍟ 0.96-1
- trim changelog

* Tue Mar 20 2007 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 0.95-1 

* Sat Sep 02 2006 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 0.94-2
- FE6 Rebuild

* Sun Jul 30 2006 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 0.94-1

* Sun Apr 23 2006 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 0.93-1

* Mon Feb 13 2006 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 0.90-2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Sun Jan 8 2006 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 0.90-1
- Updated to 0.90
- add IO::Multiplex dep
