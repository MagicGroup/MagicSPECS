Summary: Webtray for websoft
Name: webtray
Version: 0.1
Release: 1%{dist}
License: GPL
URL: http://ftp.magiclinux.org.cn/haulm
Group: Applications/Internet
Group(zh_CN): 应用程序/互联网
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)
Source0: %{name}-%{version}.tar.gz
Source1: web_url.tar.gz
Source2: web_icon.tar.gz
Prefix: %{_prefix}
Requires: qt4-webkit
Packager: haulm<haulm@126.com>, Magic Group
Autoreqprov: 0
%description
 Webtray, The web tray program.

%description -l zh_CN
Magic 网页托盘管理程序

%prep

%setup -q -n webtray

%Build
qmake-qt4
make
lrelease webtray_cn.ts
%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/opt/webtray
mkdir -p %{buildroot}/usr/bin/
mkdir -p %{buildroot}/usr/share/applications/
install -m 755 ./webtray %{buildroot}/opt/webtray
install -m 644 ./webtray_cn.qm %{buildroot}/opt/webtray
tar xvf %{SOURCE1} -C %{buildroot}/usr/share/applications/
tar xvf %{SOURCE2} -C %{buildroot}/opt/webtray/
cp webtray.png %{buildroot}/opt/webtray/
ln -s /opt/webtray/webtray %{buildroot}/usr/bin/webtray
%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}
%files
%defattr(-,root,root)
/opt/webtray
/usr/share/applications/
/usr/bin
%changelog

