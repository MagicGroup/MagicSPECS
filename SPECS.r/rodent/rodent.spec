%global   with_rodentfgr     1
%global   with_rodentdiff    1
%global   with_rodenticonmgr 1
%global   with_rodentfm      1

Name:  rodent
Summary: Advanced user file manager for Linux/BSD systems
Summary(zh_CN.UTF-8): Linux/BSD 系统下的高级用户文件管理器
Version:	5.3.16
Release:	1%{?dist}
License: GPLv3+
URL: http://xffm.org/
Source0: http://sourceforge.net/projects/xffm/files/%{version}.5/rodent-%{version}.3.tar.bz2

BuildRequires: gtk3-devel
BuildRequires: libxml2-devel
BuildRequires: file-devel
BuildRequires: libtool
BuildRequires: intltool
BuildRequires: libSM-devel
BuildRequires: librsvg2-devel
BuildRequires: libzip-devel
BuildRequires: dbh-devel >= 5.0.13
BuildRequires: tubo-devel >= 5.0.14
BuildRequires: librfm-devel >= 5.3.16-4
BuildRequires: desktop-file-utils, chrpath, procps-ng
BuildRequires:  libappstream-glib

##Fix Rodent-fgr appdata file
Patch0: rodent-fix_appdata_files.patch

%description
Rodent is fast, small and powerful parallel file manager. All operations are
done in threads, and command are inherited from the GNU or BSD operating
systems to reduce the possibility of bugs to a minimum.

%description -l zh_CN.UTF-8
Linux/BSD 系统下的高级用户文件管理器。

%if 0%{?with_rodentfgr}
%package -n  rodent-fgr
Summary:     Search tool for Rodent
Summary(zh_CN.UTF-8): %{name} 的搜索工具
Requires:    %{name}%{?_isa} = %{version}-%{release}

%description -n rodent-fgr
Search tool for Rodent. Uses fgr and grep.
Rodent is fast, small and powerful parallel file manager. All operations are
done in threads, and command are inherited from the GNU or BSD operating
systems to reduce the possibility of bugs to a minimum.
%description -n rodent-fgr -l zh_CN.UTF-8
%{name} 的搜索工具。
%endif #with_rodentfgr

%if 0%{?with_rodentdiff}
%package -n  rodent-diff
Summary:     Differences tool for Rodent
Summary(zh_CN.UTF-8): %{name} 的对比工具
Requires:    %{name}%{?_isa} = %{version}-%{release}

%description -n rodent-diff
Differences tool for Rodent. Uses system diff application (GNU or BSD).
Rodent is fast, small and powerful parallel file manager. All operations are
done in threads, and command are inherited from the GNU or BSD operating
systems to reduce the possibility of bugs to a minimum.
%description -n rodent-diff -l zh_CN.UTF-8
%{name} 的对比工具。
%endif #with_rodentdiff

%if 0%{?with_rodenticonmgr}
%package -n  rodent-iconmgr
Summary:     Icon customization dialog for Rodent applications
Summary(zh_CN.UTF-8): %{name} 的图标定制对话框
Requires:    %{name}%{?_isa} = %{version}-%{release}

%description -n rodent-iconmgr
Icon customization dialog for Rodent applications.
Rodent is fast, small and powerful parallel file manager. All operations are
done in threads, and command are inherited from the GNU or BSD operating
systems to reduce the possibility of bugs to a minimum.
%description -n rodent-iconmgr -l zh_CN.UTF-8
%{name} 的图标定制对话框。
%endif #with_rodenticonmgr

%if 0%{?with_rodentpkg}
%package -n  rodent-pkg
Summary:     Icon customization dialog for Rodent applications
Requires:    %{name}%{?_isa} = %{version}-%{release}

%description -n rodent-pkg
Search tool for Rodent. Uses fgr and grep.
Rodent is fast, small and powerful parallel file manager. All operations are
done in threads, and command are inherited from the GNU or BSD operating
systems to reduce the possibility of bugs to a minimum.
%endif #with_rodentpkg

%prep
%setup -q -n %{name}-%{version}.3

%patch0 -p0

%build
%configure --enable-static=no --enable-shared=yes \
 --disable-silent-rules --enable-ftp --enable-bluetooth
make %{?_smp_mflags} CFLAGS="%{optflags}" 


%install
make install DESTDIR=$RPM_BUILD_ROOT
magic_rpm_clean.sh 
%find_lang rodent-fgr --with-gnome
%find_lang rodent-diff --with-gnome
%find_lang rodent-iconmgr --with-gnome
%find_lang rodent-fm --with-gnome
%find_lang fgr --with-gnome
%find_lang rodent-pkg --with-gnome
%find_lang rodent-dotdesktop --with-gnome
%find_lang rodent-fstab --with-gnome
%find_lang rodent-ps --with-gnome
%find_lang rodent-samba --with-gnome
%find_lang rodent-fuse --with-gnome

## Remove libtool archives
find $RPM_BUILD_ROOT -name '*.la' -delete

## Remove pkg-config file.
## It's used just by who are building and installing from source
rm -f $RPM_BUILD_ROOT%{_libdir}/pkgconfig/%{name}.pc

%post
/bin/touch --no-create %{_datadir}/icons/rfm &>/dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/update-desktop-database &> /dev/null || :

%postun 
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/rfm &>/dev/null || :
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/rfm &>/dev/null || :
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
/usr/bin/update-desktop-database &> /dev/null || :

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/rfm &>/dev/null || :
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%check
desktop-file-edit --set-icon=%{_datadir}/pixmaps/rodent-smb.svg $RPM_BUILD_ROOT%{_datadir}/applications/Rodent-samba.desktop
desktop-file-edit --set-icon=%{_datadir}/icons/rfm/48x48/apps/rodent-root.png $RPM_BUILD_ROOT%{_datadir}/applications/Rodent-root.desktop
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/*.desktop
appstream-util validate-relax --nonet $RPM_BUILD_ROOT%{_datadir}/appdata/*.appdata.xml

%files -f rodent-fm.lang -f fgr.lang -f rodent-pkg.lang -f rodent-dotdesktop.lang -f rodent-fstab.lang -f rodent-ps.lang -f rodent-samba.lang -f rodent-fuse.lang
%doc apps/README ChangeLog AUTHORS apps/rodent-fm/docs/RTFM/RTFM.pdf
%license COPYING
%{_bindir}/rodent
%{_bindir}/rodent-root
%{_bindir}/rodent-anim
%{_bindir}/fgr
%{_bindir}/rodent-plug
%{_bindir}/rodent-desk
%{_bindir}/rodent-fm
%{_bindir}/rodent-getpass
%dir %{_libdir}/rfm/plugins
%{_libdir}/rfm/plugins/libfstab.so
%{_libdir}/rfm/plugins/libecryptfs.so
%{_libdir}/rfm/plugins/libfuse.so
%{_libdir}/rfm/plugins/libdotdesktop.so
%{_libdir}/rfm/plugins/libps.so
%{_libdir}/rfm/plugins/libftp.so
%{_libdir}/rfm/plugins/libnfs.so
%{_libdir}/rfm/plugins/libsftp.so
%{_libdir}/rfm/plugins/libshares.so
%{_libdir}/rfm/plugins/libsmb.so
%{_libdir}/rfm/plugins/libcifs.so
%{_libdir}/rfm/plugins/libworkgroup.so
%{_libdir}/rfm/plugins/libpkg.so
%{_libdir}/rfm/plugins/xml/
%dir %{_libdir}/rfm/modules
%{_libdir}/rfm/modules/libgridview.so
%{_libdir}/rfm/modules/libdeskview.so
%{_datadir}/appdata/Rodent.appdata.xml
%{_datadir}/appdata/Rodent-pkg.appdata.xml
%{_datadir}/appdata/Rodent-dotdesktop.appdata.xml
%{_datadir}/appdata/Rodent-fstab.appdata.xml
%{_datadir}/appdata/Rodent-fuse.appdata.xml
%{_datadir}/appdata/Rodent-ps.appdata.xml
%{_datadir}/appdata/Rodent-samba.appdata.xml
%{_datadir}/icons/rfm/48x48/
%{_datadir}/icons/rfm/animated/
%{_datadir}/icons/hicolor/scalable/apps/*.svg
%{_datadir}/applications/Rodent.desktop 
%{_datadir}/applications/Rodent-root.desktop
%{_datadir}/applications/Rodent-dotdesktop.desktop
%{_datadir}/applications/Rodent-fstab.desktop
%{_datadir}/applications/Rodent-ps.desktop
%{_datadir}/applications/Rodent-pkg.desktop
%{_datadir}/applications/Rodent-fuse.desktop
%{_datadir}/applications/Rodent-samba.desktop
%{_datadir}/pixmaps/rodent.svg
%{_datadir}/pixmaps/rodent-diff.svg
%{_datadir}/pixmaps/rodent-fgr.svg
%{_datadir}/pixmaps/rodent-cifs.svg
%{_datadir}/pixmaps/rodent-dotdesktop.svg
%{_datadir}/pixmaps/rodent-ecryptfs.svg
%{_datadir}/pixmaps/rodent-fstab.svg
%{_datadir}/pixmaps/rodent-ftp.svg
%{_datadir}/pixmaps/rodent-nfs.svg
%{_datadir}/pixmaps/rodent-obex.svg
%{_datadir}/pixmaps/rodent-ps.svg
%{_datadir}/pixmaps/rodent-shares.svg
%{_datadir}/pixmaps/rodent-smb.svg
%{_datadir}/pixmaps/rodent-sshfs.svg
%{_datadir}/pixmaps/rodent-workgroup.svg
%{_datadir}/pixmaps/rodent-fuse.svg
%{_datadir}/pixmaps/rodent-pkg.svg
%{_mandir}/man1/%{name}.1* 
%{_mandir}/man1/%{name}-fm.1*
%{_mandir}/man1/fgr.1* 
%{_mandir}/man1/%{name}-plug.1*
%{_mandir}/man1/%{name}-anim.1*  
%{_mandir}/man1/%{name}-desk.1* 
%{_mandir}/man1/%{name}-getpass.1*
%{_mandir}/man1/%{name}-root.1*
%{_mandir}/man1/%{name}-pkg.1*

%if 0%{?with_rodentfgr}
%files -n rodent-fgr -f rodent-fgr.lang
%{_bindir}/%{name}-fgr
%{_datadir}/icons/rfm/48x48/apps/%{name}-fgr.png
%{_datadir}/icons/hicolor/scalable/apps/%{name}-fgr.svg
%{_datadir}/applications/Rodent-fgr.desktop
%{_datadir}/pixmaps/%{name}-fgr.svg
%{_datadir}/appdata/Rodent-fgr.appdata.xml
%{_mandir}/man1/%{name}-fgr.1*
%endif #with_rodentfgr

%if 0%{?with_rodentdiff}
%files -n rodent-diff -f rodent-diff.lang
%{_bindir}/%{name}-diff
%{_datadir}/icons/rfm/48x48/apps/%{name}-diff.png
%{_datadir}/icons/hicolor/scalable/apps/%{name}-diff.svg
%{_datadir}/applications/Rodent-diff.desktop
%{_datadir}/pixmaps/%{name}-diff.svg
%{_datadir}/appdata/Rodent-diff.appdata.xml
%{_mandir}/man1/%{name}-diff.1*
%endif #with_rodentdiff

%if 0%{?with_rodenticonmgr}
%files -n rodent-iconmgr -f rodent-iconmgr.lang
%{_bindir}/%{name}-iconmgr
%{_datadir}/icons/rfm/48x48/apps/%{name}-iconmgr.png
%{_datadir}/icons/hicolor/scalable/apps/%{name}-iconmgr.svg
%{_datadir}/applications/Rodent-iconmgr.desktop
%{_datadir}/pixmaps/%{name}-iconmgr.svg
%{_datadir}/appdata/Rodent-iconmgr.appdata.xml
%{_mandir}/man1/%{name}-iconmgr.1*
%endif #with_rodenticonmgr

%changelog
* Sun Jul 05 2015 Antonio Trande <sagitterATfedoraproject.org> - 5.3.16-6
- appdata files check

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Antonio Trande <sagitterATfedoraproject.org> 5.3.16-4
- Update to 5.3.16.3
- libobex.so no packaged amymore

* Wed May 06 2015 Remi Collet <remi@fedoraproject.org> - 5.3.16-3
- rebuild for new libzip

* Mon Apr 13 2015 Antonio Trande <sagitterATfedoraproject.org> 5.3.16-2
- Fixed upstream URL

* Fri Apr 10 2015 Antonio Trande <sagitterATfedoraproject.org> 5.3.16-1
- Update to 5.3.16.0

* Sun Feb 01 2015 Antonio Trande <sagitterATfedoraproject.org> 5.3.14-3
- %%{_datadir}/appdata not owned (bz#1188047)

* Tue Jan 06 2015 Antonio Trande <sagitterATfedoraproject.org> 5.3.14-2
- Update to 5.3.14.6

* Mon Dec 15 2014 Antonio Trande <sagitterATfedoraproject.org> 5.3.14-1
- Update to 5.3.14.5
- Added %%license
- Set icon key in Rodent-samba desktop file

* Wed Oct 01 2014 Antonio Trande <sagitterATfedoraproject.org> 5.3.12-2
- Added iconview patch

* Sun Sep 28 2014 Antonio Trande <sagitterATfedoraproject.org> 5.3.12-1
- Update to 5.3.12
- libtubo and DBH minimum release changed
- rodent now requires gtk3 by default

* Mon Jul 14 2014 Antonio Trande <sagitterATfedoraproject.org> 5.2.9-1
- Release 5.2.9

* Sat Mar 22 2014 Antonio Trande <sagitterATfedoraproject.org> 5.2.8-1
- Release 5.2.8

* Sun Mar 09 2014 Antonio Trande <sagitterATfedoraproject.org> 5.2.7-1
- Update to a 5.2.7
- Rodent-pkg plugin packaged
- librfm minimum version request changed to 5.2.8

* Fri Feb 28 2014 Antonio Trande <sagitterATfedoraproject.org> 5.2.6-1
- Update to a 5.2.6

* Sat Feb 22 2014 Antonio Trande <sagitterATfedoraproject.org> 5.2.5-1
- Update to a 5.2.5

* Wed Feb 19 2014 Antonio Trande <sagitterATfedoraproject.org> 5.2.4-1
- Update to a 5.2.4

* Sun Feb 09 2014 Antonio Trande <sagitterATfedoraproject.org> 5.2.3-1.20140207gitd1d6a2
- Update to a 5.2.3 post-release (d1d6a2) from git
- librfm minimum version request changed to 5.2.3
- Rodent apps splitted in own sub-packages
- Perform autogen.sh to create system specific build files

* Sat Jan 11 2014 Antonio Trande <sagitterATfedoraproject.org> 5.2.1-1
- Update to 5.2.1
- Removed ldconfig calls
- Added --enable-bluetooth option to configure
- Devel package is not built anymore

* Tue Jan 07 2014 Antonio Trande <sagitterATfedoraproject.org> 5.2.0-2
- DBH minimum release changed 

* Sun Dec 29 2013 Antonio Trande <sagitterATfedoraproject.org> 5.2.0-1
- Update to 5.2.0
- URL tag changed
- %%check section added
- Description changed
- Defined CFLAGS in %%build
- Devel subpackage building

* Sun Oct 13 2013 Antonio Trande <sagitterATfedoraproject.org> 5.1.3-2
- Requires dependencies removed
- BuildRequires minimum versions removed

* Sat Oct 12 2013 Antonio Trande <sagitterATfedoraproject.org> 5.1.3-1
- Update to 5.1.3 - In this release all primary libraries (librfm) 
  are split off into their own package
- Added 'librfm-devel >= 5.1.0' BR
- Patch exchanged with 'sed' commands in %%build section  

* Mon Oct 07 2013 Antonio Trande <sagitterATfedoraproject.org> 5.1.2-1
- First package
