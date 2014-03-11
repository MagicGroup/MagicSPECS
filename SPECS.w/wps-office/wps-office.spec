%filter_requires_in /opt/kingsoft/wps-office/office6/qt/plugins/imageformats/libqtiff\.so$
%filter_setup

Name:           wps-office
Version:        8.1.0.3117+wpp
Release:        0.1.a1%{?dist}
Summary:        WPS Office

License:        Proprietary
URL:            http://linux.wps.cn/
Source0:        wps-office_8.1.0.3117+wpp~a1-0.1_i386.deb
BuildRequires:  /usr/bin/dpkg-deb
ExclusiveArch:  %ix86
Requires:	msttcorefonts

%description


%prep


%build



%install
dpkg-deb -x %{SOURCE0} $RPM_BUILD_ROOT
rm -fr $RPM_BUILD_ROOT/usr/share/desktop-directories/

%post
/usr/bin/update-mime-database %{_datadir}/mime &> /dev/null || :
/usr/bin/update-desktop-database &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
if [ -x /usr/bin/fc-cache ]; then 
    /usr/bin/fc-cache %{_datadir}/fonts/wps-office || : 
fi

%postun
/usr/bin/update-mime-database %{_datadir}/mime &> /dev/null || :
/usr/bin/update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
    if [ -x /usr/bin/fc-cache ]; then 
        /usr/bin/fc-cache %{_datadir}/fonts/wps-office || : 
    fi
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
#%{_bindir}/wps
%{_bindir}/wpp
/opt/kingsoft/
%{_datadir}/fonts/wps-office/
#%{_datadir}/applications/wps-office-wps.desktop
%{_datadir}/applications/wps-office-wpp.desktop
%{_datadir}/mime/packages/wps-office-wpp.xml
%{_datadir}/icons/hicolor/*/*/*
