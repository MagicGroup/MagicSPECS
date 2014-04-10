%define glib2_version                 2.31.0
%define gtk3_version                  3.5.8
%define udisks_version                2.1.0
%define gnome_settings_daemon_version 3.7.3

# Only enable if using patches that touches configure.ac,
# Makefile.am or other build system related files
#
%define enable_autoreconf 0

Summary: Disks
Summary(zh_CN.UTF-8): GNOME 的磁盘工具
Name: gnome-disk-utility
Version:	3.12.0
Release: 1%{?dist}
License: GPLv2+
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库 
URL: http://git.gnome.org/browse/gnome-disk-utility
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source0: http://download.gnome.org/sources/gnome-disk-utility/%{majorver}/%{name}-%{version}.tar.xz

BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: gtk3-devel >= %{gtk3_version}
BuildRequires: gnome-settings-daemon-devel >= %{gnome_settings_daemon_version}
BuildRequires: gettext
BuildRequires: desktop-file-utils
BuildRequires: libudisks2-devel >= %{udisks_version}
BuildRequires: gnome-common
BuildRequires: intltool
BuildRequires: libsecret-devel
BuildRequires: systemd-devel
# for xsltproc
BuildRequires: libxslt
BuildRequires: docbook-style-xsl
BuildRequires: libpwquality-devel
BuildRequires: libcanberra-devel
BuildRequires: libdvdread-devel
BuildRequires: libnotify-devel

Requires: gnome-icon-theme-symbolic
Requires: udisks2

Obsoletes: gnome-disk-utility-format
Obsoletes: nautilus-gdu
Obsoletes: gnome-disk-utility-libs
Obsoletes: gnome-disk-utility-devel
Obsoletes: gnome-disk-utility-ui-libs
Obsoletes: gnome-disk-utility-ui-devel
Obsoletes: gnome-disk-utility-nautilus

%if 0%{?enable_autoreconf}
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
%endif

%description
This package contains the Disks and Disk Image Mounter applications.
Disks supports partitioning, file system creation, encryption,
fstab/crypttab editing, ATA SMART and other features

%description -l zh_CN.UTF-8
这个包包含了磁盘和磁盘镜像挂载。
支持分区、建立文件系统、加密、fstab/crypttab 编辑、ATA SMART 等功能。

%prep
%setup -q

%build
%if 0%{?enable_autoreconf}
autoreconf
%endif
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/gnome-settings-daemon-3.0/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/gnome-settings-daemon-3.0/*.a

desktop-file-install --delete-original  \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  $RPM_BUILD_ROOT%{_datadir}/applications/gnome-disks.desktop \
  $RPM_BUILD_ROOT%{_datadir}/applications/gnome-disk-image-mounter.desktop
magic_rpm_clean.sh
%find_lang %{name}

%post
for d in hicolor HighContrast ; do
    touch --no-create %{_datadir}/icons/$d &>/dev/null || :
done
update-desktop-database %{_datadir}/applications &> /dev/null

%postun
update-desktop-database %{_datadir}/applications &> /dev/null
if [ $1 -eq 0 ] ; then
    glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :
    for d in hicolor HighContrast ; do
        touch --no-create %{_datadir}/icons/$d &>/dev/null || :
        gtk-update-icon-cache %{_datadir}/icons/$d &>/dev/null || :
    done
fi

%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :
for d in hicolor HighContrast ; do
    gtk-update-icon-cache %{_datadir}/icons/$d &>/dev/null || :
done


%files -f %{name}.lang
%{_bindir}/gnome-disks
%{_bindir}/gnome-disk-image-mounter
%{_datadir}/applications/gnome-disks.desktop
%{_datadir}/applications/gnome-disk-image-mounter.desktop
%{_datadir}/glib-2.0/schemas/org.gnome.Disks.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.plugins.gdu-sd.gschema.xml

#%dir %{_datadir}/gnome-disk-utility
#%{_datadir}/gnome-disk-utility/*.ui
%{_datadir}/icons/hicolor/*/apps/gnome-disks*
%{_datadir}/icons/HighContrast/*/apps/gnome-disks.png
%{_datadir}/applications/gnome-disk-image-writer.desktop

%{_mandir}/man1/*

%{_libdir}/gnome-settings-daemon-3.0/gdu-sd-plugin.gnome-settings-plugin
%{_libdir}/gnome-settings-daemon-3.0/libgdu-sd.so

%doc README AUTHORS NEWS COPYING

%changelog
* Wed Apr 09 2014 Liu Di <liudidi@gmail.com> - 3.12.0-1
- 更新到 3.12.0

* Wed Mar 20 2013 Richard Hughes <rhughes@redhat.com> - 3.8.0-1
- Update to 3.8.0

* Mon Feb 25 2013 Kalev Lember <kalevlember@gmail.com> - 3.7.2-2
- Require gnome-icon-theme-symbolic (#910982)

* Tue Feb 19 2013 Richard Hughes <rhughes@redhat.com> - 3.7.2-1
- Update to 3.7.2

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 07 2013 David Zeuthen <davidz@redhat.com> - 3.7.1-1%{?dist}
- Update to 3.7.1

* Fri Dec 21 2012 David Zeuthen <davidz@redhat.com> - 3.7.0-4%{?dist}
- Add files for the new gnome-settings-daemon plug-in

* Fri Dec 21 2012 David Zeuthen <davidz@redhat.com> - 3.7.0-3%{?dist}
- BR gnome-settings-daemon 3.7.3 and rebuild without --disable-gsd-plugin

* Tue Dec 18 2012 David Zeuthen <davidz@redhat.com> - 3.7.0-2%{?dist}
- Adjust BRs

* Tue Dec 18 2012 David Zeuthen <davidz@redhat.com> - 3.7.0-1%{?dist}
- Update to 3.7.0

* Fri Oct 05 2012 David Zeuthen <davidz@redhat.com> - 3.6.1-1%{?dist}
- Update to 3.6.1

* Sat Sep 22 2012 Kalev Lember <kalevlember@gmail.com> - 3.6.0-1
- Update to 3.6.0
- Drop the -Werror patch; applied upstream
- Add glib-compile-schemas scriptlets
- Relicensed from LGPLv2+ to GPLv2+

* Fri Jul 27 2012 David Zeuthen <davidz@redhat.com> - 3.5.3-2%{?dist}
- Avoid treating warnings as errors

* Fri Jul 27 2012 David Zeuthen <davidz@redhat.com> - 3.5.3-1%{?dist}
- Update to 3.5.3

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 10 2012 Ville Skyttä <ville.skytta@iki.fi> - 3.5.2-2
- Own the %%{_datadir}/gnome-disk-utility dir.

* Tue Jun 05 2012 David Zeuthen <davidz@redhat.com> - 3.5.2-1%{?dist}
- Update to 3.5.2

* Mon May 09 2012 David Zeuthen <davidz@redhat.com> - 3.5.1-4%{?dist}
- BR docbook-style-xsl for man pages

* Mon May 09 2012 David Zeuthen <davidz@redhat.com> - 3.5.1-3%{?dist}
- BR libxslt (for xsltproc)

* Mon May 09 2012 David Zeuthen <davidz@redhat.com> - 3.5.1-2%{?dist}
- BR libgnome-keyring-devel and systemd-devel

* Mon May 09 2012 David Zeuthen <davidz@redhat.com> - 3.5.1-1%{?dist}
- Update to 3.5.1

* Mon Apr 30 2012 Richard Hughes <hughsient@gmail.com> - 3.4.1-1
- Update to 3.4.1

* Mon Mar 26 2012 David Zeuthen <davidz@redhat.com> - 3.4.0-1%{?dist}
- Update to release 3.4.0

* Mon Mar 05 2012 David Zeuthen <davidz@redhat.com> - 3.3.93-1%{?dist}
- Update to release 3.3.93

* Thu Feb 23 2012 David Zeuthen <davidz@redhat.com> - 3.3.92-1%{?dist}
- Update to release 3.3.92

* Mon Feb 06 2012 David Zeuthen <davidz@redhat.com> - 3.3.91-1%{?dist}
- Update to release 3.3.91

* Tue Jan 24 2012 David Zeuthen <davidz@redhat.com> - 3.3.90-3%{?dist}
- Require udisks2 package (for the daemon) (#783974)

* Fri Jan 20 2012 David Zeuthen <davidz@redhat.com> - 3.3.90-2%{?dist}
- Rebuild

* Fri Jan 20 2012 David Zeuthen <davidz@redhat.com> - 3.3.90-1%{?dist}
- Update to release 3.3.90

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 08 2011 Adam Jackson <ajax@redhat.com> - 3.0.2-4
- Rebuild to break bogus libpng dep

* Mon Jul 11 2011 David Zeuthen <davidz@redhat.com> - 3.0.2-3%{?dist}
- BR gtk-doc

* Mon Jul 11 2011 David Zeuthen <davidz@redhat.com> - 3.0.2-2%{?dist}
- BR gnome-common

* Mon Jul 11 2011 David Zeuthen <davidz@redhat.com> - 3.0.2-1%{?dist}
- Update to 3.0.2

* Sat May 07 2011 Christopher Aillon <caillon@redhat.com> - 3.0.0-2
- Update icon cache scriptlet

* Mon Apr  4 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.0-1
- Update to 3.0.0

* Mon Mar 21 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.7-1
- Update to 2.91.7

* Mon Mar 14 2011 Tomas Bzatek <tbzatek@redhat.com> - 2.91.6-5
- Fix gnome-disk-utility-nautilus upgrade path

* Tue Feb 22 2011 Tomas Bzatek <tbzatek@redhat.com> - 2.91.6-4
- Split nautilus extension into a separate package

* Fri Feb 11 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.6-3
- Rebuild against newer gtk

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.91.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.6-1%{?dist}
- Update to 2.91.6

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> - 2.32.1-4%{?dist}
- Rebuild against newer gtk

* Fri Jan  7 2011 Matthias Clasen <mclasen@redhat.com> - 2.32.1-3%{?dist}
- Rebuild against new gtk

* Fri Dec  3 2010 Matthias Clasen <mclasen@redhat.com> - 2.32.1-2%{?dist}
- Rebuild against new gtk

* Thu Nov 11 2010 Matthias Clasen <mclasen@redhat.com> - 2.32.1-1%{?dist}
- 2.32.1

* Fri Nov  5 2010 Matthias Clasen <mclasen@redhat.com> - 2.32.0-3%{?dist}
- Fix a problem with 'disk failure' notifications

* Wed Nov  3 2010 Matthias Clasen <mclasen@redhat.com> - 2.32.0-2%{?dist}
- Rebuild against libnotify 0.7.0

* Tue Sep 28 2010 Matthias Clasen <mclasen@redhat.com> - 2.32.0-1%{?dist}
- Update to 2.32.0

* Wed Jun 16 2010 Matthias Clasen <mclasen@redhat.com> - 2.30.1-2%{?dist}
- Kill the scrollkeeper runtime dep

* Mon Mar 22 2010 David Zeuthen <davidz@redhat.com> - 2.30.1-1%{?dist}
- Update to 2.30.1

* Mon Mar 15 2010 David Zeuthen <davidz@redhat.com> - 2.30.0-1%{?dist}
- Update to 2.30.0

* Tue Feb 23 2010 David Zeuthen <davidz@redhat.com> - 2.29.90-1%{?dist}
- Update to 2.29.90

* Mon Feb 15 2010 David Zeuthen <davidz@redhat.com> - 2.29.0-0.git20100215.3%{?dist}
- Add rarian-compat to BR

* Mon Feb 15 2010 David Zeuthen <davidz@redhat.com> - 2.29.0-0.git20100215.1%{?dist}
- Update to git snapshot
- Drop upstreamed patches

* Mon Jan 18 2010 Tomas Bzatek <tbzatek@redhat.com> - 2.29.0-0.git20100115.2%{?dist}
- Install missing include

* Fri Jan 15 2010 David Zeuthen <davidz@redhat.com> - 2.29.0-0.git20100115.1%{?dist}
- BR avahi-ui-devel

* Fri Jan 15 2010 David Zeuthen <davidz@redhat.com> - 2.29.0-0.git20100115%{?dist}
- Update to git snapshot

* Wed Dec  2 2009 David Zeuthen <davidz@redhat.com> - 2.29.0-0.git20091202%{?dist}
- Update to git snapshot that requires udisks instead of DeviceKit-disks
- The UI has been completely revamped

* Fri Sep 18 2009 David Zeuthen <davidz@redhat.com> - 2.28.0-2%{?dist}
- BR libatasmart-devel

* Fri Sep 18 2009 David Zeuthen <davidz@redhat.com> - 2.28.0-1%{?dist}
- Update to upstream release 2.28.0
- Compared to previous releases, this release should whine less about SMART

* Mon Aug 17 2009 David Zeuthen <davidz@redhat.com> - 0.5-3%{?dist}
- Drop upstreamed patch

* Mon Aug 17 2009 David Zeuthen <davidz@redhat.com> - 0.5-2%{?dist}
- Rebuild

* Mon Aug 17 2009 David Zeuthen <davidz@redhat.com> - 0.5-1%{?dist}
- Update to release 0.5

* Mon Jul 27 2009 Matthias Clasen <mclasen@redhat.com> - 0.4-3%{?dist}
- Drop PolicyKit from .pc files, too

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 19 2009 David Zeuthen <davidz@redhat.com> - 0.4-1%{?dist}
- Update to release 0.4

* Fri May 01 2009 David Zeuthen <davidz@redhat.com> - 0.3-1%{?dist}
- Upstream release 0.3

* Wed Apr 15 2009 David Zeuthen <davidz@redhat.com> - 0.3-0.5.20090415git%{?dist}
- New snapshot

* Sun Apr 12 2009 David Zeuthen <davidz@redhat.com> - 0.3-0.4.20090412git%{?dist}
- New snapshot

* Fri Apr 10 2009 Matthias Clasen <mclasen@redhat.com> - 0.3-0.3.20090406git%{?dist}
- Don't own directories that belong to hicolor-icon-theme

* Wed Apr 08 2009 David Zeuthen <davidz@redhat.com> - 0.3-0.2.20090406git%{?dist}
- Fix bug in detecting when a PolicyKit error is returned (#494787)

* Mon Apr 06 2009 David Zeuthen <davidz@redhat.com> - 0.3-0.1.20090406git%{?dist}
- New snapshot

* Wed Mar 04 2009 David Zeuthen <davidz@redhat.com> - 0.2-2%{?dist}
- Don't crash when changing the LUKS passphrase on a device

* Mon Mar 02 2009 David Zeuthen <davidz@redhat.com> - 0.2-1%{?dist}
- Update to version 0.2

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-0.git20080720.2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 27 2009 Matthias Clasen <mclasen@redhat.com> 0.1-0.git20080720.2%{?dist}
- Rebuild for pkgconfig provides

* Sun Nov 23 2008 Matthias Clasen <mclasen@redhat.com> 0.1-0.git20080720.1%{?dist}
- Improve %%summary and %%description

* Fri Jul 20 2008 David Zeuthen <davidz@redhat.com> - 0.1-0.git20080720%{?dist}
- Initial Packaging
