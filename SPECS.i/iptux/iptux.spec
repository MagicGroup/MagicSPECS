Name:           iptux
Version:        0.5.1
Release: 	3%{?dist}
Source0:        %{name}-%{version}-2.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  gtk2-devel
Group:          Applications/Internet
Group(zh_CN.UTF-8):   应用程序/互联网
License:        GPLv2a+
URL:	  	http://iptux.googlecode.com/
Summary:        A GUI for ipmessage
Summary(zh_CN.UTF-8): 飞鸽传书的 Linux 图形界面版本

%description
A GUI for ipmessage

%description -l zh_CN.UTF-8
飞鸽传书的 Linux 图形界面版本

%prep
%setup -q -n %{name}-%{version}

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

%clean
rm -rf "$RPM_BUILD_ROOT"

%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/*

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.5.1-3
- 为 Magic 3.0 重建

* Tue Dec 13 2011 Liu Di <liudidi@gmail.com> - 0.5.1-2
- 为 Magic 3.0 重建

* Wed Jul 03 2009 Liu Di <liudidi@gmail.com> - 0.4.6-0.svn20090603
- 更新到 svn 20090603

* Mon Oct 27 2008 Liu Di <liudidi@gmail.com> - 0.3.2-1mgc
- 更新到 0.3.2

* Mon Oct 13 2008 Liu Di <liudidi@gmail.com> - 0.3-1mgc
- 首次打包
