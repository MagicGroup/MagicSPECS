Summary:   Library for AppStream metadata
Summary(zh_CN.UTF-8): 应用程序流元数据的库
Name:      libappstream-glib
Version: 0.5.5
Release: 1%{?dist}
License:   LGPLv2+
URL:       http://people.freedesktop.org/~hughsient/appstream-glib/
Source0:   http://people.freedesktop.org/~hughsient/appstream-glib/releases/appstream-glib-%{version}.tar.xz

BuildRequires: glib2-devel >= 2.16.1
BuildRequires: libtool
BuildRequires: docbook-utils
BuildRequires: gtk-doc
BuildRequires: gobject-introspection-devel
BuildRequires: gperf
BuildRequires: libarchive-devel
BuildRequires: libsoup-devel
BuildRequires: gdk-pixbuf2-devel
BuildRequires: gtk3-devel
BuildRequires: gettext
BuildRequires: intltool

# for the builder component
BuildRequires: fontconfig-devel
BuildRequires: freetype-devel
BuildRequires: pango-devel
BuildRequires: rpm-devel
BuildRequires: sqlite-devel
BuildRequires: gcab

# for the manpages
BuildRequires: libxslt
BuildRequires: docbook-style-xsl

# no longer required
Obsoletes: appdata-tools < 0.1.9
Provides: appdata-tools

%description
This library provides GObjects and helper methods to make it easy to read and
write AppStream metadata. It also provides a simple DOM implementation that
makes it easy to edit nodes and convert to and from the standardized XML
representation.

%description -l zh_CN.UTF-8
应用程序流元数据的库。

%package devel
Summary: GLib Libraries and headers for appstream-glib
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
GLib headers and libraries for appstream-glib.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package builder
Summary: Library and command line tools for building AppStream metadata
Summary(zh_CN.UTF-8): 构建应用程序流元数据的库和命令行工具
Requires: %{name}%{?_isa} = %{version}-%{release}

%description builder
This library and command line tool is used for building AppStream metadata
from a directory of packages.

%description builder -l zh_CN.UTF-8
构建应用程序流元数据的库和命令行工具。

%package builder-devel
Summary: GLib Libraries and headers for appstream-builder
Summary(zh_CN.UTF-8): %{name}-builder 的开发包
Requires: %{name}-builder%{?_isa} = %{version}-%{release}

%description builder-devel
GLib headers and libraries for appstream-builder.

%description builder-devel -l zh_CN.UTF-8
%{name}-builder 的开发包。

%prep
%setup -q -n appstream-glib-%{version}

%build
%configure \
        --enable-gtk-doc \
        --disable-dep11 \
        --disable-static \
        --disable-silent-rules \
        --disable-dependency-tracking

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

%__rm -f %{buildroot}%{_libdir}/libappstream-glib*.la
%__rm -f %{buildroot}%{_libdir}/libappstream-builder*.la
%__rm -f %{buildroot}%{_libdir}/asb-plugins-4/*.la
magic_rpm_clean.sh
%find_lang appstream-glib || :

%post -p /sbin/ldconfig
%post builder -p /sbin/ldconfig

%postun -p /sbin/ldconfig
%postun builder -p /sbin/ldconfig

%files -f appstream-glib.lang
%doc README.md AUTHORS NEWS COPYING
%{_libdir}/libappstream-glib.so.*
%{_libdir}/girepository-1.0/*.typelib
%{_bindir}/appstream-util
#%{_bindir}/appdata-validate
%dir %{_datadir}/bash-completion/completions/
%{_datadir}/bash-completion/completions/appstream-util
%{_mandir}/man1/appstream-util.1.gz

%files devel
%{_libdir}/libappstream-glib.so
%{_libdir}/pkgconfig/appstream-glib.pc
%dir %{_includedir}/libappstream-glib
%{_includedir}/libappstream-glib/*.h
%{_datadir}/gtk-doc/html/appstream-glib
%{_datadir}/gir-1.0/AppStreamGlib-1.0.gir
%{_datadir}/aclocal/*.m4
%{_datadir}/installed-tests/appstream-glib/*.test

%files builder
%{_bindir}/appstream-builder
%{_datadir}/bash-completion/completions/appstream-builder
%{_libdir}/asb-plugins-4/*.so
%{_libdir}/libappstream-builder.so.*
%{_mandir}/man1/appstream-builder.1.gz

%files builder-devel
%{_libdir}/libappstream-builder.so
%{_libdir}/pkgconfig/appstream-builder.pc
%dir %{_includedir}/libappstream-builder
%{_includedir}/libappstream-builder/*.h
%{_datadir}/gir-1.0/AppStreamBuilder-1.0.gir

%changelog
* Mon Nov 09 2015 Liu Di <liudidi@gmail.com> - 0.5.2-3
- 为 Magic 3.0 重建

* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 0.5.2-2
- 更新到 0.5.2

* Thu Jul 30 2015 Liu Di <liudidi@gmail.com> - 0.4.1-1
- 更新到 0.4.1

* Mon Apr 13 2015 Liu Di <liudidi@gmail.com> - 0.3.6-2
- 为 Magic 3.0 重建

* Mon Mar 30 2015 Richard Hughes <richard@hughsie.com> 0.3.6-1
- New upstream release
- Add a 'replace-screenshots' command to appstream-util
- Always upscale screenshots if they are too small
- Assume the INF DriverVer is UTC
- Remove the gtk3 dep from libappstream-glib
- Use the correct image URL for HiDPI screenshots

* Wed Mar 11 2015 Richard Hughes <richard@hughsie.com> 0.3.5-1
- New upstream release
- Add new API required for firmware support
- Add new API required for OSTree and xdg-app support

* Sat Jan 17 2015 Richard Hughes <richard@hughsie.com> 0.3.4-1
- New upstream release
- Add more applications to the blacklist
- Add show-search-tokens subcommand to appstream-util
- Add some new API for gnome-software to use
- Add the matrix-html subcommand to appstream-util
- Add the VCS information to the AppStream metadata
- Assume <image>foo</image> is a source image kind for AppData files
- Assume that stock icons are available in HiDPI sizes
- Blacklist the 40 most common search tokens
- Check if the search entries are valid before searching
- Check screenshots are a reasonable size
- Fall back to the dumb tokenizer for keywords with special chars
- Set an error if an XML file contains font markup
- Show the offending text when validation fails

* Mon Nov 24 2014 Richard Hughes <richard@hughsie.com> 0.3.3-1
- New upstream release
- Allow filtering addons in the status html pages
- Detect missing parents in the old metadata
- Do not fail to load all the desktop files if one is bad
- Improve appdata-xml.m4 deprecation notice

* Tue Nov 04 2014 Richard Hughes <richard@hughsie.com> 0.3.2-1
- New upstream release
- Add a simple 'search' command to appstream-util
- Add some more valid metadata licenses
- Do not generate metadata with an icon prefix
- Obsolete the appdata-tools package
- Show the kudo stats on the status page

* Tue Oct 21 2014 Richard Hughes <richard@hughsie.com> 0.3.1-1
- New upstream release
- Add an --enable-hidpi argument to appstream-builder
- Add AS_ICON_KIND_EMBEDDED and AS_ICON_KIND_LOCAL
- Add more applications to the blacklist
- Allow application with NoDisplay=true and an AppData file
- Allow AppStream files to be upgraded using appstream-util
- Install AppStream files with correct permissions
- Monitor the XML and icons path for changes
- Relax validation requirements for font metainfo files

* Mon Sep 01 2014 Richard Hughes <richard@hughsie.com> 0.3.0-1
- New upstream release
- Add a new kudo for high contrast icons
- A keyword search match is better than the project name
- Allow desktop->addon demotion with an AppData file
- Allow translated keywords
- Conform to the actual SPDX 2.0 license expression syntax
- Ignore AppData screenshots with xml:lang attributes
- Metadata licenses like 'CC0 and CC-BY-3.0' are content licenses
- Update the SPDX license list to v1.20

* Mon Aug 18 2014 Richard Hughes <richard@hughsie.com> 0.2.5-1
- New upstream release
- Add check-root to appstream-util
- Add some validation rules for metainfo files
- Allow desktop->addon demotion with an AppData file
- Allow different source roots to define addons
- Do not require sentence case when validating with relaxed settings
- Fix up legacy license IDs when tokenizing
- Metadata licenses like 'CC0 and CC-BY-3.0' are valid content licenses
- Never add duplicate <extends> tags

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Aug 05 2014 Richard Hughes <richard@hughsie.com> 0.2.4-1
- New upstream release
- Add an installed tests to validate appdata
- Add support for <source_pkgname> which will be in AppStream 0.8
- Add the <dbus> provide for applications automatically
- Do not load applications with NoDisplay=true when loading local
- Do not pad the compressed AppStream metadata with NUL bytes
- Do not treat app-install metadata as installed
- Markup errors should not be fatal when assembling a store

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 0.2.3-2
- Rebuilt for gobject-introspection 1.41.4

* Thu Jul 17 2014 Richard Hughes <richard@hughsie.com> 0.2.3-1
- New upstream release
- Add oxygen-icon-theme when an application depends on kde-runtime
- Add some simple filtering in the status.html page
- Be more careful with untrusted XML data
- Do not allow duplicates to be added when using as_app_add_kudo_kind()
- Do not fail to build packages with invalid KDE service files
- Record if distro metadata and screenshots are being used
- Show any package duplicates when generating metadata
- Show the builder progress in a ncurses-style panel

* Fri Jul 11 2014 Richard Hughes <richard@hughsie.com> 0.2.2-1
- New upstream release
- Add two new builder plugins to add kudos on KDE applications
- Assume local files are untrusted when parsing
- Do not allow NoDisplay=true applications to ever be in the metadata
- Never scale up small screenshots
- Never upscale icons, either pad or downscale with sharpening
- Sharpen resized screenshots after resizing with a cubic interpolation
- Write metadata of the failed applications

* Tue Jun 24 2014 Richard Hughes <richard@hughsie.com> 0.2.1-1
- New upstream release
- Add an 'appstream-util upgrade' command to convert version < 0.6 metadata
- Add packages recursively when using appstream-builder --packages-dir
- Allow empty URL sections
- Fix the xmldir in the APPSTREAM_XML_RULES m4 helper

* Thu Jun 19 2014 Richard Hughes <richard@hughsie.com> 0.2.0-1
- New upstream release
- Accept slightly truncated SPDX IDs
- Allow any SPDX license when validating in relaxed mode
- Allow as_node_get_attribute_as_int() to parse negative numbers
- Allow dumping .desktop, .appdata.xml and .metainfo.xml files in appstream-util
- Do not add addons that are packaged in the parent package
- Do not require a content license to be included into the metadata
- This is the first release that merges the createrepo_as project.
- Validate the <developer_name> tag values

* Thu Jun 12 2014 Richard Hughes <richard@hughsie.com> 0.1.7-1
- New upstream release
- Add <extends> from the draft AppStream 0.7 specification
- Add support for the 'dbus' AsProvideKind
- Add support for validating metainfo.xml files
- Allow 'appstream-util validate' to validate multiple files
- Do not log a critical warning in as_store_to_xml()
- Fix a crash when we try to validate <p></p>
- Support the non-standard X-Ubuntu-Software-Center-Name

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Richard Hughes <richard@hughsie.com> 0.1.6-1
- New upstream release
- Add some more API for createrepo_as and gnome-software
- Also support validating .appdata.xml.in files
- Correctly parse the localized descriptions from AppData files
- Fix validation of old-style AppData files without screenshot sizes
- Only autodetect the AsAppSourceKind when unknown
- Only require <project_licence> when being strict
- Only show the thumbnail when creating the HTML status page
- Retain comments in .desktop and .appdata.xml files when required

* Mon May 12 2014 Richard Hughes <richard@hughsie.com> 0.1.5-1
- New upstream release
- Add some more API for createrepo_as and gnome-software
- Be less strict with the case of the XML header
- Check the licenses against the SPDX list when validating
- Support AppData version 0.6 files too

* Fri Apr 25 2014 Richard Hughes <richard@hughsie.com> 0.1.4-1
- New upstream release
- Add some more API for createrepo_as and gnome-software
- Add tool appstream-util

* Thu Apr 10 2014 Richard Hughes <richard@hughsie.com> 0.1.3-1
- New upstream release
- Add new API required by gnome-software
- Ignore settings panels when parsing desktop files
- Load AppStream files assuming literal text strings

* Wed Mar 26 2014 Richard Hughes <richard@hughsie.com> 0.1.2-1
- New upstream release
- Add more API for gnome-software to use
- Reduce the number of small attr key allocations
- Use gperf to generate a perfect hash for the tag names
- Use the full ID for the AsStore hash

* Fri Mar 21 2014 Richard Hughes <richard@hughsie.com> 0.1.1-1
- New upstream release
- Add an 'api-version' property to AsStore
- Add the new AsUrlKind's and <architectures> from API 0.6
- Support old-style markup-less <description> tags
- Support the 'origin' attribute on the root node
- Do not crash when using getting an unset description
- Do not depend on functions introduced in Glib 2.39.1
- Fix parsing incompletely translated AppData files

* Tue Mar 18 2014 Richard Hughes <richard@hughsie.com> 0.1.0-1
- First upstream release
