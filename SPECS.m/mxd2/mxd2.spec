Summary: Magic xDSL Dialer
Summary(zh_CN): Magic xDSL 拨号器
Name: mxd2
Version: 1.0
Release: 6%{dist}
License: GPL
URL: http://ftp.magiclinux.org.cn/haulm
Group: Applications/Internet
Group(zh_CN): 应用程序/互联网
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)
#Source0:%{name}-%{ver}.tar.bz2
Source0: mxd2-%{version}.tar.gz
Source1: mxd.desktop
Source2: mxd2ctrl-%{version}.tar.gz
Prefix: %{_prefix}
Requires: rp-pppoe,ppp
Packager: haulm<haulm@126.com>, Magic Group
Autoreqprov: 0
%description
Magic xDSL Dialer.

%description -l zh_CN
Magic xDSL 拨号器

%prep

%setup -q -n mxd

%Build
qmake-qt4 -project
qmake-qt4
make
lrelease mxd_cn.ts
tar xvf %{SOURCE2}
pushd mxd2ctrl
make
popd
%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/opt/mxd
mkdir -p %{buildroot}/usr/bin/
mkdir -p %{buildroot}/etc/dbus-1/system.d/
mkdir -p %{buildroot}/usr/share/applications/
mkdir -p %{buildroot}/usr/share/polkit-1/actions/
mkdir -p %{buildroot}/usr/share/dbus-1/system-services/
install -m 755 ./mxd %{buildroot}/opt/mxd
install -m 644 ./mxd_cn.qm %{buildroot}/opt/mxd
cp %{SOURCE1} %{buildroot}/usr/share/applications/
cp -R ./images %{buildroot}/opt/mxd/
pushd mxd2ctrl
install mxd2d %{buildroot}/usr/bin/
install mxd2c %{buildroot}/usr/bin/
install -m 644 org.polkit.mxd2.policy %{buildroot}/usr/share/polkit-1/actions/org.polkit.mxd2.policy
install -m 644 org.polkit.mxd2.service %{buildroot}/usr/share/dbus-1/system-services/org.polkit.mxd2.service
install -m 644 org.polkit.mxd2.conf %{buildroot}/etc/dbus-1/system.d/org.polkit.mxd2.conf

popd
%post
if (! [ -f /etc/ppp/pppoe.conf ])
then
touch /etc/ppp/pppoe.conf
fi
if (! [ -d /etc/ppp/rp-pppoe-gui ])
then
mkdir -p /etc/ppp/rp-pppoe-gui
fi
%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}
%files
%defattr(-,root,root)
/opt/mxd
/usr/share/applications/
/etc/dbus-1/system.d/org.polkit.mxd2.conf
/usr/bin/mxd2c
/usr/bin/mxd2d
/usr/share/dbus-1/system-services/org.polkit.mxd2.service
/usr/share/polkit-1/actions/org.polkit.mxd2.policy

%changelog
* Wed Nov 11 2015 Liu Di <liudidi@gmail.com> - 1.0-6
- 为 Magic 3.0 重建

* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1.0-5
- 为 Magic 3.0 重建

* Sat Jan 03 2015 Liu Di <liudidi@gmail.com> - 1.0-4
- 为 Magic 3.0 重建

* Thu Jan 17 2013 Liu Di <liudidi@gmail.com> - 1.0-3
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 1.0-2
- 为 Magic 3.0 重建


