#%define __debug_install_post   %{_rpmconfigdir}/find-debuginfo.sh %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}" %{nil}

Name:		sopcast
Group:		Applications/Internet
Group(zh_CN.UTF-8):   应用程序/互联网
Version:	3.2.6
Release:	2%{?dist}
License:	GPL
Summary:	A P2P Stream program
Summary(zh_CN.UTF-8): P2P流媒体程序
URL:		http://www.sopcast.org
Source0:	http://download.easetuner.com/download/sp-auth.tgz
Source1:	sp-so-auth
Autoreq:	no
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
A P2P Stream program

%description -l zh_CN.UTF-8
SoP 是 Streaming over P2P 的缩写， SopCast是一个基于 P2P 的流媒体直播系统，
其核心是由 SopCast 开发组自己定义和开发的一种通讯协议，
称之为 sop:// ，也可以称为sop 技术。我们的目的是使世界
上任何人都可以以一种非常简单的方式在Internet上建立起一个自己的个人媒体世界。

%prep
%setup -q -n sp-auth

%build

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p %{buildroot}/usr/bin
install -m 755 sp-sc-auth %{buildroot}%{_bindir}/sp-sc-auth
pushd %{buildroot}/usr/bin
ln -s sp-sc-auth sp-sc
popd
install -m 755 %{SOURCE1} %{buildroot}%{_bindir}/sp-so-auth

magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr (-,root,root)
%{_bindir}/*

%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 3.2.6-2
- 为 Magic 3.0 重建


