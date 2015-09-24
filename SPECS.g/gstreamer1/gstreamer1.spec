%global         majorminor      1.0

%global         _glib2                  2.32.0
%global         _libxml2                2.4.0
%global         _gobject_introspection  1.31.1

Name:           gstreamer1
Version:	1.5.91
Release:        1%{?dist}
Summary:        GStreamer streaming media framework runtime
Summary(zh_CN.UTF-8): GStreamer 流媒体框架运行库

License:        LGPLv2+
URL:            http://gstreamer.freedesktop.org/
Source0:        http://gstreamer.freedesktop.org/src/gstreamer/gstreamer-%{version}.tar.xz
## For GStreamer RPM provides
Patch0:         gstreamer-inspect-rpm-format.patch
Source1:        gstreamer1.prov
Source2:        gstreamer1.attr

BuildRequires:  glib2-devel >= %{_glib2}
BuildRequires:  libxml2-devel >= %{_libxml2}
BuildRequires:  gobject-introspection-devel >= %{_gobject_introspection}
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  m4
BuildRequires:  check-devel
BuildRequires:  gtk-doc >= 1.3
BuildRequires:  gettext
BuildRequires:  pkgconfig

BuildRequires:  chrpath

### documentation requirements
BuildRequires:  python2
BuildRequires:  openjade
BuildRequires:  jadetex
BuildRequires:  libxslt
BuildRequires:  docbook-style-dsssl
BuildRequires:  docbook-style-xsl
BuildRequires:  docbook-utils
BuildRequires:  transfig
BuildRequires:  netpbm-progs
BuildRequires:  tetex-dvips
BuildRequires:  ghostscript
%if !0%{?rhel}
BuildRequires:  xfig
%endif

%description
GStreamer is a streaming media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new 
plugins.

%description -l zh_CN.UTF-8
GStreamer 是一个流多媒体框架，以C语言写成。

凭借GStreamer，程序员可以很容易地创建各种多媒体功能组件，包括简单的音频
回放，音频和视频播放,录音，流媒体和音频编辑。基于流水线设计，可以创建诸
如视频编辑器、流媒体广播和媒体播放器等等的很多多媒体应用。

%package devel
Summary:        Libraries/include files for GStreamer streaming media framework
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires:       %{name} = %{version}-%{release}
Requires:       glib2-devel >= %{_glib2}
Requires:       libxml2-devel >= %{_libxml2}
Requires:       check-devel


%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package devel-docs
Summary:         Developer documentation for GStreamer streaming media framework
Summary(zh_CN.UTF-8): %{name} 的开发文档
Requires:        %{name} = %{version}-%{release}
BuildArch:       noarch


%description devel-docs
This %{name}-devel-docs contains developer documentation for the
GStreamer streaming media framework.

%description devel-docs -l zh_CN.UTF-8
%{name} 的开发文档。

%prep
%setup -q -n gstreamer-%{version}
%patch0 -p1 -b .rpm-provides


%build
%configure \
  --with-package-name='Fedora GStreamer package' \
  --with-package-origin='http://download.fedoraproject.org' \
  --enable-gtk-doc \
  --enable-debug \
  --disable-tests --disable-examples
make %{?_smp_mflags} V=1


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
# Remove rpath.
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/libgstbase-1.0.so.*
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/libgstcheck-1.0.so.*
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/libgstcontroller-1.0.so.* 
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/libgstnet-1.0.so.*
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstcoreelements.so
chrpath --delete $RPM_BUILD_ROOT%{_libexecdir}/gstreamer-%{majorminor}/gst-plugin-scanner
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/gst-inspect-1.0
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/gst-launch-1.0
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/gst-typefind-1.0
magic_rpm_clean.sh
%find_lang gstreamer-%{majorminor}
# Clean out files that should not be part of the rpm.
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
find $RPM_BUILD_ROOT -name '*.a' -exec rm -f {} ';'
# Add the provides script
install -m0755 -D %{SOURCE1} $RPM_BUILD_ROOT%{_rpmconfigdir}/gstreamer1.prov
# Add the gstreamer plugin file attribute entry (rpm >= 4.9.0)
install -m0644 -D %{SOURCE2} $RPM_BUILD_ROOT%{_rpmconfigdir}/fileattrs/gstreamer1.attr

%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files -f gstreamer-%{majorminor}.lang
%doc AUTHORS COPYING NEWS README RELEASE
%{_libdir}/libgstreamer-%{majorminor}.so.*
%{_libdir}/libgstbase-%{majorminor}.so.*
%{_libdir}/libgstcheck-%{majorminor}.so.*
%{_libdir}/libgstcontroller-%{majorminor}.so.*
%{_libdir}/libgstnet-%{majorminor}.so.*

%{_libexecdir}/gstreamer-%{majorminor}/

%dir %{_libdir}/gstreamer-%{majorminor}
%{_libdir}/gstreamer-%{majorminor}/libgstcoreelements.so

%{_libdir}/girepository-1.0/Gst-%{majorminor}.typelib
%{_libdir}/girepository-1.0/GstBase-%{majorminor}.typelib
%{_libdir}/girepository-1.0/GstCheck-%{majorminor}.typelib
%{_libdir}/girepository-1.0/GstController-%{majorminor}.typelib
%{_libdir}/girepository-1.0/GstNet-%{majorminor}.typelib

%{_bindir}/gst-inspect-%{majorminor}
%{_bindir}/gst-launch-%{majorminor}
%{_bindir}/gst-typefind-%{majorminor}

%{_rpmconfigdir}/gstreamer1.prov
%{_rpmconfigdir}/fileattrs/gstreamer1.attr

%doc %{_mandir}/man1/gst-inspect-%{majorminor}.*
%doc %{_mandir}/man1/gst-launch-%{majorminor}.*
%doc %{_mandir}/man1/gst-typefind-%{majorminor}.*

%files devel
%dir %{_includedir}/gstreamer-%{majorminor}
%dir %{_includedir}/gstreamer-%{majorminor}/gst
%dir %{_includedir}/gstreamer-%{majorminor}/gst/base
%dir %{_includedir}/gstreamer-%{majorminor}/gst/check
%dir %{_includedir}/gstreamer-%{majorminor}/gst/controller
%dir %{_includedir}/gstreamer-%{majorminor}/gst/net
%{_includedir}/gstreamer-%{majorminor}/gst/*.h
%{_includedir}/gstreamer-%{majorminor}/gst/base/*.h
%{_includedir}/gstreamer-%{majorminor}/gst/check/*.h
%{_includedir}/gstreamer-%{majorminor}/gst/controller/*.h
%{_includedir}/gstreamer-%{majorminor}/gst/net/*.h

%{_libdir}/libgstreamer-%{majorminor}.so
%{_libdir}/libgstbase-%{majorminor}.so
%{_libdir}/libgstcheck-%{majorminor}.so
%{_libdir}/libgstcontroller-%{majorminor}.so
%{_libdir}/libgstnet-%{majorminor}.so

%{_datadir}/gir-1.0/Gst-%{majorminor}.gir
%{_datadir}/gir-1.0/GstBase-%{majorminor}.gir
%{_datadir}/gir-1.0/GstCheck-%{majorminor}.gir
%{_datadir}/gir-1.0/GstController-%{majorminor}.gir
%{_datadir}/gir-1.0/GstNet-%{majorminor}.gir

%{_datadir}/aclocal/gst-element-check-%{majorminor}.m4

%{_libdir}/pkgconfig/gstreamer-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-base-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-controller-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-check-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-net-%{majorminor}.pc


%files devel-docs
%doc %{_datadir}/gtk-doc/html/gstreamer-%{majorminor}
%doc %{_datadir}/gtk-doc/html/gstreamer-libs-%{majorminor}
%doc %{_datadir}/gtk-doc/html/gstreamer-plugins-%{majorminor}


%changelog
* Wed Sep 23 2015 Liu Di <liudidi@gmail.com> - 1.5.91-1
- 更新到 1.5.91

* Sun Mar 01 2015 Liu Di <liudidi@gmail.com> - 1.4.5-2
- 更新到 1.4.5

* Thu Jul 10 2014 Liu Di <liudidi@gmail.com> - 1.3.90-2
- 更新到 1.3.90

* Wed Jun 25 2014 Liu Di <liudidi@gmail.com> - 1.3.3-2
- 更新到 1.3.3

* Tue May 06 2014 Liu Di <liudidi@gmail.com> - 1.3.1-2
- 更新到 1.3.1

* Fri Apr 11 2014 Liu Di <liudidi@gmail.com> - 1.2.3-2
- 为 Magic 3.0 重建

* Mon Feb 10 2014 Brian Pepple <bpepple@fedoraproject.org> - 1.2.3-1
- Update to 1.2.3.

* Fri Dec 27 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.2.2-1
- Update to 1.2.2.

* Mon Nov 11 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.2.1-1
- Update to 1.2.1.

* Tue Sep 24 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.2.0-1
- Update to 1.2.0.

* Thu Sep 19 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.1.90-1
- Update to 1.1.90.

* Wed Aug 28 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.1.4-1
- Update to 1.1.4.

* Mon Jul 29 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.1.3-1
- Update to 1.1.3.

* Fri Jul 12 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.1.2-1
- Update to 1.1.2.

* Fri Apr 26 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.0.7-1
- Update to 1.0.7.

* Wed Mar 27 2013 Adam Jackson <ajax@redhat.com>
- Tweak BRs for RHEL

* Fri Mar 22 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.0.6-1
- Update to 1.0.6.
- Remove BR on PyXML.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan  8 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.0.5-1
- Update to 1.0.5.

* Wed Dec 19 2012 Brian Pepple <bpepple@fedoraproject.org> - 1.0.4-1
- Update to 1.0.4

* Wed Nov 21 2012 Brian Pepple <bpepple@fedoraproject.org> - 1.0.3-1
- Update to 1.0.3

* Thu Oct 25 2012 Brian Pepple <bpepple@fedoraproject.org> - 1.0.2-1
- Update to 1.0.2.

* Sun Oct  7 2012 Brian Pepple <bpepple@fedoraproject.org> - 1.0.1-1
- Update to 1.0.1

* Mon Oct  1 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.0.0-2
- Enable verbose build

* Mon Sep 24 2012 Brian Pepple <bpepple@fedoraproject.org> - 1.0.0-1
- Update to 1.0.0.

* Wed Sep 19 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.11.99-1
- Update to 0.11.99

* Fri Sep 14 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.11.94-1
- Update to 0.11.94.

* Sat Sep  8 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.11.93-2
- Add patch to gst-inspect to generate RPM provides
- Add RPM find-provides script

* Tue Aug 14 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.11.93-1
- Update to 0.11.93.
- Bump minimum version of glib2 needed.

* Fri Aug  3 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.11.92-2
- Use %%global instead of %%define.
- Remove rpath.

* Tue Jul 17 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.11.92-1
- Initial Fedora spec file.

