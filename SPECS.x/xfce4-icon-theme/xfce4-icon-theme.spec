Summary: 	Icons for Xfce
Summary(zh_CN):	Xfce的图标
Name: 		xfce4-icon-theme
Version: 	4.4.3
Release: 	2%{?dist}
License:	GPL
URL: 		http://www.xfce.org/
Source0: 	%{name}-%{version}.tar.bz2
Group: 		User Interface/Desktops
Group(zh_CN):	用户界面/桌面
BuildRoot: 	%{_tmppath}/%{name}-root
BuildArch:	noarch

%description
Icon theme for Xfce 4 Desktop Environment.

%description -l zh_CN
Xfce4桌面环境的图标主题。

%prep
%setup -q

%build
%configure
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT mandir=%{_mandir}
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README ChangeLog NEWS INSTALL COPYING AUTHORS
%{_datadir}/*
%{_libdir}/pkgconfig/xfce4-icon-theme-1.0.pc

%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 4.4.3-2
- 为 Magic 3.0 重建

* Thu Feb 21 2008 Liu Di <liudidi@gmail.com> - 4.4.2-1mgc
- update to 4.4.2

* Tue Jan 30 2007 Liu Di <liudidi@gmail.com> - 4.4.0-1mgc
- update to 4.4.0

* Thu Apr 20 2006 liudi <liudidi@gmail.com>
- first build
