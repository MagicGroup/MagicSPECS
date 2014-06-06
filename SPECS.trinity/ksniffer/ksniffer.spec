Name: ksniffer
Summary: This application is a sniffing application for KDE. It needs a lot of feature I'm working on it, but it's not yet complete but you can use it. It produces files compatible with Ethereal, WireShark, tcpdump.
Summary(zh_CN): 本程序是 KDE 下的嗅探器程序。我正致力于其拥有更多的特性，但如您所见到的那样，它还不完整。它能生成和 Ethereal、WireShark、tcpdump 兼容的文件。
Version: 0.3.2
Release: 1%{?dist}
Group: Applications/Internet
Group(zh_CN): 应用程序/互联网
License: GPL
Source: http://downloads.sourceforge.net/project/ksniffer/ksniffer/KSniffer%200.3.2/%{name}-%{version}.tar.bz2
Patch1: ksniffer-0.3.2-admin.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)
URL: http://www.ksniffer.org
Prefix: %{_prefix}
Packager: Ni Hui <shuizhuyuanluo@126.com>

%description
This application is a sniffing application for KDE. It needs a lot of feature I'm working on it, but it's not yet complete but you can use it. It produces files compatible with Ethereal, WireShark, tcpdump. The last code release is into SVN KDE in trunk/playground/network.

%description -l zh_CN
本程序是 KDE 下的嗅探器程序。我正致力于其拥有更多的特性，但如您所见到的那样，它还不完整。它能生成和 Ethereal、WireShark、tcpdump 兼容的文件。最新发布的代码在 KDE 的 SVN 的 trunk/playground/network 中。

%prep
%setup -q
%patch1 -p1
chmod 777 admin/*

%build
make -f admin/Makefile.common
%configure
#临时措施
sed -i 's/\/include\/tqt/\/include\/tqt \-lqt\-mt \-ltdecore \-ltdeui \-lDCOP \-lkio/g' ksniffer/Makefile
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
magic_rpm_clean.sh

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files
%defattr(-,root,root)
%doc AUTHORS COPYING INDEX INSTALL README TODO VERSION
%{_bindir}
%{_datadir}

%changelog
* Mon Aug 6 2007 Ni Hui <shuizhuyuanluo@126.com> - 0.3-0.1mgc
- initialize the first spec file for MagicLinux-2.1
