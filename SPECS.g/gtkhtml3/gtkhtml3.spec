%define gtkhtml_major 4.0
%define editor_major 4.0

### Abstract ###

Name: gtkhtml3
Version: 4.5.91
Release: 3%{?dist}
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Summary: GtkHTML library
Summary(zh_CN.UTF-8): GtkHTML 库
License: LGPLv2+ and GPLv2
URL: http://projects.gnome.org/evolution/
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source: http://download.gnome.org/sources/gtkhtml/%{majorver}/gtkhtml-%{version}.tar.xz

### Build Dependencies ###

BuildRequires: enchant-devel
BuildRequires: gail-devel
BuildRequires: gettext
BuildRequires: gnome-common
BuildRequires: gnome-icon-theme
BuildRequires: gsettings-desktop-schemas-devel
BuildRequires: gtk3-devel
BuildRequires: intltool
BuildRequires: iso-codes-devel
BuildRequires: libtool

%description
GtkHTML is a lightweight HTML rendering/printing/editing engine.
It was originally based on KHTMLW, but is now being developed
independently of it.

%description -l zh_CN.UTF-8
这是一个轻量级的 HTML 渲染、打印、编辑引擎。
它原来基于 KTHMLW，不过现在已经独立开发了。

%package devel
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Summary: Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires: %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n gtkhtml-%{version}

%build
autoreconf -fi
%configure --disable-static --disable-maintainer-mode
make %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS"

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

magic_rpm_clean.sh
%find_lang gtkhtml-%{gtkhtml_major}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f gtkhtml-%{gtkhtml_major}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog NEWS README COPYING TODO
%{_bindir}/gtkhtml-editor-test
%{_libdir}/libgtkhtml-%{gtkhtml_major}.so.*
%{_libdir}/libgtkhtml-editor-%{editor_major}.so.*
%{_datadir}/gtkhtml-%{gtkhtml_major}

%files devel
%defattr(-,root,root,-)
%{_includedir}/libgtkhtml-%{gtkhtml_major}
%{_libdir}/libgtkhtml-%{gtkhtml_major}.so
%{_libdir}/libgtkhtml-editor-%{editor_major}.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 4.5.91-3
- 更新到 4.10.0

* Fri Apr 11 2014 Liu Di <liudidi@gmail.com> - 4.5.91-2
- 更新到 4.8.0

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 4.5.91-2
- 为 Magic 3.0 重建

* Mon Sep 03 2012 Milan Crha <mcrha@redhat.com> - 4.5.91-1
- Update to 4.5.91

* Mon Aug 06 2012 Milan Crha <mcrha@redhat.com> - 4.5.5-1
- Update to 4.5.5

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 25 2012 Matthew Barnes <mbarnes@redhat.com> - 4.5.3-1
- Update to 4.5.3

* Mon Jun 04 2012 Milan Crha <mcrha@redhat.com> - 4.5.2-1
- Update to 4.5.2

* Sun Apr 29 2012 Matthew Barnes <mbarnes@redhat.com> - 4.5.1-1
- Update to 4.5.1

* Mon Mar 26 2012 Milan Crha <mcrha@redhat.com> - 4.4.0-1
- Update to 4.4.0

* Mon Mar 19 2012 Milan Crha <mcrha@redhat.com> - 4.3.92-1
- Update to 4.3.92

* Tue Mar 06 2012 Milan Crha <mcrha@redhat.com> - 4.3.91-1
- Update to 4.3.91

* Mon Feb 06 2012 Milan Crha <mcrha@redhat.com> - 4.3.5-1
- Update to 4.3.5

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 19 2011 Milan Crha <mcrha@redhat.com> - 4.3.3-1
- Update to 4.3.3

* Mon Nov 21 2011 Milan Crha <mcrha@redhat.com> - 4.3.2-1
- Update to 4.3.2
- Remove patch to not call g_thread_init() (fixed upstream)

* Mon Oct 24 2011 Milan Crha <mcrha@redhat.com> - 4.3.1-1
- Update to 4.3.1
- Add patch to not call g_thread_init()

* Mon Sep 26 2011 Milan Crha <mcrha@redhat.com> - 4.2.0-1
- Update to 4.2.0

* Mon Sep 19 2011 Milan Crha <mcrha@redhat.com> - 4.1.92-1
- Update to 4.1.92

* Mon Sep 05 2011 Milan Crha <mcrha@redhat.com> - 4.1.91-1
- Update to 4.1.91

* Mon Aug 29 2011 Milan Crha <mcrha@redhat.com> - 4.1.90-1
- Update to 4.1.90

* Mon Aug 15 2011 Milan Crha <mcrha@redhat.com> - 4.1.5-1
- Update to 4.1.5

* Sat Jul 23 2011 Matthew Barnes <mbarnes@redhat.com> - 4.1.4-1
- Update to 4.1.4

* Mon Jul 04 2011 Matthew Barnes <mbarnes@redhat.com> - 4.1.3-1
- Update to 4.1.3

* Tue Jun 14 2011 Milan Crha <mcrha@redhat.com> - 4.1.2-1
- Update to 4.1.2

* Mon May 09 2011 Milan Crha <mcrha@redhat.com> - 4.1.1-1
- Update to 4.1.1

* Mon Apr 04 2011 Milan Crha <mcrha@redhat.com> - 4.0.0-1
- Update to 4.0.0

* Mon Mar 21 2011 Milan Crha <mcrha@redhat.com> - 3.91.92-1
- Update to 3.91.92

* Mon Mar 07 2011 Milan Crha <mcrha@redhat.com> - 3.91.91-1
- Update to 3.91.91

* Mon Feb 21 2011 Milan Crha <mcrha@redhat.com> - 3.91.90-1
- Update to 3.91.90

* Fri Feb 11 2011 Matthias Clasen <mclasen@redhat.com> 3.91.6-4
- Rebuild against newer gtk

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.91.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> - 3.91.6-2
- Rebuild

* Mon Jan 31 2011 Milan Crha <mcrha@redhat.com> - 3.91.6-1
- Update to 3.91.6

* Mon Jan 10 2011 Milan Crha <mcrha@redhat.com> - 3.91.5-1
- Update to 3.91.5
- Remove patch for a build break (fixed upstream)

* Mon Dec 20 2010 Milan Crha <mcrha@redhat.com> - 3.91.4-1
- Update to 3.91.4
- Add patch for a build break

* Mon Nov 29 2010 Milan Crha <mcrha@redhat.com> - 3.91.3-1
- Update to 3.91.3

* Mon Nov 08 2010 Milan Crha <mcrha@redhat.com> - 3.91.2-1
- Update to 3.91.2

* Mon Oct 18 2010 Milan Crha <mcrha@redhat.com> - 3.91.1-1
- Update to 3.91.1

* Wed Oct 13 2010 Parag Nemade <paragn AT fedoraproject.org> - 3.91-0.2
- Merge-review cleanup (#225872)

* Mon Oct 11 2010 Milan Crha <mcrha@redhat.com> - 3.91.0-1
- Update to 3.91.0

* Wed Sep 29 2010 jkeating - 3.31.92-2
- Rebuilt for gcc bug 634757

* Mon Sep 13 2010 Milan Crha <mcrha@redhat.com> - 3.31.92-1.fc15
- Update to 3.31.92

* Mon Aug 30 2010 Milan Crha <mcrha@redhat.com> - 3.31.91-1.fc14
- Update to 3.31.91

* Mon Aug 16 2010 Matthew Barnes <mbarnes@redhat.com> - 3.31.90-1.fc14
- Update to 3.31.90

* Tue Aug 03 2010 Matthew Barnes <mbarnes@redhat.com> - 3.31.6-1.fc14
- Update to 3.31.6

* Tue Jul 13 2010 Milan Crha <mcrha@redhat.com> - 3.31.5-1.fc14
- Update to 3.31.5

* Mon Jun 07 2010 Milan Crha <mcrha@redhat.com> - 3.31.3-1.fc14
- Update to 3.31.3

* Mon May 24 2010 Milan Crha <mcrha@redhat.com> - 3.31.2-1.fc14
- Update to 3.31.2

* Mon May 03 2010 Milan Crha <mcrha@redhat.com> - 3.31.1-1.fc14
- Update to 3.31.1

* Mon Feb 08 2010 Milan Crha <mcrha@redhat.com> - 3.29.90-1.fc13
- Update to 3.29.90
- Removed unneeded BuildRequires.

* Mon Jan 25 2010 Milan Crha <mcrha@redhat.com> - 3.29.6-1.fc13
- Update to 3.29.6

* Tue Jan 12 2010 Milan Crha <mcrha@redhat.com> - 3.29.5-1.fc13
- Update to 3.29.5
- Correct Source URL

* Mon Dec 21 2009 Milan Crha <mcrha@redhat.com> - 3.29.4-1.fc13
- Update to 3.29.4

* Mon Nov 30 2009 Milan Crha <mcrha@redhat.com> - 3.29.3-1.fc13
- Update to 3.29.3

* Mon Nov 16 2009 Milan Crha <mcrha@redhat.com> - 3.29.2-1.fc13
- Update to 3.29.2

* Mon Oct 26 2009 Matthew Barnes <mbarnes@redhat.com> - 3.29.1-1.fc13
- Update to 3.29.1

* Mon Oct 19 2009 Milan Crha <mcrha@redhat.com> - 3.28.1-1.fc12
- Update to 3.28.1

* Mon Sep 21 2009 Milan Crha <mcrha@redhat.com> - 3.28.0-1.fc12
- Update to 3.28.0

* Mon Sep 07 2009 Milan Crha <mcrha@redhat.com> - 3.27.92-1.fc12
- Update to 3.27.92

* Mon Aug 24 2009 Milan Crha <mcrha@redhat.com> - 3.27.91-1.fc12
- Update to 3.27.91

* Mon Aug 10 2009 Milan Crha <mcrha@redhat.com> - 3.27.90-1.fc12
- Update to 3.27.90

* Mon Jul 27 2009 Milan Crha <mcrha@redhat.com> - 3.27.5-1.fc12
- Update to 3.27.5

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.27.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 13 2009 Matthew Barnes <mbarnes@redhat.com> - 3.27.4-1.fc12
- Update to 3.27.4

* Wed Jul 01 2009 Milan Crha <mcrha@redhat.com> - 3.27.3-2.fc12
- Rebuild against newer gcc

* Mon Jun 15 2009 Matthew Barnes <mbarnes@redhat.com> - 3.27.3-1.fc12
- Update to 3.27.3

* Mon May 25 2009 Matthew Barnes <mbarnes@redhat.com> - 3.27.2-1.fc12
- Update to 3.27.2
- Remove strict_build_settings since the settings are used upstream now.

* Mon May 04 2009 Matthew Barnes <mbarnes@redhat.com> - 3.27.1-1.fc12
- Update to 3.27.1

* Tue Apr 14 2009 Matthew Barnes <mbarnes@redhat.com> - 3.26.1.1-1.fc11
- Update to 3.26.1.1

* Mon Apr 13 2009 Matthew Barnes <mbarnes@redhat.com> - 3.26.1-1.fc11
- Update to 3.26.1

* Mon Mar 16 2009 Matthew Barnes <mbarnes@redhat.com> - 3.26.0-1.fc11
- Update to 3.26.0

* Mon Mar 02 2009 Matthew Barnes <mbarnes@redhat.com> - 3.25.92-1.fc11
- Update to 3.25.92

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.25.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 16 2009 Matthew Barnes <mbarnes@redhat.com> - 3.25.91-1.fc11
- Update to 3.25.91

* Fri Feb 06 2009 Matthew Barnes <mbarnes@redhat.com> - 3.25.90-2.fc11
- Update BuildRoot, Source and URL tags.
- Require gnome-common so we don't have to patch it out.

* Mon Feb 02 2009 Matthew Barnes <mbarnes@redhat.com> - 3.25.90-1.fc11
- Update to 3.25.90

* Mon Jan 19 2009 Matthew Barnes <mbarnes@redhat.com> - 3.25.5-1.fc11
- Update to 3.25.5
- Bump gtk2_version to 2.14.0

* Mon Jan 05 2009 Matthew Barnes <mbarnes@redhat.com> - 3.25.4-1.fc11
- Update to 3.25.4

* Mon Dec 15 2008 Matthew Barnes <mbarnes@redhat.com> - 3.25.3-1.fc11
- Update to 3.25.3
- Bump gnome_icon_theme_version to 2.22.0

* Mon Dec 01 2008 Matthew Barnes <mbarnes@redhat.com> - 3.25.2-1.fc11
- Update to 3.25.2

* Mon Nov 03 2008 Matthew Barnes <mbarnes@redhat.com> - 3.25.1-1.fc11
- Update to 3.25.1

* Tue Oct 21 2008 Matthew Barnes <mbarnes@redhat.com> - 3.24.1-1.fc10
- Update to 3.24.1

* Mon Sep 22 2008 Matthew Barnes <mbarnes@redhat.com> - 3.24.0-1.fc10
- Update to 3.24.0

* Mon Sep 08 2008 Matthew Barnes <mbarnes@redhat.com> - 3.23.92-1.fc10
- Update to 3.23.92

* Mon Sep 01 2008 Matthew Barnes <mbarnes@redhat.com> - 3.23.91-1.fc10
- Update to 3.23.91
- Add -Werror to CFLAGS.

* Wed Aug 20 2008 Matthew Barnes <mbarnes@redhat.com> - 3.23.90-1.fc10
- Update to 3.23.90

* Mon Aug 04 2008 Matthew Barnes <mbarnes@redhat.com> - 3.23.6-1.fc10
- Update to 3.23.6

* Tue Jul 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 3.23.5-2.fc10
- Fix license tag

* Mon Jul 21 2008 Matthew Barnes <mbarnes@redhat.com> - 3.23.5-1.fc10
- Update to 3.23.5
- Remove patch for GNOME bug #538703 (fixed upstream).
- Remove patch for GNOME bug #539289 (fixed upstream).

* Thu Jul 10 2008 Matthew Barnes <mbarnes@redhat.com> - 3.23.4-2.fc10
- Add patch for GNOME bug #538703 (load dictionaries on-demand).
- Add patch for GNOME bug #539289 (stop using GtkType already!).

* Mon Jun 16 2008 Matthew Barnes <mbarnes@redhat.com> - 3.23.4-1.fc10
- Update to 3.23.4

* Mon Jun 02 2008 Matthew Barnes <mbarnes@redhat.com> - 3.23.3-1.fc10
- Update to 3.23.3
- Remove patch for GNOME bug #524338 (fixed upstream).

* Tue May 13 2008 Matthew Barnes <mbarnes@redhat.com> - 3.23.2-4.fc10
- Add patch for GNOME bug #524338 (mail flickers when rendering).

* Mon May 12 2008 Matthew Barnes <mbarnes@redhat.com> - 3.23.2-3.fc10
- Add iso-codes-devel requirement to devel subpackage.

* Mon May 12 2008 Matthew Barnes <mbarnes@redhat.com> - 3.23.2-2.fc10
- Add enchant-devel requirement to devel subpackage.

* Mon May 12 2008 Matthew Barnes <mbarnes@redhat.com> - 3.23.2-1.fc10
- Update to 2.23.2

* Tue Apr 22 2008 Matthew Barnes <mbarnes@redhat.com> - 3.23.1-2.fc10
- Forgot the enchant-devel and iso-codes-devel requirements.

* Mon Apr 21 2008 Matthew Barnes <mbarnes@redhat.com> - 3.23.1-1.fc10
- Update to 3.23.1
- Drop libbonobo requirement.

* Mon Apr 07 2008 Matthew Barnes <mbarnes@redhat.com> - 3.18.1-1.fc9
- Update to 3.18.1

* Mon Mar 10 2008 Matthew Barnes <mbarnes@redhat.com> - 3.18.0-1.fc9
- Update to 3.18.0

* Mon Feb 25 2008 Matthew Barnes <mbarnes@redhat.com> - 3.17.92-1.fc9
- Update to 3.17.92
- Add BR: libbonobo >= 2.20.3

* Mon Feb 11 2008 Matthew Barnes <mbarnes@redhat.com> - 3.17.91-1.fc9
- Update to 3.17.91

* Fri Feb 08 2008 Matthew Barnes <mbarnes@redhat.com> - 3.17.90-2.fc9
- Remove patch for Ximian bug #50052 / GNOME bug #250052 (fixed upstream).
- Remove patch for Ximian bug #65670 / GNOME bug #265670 (fixed upstream).
- Remove patch for Ximian bug #66206 / GNOME bug #266206 (obsolete?).

* Mon Jan 28 2008 Matthew Barnes <mbarnes@redhat.com> - 3.17.90-1.fc9
- Update to 3.17.90

* Mon Jan 14 2008 Matthew Barnes <mbarnes@redhat.com> - 3.17.5-1.fc9
- Update to 3.17.5

* Mon Dec 17 2007 Matthew Barnes <mbarnes@redhat.com> - 3.17.4-1.fc9
- Update to 3.17.4

* Mon Dec 03 2007 Matthew Barnes <mbarnes@redhat.com> - 3.17.3-1.fc9
- Update to 3.17.3

* Mon Nov 12 2007 Matthew Barnes <mbarnes@redhat.com> - 3.17.2-1.fc9
- Update to 3.17.2

* Mon Oct 29 2007 Matthew Barnes <mbarnes@redhat.com> - 3.17.1-1.fc9
- Update to 3.17.1
- Remove patch for GNOME bug #443850 (fixed upstream).

* Mon Oct 15 2007 Milan Crha <mcrha@redhat.com> - 3.16.1-1.fc8
- Update to 3.16.1

* Mon Sep 17 2007 Matthew Barnes <mbarnes@redhat.com> - 3.16.0-1.fc8
- Update to 3.16.0

* Thu Sep 13 2007 Matthew Barnes <mbarnes@redhat.com> - 3.15.92-2.fc8
- Add patch for GNOME bug #443850 (fix cursor position after typing halant).

* Mon Sep 03 2007 Matthew Barnes <mbarnes@redhat.com> - 3.15.92-1.fc8
- Update to 3.15.92

* Tue Aug 28 2007 Milan Crha <mcrha@redhat.com> - 3.15.91-1.fc8
- Update to 3.15.91
- Remove patch for Red Hat bug #129212/GNOME bug #262907 (fixed upstream).
- Remove patch for GNOME bug #446894 (fixed upstream).

* Tue Aug 21 2007 Matthew Barnes <mbarnes@redhat.com> - 3.15.90-2.fc8
- Add patch for GNOME bug #446894 (regression in old printing API).

* Mon Aug 13 2007 Matthew Barnes <mbarnes@redhat.com> - 3.15.90-1.fc8
- Update to 3.15.90

* Wed Aug 01 2007 Matthew Barnes <mbarnes@redhat.com> - 3.15.6.1-1.fc8
- Update to 3.15.6.1

* Tue Jul 31 2007 Matthew Barnes <mbarnes@redhat.com> - 3.15.6-1.fc8
- Update to 3.15.6
- Remove patch for GNOME bug #380534 (fixed upstream).

* Fri Jul 27 2007 Matthew Barnes <mbarnes@redhat.com> - 3.15.5-2.fc8
- Add patch for GNOME bug #380534 (clarify version requirements).

* Mon Jul 09 2007 Matthew Barnes <mbarnes@redhat.com> - 3.15.5-1.fc8
- Update to 3.15.5

* Mon Jun 18 2007 Matthew Barnes <mbarnes@redhat.com> - 3.15.4-1.fc8
- Update to 3.15.4

* Mon Jun 04 2007 Matthew Barnes <mbarnes@redhat.com> - 3.15.3-1.fc8
- Update to 3.15.3

* Fri May 18 2007 Matthew Barnes <mbarnes@redhat.com> - 3.15.2-1.fc8
- Update to 3.15.2

* Mon Apr 09 2007 Matthew Barnes <mbarnes@redhat.com> - 3.14.1-1.fc7
- Update to 3.14.1
- Add -Wdeclaration-after-statement to strict build settings.

* Mon Mar 12 2007 Matthew Barnes <mbarnes@redhat.com> - 3.14.0-1.fc7
- Update to 3.14.0
- Bump gtkhtml_major to 3.14.

* Tue Feb 27 2007 Matthew Barnes <mbarnes@redhat.com> - 3.13.92-2.fc7
- Add flag to disable deprecated GNOME symbols.

* Mon Feb 26 2007 Matthew Barnes <mbarnes@redhat.com> - 3.13.92-1.fc7
- Update to 3.13.92
- Add mimimum version to intltool requirement (currently >= 0.35.5).

* Tue Feb 20 2007 Matthew Barnes <mbarnes@redhat.com> - 3.13.91-2.fc7
- GtkHtml no longer depends on libgnomeprint[ui].

* Mon Feb 12 2007 Matthew Barnes <mbarnes@redhat.com> - 3.13.91-1.fc7
- Update to 3.13.91
- Add flag to disable deprecated Pango symbols.
- Remove patch for GNOME bug #394182 (fixed upstream).

* Thu Feb 01 2007 Matthew Barnes <mbarnes@redhat.com> - 3.13.5-2.fc7
- Add %{?_smp_mflags} and $RPM_OPT_FLAGS to make command (RH bug #225872).

* Mon Jan 08 2007 Matthew Barnes <mbarnes@redhat.com> - 3.13.5-1.fc7
- Update to 3.13.5

* Mon Jan 08 2007 Matthew Barnes <mbarnes@redhat.com> - 3.13.4-2.fc7
- Add patch for GNOME bug #394182 (code cleanup).
- Remove patch for GNOME bug #363036 (superseded).

* Tue Dec 19 2006 Matthew Barnes <mbarnes@redhat.com> - 3.13.4-1.fc7
- Update to 3.13.4

* Mon Dec 04 2006 Matthew Barnes <mbarnes@redhat.com> - 3.13.3-1.fc7
- Update to 3.13.3
- Remove patch for GNOME bug #353424 (fixed upstream).

* Mon Nov 06 2006 Matthew Barnes <mbarnes@redhat.com> - 3.13.2-1.fc7
- Update to 3.13.2

* Fri Oct 27 2006 Matthew Barnes <mbarnes@redhat.com> - 3.13.1-4.fc7
- Remove gnome-common macros from configure.in.

* Fri Oct 27 2006 Matthew Barnes <mbarnes@redhat.com> - 3.13.1-3.fc7
- Forgot to commit the patch.

* Tue Oct 17 2006 Matthew Barnes <mbarnes@redhat.com> - 3.13.1-2.fc7
- Add patch for Gnome.org bug #363036 (so long, compiler warnings).
- Remove patch for Gnome.org bug #360619 (superseded).

* Mon Oct 16 2006 Matthew Barnes <mbarnes@redhat.com> - 3.13.1-1.fc7
- Update to 3.13.1

* Mon Oct 16 2006 Matthew Barnes <mbarnes@redhat.com> - 3.12.1-1.fc7
- Update to 3.12.1
- Use stricter build settings.
- Add patch for Gnome.org bug #360619 ("incompatible pointer type" warnings).

* Mon Sep  4 2006 Matthew Barnes <mbarnes@redhat.com> - 3.12.0-1.fc6
- Update to 3.12.0
- Remove patch for RH bug #202409 (fixed upstream).

* Tue Aug 29 2006 Matthew Barnes <mbarnes@redhat.com> - 3.11.92-2.fc6
- Add patch for Gnome.org bug #353424.

* Mon Aug 21 2006 Matthew Barnes <mbarnes@redhat.com> - 3.11.92-1.fc6
- Update to 3.11.92

* Fri Aug 18 2006 Matthew Barnes <mbarnes@redhat.com> - 3.11.91-2.fc6
- Add patch for RH bug #202409.

* Mon Aug  7 2006 Matthew Barnes <mbarnes@redhat.com> - 3.11.91-1
- Update to 3.11.91

* Tue Jul 25 2006 Matthew Barnes <mbarnes@redhat.com> - 3.11.90.1-1
- Update to 3.11.90.1

* Wed Jul 12 2006 Matthias Clasen <mclasen@redhat.com> - 3.11.4-2
- Rebuild

* Wed Jul 12 2006 Matthew Barnes <mbarnes@redhat.com> - 3.11.4-1
- Update to 3.11.4

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 3.11.3-1.1
- rebuild

* Tue Jun 13 2006 Matthias Clasen <mclasen@redhat.com> - 3.11.3-1
- Update to 3.11.3

* Tue May 16 2006 Matthew Barnes <mbarnes@redhat.com> - 3.11.2-1
- Update to 3.11.2

* Mon Apr 10 2006 Matthias Clasen <mclasen@redhat.com> - 3.10.1-2
- Update to 3.10.1
- Update patches

* Fri Apr  7 2006 Dan Williams <dcbw@redhat.com> - 3.10.0-2
- Fix crash with IM enabled

* Mon Mar 13 2006 Ray Strode <rstrode@redhat.com> - 3.10.0-1
- Update to 3.10.0

* Mon Feb 13 2006 Matthias Clasen <mclasen@redhat.com> - 3.9.91-1
- Update to 3.9.91

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 3.9.90-3.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 3.9.90-3.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 31 2006 Matthias Clasen <mclasen@redhat.com> - 3.9.90-3
- Actually apply the patch

* Tue Jan 31 2006 Matthias Clasen <mclasen@redhat.com> - 3.9.90-2
- Fix a crash

* Mon Jan 30 2006 David Malcolm <dmalcolm@redhat.com> - 3.9.90-1
- 3.9.90

* Wed Jan 25 2006 David Malcolm <dmalcolm@redhat.com> - 3.9.5-1
- 3.9.5
- be more explicit about packaged bonobo server and so files, relying less on 
  globbing

* Thu Jan 19 2006 Ray Strode <rstrode@redhat.com> - 3.9.4-3
- s/sed -ie/sed -i -e/

* Thu Jan 19 2006 Ray Strode <rstrode@redhat.com> - 3.9.4-3
- fix broken fix in 3.9.4-2

* Thu Jan 19 2006 Ray Strode <rstrode@redhat.com> - 3.9.4-2
- fix multlib shlib bonobo problem (bug 156982)

* Tue Jan  3 2006 David Malcolm <dmalcolm@redhat.com> - 3.9.4-1
- 3.9.4

* Mon Dec 19 2005 David Malcolm <dmalcolm@redhat.com> - 3.9.3-1
- 3.9.3

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Dec  6 2005 David Malcolm <dmalcolm@redhat.com> - 3.9.2-1
- 3.9.2

* Tue Nov 29 2005 David Malcolm <dmalcolm@redhat.com> - 3.8.2-1
- 3.8.2

* Thu Nov 10 2005 David Malcolm <dmalcolm@redhat.com> - 3.8.1-2
- Remove static libraries; rewrite specfile to be more explicit about the
  package payload (#172883)

* Tue Oct  4 2005 David Malcolm <dmalcolm@redhat.com> - 3.8.1-1
- 3.8.1

* Tue Sep  6 2005 David Malcolm <dmalcolm@redhat.com> - 3.8.0-1
- 3.8.0

* Tue Aug 23 2005 David Malcolm <dmalcolm@redhat.com> - 3.7.7-1
- 3.7.7

* Fri Aug 12 2005 David Malcolm <dmalcolm@redhat.com> - 3.7.6-2
- Mark libdir/gtkhtml as being owned by the package (#165771)

* Tue Aug  9 2005 David Malcolm <dmalcolm@redhat.com> - 3.7.6-1
- 3.7.6

* Tue Jul 26 2005 David Malcolm <dmalcolm@redhat.com> - 3.7.5-4
- actually add patch to CVS this time

* Tue Jul 26 2005 David Malcolm <dmalcolm@redhat.com> - 3.7.5-3
- Added patch to use pango for cursor navigation and deletion, fixing problems
  with indic scripts (#129212)

* Mon Jul 25 2005 David Malcolm <dmalcolm@redhat.com> - 3.7.5-2
- update gtkhtml_major from 3.6 to 3.8

* Mon Jul 25 2005 David Malcolm <dmalcolm@redhat.com> - 3.7.5-1
- 3.7.5

* Mon Apr 11 2005 David Malcolm <dmalcolm@redhat.com> - 3.6.2-1
- 3.6.2

* Thu Mar 17 2005 David Malcolm <dmalcolm@redhat.com> - 3.6.1-1
- 3.6.1

* Wed Mar  9 2005 David Malcolm <dmalcolm@redhat.com> - 3.6.0-2
- rebuild

* Tue Mar  8 2005 David Malcolm <dmalcolm@redhat.com> - 3.6.0-1
- 3.6.0

* Tue Mar  1 2005 David Malcolm <dmalcolm@redhat.com> - 3.5.7-1
- 3.5.7

* Tue Feb  8 2005 David Malcolm <dmalcolm@redhat.com> - 3.5.6-2
- Changed deprecated "Copyright" directive into a "License" directive
- License directive now reads "LGPL/GPL", rather than "LGPL", reflecting comment in README file

* Tue Feb  8 2005 David Malcolm <dmalcolm@redhat.com> - 3.5.6-1
- 3.5.6

* Tue Feb  1 2005 David Malcolm <dmalcolm@redhat.com> - 3.5.5-1
- 3.5.5

* Wed Jan 26 2005 David Malcolm <dmalcolm@redhat.com> - 3.5.4-1
- Upgrade to 3.5.4
- Update gtkhtml_major from 3.1 to 3.6 to locate translations
- Temporarily remove IM patch

* Tue Sep 21 2004 Owen Taylor <otaylor@redhat.com> - 3.3.2-2
- Add a patch to fix input method commit issues (#Bug 130751)

* Thu Sep 16 2004 Owen Taylor <otaylor@redhat.com> - 3.3.2-1
- Upgrade to 3.3.2 (Fixes tab display, #132208, ordering
  issues with IM preedit #130751, Leon Ho)

* Fri Sep  3 2004 Owen Taylor <otaylor@redhat.com> - 3.3.1-1
- Upgrade to 3.3.1, includes GtkFileChoose support (#130039)

* Fri Aug 13 2004 Tim Waugh <twaugh@redhat.com> - 3.3.0-3
- Prevent a crash (bug #129844).

* Mon Aug  9 2004 Owen Taylor <otaylor@redhat.com> - 3.3.0-2
- Fix a problem where preformatted text wrapped at column 0

* Wed Aug  4 2004 Owen Taylor <otaylor@redhat.com> - 3.3.0-1
- Upgrade to 3.3.0 (gnome-2-8-devel branch)

* Mon Jul 26 2004 David Malcolm <dmalcolm@redhat.com>
- rebuilt

* Thu Jul 22 2004 David Malcolm <dmalcolm@redhat.com>
- rebuilt

* Thu Jul 22 2004 David Malcolm <dmalcolm@redhat.com>
- rebuilt

* Thu Jul 22 2004 David Malcolm <dmalcolm@redhat.com>
- rebuilt

* Tue Jul 20 2004 David Malcolm <dmalcolm@redhat.com> - 3.1.18-1
- 3.1.18

* Thu Jul  8 2004 David Malcolm <dmalcolm@redhat.com>
- rebuilt

* Wed Jul  7 2004 David Malcolm <dmalcolm@redhat.com>
- rebuilt

* Tue Jul  6 2004 David Malcolm <dmalcolm@redhat.com> - 3.1.17-1
- 3.1.17

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jun  7 2004 David Malcolm <dmalcolm@redhat.com> - 3.1.16-2
- rebuilt

* Fri Jun  4 2004 David Malcolm <dmalcolm@redhat.com> - 3.1.16-1
- 3.1.16

* Fri May 21 2004 David Malcolm <dmalcolm@redhat.com> - 3.1.14-2
- rebuilt

* Thu May 20 2004 David Malcolm <dmalcolm@redhat.com> - 3.1.14-1
- 3.1.14

* Tue Apr 20 2004 David Malcolm <dmalcolm@redhat.com> - 3.1.12-1
- 3.1.12

* Wed Mar 10 2004 Jeremy Katz <katzj@redhat.com> - 3.1.9-1
- 3.1.9

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Feb 17 2004 Jeremy Katz <katzj@redhat.com> - 3.1.8-1
- 3.1.8

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jan 27 2004 Jeremy Katz <katzj@redhat.com> - 3.1.7-1
- 3.1.7

* Wed Jan 14 2004 Jeremy Katz <katzj@redhat.com> 3.1.6-0
- update to 3.1.6

* Sat Jan  3 2004 Jeremy Katz <katzj@redhat.com> 3.1.5-0
- update to 3.1.5

* Thu Sep 25 2003 Jeremy Katz <katzj@redhat.com> 3.0.9-5
- rebuild

* Thu Sep 25 2003 Jeremy Katz <katzj@redhat.com> 3.0.9-4
- add patch for XIM (#91481)

* Tue Sep 23 2003 Jeremy Katz <katzj@redhat.com> 3.0.9-3
- rebuild

* Fri Sep 19 2003 Jeremy Katz <katzj@redhat.com> 3.0.9-2
- add patch to fix crash on ia64

* Fri Sep 19 2003 Jeremy Katz <katzj@redhat.com> 3.0.9-1
- 3.0.9

* Mon Sep  8 2003 Jeremy Katz <katzj@redhat.com> 
- add some buildrequires (#103901)

* Thu Sep  4 2003 Jeremy Katz <katzj@redhat.com> 3.0.8-3
- patch from upstream copy for new libbonobo oddities (#103730)

* Mon Aug  4 2003 Jeremy Katz <katzj@redhat.com> 3.0.8-1
- 3.0.8

* Thu Jul 10 2003 Jeremy Katz <katzj@redhat.com> 3.0.7-1
- 3.0.7

* Wed Jun 11 2003 Jeremy Katz <katzj@redhat.com> 
- add some buildrequires (#97181)

* Tue Jun 10 2003 Jeremy Katz <katzj@redhat.com> 3.0.5-2
- rebuild

* Mon Jun  9 2003 Jeremy Katz <katzj@redhat.com> 3.0.5-1
- 3.0.5

* Wed Jun 5 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jun  5 2003 Jeremy Katz <katzj@redhat.com> 3.0.4-3
- rebuild

* Mon May 26 2003 Jeremy Katz <katzj@redhat.com> 3.0.4-2
- rebuild to fix deps

* Sun May 25 2003 Jeremy Katz <katzj@redhat.com> 3.0.4-1
- 3.0.4

* Tue May  6 2003 Jeremy Katz <katzj@redhat.com> 3.0.3-1
- 3.0.3

* Wed Apr 16 2003 Jeremy Katz <katzj@redhat.com> 3.0.2-2
- libtool's revenge

* Wed Apr 16 2003 Jeremy Katz <katzj@redhat.com> 3.0.2-1
- update to 3.0.2

* Sun Apr  6 2003 Jeremy Katz <katzj@redhat.com> 1.1.9-1
- update to 1.1.9

* Mon Mar 24 2003 Jeremy Katz <katzj@redhat.com> 1.1.8-6
- rebuild for new gal

* Mon Feb 24 2003 Elliot Lee <sopwith@redhat.com> 1.1.8-5
- debuginfo rebuild

* Thu Feb 20 2003 Jeremy Katz <katzj@redhat.com> 1.1.8-4
- gtkhtml capplet doesn't need to be in the menus; it's configurable 
  from within evolution

* Mon Feb 10 2003 Akira TAGOH <tagoh@redhat.com> 1.1.8-3
- don't use fontset as default. (#83899)
- improve the default font for CJK.

* Sat Feb  8 2003 Akira TAGOH <tagoh@redhat.com> 1.1.8-2
- hack to modify po dynamically to add currect XLFD for CJK.
- re-enable patches.

* Fri Feb  7 2003 Jeremy Katz <katzj@redhat.com> 1.1.8-1
- 1.1.8
- disable tagoh's patch for now.  it's not applied upstream and ends up 
  backing out some translation changes

* Fri Feb  7 2003 Akira TAGOH <tagoh@redhat.com> 1.1.7-4
- gtkhtml-1.1.7-fixfont.patch: applied to allow fontset by default.
- gtkhtml-po.tar.bz2: to changes default display/print fonts for CJK.
  perhaps it should be removed when the upstream will releases the next version.
- gtkhtml-1.1.7-domain.patch: define GNOME_EXPLICIT_TRANSLATION_DOMAIN as gtkhtml-1.1.

* Wed Feb  5 2003 Bill Nottingham <notting@redhat.com> 1.1.7-2
- fix some spewage to stdout/stderr

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Fri Dec 13 2002 Jeremy Katz <katzj@redhat.com> 1.1.7-1
- update to 1.1.7

* Tue Nov 12 2002 Jeremy Katz <katzj@redhat.com> 1.1.6-1
- update to 1.1.6

* Thu Nov  7 2002 Jeremy Katz <katzj@redhat.com> 1.1.5-3
- rebuild to really fix Xlib paths now that gnome-libs is fixed

* Tue Nov  5 2002 Jeremy Katz <katzj@redhat.com> 1.1.5-2
- rebuild to fix Xlib paths in .pc files

* Fri Nov  1 2002 Jeremy Katz <katzj@redhat.com> 1.1.5-1
- update to 1.1.5

* Thu Oct 24 2002 Jeremy Katz <katzj@redhat.com> 1.1.4-1
- remove unwanted files from buildroot
- update to 1.1.4

* Thu Sep 26 2002 Jeremy Katz <katzj@redhat.com>
- make sure we get all of the stuff from %%{_datadir}/gtkhtml-1.1

* Wed Sep 25 2002 Jeremy Katz <katzj@redhat.com>
- update to 1.1.2

* Tue Jul 23 2002 Owen Taylor <otaylor@redhat.com>
- Fix problem with finding the closest size

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jun 19 2002 Jeremy Katz <katzj@redhat.com>
- update to 1.0.4
- remove .la files

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue May 14 2002 Jeremy Katz <katzj@redhat.com>
- tweak buildrequires for libcapplet0-devel

* Tue Mar 19 2002 Jeremy Katz <katzj@redhat.com>
- update to gtkhtml 1.0.2

* Thu Mar  7 2002 Jeremy Katz <katzj@redhat.com>
- remove superflous capplet entry (#59698)

* Mon Jan 14 2002 Jeremy Katz <katzj@redhat.com>
- rebuild to get rid of ridiculous libgal18 linkage

* Sat Jan 12 2002 Jeremy Katz <katzj@redhat.com>
- update to 1.0.1

* Sun Dec  2 2001 Jeremy Katz <katzj@redhat.com>
- update to 1.0.0

* Sat Nov 17 2001 Jeremy Katz <katzj@redhat.com>
- update to 0.16.1

* Mon Nov  5 2001 Jeremy Katz <katzj@redhat.com>
- updated to 0.16

* Tue Oct 23 2001 Havoc Pennington <hp@redhat.com>
- 0.15

* Thu Oct  4 2001 Havoc Pennington <hp@redhat.com>
- 0.14
- remove --without-bonobo
- langify

* Mon Aug 20 2001 Alexander Larsson <alexl@redhat.com> 0.9.2-9
- Moved gnome-conf file to the devel package
- Fixes SHOULD-FIX bug #49796

* Mon Jul 30 2001 Alexander Larsson <alexl@redhat.com> 
- Added dependencies on -devel packages from the gtkhtml-devel package

* Fri Jul 20 2001 Alexander Larsson <alexl@redhat.com>
- Add more build dependencies

* Thu Jul 17 2001 Bill Nottingham <notting@redhat.com>
- fix devel package requirements

* Sat Jul  7 2001 Tim Powers <timp@redhat.com>
- changed bad groups
- laguified package

* Tue Jul 03 2001 Havoc Pennington <hp@redhat.com>
- fix X11/libraries -> X11/Libraries, #47137 

* Wed Jun 13 2001 Bill Nottingham <notting@redhat.com>
- fix brokenness due to gal damage

* Wed Jun  6 2001 Bill Nottingham <notting@redhat.com>
- adapt included specfile
