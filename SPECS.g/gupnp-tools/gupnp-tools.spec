Name:          gupnp-tools
Version:       0.8.9
Release:       2%{?dist}
Summary:       A collection of dev tools utilising GUPnP and GTK+
Summary(zh_CN.UTF-8): GUPnP 和 GTK+ 的开发工具集

Group:         System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:       GPLv2+
URL:           http://www.gupnp.org/
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source0:       http://ftp.gnome.org/pub/GNOME/sources/%{name}/%{majorver}/%{name}-%{version}.tar.xz

BuildRequires: gupnp-devel
BuildRequires: gupnp-av-devel
BuildRequires: gssdp-devel
BuildRequires: gtk3-devel
BuildRequires: intltool
BuildRequires: libsoup-devel
BuildRequires: libuuid-devel
BuildRequires: gnome-icon-theme-devel
BuildRequires: desktop-file-utils

%description
GUPnP is an object-oriented open source framework for creating UPnP 
devices and control points, written in C using GObject and libsoup. 
The GUPnP API is intended to be easy to use, efficient and flexible. 

GUPnP-tools is a collection of developer tools utilising GUPnP and GTK+. 
It features a universal control point application as well as a sample 
DimmableLight v1.0 implementation. 

%description -l zh_CN.UTF-8
GUPnP 和 GTK+ 的开发工具集。

%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags} V=1

%install
make install DESTDIR=%{buildroot}
magic_rpm_clean.sh
%find_lang %{name}
desktop-file-install --vendor=gupnp \
--delete-original --dir=%{buildroot}%{_datadir}/applications \
%{buildroot}/%{_datadir}/applications/gupnp-av-cp.desktop

desktop-file-install --vendor=gupnp \
--delete-original --dir=%{buildroot}%{_datadir}/applications \
%{buildroot}/%{_datadir}/applications/gupnp-network-light.desktop

desktop-file-install --vendor=gupnp \
--delete-original --dir=%{buildroot}%{_datadir}/applications \
%{buildroot}/%{_datadir}/applications/gupnp-universal-cp.desktop

%files -f %{name}.lang
%doc AUTHORS COPYING README
%dir %{_datadir}/gupnp-tools/
%dir %{_datadir}/gupnp-tools/pixmaps/
%dir %{_datadir}/gupnp-tools/xml/
%{_bindir}/gssdp-discover
%{_bindir}/gupnp-network-light
%{_bindir}/gupnp-universal-cp
%{_bindir}/gupnp-av-cp
%{_bindir}/gupnp-upload
%{_datadir}/applications/gupnp-av-cp.desktop
%{_datadir}/applications/gupnp-network-light.desktop
%{_datadir}/applications/gupnp-universal-cp.desktop
%{_datadir}/gupnp-tools/pixmaps/*.png
%{_datadir}/gupnp-tools/xml/*.xml
%{_datadir}/gupnp-tools/*.ui

%changelog
* Tue Apr 15 2014 Liu Di <liudidi@gmail.com> - 0.8.9-2
- 为 Magic 3.0 重建

* Tue Feb  4 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.8.9-1
- Update to 0.8.9
- http://ftp.gnome.org/pub/GNOME/sources/gupnp-tools/0.8/gupnp-tools-0.8.9.news

* Mon Nov 11 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.8.8-1
- Update to 0.8.8
- http://ftp.gnome.org/pub/GNOME/sources/gupnp-tools/0.8/gupnp-tools-0.8.8.news

* Wed Aug 21 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.8.7-1
- Update to 0.8.7
- http://ftp.gnome.org/pub/GNOME/sources/gupnp-tools/0.8/gupnp-tools-0.8.7.news

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 28 2013 Kalev Lember <kalevlember@gmail.com> 0.8.6.1-2
- Adapt for gnome-icon-theme packaging changes

* Thu Apr  4 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.8.6.1
- Update to 0.8.6.1
- http://ftp.gnome.org/pub/GNOME/sources/gupnp-tools/0.8/gupnp-tools-0.8.6.1.news

* Wed Mar 20 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.8.6-1
- Update to 0.8.6
- http://ftp.gnome.org/pub/GNOME/sources/gupnp-tools/0.8/gupnp-tools-0.8.6.news

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Dec 26 2012 Peter Robinson <pbrobinson@fedoraproject.org> 0.8.5-1
- Update to 0.8.5
- http://ftp.gnome.org/pub/GNOME/sources/gupnp-tools/0.8/gupnp-tools-0.8.5.news

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 12 2011 Peter Robinson <pbrobinson@fedoraproject.org> 0.8.4-1
- Update to 0.8.4
- http://ftp.gnome.org/pub/GNOME/sources/gupnp-tools/0.8/gupnp-tools-0.8.4.news

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.8.3-3
- Rebuild for new libpng

* Fri Jun 17 2011 Peter Robinson <pbrobinson@fedoraproject.org> 0.8.3-2
- rebuild for new gupnp/gssdp

* Fri Apr 15 2011 Peter Robinson <pbrobinson@fedoraproject.org> 0.8.3-1
- Update to 0.8.3

* Mon Apr 11 2011 Peter Robinson <pbrobinson@fedoraproject.org> 0.8.2-1
- Update to 0.8.2

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 jkeating - 0.8.1-2
- Rebuilt for gcc bug 634757

* Fri Sep 17 2010 Bastien Nocera <bnocera@redhat.com> 0.8.1-1
- Update to 0.8.1

* Tue Aug 17 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.8-3
- Update source URL

* Mon Mar 15 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.8-2
- Add patch to fix DSO linking. Fixes bug 564656 

* Thu Sep 17 2009 Bastien Nocera <bnocera@redhat.com> 0.8-1
- Update to 0.8

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue May 12 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.7.1-4
- Rebuild with new libuuid build req

* Tue May 12 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.7.1-3
- and add the GTKBuilder replacements

* Tue May 12 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.7.1-2
- Remove the glade files now that it uses GTKBuilder

* Tue May 12 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.7.1-1
- New upstream release

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 22 2008 Peter Robinson <pbrobinson@fedoraproject.org> 0.7-3
- Fix package summary

* Tue Oct 28 2008 Peter Robinson <pbrobinson@fedoraproject.org> 0.7-2
- Add missing files

* Tue Oct 28 2008 Peter Robinson <pbrobinson@fedoraproject.org> 0.7-1
- New upstream release

* Sat Oct 25 2008 Peter Robinson <pbrobinson@fedoraproject.org> 0.6.1-4
- Add patch and rebuild

* Sat Oct 25 2008 Peter Robinson <pbrobinson@fedoraproject.org> 0.6.1-3
- Rebuild

* Fri Oct 24 2008 Peter Robinson <pbrobinson@fedoraproject.org> 0.6.1-2
- Add patch to fix gthread issue

* Mon Sep 29 2008 Peter Robinson <pbrobinson@fedoraproject.org> 0.6.1-1
- New upstream release

* Sat Aug 30 2008 Peter Robinson <pbrobinson@fedoraproject.org> 0.6-2
- spec file review updates

* Tue Jun 17 2008 Peter Robinson <pbrobinson@fedoraproject.org> 0.6-1
- Initial release
