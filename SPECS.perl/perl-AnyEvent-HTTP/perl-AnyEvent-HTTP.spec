%global perlname AnyEvent-HTTP

Name:      perl-AnyEvent-HTTP
Version:	2.22
Release:	3%{?dist}
Summary:   Simple but non-blocking HTTP/HTTPS client  
Summary(zh_CN.UTF-8): 简单的但非阻塞式的 HTTP/HTTPS 客户端

Group:     Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License:   GPL+ or Artistic
URL:       http://search.cpan.org/dist/AnyEvent-HTTP/
Source:    http://search.cpan.org/CPAN/authors/id/M/ML/MLEHMANN/%{perlname}-%{version}.tar.gz

BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: perl
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(AnyEvent) >= 5.0

Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}


%description
This module is an AnyEvent user, you need to make sure that you use and
run a supported event loop.

This module implements a simple, stateless and non-blocking HTTP client.
It supports GET, POST and other request methods, cookies and more, all
on a very low level. It can follow redirects supports proxies and
automatically limits the number of connections to the values specified
in the RFC.

It should generally be a "good client" that is enough for most HTTP
tasks. Simple tasks should be simple, but complex tasks should still be
possible as the user retains control over request and response headers.

The caller is responsible for authentication management, cookies (if the
simplistic implementation in this module doesn't suffice), referrer and
other high-level protocol details for which this module offers only
limited support.

%description -l zh_CN.UTF-8
简单的但非阻塞式的 HTTP/HTTPS 客户端。

%prep
%setup -q -n %{perlname}-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';' -print
find %{buildroot} -type d -depth -exec rmdir {} 2>/dev/null ';' -print
%{_fixperms} %{buildroot}%{_prefix}
magic_rpm_clean.sh

%clean
rm -rf %{buildroot}


%check



%files
%defattr(-, root, root, -)
%doc Changes COPYING README
%{_mandir}/man3/Any*
%{perl_vendorlib}/AnyEvent


%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 2.22-3
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 2.22-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 2.22-1
- 更新到 2.22

* Wed Apr 22 2015 Liu Di <liudidi@gmail.com> - 2.21-1
- 更新到 2.21

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.46-9
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.46-8
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.46-7
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.46-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 14 2012 Petr Pisar <ppisar@redhat.com> - 1.46-5
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.46-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.46-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.46-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Dec 26 2010 Remi Collet <Fedora@famillecollet.com> 1.46-1
- initial spec for Extras

