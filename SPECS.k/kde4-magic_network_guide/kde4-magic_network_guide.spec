
# handle the difference between kde4 konsole and kde3 konsole parameters  --- nihui
%define kde4 1

%define real_name magic_network_guide

Summary: A wideband network setup tool.
Summary(zh_CN.UTF-8): 宽带网络设置工具
%if %kde4
Name: kde4-%{real_name}
%else
Name: %{real_name}
%endif
Version: 2.1
Release: 9%{?dist}
License: GPL
Group: Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
Source0: %{real_name}-%{version}.tar.bz2
Url: http://www.magiclinux.org
Packager: kde <athena_star at 163 dot com>
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires: ppp >= 2.4.4-6mgc rp-pppoe >= 3.8-4mgc initscripts dialog


%description
A wideband network setup tool for magic linux.

%description -l zh_CN.UTF-8
MagicLinux 的宽带网络设置向导工具，以及简繁体习惯用语互译工具。

%prep
%setup -q -n %{real_name}-%{version}

# rewrite kmng.sh script for kde4 konsole
%if %kde4
cat << EOF > tools/kmng.sh
#!/bin/bash
konsole --caption 'Magic 宽带网络设置向导' --geometry 110x32 -e /usr/sbin/magic_network_guide
EOF
%endif

%build

%install
rm -rf %{buildroot}
install -D -m755 magic_network_guide %{buildroot}%{_sbindir}/magic_network_guide
install -m755 magic_network_guide.* %{buildroot}%{_sbindir}/

pushd tools
install -D -m755 kmng.sh %{buildroot}%{_sbindir}/kmng.sh

install -D -m755 s2t.pl %{buildroot}%{_bindir}/s2t.pl
install -D -m755 t2s.pl %{buildroot}%{_bindir}/t2s.pl

install -D -m644 wizard.png %{buildroot}%{_datadir}/pixmaps/wizard.png
install -D -m600 magic_network_guide.desktop %{buildroot}%{_datadir}/applications/magic_network_guide.desktop
install -D -m600 magic_network_guide_root.desktop %{buildroot}/root/Desktop/magic_network_guide_root.desktop
popd

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files
%defattr(-,root,root)
%{_bindir}
%{_sbindir}
%{_datadir}
/root

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 2.1-9
- 为 Magic 3.0 重建

* Wed Dec 21 2011 Liu Di <liudidi@gmail.com> - 2.1-8
- 为 Magic 3.0 重建

* Tue Oct 14 2008 Liu Di <liudidi@Gmail.com> - 2.1-2mgc
- 如果设定网卡随启动激活，则开启 network 服务。

* Fri Oct 5 2007 kde <athena_star at 163 dot com> - 2.1-1mgc
- fix multi netcards probe failing bug
- jump the volume number to 2.1

* Mon Jun 18 2007 kde <athena_star at 163 dot com> - 1.2-1mgc
- update to 1.2

* Sat Jun 9 2007 kde <athena_star at 163 dot com> - 1.1-1mgc
- update to 1.1

* Sun Feb 12 2006 kde <jack@linux.net.cn> - 1.0-2mgc
- fix a bug due to netconfig in magic linux 2.0

* Sun Feb 12 2006 kde <jack@linux.net.cn> - 1.0-1mgc
- initial the spec file
