%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(0)")}

Name:       blueman
Version:    1.23
Release:    2%{?dist}
Summary:    GTK+ Bluetooth Manager
Summary(zh_CN): GTK+ 的蓝开管理器

Group:      Applications/System
Group(zh_CN):	应用程序/系统
License:    GPLv3+
URL:        http://blueman-project.org/
Source0:    http://download.tuxfamily.org/%{name}/%{name}-%{version}.tar.gz

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:  gtk2-devel >= 2.12
BuildRequires:  pygtk2-devel >= 2.12
BuildRequires:  Pyrex >= 0.9.8.0
BuildRequires:  startup-notification-devel >= 0.9
BuildRequires:  pygobject2-devel >= 2.12
BuildRequires:  bluez-libs-devel >= 4.21
BuildRequires:  intltool >= 0.35.0
BuildRequires:  dbus-python
BuildRequires:  python-devel >= 2.5
BuildRequires:  desktop-file-utils
BuildRequires:  libtool
BuildRequires:  notify-python
Requires: python >= 2.5
Requires: bluez >= 4.25
Requires: obex-data-server >= 0.4.3
Requires: pygtk2 >= 2.12
Requires: dbus
Requires: notify-python
Requires: notification-daemon
Provides: dbus-bluez-pin-helper

#Detect pygtk correctly. https://bugs.edge.launchpad.net/blueman/+bug/337877
#Patch0:  blueman-build-pygtk.patch


%description
Blueman is a tool to use Bluetooth devices.

%description -l zh_CN
管理蓝牙设备的工具

%prep
%setup -q


%build
#autoreconf -f -i

%configure --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{python_sitearch}/*.la
rm -f %{buildroot}%{_libdir}/nautilus-sendto/plugins/libnstblueman.la
mkdir -p $RPM_BUILD_ROOT%{_datadir}/gnome/
mv $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart/ $RPM_BUILD_ROOT%{_datadir}/gnome/

desktop-file-install --vendor=""     \
 --delete-original     \
 --dir=$RPM_BUILD_ROOT%{_datadir}/applications  \
 $RPM_BUILD_ROOT%{_datadir}/applications/blueman-manager.desktop


magic_rpm_clean.sh
%find_lang %{name}


%clean
rm -rf $RPM_BUILD_ROOT

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING
%{_bindir}/*
%{python_sitelib}/blueman
%{python_sitearch}/*.so
%{_libexecdir}/blueman-mechanism
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.blueman.Mechanism.conf
%{_datadir}/gnome/autostart/blueman.desktop
%{_datadir}/applications/blueman-manager.desktop
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/%{name}/
%{_datadir}/dbus-1/services/blueman-applet.service
%{_datadir}/dbus-1/system-services/org.blueman.Mechanism.service
%{_mandir}/man1/*
#预备分包
%{_libdir}/nautilus-sendto/plugins/libnstblueman.so
%{_datadir}/polkit-1/actions/org.blueman.policy

%changelog
* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 1.23-2
- 为 Magic 3.0 重建

* Thu Nov 03 2011 Liu Di <liudidi@gmail.com> - 1.23-1
- 更新到 1.23
