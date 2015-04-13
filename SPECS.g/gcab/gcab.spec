Name:           gcab
Version:        0.6
Release:        3%{?dist}
Summary:        Cabinet file library and tool
Summary(zh_CN.UTF-8): Cabinet 文件库和工具

License:        LGPLv2+
#VCS:           git:git://git.gnome.org/gcab
URL:            http://ftp.gnome.org/pub/GNOME/sources/gcab
Source0:        http://ftp.gnome.org/pub/GNOME/sources/gcab/%{version}/%{name}-%{version}.tar.xz

BuildRequires:  intltool
BuildRequires:  vala-tools
BuildRequires:  glib2-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  zlib-devel

%description
gcab is a tool to manipulate Cabinet archive.

%description -l zh_CN.UTF-8
Cabinet 文件库和工具。

%package -n libgcab1
Summary:        Library to create Cabinet archives
Summary(zh_CN.UTF-8): %{name} 的运行库

%description -n libgcab1
libgcab is a library to manipulate Cabinet archive using GIO/GObject.

%description -n libgcab1 -l zh_CN.UTF-8
%{name} 的运行库。

%package -n libgcab1-devel
Summary:        Development files to create Cabinet archives
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires:       libgcab1%{?_isa} = %{version}-%{release}
Requires:       glib2-devel
Requires:       pkgconfig

%description -n libgcab1-devel
libgcab is a library to manipulate Cabinet archive.

Libraries, includes, etc. to compile with the gcab library.

%description -n libgcab1-devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

%build
# --enable-fast-install is needed to fix libtool "cannot relink `gcab'"
%configure --disable-silent-rules --disable-static --enable-fast-install
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

rm -f %{buildroot}%{_libdir}/*.a
rm -f %{buildroot}%{_libdir}/*.la
magic_rpm_clean.sh
%find_lang %{name}

%post -n libgcab1 -p /sbin/ldconfig
%postun -n libgcab1 -p /sbin/ldconfig

%files
%doc COPYING NEWS
%{_bindir}/gcab
%{_mandir}/man1/gcab.1*

%files -n libgcab1 -f %{name}.lang
%doc COPYING NEWS
%{_libdir}/girepository-1.0/GCab-1.0.typelib
%{_libdir}/libgcab-1.0.so.*

%files -n libgcab1-devel
%{_datadir}/gir-1.0/GCab-1.0.gir
%{_datadir}/gtk-doc/html/gcab/*
%{_datadir}/vala/vapi/libgcab-1.0.vapi
%{_includedir}/libgcab-1.0/*
%{_libdir}/libgcab-1.0.so
%{_libdir}/pkgconfig/libgcab-1.0.pc

%changelog
* Mon Apr 13 2015 Liu Di <liudidi@gmail.com> - 0.6-3
- 为 Magic 3.0 重建

* Mon Mar 23 2015 Kalev Lember <kalevlember@gmail.com> - 0.6-2
- Pull in the base library package when installing -devel

* Tue Mar 17 2015 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.6-1
- Update to upstream release v0.6

* Tue Jan 06 2015 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.4-7
- Avoid directory traversal CVE-2015-0552. rhbz#1179126

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 0.4-5
- Rebuilt for gobject-introspection 1.41.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Feb 12 2013 Simone Caronni <negativo17@gmail.com> - 0.4-2
- Removed rpm 4.5 macros/tags, it cannot be built with the vala in el5/el6.
- Removed redundant requirement on libgcab1%%{_isa}, added automatically by rpm.

* Fri Feb  8 2013 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.4-1
- Update to upstream v0.4.

* Fri Feb  8 2013 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.3-3
- Align more fields.
- Use double percentage in comment.
- Include COPYING file in gcab package too.

* Fri Feb  8 2013 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.3-2
- Untabify.
- Use %%{buildroot} consitantly.
- Do not use -1.0 in package names.
- Add more tags based on the el5 spec template.
- Re-add --enable-fast-install trick, to make gcab relink.

* Sun Jan 26 2013 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.3-1
- Initial package (rhbz#895757)
