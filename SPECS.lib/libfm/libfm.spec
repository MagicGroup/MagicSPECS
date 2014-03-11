# Review: https://bugzilla.redhat.com/show_bug.cgi?id=567257

# Upstream git:
# git://pcmanfm.git.sourceforge.net/gitroot/pcmanfm/libfm

%global         usegit      0
%global         mainrel     2

%global         usegtk3     0
%if 0%{?fedora} >= 18
%global         usegtk3     1
%endif

%global         githash     d22b41fd2f738164c2cc89f6ae5d08c8bea6c65c
%global         shorthash   %(TMP=%githash ; echo ${TMP:0:10})
%global         gitdate     Sun Aug 7 19:27:20 2011 +0800
%global         gitdate_num 20110807

%if 0%{?usegit} >= 1
%global         fedorarel   %{mainrel}.D%{gitdate_num}git%{shorthash}
%else
%global         fedorarel   %{mainrel}
%endif

%global         build_doc   1

Name:           libfm
Version:        1.1.0
Release:        %{fedorarel}%{?dist}
Summary:        GIO-based library for file manager-like programs

Group:          System Environment/Libraries
License:        GPLv2+
URL:            http://pcmanfm.sourceforge.net/
%if 0%{?usegit} >= 1
Source0:        %{name}-%{version}-D%{gitdate_num}git%{shorthash}.tar.gz
%else
Source0:        http://downloads.sourceforge.net/pcmanfm/%{name}-%{version}.tar.gz
%endif
# Fedora specific patches
Patch0:         libfm-0.1.9-pref-apps.patch

BuildRequires:  libexif-devel
%if %{usegtk3}
BuildRequires:  gtk3-devel
%else
BuildRequires:  gtk2-devel >= 2.16.0
%endif
BuildRequires:  menu-cache-devel >= 0.3.2

BuildRequires:  gettext
BuildRequires:  intltool
BuildRequires:  desktop-file-utils

# Patch1
BuildRequires:	automake
BuildRequires:	libtool

BuildRequires:	gtk-doc
BuildRequires: libxslt

%if 0%{?fedora} >= 18
BuildRequires:	dbus-glib-devel
%endif

BuildRequires:  vala

%if 0%{?build_doc} < 1
Obsoletes:      %{name}-devel-docs < 0.1.15
%endif

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig


%description
LibFM is a GIO-based library used to develop file manager-like programs. It is
developed as the core of next generation PCManFM and takes care of all file-
related operations such as copy & paste, drag & drop, file associations or 
thumbnails support. By utilizing glib/gio and gvfs, libfm can access remote 
file systems supported by gvfs.

This package contains the generic non-gui functions of libfm.


%package        gtk
Summary:        File manager-related GTK+ widgets of %{name}
Group:          System Environment/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       gvfs

%description    gtk
libfm is a GIO-based library used to develop file manager-like programs. It is
developed as the core of next generation PCManFM and takes care of all file-
related operations such as copy & paste, drag & drop, file associations or 
thumbnail support. By utilizing glib/gio and gvfs, libfm can access remote 
file systems supported by gvfs.

This package provides useful file manager-related GTK+ widgets.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        gtk-devel
Summary:        Development files for %{name}-gtk
Group:          Development/Libraries
Requires:       %{name}-gtk = %{version}-%{release}
Requires:       %{name}-devel = %{version}-%{release}

%description    gtk-devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}-gtk.

%package        devel-docs
Summary:        Development documation for %{name}
Group:          Development/Libraries

%description    devel-docs
This package containg development documentation files for %{name}.


%prep
%setup -q
%patch0 -p1 -b .orig

%if %{usegtk3}
sed -i.gtk3 \
   -e 's|libfm-gtk.la|libfm-gtk3.la|' \
   docs/reference/libfm/Makefile.am
%endif
autoreconf -fi

# ???
#mkdir m4 || :
#sh autogen.sh

# treak rpath
sed -i.libdir_syssearch \
  -e '/sys_lib_dlsearch_path_spec/s|/usr/lib |/usr/lib /usr/lib64 /lib /lib64 |' \
  configure

%build
%configure \
    --enable-gtk-doc \
%if 0%{?fedora} >= 18
    --enable-udisks \
%endif
%if %{usegtk3}
    --with-gtk=3 \
%endif
    --disable-static
# To show translation status
make -C po -j1 GMSGFMT="msgfmt --statistics"
make %{?_smp_mflags} -k


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'

%if %{usegtk3}
rm -f $RPM_BUILD_ROOT%{_libdir}/pkgconfig/libfm-gtk.pc
%else
rm -f $RPM_BUILD_ROOT%{_libdir}/pkgconfig/libfm-gtk3.pc
%endif

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
desktop-file-validate %{buildroot}/%{_datadir}/applications/*.desktop
%find_lang %{name}

echo '%%defattr(-,root,root,-)' > base-header.files
echo '%%defattr(-,root,root,-)' > gtk-header.files

for f in $RPM_BUILD_ROOT%_includedir/%name-1.0/*.h
do
  bf=$(basename $f)
  for dir in actions base job
  do
    if [ -f src/$dir/$bf ]
    then
      echo %_includedir/%name-1.0/$bf >> base-header.files
    fi
  done
  for dir in gtk
  do
    if [ -f src/$dir/$bf ]
    then
      echo %_includedir/%name-1.0/$bf >> gtk-header.files
    fi
  done
done

/usr/lib/rpm/check-rpaths

%post
/sbin/ldconfig
update-mime-database %{_datadir}/mime &> /dev/null || :

%pre devel
# Directory -> symlink
if [ -d %{_includedir}/libfm ] ; then
  rm -rf %{_includedir}/libfm
fi

%postun
/sbin/ldconfig
update-mime-database %{_datadir}/mime &> /dev/null || :

%post gtk -p /sbin/ldconfig
%postun gtk -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root,-)
# FIXME: Add ChangeLog and NEWS if not empty
%doc AUTHORS
%doc COPYING
%doc README
%dir %{_sysconfdir}/xdg/libfm/
%config(noreplace) %{_sysconfdir}/xdg/libfm/pref-apps.conf
%config(noreplace) %{_sysconfdir}/xdg/libfm/libfm.conf
%{_libdir}/%{name}.so.3*
%{_datadir}/mime/packages/libfm.xml


%files gtk
%defattr(-,root,root,-)
%{_mandir}/man1/libfm-pref-apps.1.*
%{_bindir}/libfm-pref-apps
%if %{usegtk3}
%{_libdir}/%{name}-gtk3.so.3*
%else
%{_libdir}/%{name}-gtk.so.3*
%endif
#%%dir %%{_libdir}/libfm/
#%%{_libdir}/libfm/gnome-terminal
%{_datadir}/libfm/
%{_datadir}/applications/libfm-pref-apps.desktop


%files devel -f base-header.files
%defattr(-,root,root,-)
%doc TODO
%{_includedir}/libfm
%dir %{_includedir}/libfm-1.0/
%{_includedir}/libfm-1.0/fm.h
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/libfm.pc

%files gtk-devel -f gtk-header.files
%defattr(-,root,root,-)
%{_includedir}/libfm-1.0/fm-gtk.h
%if %{usegtk3}
%{_libdir}/%{name}-gtk3.so
%{_libdir}/pkgconfig/libfm-gtk3.pc
%else
%{_libdir}/%{name}-gtk.so
%{_libdir}/pkgconfig/libfm-gtk.pc
%endif

%if 0%{?build_doc}
%files devel-docs
%defattr(-,root,root,-)
%dir %{_datadir}/gtk-doc
%dir %{_datadir}/gtk-doc/html
%{_datadir}/gtk-doc/html/%{name}
%endif

%changelog
* Sun Nov 25 2012 Christoph Wickert <cwickert@fedoraproject.org> - 1.1.0-2
- Rebuild against menu-cache 0.4.x

* Sun Nov  4 2012 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.1.0-1
- 1.1.0

* Wed Sep 27 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.0.1-1
- 1.0.1

* Wed Aug 15 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.0-1
- 1.0 release

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.17-1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.17-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Oct 28 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.1.17-1
- 0.1.17

* Sun Aug 28 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.1.16-1
- 0.1.16 release

* Sun Aug  7 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.1.15-7
- Update to the latest git

* Sun May 29 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.1.15-6
- Update to the latest git, to support treeview on pcmanfm

* Tue May 03 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.1.15-5
- Update to the latest git

* Sun Apr 24 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.1.15-4
- Update to the latest git

* Sat Apr 09 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.1.15-3
- Update to the latest git

* Sun Feb 20 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.1.15-2
- Update to the latest git

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.15-1.git3ec0a717ad.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Dec  5 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- Update to the latest git

* Wed Oct 13 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.1.14-1
- Update to 0.1.14, drop patches

* Fri Jun 25 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.1.12-4
- Fix crash with --desktop mode when clicking volume icon
  (bug 607069)

* Thu Jun 10 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.1.12-3
- Fix an issue that pcmanfm // crashes (upstream bug 3012747)

* Fri Jun  4 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.1.12-2
- Fix an issue in sorting by name in cs_CZ.UTF-8 (upstream bug 3009374)

* Sat May 29 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.1.12-1
- Update to 0.1.12, drop upstreamed patches

* Sat May 29 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.1.11-7
- Fix crash of gnome-terminal wrapper with certain path settings
  (bug 596598, 597270)

* Tue May 25 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.1.11-5
- Translation update from git
- Fix an issue in sorting by name in ja_JP.UTF-8 (upstream bug 3002788)

* Sun May  9 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.1.11-4
- Translation update from git

* Fri May  7 2010 Mamrou Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.1.11-3
- Remove runpath_var=... trick on libtool which causes internal
  linkage error,
  and treak sys_lib_dlsearch_path_spec instead for rpath issue on x86_64

* Fri May  7 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.1.11-2
- Fix crash of wrapper of gnome-terminal when libfm.conf doesn't exist or so
  (bug 589730)

* Thu Apr 29 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.1.11-1
- Update to 0.1.11

* Sun Apr 18 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.1.10-1
- Update to 0.1.10

* Sun Mar 21 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.1.9-2
- Own %%{_libdir}/libfm
- Validate desktop file

* Fri Mar 19 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.1.9-1
- Update to 0.1.9 (Beta 1)

* Sat Mar 13 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.1.5-1
- Update to 0.1.5 (Alpha 2)

* Fri Mar 05 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.1.1-1
- Update to 0.1.1 (Alpha 1)

* Mon Feb 22 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.1-1
- Initial packaging

