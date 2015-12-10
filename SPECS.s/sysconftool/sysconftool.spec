Summary:	Macros for aclocal to install configuration files
Summary(zh_CN.UTF-8): 安装配置文件的 aclocal 宏
Name:		sysconftool
Version:	0.17
Release:	4%{?dist}
License:	GPLv3 with exceptions
Source0:	http://downloads.sourceforge.net/project/courier/sysconftool/%{version}/%{name}-%{version}.tar.bz2
URL:		http://www.courier-mta.org/sysconftool/
BuildArch:	noarch
BuildRequires:	autoconf
BuildRequires:	automake

%description
sysconftool is a development utility that helps to install application
configuration files. sysconftool allows an existing application to be
upgraded without losing the older version's configuration settings.

%description -l zh_CN.UTF-8
安装配置文件的 aclocal 宏。

%prep
%setup -q

%build
autoreconf
%configure

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

# make the symlinks relative
ln -sf ../share/sysconftool/sysconftoolcheck $RPM_BUILD_ROOT%{_bindir}/
ln -sf ../share/sysconftool/sysconftoolize.pl $RPM_BUILD_ROOT%{_bindir}/sysconftoolize
magic_rpm_clean.sh

%check
make check

%files
%doc AUTHORS ChangeLog COPYING *.html NEWS
%{_bindir}/sysconftoolcheck
%{_bindir}/sysconftoolize
%{_datadir}/sysconftool
%{_mandir}/man1/sysconftool.1*
%{_mandir}/man1/sysconftoolcheck.1*
%{_mandir}/man7/sysconftool.7*
%{_datadir}/aclocal/sysconftool.m4

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 0.17-4
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 0.17-3
- 为 Magic 3.0 重建

* Tue Sep 29 2015 Liu Di <liudidi@gmail.com> - 0.17-2
- 为 Magic 3.0 重建

* Sun Oct 13 2013 Dominik Mierzejewski <rpm@greysector.net> 0.17-1
- updated to 0.17
- drop obsolete spec constructs and unnecessary macros
- clean up file list
- include HTML docs

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 0.16-5
- Perl 5.18 rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jul 18 2011 Dominik Mierzejewski <rpm@greysector.net> 0.16-1
- updated to 0.16
- license changed to GPLv3 with OpenSSL exception

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat May 08 2010 Dominik Mierzejewski <rpm@greysector.net> 0.15-7
- fix source URL

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Sep  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.15-4
- fix license tag

* Mon Sep 18 2006 Dominik Mierzejewski <rpm@greysector.net> 0.15-3
- mass rebuild
- simplify autotools invocation

* Sun Jul 30 2006 Dominik Mierzejewski <rpm@greysector.net> 0.15-2
- bump the release to fix tag and build

* Sun Jan 08 2006 Dominik Mierzejewski <rpm@greysector.net> 0.15-1
- FE compliance
- updated to 0.15

* Sat Jun 18 2005 Dominik Mierzejewski <rpm@greysector.net> 0.14-1
- adapted for Fedora Core from PLD spec
