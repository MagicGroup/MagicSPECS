Summary:	Tray applet that disables touchpad automatically while you are typing text
Summary(zh_CN): 管理触摸板的面板小程序
Name:		touchfreeze
Version:	0.2.3
Release:	4%{?dist}
Group:          Applications/Utilities
Group(zh_CN.UTF-8):   应用程序/工具
License:	GPL v3
Source0:	http://qsynaptics.sourceforge.net/%{name}-%{version}.tar.gz
URL:		http://qsynaptics.sourceforge.net/
BuildRequires:	qt4-core-devel
BuildRequires:	qmake >= 4.3.3-3
Requires:	xorg-x11-drv-synaptics
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Annoyed when you are typing a document and accidentally the palm of
your hand brushes the touchpad, changing the position of the cursor in
your document or accidentally clicking on an option. TouchFreeze is
simple utility that solves this problem. It automatically disables
touchpad while you are typing text.

%description -l zh_CN
管理触摸板的面板小程序，是 ksynapatics 的替代品。

%prep
%setup -q
sed -i '$a\LIBS+=-lX11' TouchFreeze.pro

%build
qmake4
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}
install touchfreeze $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS README
%attr(755,root,root) %{_bindir}/touchfreeze

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 0.2.3-4
- 为 Magic 3.0 重建

* Sun Oct 04 2015 Liu Di <liudidi@gmail.com> - 0.2.3-3
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 0.2.3-2
- 为 Magic 3.0 重建

