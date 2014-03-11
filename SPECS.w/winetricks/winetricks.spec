%define date 20110629

Name: winetricks
Summary: Quick script to install redistributable runtime libraries
Summary(zh_CN.UTF-8): 快速安装可分发运行库的脚本
Version: 0.0.1
Release: 0.%{date}.1%{?dist}.1
License: GPLv2
URL: http://code.google.com/p/winezeug/
Group: Applications/Emulators
Group(zh_CN.UTF-8): 应用程序/模拟器
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: http://www.kegel.com/wine/%{name}
Source1: %{name}.desktop

Requires: wine

BuildArch: noarch

%description
winetricks is a quick and dirty script to download and
install various redistributable runtime libraries
sometimes needed to run programs in Wine.

%description -l zh_CN.UTF-8
winetricks 是个快速下载并安装那些 Wine 程序所需的可分发运行库的脚本。

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/applications
install -m 0755 %{SOURCE0} %{buildroot}%{_bindir}/%{name}
install -m 0644 %{SOURCE1} %{buildroot}%{_datadir}/applications/%{name}.desktop

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop

%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 0.0.1-0.20110629.1.1
- 为 Magic 3.0 重建

* Mon Apr 26 2010 Ni Hui <shuizhuyuanluo@126.com> - 0.0.1-0.20100424.1mgc
- initial rpm package
