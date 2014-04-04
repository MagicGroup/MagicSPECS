Name:		fcitx-table-other
Version:	0.2.2
Release:	1%{?dist}
Summary:	Other tables for Fcitx
Summary(zh_CN.UTF-8): Fcitx 的其它码表
Group:		System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:	GPLv3+
URL:		https://fcitx-im.org/wiki/Fcitx
Source0:	http://download.fcitx-im.org/fcitx-table-other/%{name}-%{version}.tar.xz

BuildRequires:	cmake, fcitx-devel, gettext, intltool, libtool, fcitx
BuildArch:	noarch
Requires:	fcitx

%description
Fcitx-table-other is a fork of ibus-table-others for Fcitx,
provides additional tables.

%description -l zh_CN.UTF-8
这是 ibus-table-others 的移植，提供了一些附加码表。

%prep
%setup -q -n %{name}-%{version}


%build
mkdir -pv build
pushd build
%cmake ..
make VERBOSE=1

%install
rm -rf $RPM_BUILD_ROOT
pushd build
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
popd
magic_rpm_clean.sh
%find_lang %{name} 

%clean
rm -rf %{buildroot}

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING README
%{_datadir}/fcitx/table/*.mb
%{_datadir}/fcitx/table/*.conf
%{_datadir}/fcitx/imicon/*.png
%{_datadir}/icons/hicolor/64x64/apps/*.png
%{_datadir}/icons/hicolor/48x48/apps/*.png
%{_datadir}/icons/hicolor/32x32/apps/*.png


%changelog
* Fri Aug 23 2013 Robin Lee <cheeselee@fedoraproject.org> - 0.2.2-1
- Update to 0.2.2
- Don't run make with -j, there is race condition for this package
- Update URL and Source0 URL

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Dec 09 2012 Liang Suilong <liangsuilong@gmail.com> - 0.2.1-1
- Upstream to fcitx-table-other-0.2.1

* Sun May 13 2012 Liang Suilong <liangsuilong@gmail.com> - 0.1.0-1
- Initial Release
