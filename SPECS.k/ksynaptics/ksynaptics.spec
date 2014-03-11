Name:		ksynaptics
Summary:	KDE configuration for synaptics module
Summary(zh_CN.UTF-8):	配置触摸板的KDE模块
Version:	0.3.3
Release:	1%{?dist}
License:	GPL
Group:		Applications/Utilities
Group(zh_CN.UTF-8):	应用程序/工具
URL:		http://sourceforge.net/projects/qsynaptics
Source0:	http://qsynaptics.sourceforge.net/%{name}-%{version}.tar.bz2
Patch1:		ksynaptics-0.3.3-admin.patch
BuildRoot:	%_tmppath/%{name}-%{version}-%{release}-root-%(id -u -n)
BuildRequires:	kdelibs-devel, gettext, desktop-file-utils
Requires:       hicolor-icon-theme


%description
KSynaptics (previously QSynaptics) is a Qt/KDE based configuration
utility for the synaptics touchpad drivers. 

%description -l zh_CN.UTF-8
KSynaptics（以前的QSynaptics）是一个基于Qt/KDE的配置工具，用来配置
触摸板的驱动。

%prep 
%setup -q
%patch1 -p1

%build
make -f admin/Makefile.common
%configure --disable-rpath
#临时措施
sed -i 's/\/include\/tqt/\/include\/tqt \-lqt\-mt \-ltdecore \-ltdeui \-lDCOP \-lkio/g' ksynaptics/src/Makefile
make %{?_smp_flags}


%install
rm -rf $RPM_BUILD_ROOT
#%makeinstall
make DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT%{_datadir}/locale

#install -c -m 644 %{name}/%{name}.desktop %{buildroot}%{_datadir}/applications/%{name}.desktop
#desktop-file-install \
#       --vendor="" --add-category=X-Fedora \
#       --dir %{buildroot}%{_datadir}/applications/ \
#       $RPM_BUILD_ROOT/%{_datadir}/applications/%{name}.desktop

magic_rpm_clean.sh
#%find_lang %{name}

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
%defattr(-,root,root,-)
%doc AUTHORS COPYING INSTALL README TODO
%{_bindir}/syndock
%{_libdir}/trinity/kcm_ksynaptics.la
%{_libdir}/trinity/kcm_ksynaptics.so
%{_libdir}/trinity/syndock.la
%{_libdir}/trinity/syndock.so
%{_libdir}/libtdeinit_syndock.la
%{_libdir}/libtdeinit_syndock.so
%{_datadir}/applications/kde/ksynaptics.desktop
%{_datadir}/autostart/syndock.desktop
%{_datadir}/config.kcfg/kcm_ksynaptics.kcfg
%{_datadir}/icons/hicolor/128x128/apps/ksynaptics.png
%{_datadir}/icons/hicolor/128x128/apps/syndockdisabled.png
%{_datadir}/icons/hicolor/16x16/apps/ksynaptics.png
%{_datadir}/icons/hicolor/16x16/apps/syndockdisabled.png
%{_datadir}/icons/hicolor/32x32/apps/ksynaptics.png
%{_datadir}/icons/hicolor/32x32/apps/syndockdisabled.png
%{_datadir}/icons/hicolor/48x48/apps/ksynaptics.png
%{_datadir}/icons/hicolor/48x48/apps/syndockdisabled.png
%{_datadir}/icons/hicolor/64x64/apps/ksynaptics.png
%{_datadir}/icons/hicolor/64x64/apps/syndockdisabled.png


%changelog
* Wed Feb 28 2007 Liu Di <liudidi@gmail.com> - 0.3.3-1mgc
- update to 0.3.3

* Mon Oct 09 2006 Liu Di <liudidi@gmail.com> - 0.3.1-1mgc
- rebuild for Magic

* Thu Sep  7 2006 - Orion Poplawski <orion@cora.nwra.com> - 0.3.1-3
- Rebuild for FC6

* Fri Jul 28 2006 - Orion Poplawski <orion@cora.nwra.com> - 0.3.1-2
- Add icon post/postun scripts 
- Add Requires: hicolor-icon-theme
- Remove old QTDIR hack
- Cleanup desktop file

* Fri Jul 28 2006 - Orion Poplawski <orion@cora.nwra.com> - 0.3.1-1
- Update to 0.3.1

* Thu Mar  2 2006 - Orion Poplawski <orion@cora.nwra.com> - 0.3.0-1
- Update to 0.3.0

* Thu Nov  3 2005 - Orion Poplawski <orion@cora.nwra.com> - 0.2.3-1
- Initial Fedora Extras version
