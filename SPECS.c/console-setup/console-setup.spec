
Name:		console-setup
Version:	1.107
Release:	2%{?dist}
Summary:	Tools for configuring the console using X Window System key maps
Summary(zh_CN.UTF-8): 使用 X 窗口系统的键盘映射配置控制台的工具

Group:		Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
# For a breakdown of the licensing, see COPYRIGHT, copyright, copyright.fonts and copyright.xkb
License:	GPLv2+ and MIT and Public Domain
URL:		http://packages.debian.org/cs/sid/console-setup
Source0:	http://ftp.de.debian.org/debian/pool/main/c/%{name}/%{name}_%{version}.tar.xz

# Fixes installing paths to Fedora style
Patch0:		console-setup-1.76-paths.patch
# Fixes FSF address, sent to upstream
Patch1:		console-setup-1.76-fsf-address.patch

Requires:	kbd
# require 'xkeyboard-config' to have X Window keyboard descriptions?

BuildArch:	noarch

%description
This package provides the console with the same keyboard configuration
scheme that X Window System has. Besides the keyboard, the package configures
also the font on the console.  It includes a rich collection of fonts and
supports several languages that would be otherwise unsupported on the console
(such as Armenian, Georgian, Lao and Thai).

%description -l zh_CN.UTF-8
这个包提供了让控制台和 X 窗口系统使用一样的键盘配置方案的功能。除了键盘，还可以
配置控制台的字体。


%prep
%setup -q
%patch0 -p1 -b .paths
%patch1 -p1 -b .fsf-address


%build
make build-linux


%install
rm -rf $RPM_BUILD_ROOT
make prefix=$RPM_BUILD_ROOT install-linux
# we don't want another set of keyboard descriptions, we want to use descriptions from
# xkeyboard-config (require it?), so removing it
# or maybe have these from tarball it in optional subpackage?
rm -rf $RPM_BUILD_ROOT/etc/console-setup
magic_rpm_clean.sh

%files
%doc README COPYRIGHT CHANGES copyright.fonts copyright.xkb Fonts/copyright
%{_bindir}/ckbcomp
%{_bindir}/setupcon
%config(noreplace) %{_sysconfdir}/default/console-setup
%config(noreplace) %{_sysconfdir}/default/keyboard
%{_datadir}/consolefonts
%{_datadir}/consoletrans
%{_mandir}/*/*


%changelog
* Wed Apr 23 2014 Liu Di <liudidi@gmail.com> - 1.107-2
- 为 Magic 3.0 重建

* Thu Apr 10 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.107-1
- Update to latest upstream version
  Resolves: #1084949

* Thu Mar 20 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.106-1
- Update to latest upstream version
  Resolves: #1078695

* Thu Jan 02 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.104-1
- Update to latest upstream version
  Resolves: #1040384

* Wed Nov 06 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.102-1
- Update to latest upstream version
  Resolves: #1026672
- Fix bogus date in %%changelog

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.87-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.87-3
- Perl 5.18 rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.87-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 29 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.87-1
- Update to latest upstream version

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.80-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 04 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.80-1
- Update to latest upstream version
- Fix files listed twice build warning

* Tue Jun 26 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.76-2
- Fix License field
- Do not own /etc/default directory
- Fix FSF address in ckbcomp utility
- Fix paths in manpages

* Wed Jun 20 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.76-1
- Initial support
