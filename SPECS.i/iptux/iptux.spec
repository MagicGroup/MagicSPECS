Name:           iptux
Version:	0.6.3
Release: 	5%{?dist}
Source0:        https://github.com/iptux-src/iptux/archive/v%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  gtk2-devel
Group:          Applications/Internet
Group(zh_CN.UTF-8):   应用程序/互联网
License:        GPLv2a+
URL:	  	https://github.com/iptux-src/iptux/
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
make install DESTDIR=%{buildroot}

%clean
rm -rf "$RPM_BUILD_ROOT"

%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/*

%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 0.6.3-5
- 为 Magic 3.0 重建

* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 0.6.3-4
- 更新到 0.6.3

* Fri Apr 18 2014 Liu Di <liudidi@gmail.com> - 0.6.2-3
- 更新到 0.6.2

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
