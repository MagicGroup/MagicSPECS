Summary: Utility to autorestart SSH tunnels
Summary(zh_CN.UTF-8): 自动重启动 SSH 隧道的工具
Name: autossh
Version: 1.4c
Release: 6%{?dist}
License: BSD
Group: Applications/Internet
Group(zh_CN.UTF-8): 应用程序/互联网
URL: http://www.harding.motd.ca/autossh/index.html
Source0: http://www.harding.motd.ca/autossh/autossh-1.4c.tgz
# Sent upstream 2011-10-30
Patch0: autossh-1.4c-ldflags.patch
BuildRequires: /usr/bin/ssh
Requires: /usr/bin/ssh
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
autossh is a utility to start and monitor an ssh tunnel. If the tunnel
dies or stops passing traffic, autossh will automatically restart it.

%description -l zh_CN.UTF-8
autossh 是一个启动和监视 ssh 隧道的工具。如果隧道断开或停止传输数据，
autossh 会自动重新启动它。

%prep

%setup -q
%patch0 -p1

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
mkdir -p examples

cp -p autossh.host rscreen examples
chmod 0644 examples/*

install -m 0755 -p autossh $RPM_BUILD_ROOT%{_bindir}
cp -p autossh.1 $RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%doc CHANGES README
%doc examples
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4c-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4c-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4c-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4c-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 14 2011 Ville Skyttä <ville.skytta@iki.fi> - 1.4c-2
- Patch build to honor $LDFLAGS.

* Sun Oct 30 2011 Alexander Boström <abo@root.snowtree.se> - 1.4c-1
- Upgrade to 1.4c

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4a-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4a-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4a-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 15 2008 Chris Ricker <kaboom@oobleck.net> 1.4a-1
- new version

* Mon Sep 11 2006 Chris Ricker <kaboom@oobleck.net> 1.3-4
- Bump and rebuild

* Tue Feb 14 2006 Chris Ricker <kaboom@oobleck.net> 1.3-3
- Bump and rebuild

* Fri Jun 03 2005 Chris Ricker <kaboom@oobleck.net> 1.3-2%{?dist}
- Add dist tag

* Fri Jun 03 2005 Chris Ricker <kaboom@oobleck.net> 1.3-2
- Changes from Ville Skyttä (use mkdir -p, remove extraneous attr)

* Tue Apr 26 2005 Chris Ricker <kaboom@oobleck.net> 1.3-1
- Initial package
