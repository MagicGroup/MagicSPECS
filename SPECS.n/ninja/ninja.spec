Name: ninja
Version: 1.5.8.1
Release: 18
License: GPLv2+
Summary: Text based Internet Relay Chat (IRC) client
Summary(zh_CN.UTF-8): 文本界面的 IRC 客户端
Group: Applications/Internet
Group(zh_CN.UTF-8): 应用程序/互联网
URL: http://qoop.org/ftp/ninja/
Source0: http://qoop.org/ftp/ninja/sources/%{name}-%{version}.tar.gz
Patch0: %{name}-%{version}-doc.patch
Patch1: %{name}-%{version}-build.patch
Patch2: ninja.signal-11-718920.patch
BuildRequires: ncurses-devel

%description
Ninja IRC is yet another ircII-based IRC client. Its many extra features
include enhanced socket handling, additional resolving capabilities,
ANSI and MIRC color support, MIRC-style DCC RESUME, cloak mode, a friend
list, an enemy list, SOCKS v4&5 proxy support, more ircii $func()
functions, auto-rejoin, cycling auto-reconnect, auto-dcc get, improved
ban/unban handling, cached information, NDCC file offering, and much
more.

Install Ninja IRC if you want to participate (troll, lurk, hang out) in
irc channels.  Especially if you want to have power features.

%description -l zh_CN.UTF-8
文本界面的 IRC 客户端。

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%configure
make

%install
rm -rf %{buildroot}
%makeinstall

ln -sf %{name}-%{version} %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_mandir}/man1/
mv %{buildroot}%{_mandir}/ninja.* %{buildroot}%{_mandir}/man1/
rm %{buildroot}/%{_datadir}/%{name}/help/.date
magic_rpm_clean.sh

%files
%defattr(-,root,root, 755)
%{_bindir}/%{name}
%{_bindir}/%{name}-%{version}
%{_bindir}/%{name}io
%{_bindir}/%{name}flush
%{_bindir}/%{name}wserv
%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/script
%{_datadir}/%{name}/translation
%{_datadir}/%{name}/help
%{_mandir}/man1/*
%defattr(644,root,root, 755)
%doc README ChangeLog BUGS+TODO COPYING

%changelog
* Sun Sep 20 2015 Liu Di <liudidi@gmail.com> - 1.5.8.1-18
- 为 Magic 3.0 重建

* Mon Feb 16 2015 Liu Di <liudidi@gmail.com> - 1.5.8.1-17
- 为 Magic 3.0 重建

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.8.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.8.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.8.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Mar 28 2012 Adrian Reber <adrian@lisas.de> - 1.5.8.1-13
- fixed "Process /usr/bin/ninja-1.5.8.1 was killed by signal 11" (#718920)
- removed buildroot and clean section

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.8.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.8.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.8.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.8.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 14 2008 Adrian Reber <adrian@lisas.de> - 1.5.8.1-8
- rebuilt for gcc43
- license is probably GPLv2+
- made rpmlint happy
- added patch to actually build again

* Wed Aug 22 2007 Adrian Reber <adrian@lisas.de> - 1.5.8.1-7
- fix URLs (#251285)

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 1.5.8.1-6
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Sat Sep 16 2006 Adrian Reber <adrian@lisas.de> - 1.5.8.1-5
- rebuilt

* Sun Mar 12 2006 Adrian Reber <adrian@lisas.de> - 1.5.8.1-4
- rebuilt

* Fri Apr  1 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.5.8.1-3
- Include ninja directory in datadir.

* Tue Feb 25 2003 Adrian Reber <adrian@lisas.de> - 1.5.8.1-0.fdr.1
- applied fedora naming conventions

* Mon Sep 23 2002 Vladimir Furtado Krachinski <vladimir@conectiva.com.br>
+ 2002-09-23 15:33:37 (15665)
- Changed %%doc permissions

* Fri Sep 20 2002 Vladimir Furtado Krachinski <vladimir@conectiva.com.br>
+ 2002-09-20 14:50:25 (15574)
- First Build for Conectiva Linux
- Added documentation patch

* Fri Sep 20 2002 Vladimir Furtado Krachinski <vladimir@conectiva.com.br>
+ 2002-09-20 14:39:39 (15573)
- Created snapshot directory for ninja.
