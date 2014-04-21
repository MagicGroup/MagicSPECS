%define gconf2_version 2.14

Summary: Editor/admin tool for GConf
Summary(zh_CN.UTF-8): GConf 的编辑管理工具
Name: gconf-editor
Version: 3.0.1
Release: 2%{?dist}
URL: http://www.gnome.org
#VCS: git:git://git.gnome.org/gconf-editor
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source0: http://download.gnome.org/sources/gconf-editor/%{majorver}/%{name}-%{version}.tar.xz
License: GPLv2+ and GFDL
Group: Applications/System
Group(zh_CN.UTF-8): 应用程序/系统

Requires(pre): GConf2 >= %{gconf2_version}
Requires(post): GConf2 >= %{gconf2_version}
Requires(preun): GConf2 >= %{gconf2_version}

BuildRequires: GConf2-devel
BuildRequires: gtk3-devel
BuildRequires: desktop-file-utils
BuildRequires: scrollkeeper
BuildRequires: gettext
BuildRequires: gnome-doc-utils
BuildRequires: intltool
BuildRequires: gnome-common
BuildRequires: autoconf automake libtool

%description
gconf-editor allows you to browse and modify GConf configuration
sources.

%description -l zh_CN.UTF-8
这个包允许你浏览和修改 GConf 配置源码。

%prep
%setup -q

%build
%configure --disable-scrollkeeper
make %{?_smp_mflags}

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

# stuff we don't want
rm -rf $RPM_BUILD_ROOT/var/scrollkeeper

desktop-file-install --vendor gnome --delete-original       \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications             \
  $RPM_BUILD_ROOT%{_datadir}/applications/*
magic_rpm_clean.sh
%find_lang %{name} --with-gnome

%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/gconf-editor.schemas > /dev/null || :

touch --no-create %{_datadir}/icons/hicolor >& /dev/null || :

%pre
if [ "$1" -gt 1 ]; then
  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
  gconftool-2 --makefile-uninstall-rule %{_sysconfdir}/gconf/schemas/gconf-editor.schemas > /dev/null || :
fi

%preun
if [ "$1" -eq 0 ]; then
  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
  gconftool-2 --makefile-uninstall-rule %{_sysconfdir}/gconf/schemas/gconf-editor.schemas > /dev/null || :
fi

%postun
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor &>/dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS NEWS README COPYING
%{_bindir}/gconf-editor
%{_datadir}/icons/hicolor/*/apps/gconf-editor.png
%{_datadir}/gconf-editor
%{_datadir}/applications/gnome-gconf-editor.desktop
%{_mandir}/man1/gconf-editor.1.gz
%{_sysconfdir}/gconf/schemas/gconf-editor.schemas
%dir %{_datadir}/omf/gconf-editor

%changelog
* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 3.0.1-2
- 为 Magic 3.0 重建

* Tue Nov 22 2011 Tomas Bzatek <tbzatek@redhat.com> - 3.0.1-1
- Update to 3.0.1

* Sat May 07 2011 Christopher Aillon <caillon@redhat.com> - 3.0.0-2
- Update icon cache scriptlet

* Mon Apr 04 2011 Cosimo Cecchi <cosimoc@redhat.com> - 3.0.0-1
* Update to 3.0.0

* Mon Mar  7 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.91.1-1
- Update to 2.91.91.1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.32.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 Matthias Clasen <mclasen@redhat.com> - 2.32.0-1
- Update to 2.32.0

* Thu Aug  5 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.6-1
- Update to 2.31.6

* Tue Jul 13 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.5-1
- Update to 2.31.5

* Tue Mar 30 2010 Matthias Clasen <mclasen@redhat.com> - 2.30.0-1
- Update to 2.30.0

* Thu Mar 11 2010 Matthias Clasen <mclasen@redhat.com> - 2.29.92-1
- Update to 2.29.92

* Mon Sep 21 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.0-1
- Update to 2.28.0

* Mon Aug 24 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.91-1
- Update to 2.27.91

* Wed Jul 29 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.0-3
- Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.26.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 12 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.0-2
- Port to PolicyKit 1

* Tue Mar 17 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.0-1
- Update to 2.26.0

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.91-1
- Update to 2.25.91

* Mon Oct 20 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.1-1
- Update to 2.24.1

* Tue Sep 23 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0.1-1
- Update to 2.24.0.1

* Tue Sep 23 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-2
- Update to 2.24.0

* Tue Sep  2 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.91-1
- Update to 2.23.91

* Sat Jul 26 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.0-2
- Fix missing icon

* Mon Mar 10 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.0-1
- Update to 2.22.0

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.20.0-3
- Autorebuild for GCC 4.3

* Sun Nov 18 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.0-2
- Correct license field
- Minor spec file cleanups

* Tue Sep 18 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.0-1
- Update to 2.20.0

* Fri Sep 14 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.92-1
- Update to 2.19.92

* Mon Sep  3 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.2-1
- Update to 2.18.2

* Thu Aug 23 2007 Adam Jackson <ajax@redhat.com> - 2.18.0-3
- Rebuild for build ID

* Wed Aug  8 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.0-2
- Update the license field
- Use %%find_lang for help files
 
* Wed Mar 13 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.0-1
- Update to 2.18.0

* Fri Feb 23 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.0-2
- Fix small issues

* Tue Dec 19 2006 Matthias Clasen <mclasen@redhat.com> - 2.17.0-1
- Update to 2.17.0

* Wed Oct 18 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.0-3
- Fix scripts according to packaging guidelines

* Thu Sep  7 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.0-2.fc6
- Require scrollkeeper for %%post and %%postun

* Mon Sep  4 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.0-1.fc6
- Update to 2.16.0

* Sat Aug 12 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.91-1.fc6
- Update to 2.15.91

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.14.0-4.1
- rebuild

* Fri Jun  9 2006 Matthias Clasen <mclasen@redhat.com> 2.14.0-4
- Add missing BuildRequires

* Tue Jun  6 2006 Matthias Clasen <mclasen@redhat.com> 2.14.0-3
- Rebuild

* Tue Mar 28 2006 Ray Strode <rstrode@redhat.com> - 2.14.0-2
- Use gconf_value_free instead of g_free (bug 186479)

* Mon Mar 13 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.0-1
- Update to 2.14.0

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.13.90-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.13.90-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan 30 2006 Matthias Clasen <mclasen@redhat.com> 2.13.90-1
- Update to 2.13.90

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov 30 2005 Matthias Clasen <mclasen@redhat.com> 2.12.1-1
- Update to 2.12.1

* Wed Oct 12 2005 Ray Strode <rstrode@redhat.com> 2.12.0-2
- uninstall schemas when removing rpm

* Thu Sep  8 2005 Matthias Clasen <mclasen@redhat.com> 2.12.0-1
- Update to 2.12.0

* Wed Apr 27 2005 Jeremy Katz <katzj@redhat.com> - 2.10.0-5
- fix the %%post to install the gconf schema correctly too (#152238)

* Wed Apr 27 2005 Jeremy Katz <katzj@redhat.com> - 2.10.0-4
- silence %%post

* Mon Mar 28 2005 Christopher Aillon <caillon@redhat.com>
- rebuilt

* Fri Mar 25 2005 Christopher Aillon <caillon@redhat.com> 2.10.0-2
- Update the GTK+ theme icon cache on (un)install

* Thu Mar 17 2005 Ray Strode <rstrode@redhat.com> - 2.10.0-1
- Update to upstream version 2.10.0

* Wed Mar  2 2005 Mark McLoughlin <markmc@redhat.com> 2.9.91-2
- Rebuild with gcc4

* Fri Feb 11 2005 Matthias Clasen <mclasen@redhat.com> 2.9.91-1
- Update to 2.9.91

* Fri Jan 28 2005 Matthias Clasen <mclasen@redhat.com> 2.9.3-1
- Update to 2.9.3

* Tue Oct 12 2004 Mark McLoughlin <markmc@redhat.com> 2.8.0-2
- Add patch to fix warnings on startup (#132164)
- Add BuildRequies: scrollkeeper

* Tue Sep 21 2004 Mark McLoughlin <markmc@redhat.com> 2.8.0-1
- Update to 2.8.0

* Mon Aug 30 2004 Mark McLoughlin <markmc@redhat.com> 2.7.91-1
- Update to 2.7.91

* Tue Aug  3 2004 Mark McLoughlin <markmc@redhat.com> 2.7.90-1
- Update to 2.7.90
- Install schemas, require libgnomeui and package help docs

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Jun  4 2004 Mark McLoughlin <markmc@redhat.com> 2.6.0-2
- Add BuildRequires: perl-XML-Parser (bug #124168)

* Wed Mar 31 2004 Mark McLoughlin <markmc@redhat.com> 2.6.0-1
- Update to 2.6.0

* Wed Mar 10 2004 Mark McLoughlin <markmc@redhat.com> 2.5.91-1
- Update to 2.5.91

* Tue Feb 24 2004 Mark McLoughlin <markmc@redhat.com> 2.5.4-1
- Update to 2.5.4
- Remove extraneous fontconfig BuildRequires
- Package manpages

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Oct  3 2003 Alexander Larsson <alexl@redhat.com> 2.4.0-1
- 2.4.0

* Wed Aug 20 2003 Alexander Larsson <alexl@redhat.com> 2.3.6-1
- update for gnome 2.3

* Wed Jul 30 2003 Havoc Pennington <hp@redhat.com> 0.5.0-2
- rebuild

* Tue Jul  8 2003 Havoc Pennington <hp@redhat.com> 0.5.0-1
- 0.5.0

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 14 2003 Havoc Pennington <hp@redhat.com> 0.4.0-3
- nuke buildreq Xft

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Sun Jan 12 2003 Havoc Pennington <hp@redhat.com>
- 0.4

* Mon Dec  9 2002 Havoc Pennington <hp@redhat.com>
- 0.3.1

* Thu Aug  8 2002 Havoc Pennington <hp@redhat.com>
- 0.3

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun Jun 16 2002 Havoc Pennington <hp@redhat.com>
- require gconf 1.2.0, rebuild with that
- use desktop-file-install for .desktop file
- include .desktop file and pixmaps in file list

* Fri Jun 07 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Tue Jun 04 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon May 20 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Mon May 20 2002 Havoc Pennington <hp@redhat.com>
- 0.2

* Fri May  3 2002 Havoc Pennington <hp@redhat.com>
- rebuild with new libs

* Fri May 03 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Wed Apr 17 2002 Havoc Pennington <hp@redhat.com>
- Initial build.

