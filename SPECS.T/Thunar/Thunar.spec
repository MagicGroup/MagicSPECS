%global minorversion 1.4

Name:           Thunar
Version:        1.4.0
Release:        3%{?dist}
Summary:        Thunar File Manager

Group:          User Interface/Desktops
License:        GPLv2+
URL:            http://thunar.xfce.org/
#VCS git:git://git.xfce.org/xfce/thunar
Source0:        http://archive.xfce.org/src/xfce/thunar/%{minorversion}/%{name}-%{version}.tar.bz2
Source1:        thunar-sendto-bluetooth.desktop
Source2:        thunar-sendto-audacious-playlist.desktop
Source3:        thunar-sendto-quodlibet-playlist.desktop
Patch1:         Thunar-1.3.1-desktop-fix.patch
Buildroot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  pkgconfig(dbus-glib-1) >= 0.34
BuildRequires:  pkgconfig(exo-1) >= 0.6.0
BuildRequires:  pkgconfig(gudev-1.0) >= 145
BuildRequires:  pkgconfig(libexif) >= 0.6.0
BuildRequires:  pkgconfig(libpcre) >= 6.0
BuildRequires:  pkgconfig(libstartup-notification-1.0) >= 0.4
BuildRequires:  pkgconfig(libnotify) >= 0.4.0
BuildRequires:  pkgconfig(libxfce4ui-1) >= 4.9.0
BuildRequires:  pkgconfig(libxfce4panel-1.0) >= 4.9.0
BuildRequires:  freetype-devel
BuildRequires:  libpng-devel >= 2:1.2.2-16
BuildRequires:  libICE-devel
BuildRequires:  pkgconfig
BuildRequires:  intltool gettext
BuildRequires:  desktop-file-utils >= 0.7
BuildRequires:  gtk-doc
Requires:       shared-mime-info
Requires:       dbus-x11

# obsolete xffm to allow for smooth upgrades
Provides:       xffm = 4.2.4
Obsoletes:      xffm <= 4.2.3-5.fc6

# thunar-shares-plugin isn't in F15
Provides:       thunar-shares-plugin = 0.2.0-4
Obsoletes:      thunar-shares-plugin <= 0.2.0-3.fc15

# Provide lowercase name to help people find the package. 
Provides:       thunar = %{version}-%{release}

%description
Thunar is a new modern file manager for the Xfce Desktop Environment. It has 
been designed from the ground up to be fast and easy-to-use. Its user interface 
is clean and intuitive, and does not include any confusing or useless options. 
Thunar is fast and responsive with a good start up time and directory load time.

%package devel
Summary: Development tools for Thunar file manager
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig
Requires: exo-devel >= %{exoversion}

%description devel
libraries and header files for the Thunar file manager.

%prep
%setup -q

%patch1 -p1

# fix icon in thunar-sendto-email.desktop
sed -i 's!internet-mail!mail-message-new!' \
        plugins/thunar-sendto-email/thunar-sendto-email.desktop.in.in

%build
%configure --enable-dbus --enable-gtk-doc
# Remove rpaths
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

# The LD_LIBRARY_PATH hack is needed for --enable-gtk-doc
# because lt-thunarx-scan is linked against libthunarx
export LD_LIBRARY_PATH=$( pwd )/thunarx/.libs

make %{?_smp_mflags} V=1


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT mandir=%{_mandir}

make -C examples distclean

# 2 of the example files need to not be executable 
# so they don't pull in dependencies. 
chmod 644 examples/thunar-file-manager.py
chmod 644 examples/xfce-file-manager.py

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
magic_rpm_clean.sh
%find_lang Thunar

desktop-file-install --vendor magic --delete-original          \
        --dir ${RPM_BUILD_ROOT}%{_datadir}/applications         \
        ${RPM_BUILD_ROOT}%{_datadir}/applications/thunar-settings.desktop

desktop-file-install --vendor magic --delete-original          \
        --dir ${RPM_BUILD_ROOT}%{_datadir}/applications         \
        --delete-original                                       \
        ${RPM_BUILD_ROOT}%{_datadir}/applications/Thunar-bulk-rename.desktop

desktop-file-install --vendor magic --delete-original          \
        --dir ${RPM_BUILD_ROOT}%{_datadir}/applications         \
        --remove-mime-type x-directory/gnome-default-handler    \
        --remove-mime-type x-directory/normal                   \
        ${RPM_BUILD_ROOT}%{_datadir}/applications/Thunar-folder-handler.desktop

desktop-file-install --vendor magic --delete-original          \
        --dir ${RPM_BUILD_ROOT}%{_datadir}/applications         \
        ${RPM_BUILD_ROOT}%{_datadir}/applications/Thunar.desktop

# install additional sendto helpers
desktop-file-install --vendor ""                                \
        --dir ${RPM_BUILD_ROOT}%{_datadir}/Thunar/sendto        \
        %{SOURCE1}

desktop-file-install --vendor ""                                \
        --dir ${RPM_BUILD_ROOT}%{_datadir}/Thunar/sendto        \
        %{SOURCE2}

desktop-file-install --vendor ""                                \
        --dir ${RPM_BUILD_ROOT}%{_datadir}/Thunar/sendto        \
        %{SOURCE3}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
for target in %{_defaultdocdir}/Thunar/html/*/images
do
       if [ -d $target ]
       then
               rm -rf $target
       fi
done

%post
/usr/sbin/ldconfig
update-desktop-database &> /dev/null ||:
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :


%postun
/usr/sbin/ldconfig
update-desktop-database &> /dev/null ||:
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi


%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files -f Thunar.lang
%defattr(-,root,root,-)
%doc README TODO ChangeLog NEWS INSTALL COPYING AUTHORS HACKING THANKS
%doc docs/README.gtkrc
%doc docs/README.thunarrc
# exclude docs that we have moved to the above
%exclude %{_datadir}/doc/Thunar/README.gtkrc
%exclude %{_datadir}/doc/Thunar/README.thunarrc
%{_bindir}/Thunar
%{_bindir}/thunar
%{_bindir}/thunar-settings
%{_libdir}/libthunar*.so.*
%dir %{_libdir}/thunarx-*/
%{_libdir}/thunarx-*/thunar*.so
%dir %{_libdir}/Thunar/
%{_libdir}/Thunar/ThunarBulkRename
%{_libdir}/Thunar/thunar-sendto-email
%dir %{_datadir}/Thunar/
%dir %{_datadir}/Thunar/sendto/
%{_datadir}/Thunar/sendto/*.desktop
%{_datadir}/applications/*.desktop
%{_datadir}/dbus-1/services/org.xfce.FileManager.service
%{_datadir}/dbus-1/services/org.xfce.Thunar.service
%{_datadir}/doc/%{name}/
%{_datadir}/icons/hicolor/*/*/*
%{_datadir}/pixmaps/Thunar/
%{_datadir}/xfce4/panel-plugins/thunar-tpa.desktop
%{_libdir}/xfce4/panel/plugins/libthunar-tpa.so
%{_mandir}/man1/Thunar.1*
%dir %{_sysconfdir}/xdg/Thunar
%config(noreplace) %{_sysconfdir}/xdg/Thunar/uca.xml

%files devel
%defattr(-,root,root,-)
%doc examples
%{_includedir}/thunarx-*/
%{_libdir}/libthunar*.so
%{_libdir}/pkgconfig/thunarx-*.pc
%doc %{_datadir}/gtk-doc/html/*


%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1.4.0-3
- 为 Magic 3.0 重建

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Apr 29 2012 Christoph Wickert <cwickert@fedoraproject.org> - 4.10.0-1
- Update to 1.4.0 (Xfce 4.10 final)
- Make build verbose
- Add VCS key

* Sat Apr 14 2012 Kevin Fenzi <kevin@scrye.com> - 1.3.2-1
- Update to 1.3.2 (Xfce 4.10pre2)

* Mon Apr 02 2012 Kevin Fenzi <kevin@scrye.com> - 1.3.1-1
- Update to 1.3.1

* Fri Feb 10 2012 Petr Pisar <ppisar@redhat.com> - 1.3.0-7
- Rebuild against PCRE 8.30

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 10 2011 Christoph Wickert <cwickert@fedoraproject.org> - 1.3.0-5
- Own %%{_libdir}/Thunar/

* Wed Apr 21 2011 Christoph Wickert <cwickert@fedoraproject.org> - 1.3.0-4
- Fix format string flaw CVE-2011-1588 (#698290)

* Tue Mar 15 2011 Christoph Wickert <cwickert@fedoraproject.org> - 1.3.0-3
- Add missing BRs: libexif-devel, libICE-devel and libnotify-devel

* Tue Mar 08 2011 Christoph Wickert <cwickert@fedoraproject.org> - 1.3.0-2
- Obsolete old plugins (#682491)
- Add sendto helper for quodlibet

* Mon Feb 14 2011 Christoph Wickert <cwickert@fedoraproject.org> - 1.3.0-1
- Update to 1.3.0

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 30 2011 Kevin Fenzi <kevin@tummy.com> - 1.2.1-1
- Update to 1.2.1

* Sat Jan 22 2011 Kevin Fenzi <kevin@tummy.com> - 1.2.0-2
- Add hack for upgrades (works around bug #670210)

* Sun Jan 16 2011 Kevin Fenzi <kevin@tummy.com> - 1.2.0-1
- Update to 1.2.0

* Sun Jan 02 2011 Christoph Wickert <cwickert@fedoraproject.org> - 1.1.6-1
- Update to 1.1.6

* Sun Dec 05 2010 Christoph Wickert <cwickert@fedoraproject.org> - 1.1.5-1
- Update to 1.1.5

* Mon Nov 08 2010 Christoph Wickert <cwickert@fedoraproject.org> - 1.1.4-1
- Update to 1.1.4
- Drop obsolete build requirements: GConf2-devel, fam-devel, hal-devel, 
  libjpeg-devel, libxslt-devel.
- Remove old patches

* Mon Nov 01 2010 Kevin Fenzi <kevin@tummy.com> - 1.0.2-4
- Add patch for trash icon. (#647734)

* Sat Oct 16 2010 Kevin Fenzi <kevin@tummy.com> - 1.0.2-3
- Add patch for Drag and drop issue. (#633171)

* Thu Jun 17 2010 Christoph Wickert <cwickert@fedoraproject.org> - 1.0.2-2
- Fix conditional requirement for hal-storage-addon

* Fri May 21 2010 Kevin Fenzi <kevin@tummy.com> - 1.0.2-1
- Update to 1.0.2

* Fri Apr 30 2010 Christoph Wickert <cwickert@fedoraproject.org> - 1.0.1-7
- Require hal-storage-addon
- Remove obsolete mime types (#587256)
- Update icon-cache scriptlets

* Thu Apr 15 2010 Kevin Fenzi <kevin@tummy.com> - 1.0.1-6
- Bump release

* Thu Apr 15 2010 Kevin Fenzi <kevin@tummy.com> - 1.0.1-5
- Add patch to fix directory umask issue. Fixes bug #579087

* Sat Feb 13 2010 Kevin Fenzi <kevin@tummy.com> - 1.0.1-4
- Add patch for DSO linking. Fixes bug #564714

* Thu Sep 10 2009 Kevin Fenzi <kevin@tummy.com> - 1.0.1-3
- Require dbus-x11 (#505499)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Apr 19 2009 Kevin Fenzi <kevin@tummy.com> - 1.0.1-1
- Update to 1.0.1

* Thu Feb 26 2009 Kevin Fenzi <kevin@tummy.com> - 1.0.0-1
- Update to 1.0.0

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.99.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 26 2009 Kevin Fenzi <kevin@tummy.com> - 0.9.99.1-1
- Update to 0.9.99.1

* Tue Jan 13 2009 Kevin Fenzi <kevin@tummy.com> - 0.9.93-1
- Update to 0.9.93

* Fri Dec 26 2008 Kevin Fenzi <kevin@tummy.com> - 0.9.92-1
- Update to 0.9.92

* Mon Oct 27 2008 Christoph Wickert <cwickert@fedoraproject.org> - 0.9.3-1
- Update to 0.9.3
- Respect xdg user directory paths (#457740)
- Don't spawn zombies (bugzilla.xfce.org #2983)
- Add additional sendto helpers for bluethooth and audaciuos (#450784)

* Sat Feb 23 2008 Kevin Fenzi <kevin@tummy.com> - 0.9.0-4
- Remove requires on xfce-icon-theme. See bug 433152

* Sun Feb 10 2008 Kevin Fenzi <kevin@tummy.com> - 0.9.0-3
- Rebuild for gcc43

* Mon Dec  3 2007 Kevin Fenzi <kevin@tummy.com> - 0.9.0-2
- Add thunar-vfs patch. 

* Sun Dec  2 2007 Kevin Fenzi <kevin@tummy.com> - 0.9.0-1
- Update to 0.9.0

* Mon Aug 27 2007 Kevin Fenzi <kevin@tummy.com> - 0.8.0-3
- Update License tag

* Mon Jul  9 2007 Kevin Fenzi <kevin@tummy.com> - 0.8.0-2
- Add provides for lowercase name

* Sun Jan 21 2007 Kevin Fenzi <kevin@tummy.com> - 0.8.0-1
- Upgrade to 0.8.0

* Mon Dec 18 2006 Kevin Fenzi <kevin@tummy.com> - 0.5.0-0.3.rc2
- Own the thunarx-1 directory

* Sat Nov 11 2006 Kevin Fenzi <kevin@tummy.com> - 0.5.0-0.2.rc2
- Increase exo version 

* Thu Nov 09 2006 Kevin Fenzi <kevin@tummy.com> - 0.5.0-0.1.rc2
- Upgrade to 0.5.0rc2

* Mon Oct 09 2006 Kevin Fenzi <kevin@tummy.com> - 0.4.0-0.11.rc1
- Add shared-mime-info and xfce4-icon-theme as Requires (fixes #209592)

* Fri Oct 06 2006 Kevin Fenzi <kevin@tummy.com> - 0.4.0-0.10.rc1
- Tweak Obsoletes versions

* Fri Oct 06 2006 Kevin Fenzi <kevin@tummy.com> - 0.4.0-0.9.rc1
- Obsolete xffm for now. 

* Thu Oct 05 2006 Kevin Fenzi <kevin@tummy.com> - 0.4.0-0.8.rc1
- Really re-enable the trash plugin. 

* Thu Oct 05 2006 Kevin Fenzi <kevin@tummy.com> - 0.4.0-0.7.rc1
- Re-enable trash plugin in Xfce 4.4rc1

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> - 0.4.0-0.6.rc1
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Sat Sep 16 2006 Kevin Fenzi <kevin@tummy.com> - 0.4.0-0.5.rc1
- Remove duplicate thunar-sendto-email.desktop entry from files. 

* Fri Sep 15 2006 Kevin Fenzi <kevin@tummy.com> - 0.4.0-0.4.rc1
- Added Requires: exo-devel >= 0.3.1.10 to devel. 
- exclude docs moved from datadir to docs
- Fixed datdir including files twice

* Thu Sep 14 2006 Kevin Fenzi <kevin@tummy.com> - 0.4.0-0.3.rc1
- Cleaned up BuildRequires some more
- Disabled tpa plugin and desktop for now
- Moved some files from doc/Thunar to be %%doc
- Changed man to use wildcard in files
- Added examples to devel subpackage
- Made sure some examples are not executable. 

* Tue Sep 12 2006 Kevin Fenzi <kevin@tummy.com> - 0.4.0-0.2.rc1
- Added some BuildRequires
- Added --with-gtkdoc and gtkdoc files to devel

* Wed Sep  6 2006 Kevin Fenzi <kevin@tummy.com> - 0.4.0-0.1.rc1
- Inital package for fedora extras

