%define	major_version	0.9
%define liboil_version	0.3.1
%define	gtk2_version	2.8.0
%define pango_version	1.16

Name:		swfdec
Version:	%{major_version}.2
Release:	5%{?dist}
Summary:	Flash animation rendering library
Summary(zh_CN): Flash 动画渲染库

Group:		System Environment/Libraries
Group(zh_CN):	系统环境/库
License:	LGPLv2+
URL:		http://swfdec.freedesktop.org/
Source0:	http://swfdec.freedesktop.org/download/%{name}/%{major_version}/%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	alsa-lib-devel
BuildRequires:	glib2-devel >= 2.16
BuildRequires:	gstreamer-devel >= 0.10.11
BuildRequires:	gstreamer-plugins-base-devel >= 0.10.15
BuildRequires:	gtk2-devel >= %{gtk2_version}
BuildRequires:	liboil-devel >= %{liboil_version}
BuildRequires:	libsoup-devel >= 2.4.0
BuildRequires:	pango-devel >= %{pango_version}

Requires(pre):	/sbin/ldconfig
Requires(post):	/sbin/ldconfig


%description
swfdec is a library for rendering Adobe Flash animations. Currently it handles
most Flash 3, 4 and many Flash 7 videos. 

%description -l zh_CN
Flash 动画渲染库。

%package	devel
Summary:	Development files for %{name}
Summary(zh_CN): %name 的开发包
Group:		Development/Libraries
Group(zh_CN):	开发/库
Requires:	%{name} = %{version}-%{release}
Requires:	liboil-devel >= %{liboil_version}
Requires:	pango-devel >= %{pango_version}
Requires:	pkgconfig


%description	devel
%{name}-devel contains the files needed to build packages that depend on
swfdec.

%description devel -l zh_CN
%name 的开发包

%package	gtk
Summary:	A library for easy embedding of Flash files in an application
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires(pre):	/sbin/ldconfig
Requires(post):	/sbin/ldconfig


%description	gtk
%{name}-gtk is a library for developers that allows one to easily embed
Flash videos and animations into their appplications. 


%package	gtk-devel
Summary:	Development files for swfdec-gtk
Group:		Development/Libraries
Requires:	%{name}-gtk = %{version}-%{release}
Requires:	%{name}-devel = %{version}-%{release}
Requires:	gtk2-devel >= %{gtk2_version}


%description	gtk-devel
%{name}-gtk is a library for developers that allows one to easily embed
Flash videos and animations into their appplications. This package contains
files necessary to build packages and appplications that use %{name}-gtk.


%prep
%setup -q

		
%build
%configure --disable-static --with-audio=alsa

# remove rpath from libtool
sed -i.rpath 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i.rpath 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install INSTALL='install -p'
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%check
# Disabling test since it will fail due to the gstreamer mp3 plugin
# not being available in Fedora.
#
#export LD_LIBRARY_PATH=`pwd`/libswfdec/.libs:`pwd`/libswfdec-gtk/.libs
#make check
#unset LD_LIBRARY_PATH


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig


%post gtk -p /sbin/ldconfig


%postun	-p /sbin/ldconfig


%postun gtk -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README 
%{_libdir}/libswfdec-%{major_version}.so.*


%files	devel
%defattr(-,root,root,-)
%{_datadir}/gtk-doc/html/%{name}/
%{_libdir}/pkgconfig/%{name}-%{major_version}.pc
%{_libdir}/libswfdec-%{major_version}.so
%dir %{_includedir}/%{name}-%{major_version}
%{_includedir}/%{name}-%{major_version}/swfdec/


%files	gtk
%defattr(-,root,root,-)
#%{_datadir}/icons/hicolor/*/apps/%{name}.png
#%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_libdir}/libswfdec-gtk-%{major_version}.so.*


%files	gtk-devel
%defattr(-,root,root,-)
%{_libdir}/libswfdec-gtk-%{major_version}.so
%{_libdir}/pkgconfig/%{name}-gtk-%{major_version}.pc
%{_includedir}/%{name}-%{major_version}/swfdec-gtk/


%changelog
* Tue Sep 29 2015 Liu Di <liudidi@gmail.com> - 0.9.2-5
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 0.9.2-4
- 为 Magic 3.0 重建

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Nov 11 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.9.2-1
- Update to 0.9.2.

* Thu Oct 23 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.8.2-1
- Update to 0.8.2.

* Mon Sep  8 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.8.0-1
- Update to 0.8.0.

* Wed Jul 30 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.7.4-1
- Update to 0.7.4.

* Wed Jun 25 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.7.2-1
- Update to 0.7.2

* Wed Apr 23 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.6.6-1
- Update to 0.6.6.
- Drop memory-overwrite patch.  Fixed upstream.
- Drop alsa patch. Fixed upstream.

* Thu Apr 10 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.6.4-3
- Add patch to fix memory overwrite error. (#441614)

* Thu Apr 10 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.6.4-2
- Build w/ alsa backend instead of pulse audio.
- Add patch to fix alsa support. (#441617).
- Drop unnecessary BR on js-devel and gnome-vfs2-devel.
- Add BR on glib2-devel.

* Wed Apr  9 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.6.4-1
- Update to 0.6.4.

* Sat Mar 29 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.6.2-1
- Update to 0.6.2.

* Wed Feb 20 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.6.0-1
- Update to 0.6.0.
- Bump minimum version of gstreamer needed.
- Add BR for gstreamer-plugins-base-devel.

* Thu Feb 14 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.5.90-3
- Rebuild for new libsoup.

* Fri Feb  8 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.5.90-2
- Rebuild for gcc-4.3.

* Tue Jan 29 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.5.90-1
- Update to 0.5.90.
- Bump BR minimum versions for libsoup & pango.

* Wed Dec 19 2007 Brian Pepple <bpepple@fedoraproject.org> - 0.5.5-2
- Build w/ pulse audio support.

* Mon Dec 17 2007 Brian Pepple <bpepple@fedoraproject.org> - 0.5.5-1
- Update to 0.5.5.

* Fri Nov 16 2007 Brian Pepple <bpepple@fedoraproject.org> - 0.5.4-2
- Add requires for pango-devel to devel pkg.
- Keep timestamp on installed files.

* Thu Nov 15 2007 Brian Pepple <bpepple@fedoraproject.org> - 0.5.4-1
- Update to 0.5.4.
- Use valid license tag.
- Remove BR on ffmpeg & libmad, and only build gstreamer backend.

* Fri Oct 12 2007  Peter Gordon <peter@thecodergeek.com> - 0.5.3-1
- Update to new upstream release (0.5.3)

* Wed Oct 10 2007  Peter Gordon <peter@thecodergeek.com> - 0.5.2-1
- Update to new upstream release (0.5.2)

* Wed Aug 15 2007  Peter Gordon <peter@thecodergeek.com> - 0.5.1-1
- Update to new upstream release (0.5.1)

* Thu Jul  5 2007 kwizart <kwizart at gmail.com> - 0.4.5-1
- Update to 0.4.5 (bugfix)
- Add BR ffmpeg-devel libmad-devel (enabled in configure)
- Remove rpath (libtool method)

* Sat Apr 28 2007 Peter Gordon <peter@thecodergeek.com> - 0.4.4-1
- Update to new upstream release (0.4.4), which adds two new subpackages:
  swfdec-gtk and swfdec-gtk-devel.

* Sun Mar 25 2007 Peter Gordon <peter@thecodergeek.com> - 0.4.3-2
- Add js-devel to the BuildRequires to fix compilation in Mock.
  (Thanks to  Julian Sikorski; Livna bug #1453) 

* Sat Mar 24 2007 Peter Gordon <peter@thecodergeek.com> - 0.4.3-1
- Update to new upstream release (0.4.3), with lots of spec cleanups
- Spec file based heavily on Thomas Vander Stichele's 0.3.6 stuff.

* Sun Dec 03 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.3.6-0.gst.2
- fix pre/post scripts

* Sun Dec 03 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.3.6-0.gst.1
- new upstream
- remove swf_play
- add js-devel and gimp-devel buildrequires
- add gimp plugin

* Fri Jun 24 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.3.5-0.gst.1
- updated to new upstream

* Tue May 17 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.3.4-0.gst.1
- updated to new upstream

* Thu Mar 03 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.3.2-0.lvn.1
- updated to new liboil and upstream release

* Thu Nov 11 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- new upstream release

* Thu May 20 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.2.2-0.lvn.2
- require gcc-c++ for libtool
- fix pre/post req
- fix gtk loaders location
- work around FC2 packaging bug for SDL-devel

* Tue Mar 02 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.2.2-0.lvn.1: updated for rpm.livna.us (without mozilla plugin)

* Mon May 19 2003 Thomas Vander Stichele <thomas at apestaart dot org>
- Updated for 0.2.2

* Wed Feb 05 2003 Christian F.K. Schaller <Uraeus@linuxrising.org>
- Update spec to handle pixbuf loader
* Sat Oct 26 2002 Christian F.K. Schaller <Uraeus@linuxrising.org>
- First attempt at spec
