Name:		totem-pl-parser
Version:	3.10.5
Release:	2%{?dist}
Summary:	Totem Playlist Parser library
Summary(zh_CN.UTF-8): Totem 播放列表解析库

Group:		System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:	LGPLv2+
Url:		http://www.gnome.org/projects/totem/
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source0:	http://download.gnome.org/sources/%{name}/%{majorver}/%{name}-%{version}.tar.xz
Obsoletes:	totem-plparser

BuildRequires:	glib2-devel
BuildRequires:	gmime-devel
BuildRequires:	libxml2-devel
BuildRequires:	libsoup-devel
BuildRequires:	gobject-introspection-devel
BuildRequires:	gettext
BuildRequires:	libquvi-devel
BuildRequires:	libarchive-devel
BuildRequires:	perl(XML::Parser) intltool

%description
A library to parse and save playlists, as used in music and movie players.

%description -l zh_CN.UTF-8
Totem 播放列表解析库。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Obsoletes:	totem-devel < 2.21.90
Requires:       %{name} = %{version}-%{release}
Requires:	pkgconfig
Requires:	gobject-introspection-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

%build
%configure --enable-static=no
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
magic_rpm_clean.sh
%find_lang %{name} --with-gnome

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING.LIB NEWS README
%{_libdir}/*.so.*
%{_libdir}/girepository-1.0/*.typelib
%{_libexecdir}/totem-pl-parser-videosite

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gtk-doc/html/totem-pl-parser
%{_datadir}/gir-1.0/*.gir

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 3.10.5-2
- 为 Magic 3.0 重建

* Sun Oct 04 2015 Liu Di <liudidi@gmail.com> - 3.10.5-1
- 更新到 3.10.5

* Thu Dec 25 2014 Liu Di <liudidi@gmail.com> - 3.10.3-1
- 更新到 3.10.3

* Thu Apr 10 2014 Liu Di <liudidi@gmail.com> - 3.10.2-1
- 更新到 3.10.2

* Tue Mar 26 2013 Kalev Lember <kalevlember@gmail.com> - 3.4.4-1
- Update to 3.4.4

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 17 2013 Tomas Bzatek <tbzatek@redhat.com> - 3.4.3-2
- Rebuilt for new libarchive

* Wed Sep 19 2012 Tomas Bzatek <tbzatek@redhat.com> - 3.4.3-1
- Update to 3.4.3

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri May 18 2012 Richard Hughes <hughsient@gmail.com> - 3.4.2-1
- Update to 3.4.2

* Sat Apr 28 2012 Bastien Nocera <bnocera@redhat.com> 3.4.1-2
- Remove dependency on gtk2-devel for the devel sub-package

* Mon Apr 16 2012 Richard Hughes <hughsient@gmail.com> - 3.4.1-1
- Update to 3.4.1

* Tue Mar 27 2012 Richard Hughes <hughsient@gmail.com> - 3.4.0-1
- Update to 3.4.0

* Tue Mar 20 2012 Kalev Lember <kalevlember@gmail.com> - 3.3.92-1
- Update to 3.3.92

* Sun Feb 26 2012 Matthias Clasen <mclasen@redhat.com> - 3.2.0-1
- Update to 3.2.0

* Thu Jan 26 2012 Tomas Bzatek <tbzatek@redhat.com> - 2.32.6-5
- Rebuilt for new libarchive

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.32.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 17 2011 Daniel Drake <dsd@laptop.org> 2.32.6-3
- Add upstream compile fix for libquvi.so.7 (and rebuild for this version)
- Add upstream compile fix for glib-2.31

* Wed Nov 16 2011 Peter Robinson <pbrobinson@fedoraproject.org> 2.32.6-2
- Rebuild for new libarchive and quvi

* Tue Sep 20 2011 Bastien Nocera <bnocera@redhat.com> 2.32.6-1
- Update to 2.32.6

* Mon Jun 27 2011 Adam Williamson <awilliam@redhat.com> 2.32.5-2
- rebuild for new quvi

* Wed May 11 2011 Bastien Nocera <bnocera@redhat.com> 2.32.5-1
- Update to 2.32.5

* Mon Mar 21 2011 Bastien Nocera <bnocera@redhat.com> 2.32.4-1
- Update to 2.32.4

* Mon Feb 21 2011 Bastien Nocera <bnocera@redhat.com> 2.32.3-1
- Update to 2.32.3

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.32.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 31 2011 Bastien Nocera <bnocera@redhat.com> 2.32.2-2
- Fix quvi version dependency

* Fri Jan 28 2011 Bastien Nocera <bnocera@redhat.com> 2.32.2-1
- Update to 2.32.2

* Thu Jan 13 2011 Matthias Clasen <mclasen@redhat.com> 2.32.1-2
- Move girs to -devel

* Mon Oct 18 2010 Bastien Nocera <bnocera@redhat.com> 2.32.1-1
- Update to 2.32.1

* Tue Sep 28 2010 Bastien Nocera <bnocera@redhat.com> 2.32.0-1
- Update to 2.32.0

* Wed Sep 22 2010 Matthias Clasen <mclasen@redhat.com> 2.31.92-1
- Update to 2.31.92
- Rebuild against newer gobject-introspection

* Mon Sep 13 2010 Bastien Nocera <bnocera@redhat.com> 2.30.3-1
- Update to 2.30.3

* Wed Aug 04 2010 Bastien Nocera <bnocera@redhat.com> 2.30.2-1
- Update to 2.30.2

* Thu Jul 15 2010 Colin Walters <walters@verbum.org> - 2.30.1-2
- Rebuild with new gobject-introspection

* Wed May 12 2010 Bastien Nocera <bnocera@redhat.com> 2.30.1-1
- Update to 2.30.1

* Mon Mar 29 2010 Bastien Nocera <bnocera@redhat.com> 2.30.0-1
- Update to 2.30.0

* Mon Mar 15 2010 Bastien Nocera <bnocera@redhat.com> 2.29.92-1
- Update to 2.29.92

* Sat Feb 13 2010 Caolán McNamara <caolanm@redhat.com> 2.29.1-2
- Rebuild for gmime26

* Tue Jan 26 2010 Bastien Nocera <bnocera@redhat.com> 2.29.1-1
- Update to 2.29.1

* Fri Dec 11 2009 Bastien Nocera <bnocera@redhat.com> 2.28.2-1
- Update to 2.28.2

* Thu Oct 15 2009 Bastien Nocera <bnocera@redhat.com> 2.28.1-2
- Fix crasher when parsing multiple XML-ish playlists in Rhythmbox

* Tue Sep 29 2009 Bastien Nocera <bnocera@redhat.com> 2.28.1-1
- Update to 2.28.1

* Mon Sep 21 2009 Bastien Nocera <bnocera@redhat.com> 2.28.0-2
- Update source URL

* Mon Sep 21 2009 Bastien Nocera <bnocera@redhat.com> 2.28.0-1
- Update to 2.28.0

* Tue Sep 15 2009 Bastien Nocera <bnocera@redhat.com> 2.27.92-1
- Update to 2.27.92

* Tue Sep 08 2009 Bastien Nocera <bnocera@redhat.com> 2.27.2-4
- Version Obsoletes for totem-devel (#520874)

* Tue Aug 11 2009 Bastien Nocera <bnocera@redhat.com> 2.27.2-3
- Fix URL

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 Bastien Nocera <bnocera@redhat.com> 2.27.2-1
- Update to 2.27.2

* Wed May 06 2009 Bastien Nocera <bnocera@redhat.com> 2.27.1-1
- Update to 2.27.1

* Tue Mar 31 2009 - Bastien Nocera <bnocera@redhat.com> - 2.26.1-1
- Update to 2.26.1

* Mon Mar 16 2009 - Bastien Nocera <bnocera@redhat.com> - 2.26.0-1
- Update to 2.26.0

* Tue Mar 03 2009 - Bastien Nocera <bnocera@redhat.com> - 2.25.92-1
- Update to 2.25.92

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 17 2009 - Bastien Nocera <bnocera@redhat.com> - 2.25.91-1
- Update to 2.25.91

* Tue Feb 03 2009 - Bastien Nocera <bnocera@redhat.com> - 2.25.90-1
- Update to 2.25.90

* Tue Feb 03 2009 - Bastien Nocera <bnocera@redhat.com> - 2.25.1-3
- Rebuild for new libcamel

* Tue Dec 09 2008 - Bastien Nocera <bnocera@redhat.com> - 2.25.1-2
- Add evolution-data-server-devel Requires for the devel package

* Mon Dec 08 2008 - Bastien Nocera <bnocera@redhat.com> - 2.25.1-1
- Update to 2.25.1

* Fri Dec 05 2008 Matthew Barnes <mbarnes@redhat.com> - 2.24.2-3
- Rebuild against newer libcamel.

* Fri Nov 14 2008 Matthias Clasen  <mclasen@redhat.com> - 2.24.2-2
- Rebuild

* Thu Oct 30 2008 - Bastien Nocera <bnocera@redhat.com> - 2.24.2-1
- Update to 2.24.2

* Tue Oct 21 2008 Matthias Clasen  <mclasen@redhat.com> - 2.24.1-2
- Rebuild

* Tue Oct 07 2008 - Bastien Nocera <bnocera@redhat.com> - 2.24.1-1
- Update to 2.24.1

* Sun Sep 21 2008 - Bastien Nocera <bnocera@redhat.com> - 2.24.0-1
- Update to 2.24.0

* Fri Aug 29 2008 - Bastien Nocera <bnocera@redhat.com> - 2.23.91-1
- Update to 2.23.91

* Tue Aug  5 2008 Matthias Clasen  <mclasen@redhat.com> - 2.23.3-2
- Rebuild

* Mon Jul 14 2008 - Bastien Nocera <bnocera@redhat.com> - 2.23.3-1
- Update to 2.23.3
- Fixes crasher when totem_cd_detect_type() generates an error (#455014)

* Wed Jun 11 2008 - Bastien Nocera <bnocera@redhat.com> - 2.23.2-1
- Update to 2.23.2

* Tue May 13 2008 - Bastien Nocera <bnocera@redhat.com> - 2.23.1-2
- Rebuild

* Fri May 09 2008 - Bastien Nocera <bnocera@redhat.com> - 2.23.1-1
- Update to 2.23.1
- Remove gnome-vfs2 dependencies

* Wed May 07 2008 - Bastien Nocera <bnocera@redhat.com> - 2.22.2-3
- Rebuild for new libcamel

* Sun May  4 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.2-2
- Fix source url

* Tue Apr 08 2008 - Bastien Nocera <bnocera@redhat.com> - 2.22.2-1
- Update to 2.22.2

* Mon Mar 10 2008 - Bastien Nocera <bnocera@redhat.com> - 2.22.1-1
- Update to 2.22.1

* Mon Mar 10 2008 - Bastien Nocera <bnocera@redhat.com> - 2.22.0-1
- Update to 2.22.0

* Sun Feb 24 2008 - Bastien Nocera <bnocera@redhat.com> - 2.21.92-1
- Update to 2.21.92

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.21.91-3
- Autorebuild for GCC 4.3

* Tue Jan 29 2008 - Matthew Barnes <mbarnes@redhat.com> - 2.21.21-2
- Rebuild against newer libcamel-1.2.

* Mon Jan 21 2008 - Bastien Nocera <bnocera@redhat.com> - 2.21.91-1
- Update to 2.21.91

* Mon Jan 07 2008 - Bastien Nocera <bnocera@redhat.com> - 2.21.90-1
- Update to 2.21.90

* Thu Dec 06 2007 - Bastien Nocera <bnocera@redhat.com> - 2.21.6-1
- First package

