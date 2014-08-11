Name:		mate-icon-theme
Version:	1.4.0
Release:	7%{?dist}
Summary:	Icon theme for MATE Desktop
Summary(zh_CN.UTF-8): MATE 桌面的图标主题
License:	GPLv2+ and LGPLv2+
URL:		http://mate-desktop.org
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source0:	http://pub.mate-desktop.org/releases/%{majorver}/%{name}-%{version}.tar.xz

BuildArch:	noarch

BuildRequires:	mate-common icon-naming-utils

Provides: mate-icon-theme = %{version}-%{release}
Obsoletes: mate-icon-theme-legacy < %{version}-%{release}

%description
Icon theme for MATE Desktop

%description -l zh_CN.UTF-8
MATE 桌面的图标主题。

%package devel
Summary: Development files for mate-icon-theme
Summary(zh_CN.UTF-8): %{name} 的开发包

%description devel
Development files for mate-icon-theme

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q
NOCONFIGURE=1 ./autogen.sh

%build
%configure  --enable-icon-mapping --disable-static
make %{?_smp_mflags} V=1


%install
make install DESTDIR=%{buildroot}
magic_rpm_clean.sh

%post
/usr/bin/touch --no-create %{_datadir}/icons/mate &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /usr/bin/touch --no-create %{_datadir}/icons/mate &>/dev/null
    /usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/mate &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/mate &>/dev/null || :

%files
%doc AUTHORS COPYING README
%{_datadir}/icons/mate/

%files devel
%{_datadir}/pkgconfig/mate-icon-theme.pc


%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.4.0-7
- 为 Magic 3.0 重建

* Mon Aug 13 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.4.0-6
- add obsolete mate-icon-theme-legacy
- bump version to 1.4.0-6 for updating external repo

* Sun Aug 12 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-3
- Make the scriptlets reference mate instead of hicolor

* Sun Aug 12 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-2
- Add macros for icon cache, move autogen to prep section

* Fri Aug 10 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-1
- Initial release
