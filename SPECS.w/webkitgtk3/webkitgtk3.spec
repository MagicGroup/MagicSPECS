## NOTE: Lots of files in various subdirectories have the same name (such as
## "LICENSE") so this short macro allows us to distinguish them by using their
## directory names (from the source tree) as prefixes for the files.
%global         add_to_doc_files()      \
        mkdir -p %{buildroot}%{_docdir}/%{name}-%{version} ||: ; \
        cp -p %1  %{buildroot}%{_docdir}/%{name}-%{version}/$(echo '%1' | sed -e 's!/!.!g')

Name:           webkitgtk3
Version:        1.11.2
Release:        3%{?dist}
Summary:        GTK+ Web content engine library

Group:          Development/Libraries
License:        LGPLv2+ and BSD
URL:            http://www.webkitgtk.org/

Source0:        http://webkitgtk.org/releases/webkitgtk-%{version}.tar.xz

Patch1:         webkit-1.3.4-no-execmem.patch
Patch2:         webkit-1.1.14-nspluginwrapper.patch
# Explicitly link with -lrt
# https://bugs.webkit.org/show_bug.cgi?id=103194
Patch3:         webkitgtk-librt.patch
# workarounds for non-JIT arches
# https://bugs.webkit.org/show_bug.cgi?id=104270
Patch4:         webkit-1.11.2-yarr.patch
# https://bugs.webkit.org/show_bug.cgi?id=105295
Patch5:         webkit-1.11.2-includes.patch
# https://bugs.webkit.org/show_bug.cgi?id=103128
Patch6:         webkit-1.11.2-Double2Ints.patch

Patch7:         webkitgtk-1.11.2-mips64-fix.patch

BuildRequires:  bison
BuildRequires:  chrpath
BuildRequires:  enchant-devel
BuildRequires:  flex
BuildRequires:  geoclue-devel
BuildRequires:  gettext
BuildRequires:  gperf
BuildRequires:  gstreamer1-devel
BuildRequires:  gstreamer1-plugins-base-devel
BuildRequires:  gtk2-devel
BuildRequires:  gtk3-devel >= 3.0
BuildRequires:  gtk-doc
BuildRequires:  libsoup-devel >= 2.37.2.1
BuildRequires:  libicu-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libpng-devel
BuildRequires:  libsecret-devel
BuildRequires:  libxslt-devel
BuildRequires:  libXt-devel
BuildRequires:  pcre-devel
BuildRequires:  sqlite-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  perl-Switch
BuildRequires:  ruby
BuildRequires:  mesa-libGL-devel

## Conditional dependencies...
%if %{with pango}
BuildRequires:  pango-devel
%else
BuildRequires:  cairo-devel
BuildRequires:  fontconfig-devel
BuildRequires:  freetype-devel
%endif

%description
WebKitGTK+ is the port of the portable web rendering engine WebKit to the
GTK+ platform.

This package contains WebKitGTK+ for GTK+ 3.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig
Requires:       gtk3-devel

%description    devel
The %{name}-devel package contains libraries, build data, and header
files for developing applications that use %{name}.

%package        doc
Summary:        Documentation files for %{name}
Group:          Documentation
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description    doc
This package contains developer documentation for %{name}.

%prep
%setup -qn "webkitgtk-%{version}"
# tbzatek - doesn't apply, is this fixed?
# %patch1 -p1 -b .no-execmem
%patch2 -p1 -b .nspluginwrapper
%patch3 -p1 -b .librt
%patch4 -p1 -b .yarr
%patch5 -p1 -b .includes
%patch6 -p1 -b .double2ints
%patch7 -p1 -b .mips64

# For patch3
autoreconf --verbose --install -I Source/autotools

%build
%ifarch s390 %{arm} ppc
# Use linker flags to reduce memory consumption on low-mem architectures
%global optflags %{optflags} -Wl,--no-keep-memory -Wl,--reduce-memory-overheads
%endif
%ifarch s390 s390x
# Decrease debuginfo verbosity to reduce memory consumption even more
%global optflags %(echo %{optflags} | sed 's/-g/-g1/')
%endif

# Build with -g1 on all platforms to avoid running into 4 GB ar format limit
# https://bugs.webkit.org/show_bug.cgi?id=91154
%global optflags %(echo %{optflags} | sed 's/-g /-g1 /')

# explicitly disable JIT on ARM https://bugs.webkit.org/show_bug.cgi?id=85076
CFLAGS="%{optflags} -DLIBSOUP_I_HAVE_READ_BUG_594377_AND_KNOW_SOUP_PASSWORD_MANAGER_MIGHT_GO_AWAY" %configure                                                   \
                        --with-gstreamer=1.0                    \
                        --with-gtk=3.0                          \
%ifarch %{arm} s390 s390x ppc ppc64 mips64el
                        --disable-jit                           \
%else
                        --enable-jit                            \
%endif
                        --enable-introspection

mkdir -p DerivedSources/webkit
mkdir -p DerivedSources/WebCore
mkdir -p DerivedSources/ANGLE
mkdir -p DerivedSources/WebKit2
mkdir -p DerivedSources/InjectedBundle
%define _smp_mflags -j1
make %{_smp_mflags} V=1

%install
make install DESTDIR=%{buildroot}

install -d -m 755 %{buildroot}%{_libexecdir}/%{name}
install -m 755 Programs/GtkLauncher %{buildroot}%{_libexecdir}/%{name}

# Remove lib64 rpaths
chrpath --delete %{buildroot}%{_bindir}/jsc-3
chrpath --delete %{buildroot}%{_libdir}/libwebkitgtk-3.0.so
chrpath --delete %{buildroot}%{_libdir}/libwebkit2gtk-3.0.so
chrpath --delete %{buildroot}%{_libexecdir}/%{name}/GtkLauncher
chrpath --delete %{buildroot}%{_libexecdir}/WebKitPluginProcess
chrpath --delete %{buildroot}%{_libexecdir}/WebKitWebProcess

# for some reason translations don't get installed in 1.3.7
%find_lang webkitgtk-3.0

## Finally, copy over and rename the various files for %%doc inclusion.
%add_to_doc_files Source/WebKit/LICENSE
%add_to_doc_files Source/WebKit/gtk/po/README
%add_to_doc_files Source/WebKit/gtk/NEWS
%add_to_doc_files Source/WebCore/icu/LICENSE
%add_to_doc_files Source/WebCore/LICENSE-APPLE
%add_to_doc_files Source/WebCore/LICENSE-LGPL-2
%add_to_doc_files Source/WebCore/LICENSE-LGPL-2.1
%add_to_doc_files Source/JavaScriptCore/COPYING.LIB
%add_to_doc_files Source/JavaScriptCore/THANKS
%add_to_doc_files Source/JavaScriptCore/AUTHORS
%add_to_doc_files Source/JavaScriptCore/icu/README
%add_to_doc_files Source/JavaScriptCore/icu/LICENSE


%post -p /sbin/ldconfig

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :
fi

%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :


%files -f webkitgtk-3.0.lang
%doc %{_docdir}/%{name}-%{version}/
%exclude %{_libdir}/*.la
%{_libdir}/libwebkitgtk-3.0.so.*
%{_libdir}/libwebkit2gtk-3.0.so.*
%{_libdir}/libjavascriptcoregtk-3.0.so.*
%{_libdir}/girepository-1.0/WebKit-3.0.typelib
%{_libdir}/girepository-1.0/WebKit2-3.0.typelib
%{_libdir}/girepository-1.0/JSCore-3.0.typelib
%{_libexecdir}/%{name}/
%{_libexecdir}/WebKitPluginProcess
%{_libexecdir}/WebKitWebProcess
%{_datadir}/webkitgtk-3.0

%files  devel
%{_bindir}/jsc-3
%{_includedir}/webkitgtk-3.0
%{_libdir}/libwebkitgtk-3.0.so
%{_libdir}/libwebkit2gtk-3.0.so
%{_libdir}/libjavascriptcoregtk-3.0.so
%{_libdir}/pkgconfig/webkitgtk-3.0.pc
%{_libdir}/pkgconfig/webkit2gtk-3.0.pc
%{_libdir}/pkgconfig/javascriptcoregtk-3.0.pc
%{_datadir}/gir-1.0/WebKit-3.0.gir
%{_datadir}/gir-1.0/WebKit2-3.0.gir
%{_datadir}/gir-1.0/JSCore-3.0.gir

%files doc
%dir %{_datadir}/gtk-doc
%dir %{_datadir}/gtk-doc/html
%{_datadir}/gtk-doc/html/webkitgtk
%{_datadir}/gtk-doc/html/webkit2gtk


%changelog
* Tue Dec 18 2012 Dan Horák <dan[at]danny.cz> - 1.11.2-3
- fix 32-bit non-JIT arches

* Tue Dec 18 2012 Dan Horák <dan[at]danny.cz> - 1.11.2-2
- fix build for non-JIT arches

* Sat Nov 24 2012 Kalev Lember <kalevlember@gmail.com> - 1.11.2-1
- Update to 1.11.2
- Add a patch to explicitly link with librt

* Wed Oct 17 2012 Kalev Lember <kalevlember@gmail.com> - 1.10.1-1
- Update to 1.10.1
- Enable the parallel build
- Drop the upstreamed Geode-compatibility patch

* Fri Oct  5 2012 Daniel Drake <dsd@laptop.org> - 1.10.0-2
- Restore compatibility with AMD Geode processors

* Mon Sep 24 2012 Kalev Lember <kalevlember@gmail.com> - 1.10.0-1
- Update to 1.10.0
- Adjust for webkit -> webkitgtk upstream tarball rename

* Wed Sep 19 2012 Kalev Lember <kalevlember@gmail.com> - 1.9.92-2
- Build with gstreamer1

* Wed Sep 19 2012 Kalev Lember <kalevlember@gmail.com> - 1.9.92-1
- Update to 1.9.92

* Wed Sep 05 2012 Kalev Lember <kalevlember@gmail.com> - 1.9.91-1
- Update to 1.9.91

* Sun Sep  2 2012 Matthias Clasen <mclasen@redhat.com> - 1.9.90-2
- Rebuild

* Wed Aug 29 2012 Daniel Drake <dsd@laptop.org> - 1.9.90-1
- Update to latest release (#850520)

* Thu Aug  9 2012 Daniel Drake <dsd@laptop.org> - 1.9.5-2
- Add upstream patch to fix build without JIT (#843428)
- Add upstream patch to fix build with latest gcc/bison

* Wed Jul 18 2012 Kalev Lember <kalevlember@gmail.com> - 1.9.5-1
- Update to 1.9.5
- Build with -g1 to avoid running into 4 GB ar format limit

* Wed Jul 11 2012 Ville Skyttä <ville.skytta@iki.fi> - 1.9.4-3
- Fix %%post scriptlet dependencies.

* Wed Jul 04 2012 Dan Horák <dan[at]danny.cz> - 1.9.4-2
- apply workaround for s390x until #835957 is resolved (static library archive > 4 GB)

* Thu Jun 28 2012 Kalev Lember <kalevlember@gmail.com> - 1.9.4-1
- Update to 1.9.4

* Thu Jun 07 2012 Kalev Lember <kalevlember@gmail.com> - 1.9.3-1
- Update to 1.9.3
- Build webkit2gtk and BR gtk2-devel for its plugin process

* Tue May 15 2012 Karsten Hopp <karsten@redhat.com> 1.8.1-3
- disable JIT on PPC(64) as the autodetection enables it even if not supported

* Mon May 14 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.8.1-2
- Explicitly disable JIT on ARM as it's not currently stable with JS heavy pages

* Tue Apr 24 2012 Kalev Lember <kalevlember@gmail.com> - 1.8.1-1
- Update to 1.8.1
- Dropped the backported patches
- Remove lib64 rpaths with chrpath
- Update gsettings rpm scriptlets

* Wed Apr 18 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.8.0-3
- Add upstream patch to fix crash when SSE2 isn't present
- Add upstream patch to flickering when some widgets are drawn

* Mon Apr 09 2012 Kalev Lember <kalevlember@gmail.com> - 1.8.0-2
- Finish splitting out a -doc subpackage (#808917)

* Wed Mar 28 2012 Richard Hughes <rhughes@redhat.com> - 1.8.0-1
- Update to 1.8.0.

* Sat Mar 24 2012 Dan Horák <dan[at]danny.cz> - 1.7.92-2
- add ppc to low mem arches
- decrease debuginfo verbosity on s390 to save memory

* Wed Mar 21 2012 Kalev Lember <kalevlember@gmail.com> - 1.7.92-1
- Update to 1.7.92
- Don't pass --enable-geolocation to configure; it's now enabled by default

* Thu Mar 15 2012 Karsten Hopp <karsten@redhat.com> 1.7.91-2
- disable jit on ppc(64)

* Thu Mar  8 2012 Matthias Clasen <mclasen@redhat.com> - 1.7.91-1
- Update to 1.7.91

* Tue Feb 28 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.7.5-3
- Add ARM to and optimise compile flags for low mem arches

* Mon Feb 20 2012 Dan Horák <dan[at]danny.cz> - 1.7.5-2
- don't enable jit on s390(x)

* Tue Feb  7 2012 Matthias Clasen <mclasen@redhat.com> - 1.7.5-1
- Update to 1.7.5

* Tue Jan 17 2012 Matthias Clasen <mclasen@redhat.com> - 1.7.4-1
- Update to 1.7.4

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 20 2011 Matthias Clasen <mclasen@redhat.com> - 1.7.3-1
- Update to 1.7.3

* Thu Nov 24 2011 Tomas Bzatek <tbzatek@redhat.com> - 1.7.2-1
- Update to 1.7.2

* Mon Nov 7 2011 Matthias Clasen <mclasen@redhat.com> 1.7.1-2
- Rebuild against new libpng

* Wed Nov  2 2011 Matthias Clasen <mclasen@redhat.com> 1.7.1-1
- Update to 1.7.1

* Wed Oct 12 2011 Dan Horák <dan[at]danny.cz> 1.6.1-2
- fix build on s390(x)

* Wed Sep 28 2011 Ray Strode <rstrode@redhat.com> 1.6.1-1
- Update to 1.6.1

* Fri Sep 09 2011 Caolán McNamara <caolanm@redhat.com> - 1.5.1-2
- rebuild for icu 4.8.1

* Thu Jun 16 2011 Tomas Bzatek <tbzatek@redhat.com> - 1.5.1-1
- Update to 1.5.1

* Tue Jun 14 2011 Bastien Nocera <bnocera@redhat.com> 1.4.0-3
- Rebuild against newer GTK+

* Wed May 11 2011 Cosimo Cecchi <cosimoc@redhat.com> 1.4.0-2
- Add a doc package for gtk-doc documentation

* Tue Apr 26 2011 Matthias Clasen <mclasen@redhat.com> 1.4.0-1
- Update to 1.4.0

* Tue Mar 22 2011 Matthias Clasen <mclasen@redhat.com> 1.3.13-1
- Update to 1.3.13

* Thu Feb 10 2011 Matthias Clasen <mclasen@redhat.com> 1.3.10-3
- Rebuild against newer gtk

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> 1.3.11-1
- 1.3.11

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> 1.3.10-2
- Rebuild against newer gtk

* Mon Jan 10 2011 Matthias Clasen <mclasen@redhat.com> 1.3.10-1
- Update to 1.3.10

* Sun Jan  9 2011 Matthias Clasen <mclasen@redhat.com> 1.3.9-1
- Update to 1.3.9

* Fri Dec  3 2010 Matthias Clasen <mclasen@redhat.com> 1.3.7-2
- Rebuild against new gtk

* Wed Dec  1 2010 Matthias Clasen <mclasen@redhat.com> 1.3.7-1
- Update to 1.3.7

* Wed Nov 11 2010 Matthias Clasen <mclasen@redhat.com> 1.3.6-1
- Update to 1.3.6
- Disable the s390 patch again :-( Upstream it, maybe ?

* Thu Nov 11 2010 Dan Horák <dan[at]danny.cz> - 1.3.5-2
- Updated and re-enabled the s390 patch

* Mon Nov  1 2010 Matthias Clasen <mclasen@redhat.com> 1.3.5-1
- Update to 1.3.5

* Wed Sep 29 2010 jkeating - 1.3.4-3
- Rebuilt for gcc bug 634757

* Fri Sep 24 2010 Matthias Clasen <mclasen@redhat.com> 1.3.4-2
- Enable JIT/patch for execmem
- Move inspector to the main package

* Thu Sep 23 2010 Matthias Clasen <mclasen@redhat.com> 1.3.4-1
- Update to 1.3.4

* Wed Aug 25 2010 Dan Horák <dan[at]danny.cz> - 1.3.3-4
- Do not generate debug information to prevent linker memory exhaustion on s390 with its 2 GB address space

* Wed Jul 21 2010 Dan Horák <dan[at]danny.cz> - 1.3.3-3
- Fix build on s390(x)

* Thu Jul 15 2010 Colin Walters <walters@verbum.org> - 1.3.3-2
- Rebuild with new gobject-introspection

* Fri Jul  9 2010 Matthias Clasen <mclasen@redhat.com> 1.3.2-2
- Fix conflicting gettext domain with webkitgtk
- Drop the -doc subpackage

* Thu Jul  1 2010 Matthias Clasen <mclasen@redhat.com> 1.3.2-1
- Initial packaging
