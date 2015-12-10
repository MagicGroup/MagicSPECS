# $Id: perl-CDDB_get.spec 3902 2006-01-08 10:48:15Z dries $
# Authority: dries
# Upstream: Armin Obersteiner <armin$xos,net>

%define perl_vendorlib %(eval "`perl -V:installvendorlib`"; echo $installvendorlib)
%define perl_vendorarch %(eval "`perl -V:installvendorarch`"; echo $installvendorarch)

%define real_name CDDB_get

Summary: Reads the CDDB entry for an audio CD in your drive
Summary(zh_CN): 读取您驱动器中音频 CD 的 CDDB 条目
Name: perl-CDDB_get
Version:	2.28
Release:	3%{?dist}
License: Artistic/GPL
Group: Applications/CPAN
Group(zh_CN): 应用程序/CPAN
URL: http://search.cpan.org/dist/CDDB_get/

Source: http://search.cpan.org/CPAN/authors/id/F/FO/FONKIE/CDDB_get-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildArch: noarch
BuildRequires: perl

%description
This module/script gets the CDDB info for an audio cd. You need
LINUX, SUNOS or *BSD, a cdrom drive and an active internet connection
in order to do that.

%description -l zh_CN
此模块/脚本用于从音频 cd 中获取 CDDB 信息。您需要 LINUX、SUNOS 或 *BSD，
一个 cdrom 驱动器以及活动的互联网连接。

%prep
%setup -n %{real_name}-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS="vendor" PREFIX="%{buildroot}%{_prefix}"
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%makeinstall
%{__rm} -rf %{buildroot}%{perl_archlib} %{buildroot}%{perl_vendorarch}

%clean
%{__rm} -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files
%defattr(-, root, root, 0755)
%doc Changes README
%doc %{_mandir}/man3/*
%{_bindir}/cddb.pl
%{perl_vendorlib}/CDDB_get.pm
%{perl_vendorlib}/auto/CDDB_get/
%{perl_vendorlib}/auto/CDDB_cache/
%{perl_vendorlib}/cddb.pl
%{perl_vendorlib}/CDDB_cache.pm

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 2.28-3
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 2.28-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 2.28-1
- 更新到 2.28

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.27-4
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 2.27-3
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 2.27-2
- 为 Magic 3.0 重建

* Sun Oct 14 2007 Ni Hui <shuizhuyuanluo@126.com> - 2.27-0.1mgc
- rebuild for Magic Linux-2.1

* Sat Jan  7 2006 Dries Verachtert <dries@ulyssis.org> - 2.27-1 - 3902/dries
- Updated to release 2.27.

* Sat Nov  5 2005 Dries Verachtert <dries@ulyssis.org> - 2.25-1
- Updated to release 2.25.

* Sat Apr  9 2005 Dries Verachtert <dries@ulyssis.org> - 2.23-1
- Initial package.
