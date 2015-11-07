%define build_number 0.rc1

Name:      ruijieclient
Version:   1.0
Release:   %{build_number}%{?dist}.3
Summary:   a ruijie network supplicant for GNU/Linux
Summary(zh_CN.UTF-8): Linux 下的锐捷认证支持

Group:     Applications/Internet
Group(zh_CN.UTF-8): 应用程序/互联网
License:   LGPLv2+
URL:       http://code.google.com/p/ruijieclient/
Source0:   http://ruijieclient.googlecode.com/files/ruijieclient-%{version}-rc1.tar.gz
BuildRoot: %{_tmppath}/%{name}_%{version}-%{release}-root_%(%{__id_u} -n)

BuildRequires: libpcap-devel glibc-devel libxml2-devel
Requires: libpcap glibc kernel libxml2

%description
RuijieClient is a ruijie network supplicant for GNU/Linux  which is based on mystar, but re-writed form scratch.

%description -l zh_CN.UTF-8
功能更为强大的，基于MyStar的命令行界面的自由锐捷认证Linux客户端

支持静态认证和3种DHCP认证 
支持2种服务器发现包 
支持客户端版本欺骗 
支持伪造IP 
支持智能重连 
支持后台daemon驻留，可以加入Linux启动脚本 
支持服务器消息读取和转码 
良好的嵌入式移植特性 
支持2种文件配置和命令行传参配置 

%prep
%setup -q -n %{name}-%{version}-rc1

%build
#./autogen.sh
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
chmod 4755 $RPM_BUILD_ROOT/usr/bin/ruijieclient

%clean
rm -rf $RPM_BUILD_ROOT

%post
update-desktop-database %{_datadir}/applications &>/dev/null || :


%postun
update-desktop-database %{_datadir}/applications &>/dev/null || :

%files
%defattr(-,root,root,-)
%{_prefix}/bin/ruijieclient
%{_docdir}/ruijieclient/README

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.0-0.rc1.3
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.0-0.rc1.2
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 1.0-0.rc1.1
- 为 Magic 3.0 重建


* Sat Jun 13 2009 Gong Han <gong@fedoraproject.org> - 0.8-1
- Creat a spec file
