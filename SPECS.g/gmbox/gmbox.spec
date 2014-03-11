%define betatag beta
Name:		gmbox	
Group:		Applications/Internet
Group(zh_CN.UTF-8):   应用程序/互联网
Version:	0.4
%if %{betatag}
Release:	0.%{betatag}.1%{?dist}.1
%else
Release:	1{?dist}
%endif
License:	GPL
Summary:	Google music box 
Summary(zh_CN.UTF-8): google音乐下载器
URL:		http://code.google.com/p/gmbox/
Source0:	http://gmbox.googlecode.com/files/%{name}-gtk-%{version}%{?betatag}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-root

BuildArch:	noarch
Requires:	pygtk2

%description
Google music box

%description -l zh_CN.UTF-8
google音乐下载器，基本特性是: 

支持谷歌音乐的"榜单下载"和"搜索下载",而且,这两者都包含歌曲和专辑. 
简单的可配置性 
linux系统可以调用mid3iconv自动修改歌曲的ID3信息编码 
跨平台性,使用python做为核心,可以运行于大部分linux和windows操作系统,理论上mac也可以,没条件测试 
界面和核心分离,默认有一个使用pygtk的界面,也可以使用命令行方式操作 

%prep
%if %{betatag}
%setup -q -n %{name}-gtk
%else
%setup -q -n %name
%endif

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/gmbox
install -d %{buildroot}%{_datadir}/applications
cp -rv . %{buildroot}%{_datadir}/gmbox
install -m 0644 debian/gmbox.desktop %{buildroot}/usr/share/applications
ln -sf %{_datadir}/gmbox/gmbox-gtk.py %{buildroot}%{_bindir}/gmbox

magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-,root,root)
%{_bindir}/*
%{_datadir}/*

%changelog
* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 0.4-0.beta.1.1
- 为 Magic 3.0 重建

* Fri Dec 02 2011 Liu Di <liudidi@gmail.com> - 0.4-0.beta.1
- 更新到 0.4 beta
