# first two digits of version
%define release_version %(echo %{version} | awk -F. '{print $1"."$2}')

Name:		grilo-plugins
Version:	0.2.16
Release:	6%{?dist}
Summary:	Plugins for the Grilo framework
Summary(zh_CN.UTF-8): Grilo 框架的插件

Group:		Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
License:	LGPLv2+
Url:		https://live.gnome.org/Grilo
Source0:	http://ftp.gnome.org/pub/GNOME/sources/grilo-plugins/%{release_version}/grilo-plugins-%{version}.tar.xz

BuildRequires:	grilo-devel >= 0.2.4
BuildRequires:	glib2-devel >= 2.26.0
BuildRequires:	libxml2-devel
BuildRequires:	gupnp-devel >= 0.13.0
BuildRequires:	gupnp-av-devel >= 0.5.0
BuildRequires:	sqlite-devel
BuildRequires:	libgdata-devel
BuildRequires:	tracker-devel >= 0.9.0
BuildRequires:	libquvi-devel
BuildRequires:	gmime-devel
BuildRequires:	libdmapsharing-devel
BuildRequires:	json-glib-devel

Requires:	grilo >= 0.2.4
Requires:	gupnp >= 0.13.0
Requires:	gupnp-av >= 0.5.0
# For the documentation directories
Requires:	yelp


%description
Grilo is a framework that provides access to different sources of
multimedia content, using a pluggable system.
This package contains plugins to get information from theses sources:
- Apple Trailers
- Bookmarks
- Filesystem
- Flickr
- Gravatar
- iTunes Music Sharing
- Jamendo
- Last.fm (for album arts)
- Local metadata (album arts and thumbnails)
- Metadata Store
- Podcasts
- Shoutcast
- Tracker
- UPnP
- Vimeo
- Youtube

%description -l zh_CN.UTF-8 
Grilo 框架的插件，包括这些源的支持：
- Apple Trailers
- Bookmarks
- Filesystem
- Flickr
- Gravatar
- iTunes Music Sharing
- Jamendo
- Last.fm (for album arts)
- Local metadata (album arts and thumbnails)
- Metadata Store
- Podcasts
- Shoutcast
- Tracker
- UPnP
- Vimeo
- Youtube

%prep
%setup -q


%build
%configure				\
	--disable-static		\
	--disable-fakemetadata		\
	--disable-shoutcast		\
	--enable-apple-trailers		\
	--enable-bookmarks		\
	--enable-dmap			\
	--enable-filesystem		\
	--enable-flickr			\
	--enable-gravatar		\
	--enable-jamendo		\
	--enable-lastfm-albumart	\
	--enable-localmetadata		\
	--enable-metadata-store		\
	--enable-podcasts		\
	--enable-tmdb			\
	--enable-tracker		\
	--enable-upnp			\
	--enable-vimeo			\
	--enable-youtube		\
	--enable-tracker

# Silence unused-direct-shlib-dependency
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool

make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

# Remove files that will not be packaged
rm -f $RPM_BUILD_ROOT%{_libdir}/grilo-%{release_version}/*.la
rm -f $RPM_BUILD_ROOT%{_bindir}/*
magic_rpm_clean.sh

%files
%doc AUTHORS COPYING NEWS README
%{_libdir}/grilo-%{release_version}/*.so*
%{_libdir}/grilo-%{release_version}/*.xml
%{_datadir}/grilo-plugins/grl-lua-factory/grl-euronews.lua
%{_datadir}/grilo-plugins/grl-lua-factory/grl-guardianvideos.lua
%{_datadir}/grilo-plugins/grl-lua-factory/grl-metrolyrics.lua
%{_datadir}/grilo-plugins/grl-lua-factory/grl-radiofrance.lua
%{_datadir}/help/C/examples/example-tmdb.c
%{_datadir}/help/C/grilo-plugins/grilo-plugins.xml
%{_datadir}/help/C/grilo-plugins/legal.xml
%{_datadir}/locale/zh_CN/LC_MESSAGES/grilo-plugins.mo
%{_datadir}/locale/zh_HK/LC_MESSAGES/grilo-plugins.mo
%{_datadir}/locale/zh_TW/LC_MESSAGES/grilo-plugins.mo
                                                         

%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 0.2.16-6
- 为 Magic 3.0 重建

* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 0.2.16-5
- 更新到 0.2.16

* Fri Jul 18 2014 Liu Di <liudidi@gmail.com> - 0.2.12-4
- 为 Magic 3.0 重建

* Wed Apr 16 2014 Liu Di <liudidi@gmail.com> - 0.2.12-3
- 更新到 0.2.12

* Wed Apr 16 2014 Liu Di <liudidi@gmail.com> - 0.2.6-3
- 为 Magic 3.0 重建

* Fri Apr 11 2014 Liu Di <liudidi@gmail.com> - 0.2.6-2
- 为 Magic 3.0 重建

* Wed Mar 20 2013 Kalev Lember <kalevlember@gmail.com> - 0.2.6-1
- Update to 0.2.6

* Mon Jan 28 2013 Matthias Clasen <mclasen@redhat.com> - 0.2.5-3
- Fix build against newer tracker

* Sun Jan 27 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.2.5-2
- Rebuild for tracker

* Thu Dec 20 2012 Bastien Nocera <bnocera@redhat.com> 0.2.5-1
- Update to 0.2.5

* Tue Dec 04 2012 Bastien Nocera <bnocera@redhat.com> 0.2.4-1
- Update to 0.2.4

* Tue Nov 13 2012 Kalev Lember <kalevlember@gmail.com> 0.2.3-1
- Update to 0.2.3

* Fri Oct 05 2012 Bastien Nocera <bnocera@redhat.com> 0.2.2-1
- Update to 0.2.2

* Wed Oct 03 2012 Bastien Nocera <bnocera@redhat.com> 0.2.1-1
- Update to 0.2.1

* Fri Aug 31 2012 Debarshi Ray <rishi@fedoraproject.org> 0.2.0-1
- update to 0.2.0

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri May 25 2012 Bastien Nocera <bnocera@redhat.com> 0.1.19-1
- Update to 0.1.19

* Fri Mar 16 2012 Adam Williamson <awilliam@redhat.com> - 0.1.18-4
- Rebuild for new tracker again

* Tue Feb 28 2012 Matthias Clasen <mclasen@redhat.com> - 0.1.18-3
- Rebuild for new tracker

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 12 2011 Bastien Nocera <bnocera@redhat.com> 0.1.18-1
- Update to 0.1.18

* Thu Nov 17 2011 Daniel Drake <dsd@laptop.org> 0.1.17-2
- rebuild for libquvi.so.7

* Mon Oct 17 2011 Bastien Nocera <bnocera@redhat.com> 0.1.17-1
- Update to 0.1.17

* Mon Jul 04 2011 Bastien Nocera <bnocera@redhat.com> 0.1.16-1
- Update to 0.1.16

* Fri Jun 17 2011 Peter Robinson <pbrobinson@gmail.com> 0.1.15-5
- rebuild for new gupnp/gssdp

* Fri May 20 2011 Bastien Nocera <bnocera@redhat.com> 0.1.15-4
- Update with more comments from Kalev Lember <kalev@smartlink.ee>

* Fri May 20 2011 Bastien Nocera <bnocera@redhat.com> 0.1.15-3
- Update with comments from Kalev Lember <kalev@smartlink.ee>

* Fri May 20 2011 Bastien Nocera <bnocera@redhat.com> 0.1.15-2
- Fix a few rpmlint warnings

* Thu Apr 21 2011 Bastien Nocera <bnocera@redhat.com> 0.1.15-1
- Fist package, based on upstream work by Juan A.
  Suarez Romero <jasuarez@igalia.com>

