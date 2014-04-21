%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:		gnome-dvb-daemon
Version:	0.2.10
Release:	1%{?dist}
Summary:	Digital Television manager
Summary(zh_CN.UTF-8): 数字电视管理器

Group:		Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
License:	GPLv3+
URL:		http://live.gnome.org/DVBDaemon
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gnome-dvb-daemon/0.2/%{name}-%{version}.tar.xz

BuildRequires:	intltool
BuildRequires:	gstreamer-plugins-good
BuildRequires:	gstreamer-plugins-base-devel
BuildRequires:	gstreamer-plugins-bad-free
# Daemon
BuildRequires:	dbus-glib-devel pkgconfig(gee-1.0) sqlite-devel gstreamer-rtsp-devel libgudev1-devel
# UI
BuildRequires:	python-devel gstreamer-python-devel pygobject3-devel dbus-python
# Plugin
BuildRequires:	totem-devel

Requires:	hicolor-icon-theme
Requires:	pygobject3 gstreamer-python
Requires:	gstreamer-plugins-bad-free
# For initial tuning data
Requires:	dvb-apps

%description
gnome-dvb-daemon contains a daemon responsible for handling Digital Television
adapters, including recording, listing programs schedules and scanning for
channels.

This package also contains a Totem plugin for the movie player and a plugin
for sharing recordings and live TV over UPNP using Rygel.

%description -l zh_CN.UTF-8
数字电视管理器，支持录像、任务计划和扫描频道等。

%prep
%setup -q

%build
%configure --enable-totem-plugin=yes
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT/%{_datadir}/applications/*.desktop
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
%doc AUTHORS COPYING README
%{_bindir}/*
%{python_sitelib}/*
%{_datadir}/dbus-1/services/org.gnome.DVB.service
%{_datadir}/dbus-1/services/org.gnome.UPnP.MediaServer2.DVBDaemon.service
# So as not to require Totem itself
%dir %{_libdir}/totem/
%dir %{_libdir}/totem/plugins/
%{_libdir}/totem/plugins/dvb-daemon/
%{_datadir}/icons/hicolor/*/apps/*.*

%changelog
* Wed Oct 24 2012 Bastien Nocera <bnocera@redhat.com> 0.2.10-1
- Update to 0.2.10

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 07 2012 Richard Hughes <hughsient@gmail.com> - 0.2.9-1
- Update to 0.2.9

* Wed Mar 21 2012 Kalev Lember <kalevlember@gmail.com> 0.2.8-1
- Update to 0.2.8

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 12 2011 Bastien Nocera <bnocera@redhat.com> 0.2.7-1
- Update to 0.2.7

* Fri Dec 09 2011 Bastien Nocera <bnocera@redhat.com> 0.2.6-1
- Update to 0.2.6

* Wed Nov 09 2011 Adam Williamson <awilliam@redhat.com> 0.2.5-1
- adjust libgee buildrequire so it'll use the 0.6 one and fix build

* Tue Nov 01 2011 Bastien Nocera <bnocera@redhat.com>
- Update to 0.2.5

* Tue May 24 2011 Bastien Nocera <bnocera@redhat.com> 0.2.1-1
- Update to 0.2.1

* Mon May 16 2011 Bastien Nocera <bnocera@redhat.com> 0.2.0-1
- Update to 0.2.0

* Thu Apr 21 2011 Bastien Nocera <bnocera@redhat.com> 0.1.90-1
- Update to 0.1.90

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 17 2011 Bastien Nocera <bnocera@redhat.com> 0.1.23-1
- Update to 0.1.23

* Wed Oct 20 2010 Bastien Nocera <bnocera@redhat.com> 0.1.22-1
- Update to 0.1.22

* Tue Sep 07 2010 Bastien Nocera <bnocera@redhat.com> 0.1.21-1
- Update to 0.1.21

* Sat Jul 31 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.1.20-4
- Now the package is in, we re-enable the disabled bits

* Fri Jul 30 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.1.20-3
- Need to bootstrap against itself. Since totem requires this package, we
  disable the totem plugin for now. 

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.1.20-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Jun 22 2010 Bastien Nocera <bnocera@redhat.com> 0.1.20-1
- Update to 0.1.20

* Thu May 27 2010 Bastien Nocera <bnocera@redhat.com> 0.1.19-2
- Remove bizarre white spaces to be real ones

* Thu May 27 2010 Bastien Nocera <bnocera@redhat.com> 0.1.19-1
- Update to 0.1.19

* Thu May 27 2010 Bastien Nocera <bnocera@redhat.com> 0.1.18-1
- Update to 0.1.18

* Thu Mar 18 2010 Bastien Nocera <bnocera@redhat.com> 0.1.16-1
- Update to 0.1.16

* Tue Mar 09 2010 Bastien Nocera <bnocera@redhat.com> 0.1.15-1
- Update to 0.1.15

* Tue Mar 02 2010 Bastien Nocera <bnocera@redhat.com> 0.1.14-4
- Own the totem plugins directory as well

* Wed Feb 24 2010 Bastien Nocera <bnocera@redhat.com> 0.1.14-3
- Fix a few comments from the review

* Mon Feb 01 2010 Bastien Nocera <bnocera@redhat.com> 0.1.14-2
- Remove gstreamer-plugins-flumpegdemux requires

* Thu Dec 24 2009 Bastien Nocera <bnocera@redhat.com> 0.1.14-1
- Update to 0.1.14
- Add dvb-apps for initial tuning data

* Wed Dec 16 2009 Bastien Nocera <bnocera@redhat.com> 0.1.13-1
- Update to 0.1.13

* Thu Apr 30 2009 Bastien Nocera <bnocera@redhat.com> 0.1.5-1
- First package

