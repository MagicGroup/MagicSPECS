Summary: 	Time-managing application for xfce4.
Summary(zh_CN):	Xfce4的时间管理程序
Name: 		orage
Version: 	4.8.4
Release: 	1%{?dist}
License:	GPL
URL: 		http://www.xfce.org/
Source0: 	http://archive.xfce.org/src/apps/orage/%{name}-%{version}.tar.bz2
Group: 		User Interface/Desktops
Group(zh_CN):	用户界面/桌面
BuildRoot: 	%{_tmppath}/%{name}-root
BuildRequires:	xfce4-panel-devel
Requires:	xfce4-panel

%description
Time-managing application for xfce4

%description -l zh_CN
xfce4的时间管理程序

%prep
%setup -q

%build
%configure --enable-final
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT mandir=%{_mandir}
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%postun
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%files
%defattr(-,root,root)
%doc README ChangeLog INSTALL COPYING AUTHORS
%{_bindir}/
%{_datadir}/
/usr/libexec/xfce4/panel-plugins/xfce4-orageclock-plugin

%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 4.8.3-2
- 为 Magic 3.0 重建

* Thu Feb 21 2008 Liu Di <liudidi@gmail.com> - 4.4.2-1mgc
- update to 4.4.2

* Tue Jan 30 2007 Liu Di <liudidi@gmail.com> - 4.4.0-1mgc
- update to 4.4.0
