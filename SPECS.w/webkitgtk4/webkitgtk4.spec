## NOTE: Lots of files in various subdirectories have the same name (such as
## "LICENSE") so this short macro allows us to distinguish them by using their
## directory names (from the source tree) as prefixes for the files.
%global add_to_license_files() \
        mkdir -p _license_files ; \
        cp -p %1 _license_files/$(echo '%1' | sed -e 's!/!.!g')

%global _hardened_build 1

Name:           webkitgtk4
Version:        2.10.2
Release:        1%{?dist}
Summary:        GTK+ Web content engine library

License:        LGPLv2
URL:            http://www.webkitgtk.org/
Source0:        http://webkitgtk.org/releases/webkitgtk-%{version}.tar.xz

Patch0:         webkitgtk-2.9.4-nspluginwrapper.patch
# https://bugs.webkit.org/show_bug.cgi?id=142074
Patch1:         webkitgtk-2.7.90-user-agent-branding.patch
# CLoop fixes (applied just on secondary arches)
Patch2:         webkitgtk-2.5.90-cloop_fix.patch
Patch3:         webkitgtk-2.8.0-page_size_align.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1206161
Patch4:         webkitgtk-2.8.0-s390_fixes.patch
# https://bugs.webkit.org/show_bug.cgi?id=135972
Patch6:         webkitgtk-2.9.4-youtube.patch

BuildRequires:  at-spi2-core-devel
BuildRequires:  bison
BuildRequires:  cairo-devel
BuildRequires:  cmake
BuildRequires:  enchant-devel
BuildRequires:  flex
BuildRequires:  fontconfig-devel
BuildRequires:  freetype-devel
BuildRequires:  geoclue2-devel
BuildRequires:  gettext
BuildRequires:  glib2-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  gperf
BuildRequires:  gstreamer1-devel
BuildRequires:  gstreamer1-plugins-base-devel
BuildRequires:  gtk2-devel
BuildRequires:  gtk3-devel
BuildRequires:  gtk-doc
BuildRequires:  harfbuzz-devel
BuildRequires:  libicu-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libnotify-devel
BuildRequires:  libpng-devel
BuildRequires:  libsecret-devel
BuildRequires:  libsoup-devel
BuildRequires:  libwebp-devel
BuildRequires:  libxslt-devel
BuildRequires:  libXt-devel
BuildRequires:  libwayland-client-devel
BuildRequires:  libwayland-egl-devel
BuildRequires:  libwayland-server-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  pcre-devel
BuildRequires:  perl-Switch
BuildRequires:  ruby
BuildRequires:  sqlite-devel
BuildRequires:  hyphen-devel
%ifarch ppc
BuildRequires:  libatomic
%endif
Requires:       geoclue2

# Obsolete libwebkit2gtk from the webkitgtk3 package
Obsoletes:      libwebkit2gtk < 2.5.0
Provides:       libwebkit2gtk = %{version}-%{release}

# We're supposed to specify a version here, but this is pointless because ANGLE
# doesn't do normal releases. WebKit uses git snapshots.
Provides:	bundled(angle)

# Filter out provides for private libraries
%global __provides_exclude_from ^%{_libdir}/webkit2gtk-4\\.0/.*\\.so$

%description
WebKitGTK+ is the port of the portable web rendering engine WebKit to the
GTK+ platform.

This package contains WebKitGTK+ for GTK+ 3.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries, build data, and header
files for developing applications that use %{name}.

%package        doc
Summary:        Documentation files for %{name}
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description    doc
This package contains developer documentation for %{name}.

%prep
%setup -q -n webkitgtk-%{version}
%patch0 -p1 -b .nspluginwrapper
%patch1 -p1 -b .user_agent
#%ifarch s390 s390x %{arm} ppc %{power64}
# FIXME Temporarily disabled due to https://bugzilla.redhat.com/show_bug.cgi?id=1167004
# Enabled just on secondary arches where we use CLoop
#%patch2 -p1 -b .cloop_fix
#%patch3 -p1 -b .page_size_align
#%endif
%ifarch s390
%patch4 -p1 -b .s390_fixes
%endif
%patch6 -p1 -b .youtube

# Remove bundled libraries
rm -rf Source/ThirdParty/leveldb/
rm -rf Source/ThirdParty/gtest/
rm -rf Source/ThirdParty/qunit/

%build
%ifarch s390 aarch64
# Use linker flags to reduce memory consumption - on other arches the ld.gold is
# used and also it doesn't have the --reduce-memory-overheads option
%global optflags %{optflags} -Wl,--no-keep-memory -Wl,--reduce-memory-overheads
%endif

# Decrease debuginfo even on ix86 because of:
# https://bugs.webkit.org/show_bug.cgi?id=140176
%ifarch s390 s390x %{arm} %{ix86} ppc %{power64}
# Decrease debuginfo verbosity to reduce memory consumption even more
%global optflags %(echo %{optflags} | sed 's/-g /-g1 /')
%endif

%ifarch ppc
# Use linker flag -relax to get WebKit build under ppc(32) with JIT disabled
%global optflags %{optflags} -Wl,-relax -latomic
%endif

%ifarch s390 s390x %{arm} ppc %{power64}
# Turn off bmalloc on secondary arches (as it is not ready for them)
%global optflags %{optflags} -DUSE_BMALLOC=0
%endif

%if 0%{?fedora}
%global optflags %{optflags} -DUSER_AGENT_GTK_DISTRIBUTOR_NAME=\'\\"Fedora\\"\'
%endif

# Disable ld.gold on s390 as it does not have it.
# Also for aarch64 as the support is in upstream, but not packaged in Fedora.
mkdir -p %{_target_platform}
pushd %{_target_platform}
%cmake \
  -DPORT=GTK \
  -DCMAKE_BUILD_TYPE=Release \
  -DENABLE_GTKDOC=ON \
  -DENABLE_MINIBROWSER=ON \
%ifarch s390 aarch64
  -DUSE_LD_GOLD=OFF \
%endif
%ifarch s390 s390x ppc %{power64} aarch64
  -DENABLE_JIT=OFF \
%endif
  ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
%make_install -C %{_target_platform}

%find_lang WebKit2GTK-4.0

# Finally, copy over and rename various files for %%license inclusion
%add_to_license_files Source/JavaScriptCore/COPYING.LIB
%add_to_license_files Source/JavaScriptCore/icu/LICENSE
%add_to_license_files Source/ThirdParty/ANGLE/LICENSE
%add_to_license_files Source/ThirdParty/ANGLE/src/third_party/compiler/LICENSE
%add_to_license_files Source/ThirdParty/ANGLE/src/third_party/murmurhash/LICENSE
%add_to_license_files Source/WebCore/icu/LICENSE
%add_to_license_files Source/WebCore/LICENSE-APPLE
%add_to_license_files Source/WebCore/LICENSE-LGPL-2
%add_to_license_files Source/WebCore/LICENSE-LGPL-2.1
%add_to_license_files Source/WebInspectorUI/UserInterface/External/CodeMirror/LICENSE
%add_to_license_files Source/WebInspectorUI/UserInterface/External/Esprima/LICENSE
%add_to_license_files Source/WTF/icu/LICENSE
%add_to_license_files Source/WTF/wtf/dtoa/COPYING
%add_to_license_files Source/WTF/wtf/dtoa/LICENSE

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f WebKit2GTK-4.0.lang
%license _license_files/*
%{_libdir}/libjavascriptcoregtk-4.0.so.*
%{_libdir}/libwebkit2gtk-4.0.so.*
%{_libdir}/girepository-1.0/JavaScriptCore-4.0.typelib
%{_libdir}/girepository-1.0/WebKit2-4.0.typelib
%{_libdir}/girepository-1.0/WebKit2WebExtension-4.0.typelib
%{_libdir}/webkit2gtk-4.0/
%{_libexecdir}/webkit2gtk-4.0/

%files devel
%{_bindir}/jsc
%{_bindir}/MiniBrowser
%{_includedir}/webkitgtk-4.0/
%{_libdir}/libjavascriptcoregtk-4.0.so
%{_libdir}/libwebkit2gtk-4.0.so
%{_libdir}/pkgconfig/javascriptcoregtk-4.0.pc
%{_libdir}/pkgconfig/webkit2gtk-4.0.pc
%{_libdir}/pkgconfig/webkit2gtk-web-extension-4.0.pc
%{_datadir}/gir-1.0/JavaScriptCore-4.0.gir
%{_datadir}/gir-1.0/WebKit2-4.0.gir
%{_datadir}/gir-1.0/WebKit2WebExtension-4.0.gir

%files doc
%dir %{_datadir}/gtk-doc
%dir %{_datadir}/gtk-doc/html
%{_datadir}/gtk-doc/html/webkit2gtk-4.0/
%{_datadir}/gtk-doc/html/webkitdomgtk-4.0/

%changelog
* Thu Oct 15 2015 Tomas Popela <tpopela@redhat.com> - 2.10.2-1
- Update to 2.10.2

* Thu Oct 15 2015 Kalev Lember <klember@redhat.com> - 2.10.1-2
- Rebuilt

* Wed Oct 14 2015 Tomas Popela <tpopela@redhat.com> - 2.10.1-1
- Update to 2.10.1

* Fri Oct 09 2015 Michael Catanzaro <mcatanzaro@igalia.com> - 2.10.0-2
- Add provides bundled(angle) since it's finally safe to do so.

* Mon Sep 21 2015 Kalev Lember <klember@redhat.com> - 2.10.0-1
- Update to 2.10.0

* Wed Sep 16 2015 Tomas Popela <tpopela@redhat.com> - 2.9.92-1
- Update to 2.9.92

* Wed Aug 26 2015 Kalev Lember <klember@redhat.com> - 2.9.91-1
- Update to 2.9.91

* Mon Aug 24 2015 Michael Catanzaro <mcatanzaro@igalia.com> - 2.9.90-2
- Remove the address space limit patch: it was causing too many problems.
- (Warning! This means Red Hat Bugzilla can hang your computer again.)
- Improve the YouTube patch to avoid spamming the journal with rpm output.
- Add patch from upstream to workaround severe a performance regression.
- No need to explicitly enable Wayland support anymore; it's now default.

* Wed Aug 19 2015 Kalev Lember <klember@redhat.com> - 2.9.90-1
- Update to 2.9.90

* Mon Aug 03 2015 Tomas Popela <tpopela@redhat.com> - 2.9.5-1
- Update to 2.9.5

* Sat Aug 01 2015 Michael Catanzaro <mcatanzaro@igalia.com> - 2.9.4-3
- Make YouTube work.

* Tue Jul 28 2015 Michael Catanzaro <mcatanzaro@igalia.com> - 2.9.4-2
- Exempt the plugin process from the address space limit.

* Wed Jul 22 2015 Tomas Popela <tpopela@redhat.com> - 2.9.4-1
- Update to 2.9.4

* Thu Jul 09 2015 Michael Catanzaro <mcatanzaro@igalia.com> - 2.9.3-3
- Prevent runaway web processes from using unlimited memory.

* Wed Jul 01 2015 Michael Catanzaro <mcatanzaro@igalia.com> - 2.9.3-2
- Enable Wayland support at long last. Hopefully fixes #1220811.

* Tue Jun 23 2015 Tomas Popela <tpopela@redhat.com> - 2.9.3-1
- Update to 2.9.3

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 27 2015 Tomas Popela <tpopela@redhat.com> - 2.9.2-1
- Update to 2.9.2

* Thu May 07 2015 Tomas Popela <tpopela@redhat.com> - 2.9.1-1
- Update to 2.9.1
- Add hyphen-devel as BR

* Tue Apr 21 2015 Michael Catanzaro <mcatanzaro@igalia.com> - 2.8.1-2
- Reenable fast matrix multiplication on x86_64

* Tue Apr 14 2015 Tomas Popela <tpopela@redhat.com> - 2.8.1-1
- Update to 2.8.1

* Wed Apr 08 2015 Michael Catanzaro <mcatanzaro@igalia.com> - 2.8.0-4
- Build with support for HTML5 desktop notifications

* Wed Apr 08 2015 Tomas Popela <tpopela@redhat.com> - 2.8.0-3
- Fix CLoop on secondary arches

* Fri Mar 27 2015 Than Ngo <than@redhat.com> - 2.8.0-2
- Fix build failures on s390
- Fix build failures with gcc 5
- Decrease the debuginfo verbosity on ppc and others

* Mon Mar 23 2015 Tomas Popela <tpopela@redhat.com> - 2.8.0-1
- Update to 2.8.0

* Tue Mar 17 2015 Tomas Popela <tpopela@redhat.com> - 2.7.92-1
- Update to 2.7.92
- Re-enable parallel build
- Compile and ship MiniBrowser

* Mon Mar 16 2015 Michael Catanzaro <mcatanzaro@gnome.org> 2.7.91-3
- Add a couple patches to fix more crashes

* Wed Mar 04 2015 Michael Catanzaro <mcatanzaro@gnome.org> 2.7.91-2
- Add patch to make gnome-online-accounts 3.15.91 not crash

* Tue Mar 03 2015 Tomas Popela <tpopela@redhat.com> - 2.7.91-1
- Update to 2.7.91

* Thu Feb 26 2015 Michael Catanzaro <mcatanzaro@gnome.org> - 2.7.90-10
- Add Fedora branding to the user agent

* Thu Feb 19 2015 Tomas Popela <tpopela@redhat.com> - 2.7.90-9
- Fix the build with cmake 3.2.x

* Thu Feb 19 2015 Tomas Popela <tpopela@redhat.com> - 2.7.90-8
- Fix crash in CLoop
- Forgot to reset the release number so continuing with 8
- Decrease the debuginfo verbosity on s390x

* Wed Feb 18 2015 Tomas Popela <tpopela@redhat.com> - 2.7.90-7
- Update to 2.7.90
- Add JIT and CLoop fixes

* Mon Feb 16 2015 Michael Catanzaro <mcatanzaro@gnome.org> - 2.7.4-7
- Remove disable codec installer patch, not needed in GNOME 3.15.90

* Tue Feb 10 2015 Michael Catanzaro <mcatanzaro@gnome.org> - 2.7.4-6
- Temporarily disable cloop patch since it breaks js
- Add patch for gmutexlocker namespace collision with glib 2.43.4

* Fri Feb 06 2015 Michael Catanzaro <mcatanzaro@gnome.org> - 2.7.4-5
- Revert yesterday's changes since they don't help.

* Thu Feb 05 2015 Michael Catanzaro <mcatanzaro@gnome.org> - 2.7.4-4
- Disable JIT to see if it fixes js.

* Thu Feb 05 2015 Michael Catanzaro <mcatanzaro@gnome.org> - 2.7.4-3
- Disable hardened build to see if it fixes js

* Mon Jan 26 2015 David Tardon <dtardon@redhat.com> - 2.7.4-2
- rebuild for ICU 54.1

* Tue Jan 20 2015 Tomas Popela <tpopela@redhat.com> - 2.7.4-1
- Update to 2.7.4

* Mon Jan 19 2015 Tomas Popela <tpopela@redhat.com> - 2.7.3-3
- Fix compilation on secondary arches

* Thu Jan 08 2015 Tomas Popela <tpopela@redhat.com> - 2.7.3-2
- Decrease debuginfo verbosity on ix86 to let it build

* Tue Dec 16 2014 Tomas Popela <tpopela@redhat.com> - 2.7.3-1
- Update to 2.7.3

* Tue Dec 09 2014 Michael Catanzaro <mcatanzaro@gnome.org> - 2.7.2-3
- Disable the PackageKit codec installer

* Sun Dec 07 2014 Michael Catanzaro <mcatanzaro@gnome.org> - 2.7.2-2
- Enable hardened build

* Mon Nov 24 2014 Tomas Popela <tpopela@redhat.com> - 2.7.2-1
- Update to 2.7.2
- Don't use ld.gold on s390 and aarch64

* Wed Nov 12 2014 Tomas Popela <tpopela@redhat.com> - 2.7.1-5
- Enable JIT where possible (accidentally turned off when updating to 2.5.90)

* Fri Nov 07 2014 Kalev Lember <kalevlember@gmail.com> - 2.7.1-4
- Build developer documentation

* Fri Oct 31 2014 Michael Catanzaro <mcatanzaro@gnome.org> - 2.7.1-3
- Obsolete libwebkit2gtk < 2.5.0 to be future-proof

* Fri Oct 31 2014 Kalev Lember <kalevlember@gmail.com> - 2.7.1-2
- Bump libwebkit2gtk obsoletes version

* Wed Oct 29 2014 Tomas Popela <tpopela@redhat.com> - 2.7.1-1
- Update to 2.7.1

* Wed Oct 22 2014 Tomas Popela <tpopela@redhat.com> - 2.6.2-1
- Update to 2.6.2

* Tue Oct 21 2014 Tomas Popela <tpopela@redhat.com> - 2.6.1-2
- Disable the SSLv3 to address the POODLE vulnerability

* Tue Oct 14 2014 Tomas Popela <tpopela@redhat.com> - 2.6.1-1
- Update to 2.6.1

* Thu Sep 25 2014 Tomas Popela <tpopela@redhat.com> - 2.6.0-1
- Add the wrongly removed CLoop patch and remove the one that was upstreamed

* Wed Sep 24 2014 Kalev Lember <kalevlember@gmail.com> - 2.6.0-1
- Update to 2.6.0

* Mon Sep 22 2014 Tomas Popela <tpopela@redhat.com> - 2.5.90-1
- Update to 2.5.90

* Tue Aug 26 2014 Kalev Lember <kalevlember@gmail.com> - 2.5.3-7
- Obsolete libwebkit2gtk from the webkitgtk3 package

* Tue Aug 26 2014 David Tardon <dtardon@redhat.com> - 2.5.3-6
- rebuild for ICU 53.1

* Mon Aug 25 2014 Tomas Popela <tpopela@redhat.com> - 2.5.3-5
- Add support for secondary arches

* Fri Aug 22 2014 Michael Catanzaro <mcatanzaro@gnome.org> - 2.5.3-4
- Add webkitgtk-2.5.3-toggle-buttons.patch

* Thu Aug 21 2014 Kalev Lember <kalevlember@gmail.com> - 2.5.3-3
- More package review fixes (#1131284)
- Correct the license tag to read LGPLv2
- Filter out provides for private libraries

* Tue Aug 19 2014 Kalev Lember <kalevlember@gmail.com> - 2.5.3-2
- Remove bundled leveldb, gtest, qunit in %%prep (#1131284)

* Fri Aug 15 2014 Kalev Lember <kalevlember@gmail.com> - 2.5.3-1
- Update to 2.5.3

* Fri Aug 01 2014 Kalev Lember <kalevlember@gmail.com> - 2.5.1-1
- Initial Fedora packaging, based on the webkitgtk3 package
