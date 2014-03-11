Summary: X client for remote desktop into Windows Terminal Server
Summary(zh_CN.UTF-8): 在 X 中显示 Windows 终端服务器桌面
Name: rdesktop
Version: 1.7.1
Release: 2%{?dist}
License: GPL
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
URL: http://www.rdesktop.org/

Packager: Liu Di <liudidi@gmail.com>
Vendor: MagicLinux

Source: http://dl.sf.net/rdesktop/rdesktop-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: openssl-devel, libX11-devel

%description
rdesktop is an open source client for Windows NT Terminal Server and
Windows 2000 & 2003 Terminal Services, capable of natively speaking 
Remote Desktop Protocol (RDP) in order to present the user's NT
desktop. Unlike Citrix ICA, no server extensions are required.

%description -l zh_CN.UTF-8
rdesktop 是 Windows NT 终端服务器和 Windows 2000 终端服务器的开源客户。
它能够使用本地机器语言的远程桌面协议 (RDP) 来显示用户的 NT 桌面。与 
Citrix ICA 不同，它不要求任何服务器扩展。

%prep
%setup

%build
%configure
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}"

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc COPYING doc/*.txt doc/AUTHORS doc/ChangeLog doc/HACKING doc/TODO README
%doc %{_mandir}/man1/rdesktop.1*
%{_bindir}/rdesktop
%{_datadir}/rdesktop/

%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 1.7.1-2
- 为 Magic 3.0 重建

* Sun Feb 05 2006 liudi <liudidi@gmail.com>
- Build for Magiclinux 2.0 rc3
* Fri May 27 2005 Dag Wieers <dag@wieers.com> - 1.4.1-0 - 3663/dries
- Initial package. (using DAR)
