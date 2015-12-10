Name:          libsocialweb
Version:       0.25.21
Release:       4%{?dist}
Summary:       A social network data aggregator
Summary(zh_CN.UTF-8): 社交网络数据聚合程序

Group:         Applications/Internet
Group(zh_CN.UTF-8): 应用程序/互联网
License:       LGPLv2
URL:           http://www.gnome.org/
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source0:       ftp://ftp.gnome.org/pub/gnome/sources/%{name}/%{majorver}/%{name}-%{version}.tar.xz
Source1: flickr
Source2: twitter
Source3: lastfm
Source4: twitpic
Source5: facebook
Source6: facebook.key
Patch0: libsocialweb-gir-fix.patch

BuildRequires: dbus-glib-devel
BuildRequires: geoclue-devel
BuildRequires: glib2-devel
BuildRequires: GConf2-devel
BuildRequires: libgnome-keyring-devel
BuildRequires: gobject-introspection-devel
BuildRequires: intltool
BuildRequires: json-glib-devel
BuildRequires: libsoup-devel
BuildRequires: libxslt-devel
BuildRequires: NetworkManager-glib-devel
BuildRequires: rest-devel
BuildRequires: vala-devel
BuildRequires: vala-tools

Requires: %{name}-keys = %{version}-%{release}

%description
libsocialweb is a social data server which fetches data from the "social web", 
such as your friend's blog posts and photos, upcoming events, recently played 
tracks, and pending eBay* auctions. It also provides a service to update 
your status on web services which support it, such as MySpace* and Twitter*.

%description -l zh_CN.UTF-8
社交网络数据聚合程序。

%package devel
Summary: Development package for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
Files for development with %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package keys
Summary: API keys for %{name}
Summary(zh_CN.UTF-8): %{name} 的 API 键
Group: Applications/Internet
Group(zh_CN.UTF-8): 应用程序/互联网
BuildArch: noarch
Requires: %{name} = %{version}-%{release}

%description keys
Keys allowing access to various web services through libsocialweb.

%description keys -l zh_CN.UTF-8
%{name} 的 API 键。

%prep
%setup -q
%patch0 -p1 -b .fix-gir

chmod 644 examples/*.py 

## nuke unwanted rpaths, see also
## https://fedoraproject.org/wiki/Packaging/Guidelines#Beware_of_Rpath
sed -i -e 's|"/lib /usr/lib|"/%{_lib} %{_libdir}|' configure

%build
%configure --with-gnome --with-online=networkmanager --disable-static --enable-all-services --enable-vala-bindings

make %{?_smp_mflags} V=1

%install
make install DESTDIR=%{buildroot} INSTALL='install -p'

#Remove libtool archives and static libs.
find %{buildroot} -name '*.la' -exec rm -f {} ';'
find %{buildroot} -name '*.a' -exec rm -f {} ';'

mkdir -p %{buildroot}/%{_datadir}/libsocialweb/keys
cp %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} %{SOURCE6} %{buildroot}/%{_datadir}/libsocialweb/keys
magic_rpm_clean.sh
%find_lang %{name}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING TODO
%{_libdir}/libsocialweb*.so.*
%{_libdir}/libsocialweb/
%{_libdir}/girepository-1.0/SocialWebClient-0.25.typelib
%dir %{_datadir}/libsocialweb/
%{_datadir}/libsocialweb/services/
%{_datadir}/dbus-1/services/libsocialweb.service
%{_libexecdir}/libsocialweb-core

%files devel
%defattr(-,root,root,-)
%doc tests/*.c examples/*c examples/*.py
%doc %{_datadir}/gtk-doc/html/libsocialweb
%doc %{_datadir}/gtk-doc/html/libsocialweb-client
%doc %{_datadir}/gtk-doc/html/libsocialweb-dbus
%{_includedir}/libsocialweb
%{_libdir}/pkgconfig/libsocialweb*
%{_libdir}/libsocialweb*so
%{_datadir}/gir-1.0/SocialWebClient-0.25.gir
%{_datadir}/vala/vapi/libsocialweb-client.deps
%{_datadir}/vala/vapi/libsocialweb-client.vapi

%files keys
%defattr(-,root,root,-)
%{_datadir}/libsocialweb/keys

%changelog
* Mon Nov 09 2015 Liu Di <liudidi@gmail.com> - 0.25.21-4
- 为 Magic 3.0 重建

* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 0.25.21-3
- 为 Magic 3.0 重建

* Thu Jul 31 2014 Liu Di <liudidi@gmail.com> - 0.25.21-2
- 为 Magic 3.0 重建

* Tue Oct 16 2012 Peter Robinson <pbrobinson@fedoraproject.org> 0.25.21-1
- update to 0.25.21. Fixes CVE-2012-4511, RHBZ 865126

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.25.20-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Mar  7 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.25.20-3
- fix gnome-keyring deps

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.25.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Nov 12 2011 Peter Robinson <pbrobinson@fedoraproject.org> 0.25.20-1
- update to 0.25.20. Fixes CVE-2011-4129, RHBZ 752022

* Mon Jul 04 2011 Bastien Nocera <bnocera@redhat.com> 0.25.19-1
- Update to 0.25.19

* Wed Jun 15 2011 Peter Robinson <pbrobinson@fedoraproject.org> 0.25.18-1
- Update to 0.25.18

* Sun May 22 2011 Peter Robinson <pbrobinson@fedoraproject.org> 0.25.17-1
- Update to 0.25.17

* Sun Apr 24 2011 Peter Robinson <pbrobinson@fedoraproject.org> 0.25.16-1
- Update to 0.25.16, update twitter keys

* Mon Apr 11 2011 Peter Robinson <pbrobinson@fedoraproject.org> 0.25.15-1
- Update to 0.25.15, enable gobject-introspection support

* Sun Apr  3 2011 Peter Robinson <pbrobinson@fedoraproject.org> 0.25.14-1
- Update to 0.25.14

* Mon Mar 28 2011 Peter Robinson <pbrobinson@fedoraproject.org> 0.25.13-1
- Update to 0.25.13

* Fri Mar 25 2011 Dan Williams <dcbw@redhat.com> 0.25.12-2
- Update for NetworkManager 0.9

* Wed Mar 23 2011 Peter Robinson <pbrobinson@fedoraproject.org> 0.25.12-1
- Update to 0.25.12

* Tue Feb 22 2011 Peter Robinson <pbrobinson@fedoraproject.org> 0.25.11-2
- add generic facebook api key

* Tue Feb 22 2011 Peter Robinson <pbrobinson@fedoraproject.org> 0.25.11-1
- Update to 0.25.11
- Add support for Facebook, Plurk, Sina, SmugMug, and YouTube.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.25.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Oct 29 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.25.7-1
- Update to 0.25.7
- libsocialweb is now hosted at gnome.org so we have real tarfiles

* Tue Sep 27 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.25.5-1
- Update to 0.25.5

* Wed Sep 22 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.25.4-1
- Update to 0.25.4

* Tue Sep  7 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.25.3-2
- Add api key for twitpic

* Mon Aug 30 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.25.3-1
- Update to 0.25.3, MySpace and Digg are obsolete upstream

* Thu Aug 26 2010 Bastien Nocera <bnocera@redhat.com> 0.25.1-2
- Add API keys to the -keys sub-package

* Sat Aug  7 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.25.1-1
- Update to 0.25.1, disable MySpace and Digg until they build again

* Sun Jul 11 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.24.9-1
- Update to 0.24.9

* Wed May 12 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.24.8-1
- rename package from mojito to libsocialweb
- Update to 0.24.8

* Mon Jan 25 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.22.1-1
- Update to 0.22.1

* Mon Jan 25 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.22.0-2
- Add upstream patch to fix crash

* Tue Jan 12 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.22.0-1
- New major upstream 0.22.0 release

* Wed Dec  2 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.21.7-1
- Update to 0.21.7

* Thu Nov 19 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.21.6-1
- Update to 0.21.6, move to the official tarball release

* Mon Oct 26 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.21.5-1
- Update to 0.21.5

* Wed Oct 21 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.21.4-2
- enable digg support

* Wed Oct 21 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.21.4-1
- Update to 0.21.4

* Sat Oct 10 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.21.3-1
- Update to 0.21.3

* Fri Oct  2 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.21.2-1
- Update to 0.21.2

* Tue Sep 15 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.21.1-1
- Update to 0.21.1

* Thu Sep  3 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.20.1-1
- Update to 0.20.1

* Mon Aug 31 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.20-5
- Actually commit patch for detection of new NetworkManager

* Mon Aug 31 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.20-4
- Add patch for detection of new NetworkManager

* Mon Aug 31 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.20-3
- Rebuild for new NetworkManager

* Sat Aug 22 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.20-2
- Enable twitter, lastfm, MySpace and Flickr networks

* Wed Aug 19 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.20-1
- Update to 0.20

* Wed Aug  5 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.19.2-2
- A few minor spec file cleanups

* Wed Aug  5 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.19.2-1
- Update to 0.19.2 - updated translations

* Tue Jul 28 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.19.1-1
- Update to 0.19.1 - updated translations

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jul 18 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.19-1
- Update to 0.19

* Mon Jul  6 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.18.1-1
- Update to 0.18.1

* Mon Jul  6 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.17-3
- Add some additional buildreqs

* Mon Jul  6 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.17-2
- Add some additional buildreqs

* Mon Jul  6 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.17-1
- Update to new 0.17 release, add language support and more backends

* Wed Jun 17 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.10.3-2
- Add extra build deps

* Wed Jun 17 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.10.3-1
- Initial packaging
