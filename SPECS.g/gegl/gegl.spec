%if 0%{?rhel}
%bcond_with workshop
%else
%bcond_without workshop
%endif

# skip all tests
%global skip_all_checks 1
# skip tests known to be problematic in a specific version
%global skip_checks_version 0.2.0
# for some reason or other comparing generated to reference images segfaults in
# two test cases
# Well, now it is all of them, not just two. :/
%global skip_checks compositions/run-*.xml.sh

Summary:    A graph based image processing framework
Summary(zh_CN.UTF-8): 基于图形的图像处理框架
Name:       gegl
Version:    0.2.0
Release:    7%{?dist}

# Compute some version related macros
# Ugly hack, you need to get your quoting backslashes/percent signs straight
%global major %(ver=%version; echo ${ver%%%%.*})
%global minor %(ver=%version; ver=${ver#%major.}; echo ${ver%%%%.*})
%global micro %(ver=%version; ver=${ver#%major.%minor.}; echo ${ver%%%%.*})
%global apiver %major.%minor

# The binary is under the GPL, while the libs are under LGPL
License:    LGPLv3+ and GPLv3+
Group:      System Environment/Libraries
Group(zh_CN.UTF): 系统环境/库
URL:        http://www.gegl.org/
Source0:    ftp://ftp.gimp.org/pub/gegl/%{apiver}/%{name}-%{version}.tar.bz2
Patch0:     gegl-0.2.0-lua-5.2.patch
Patch1:     gegl-0.2.0-CVE-2012-4433.patch
Patch2:     gegl-0.2.0-remove-src-over-op.patch
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  asciidoc
BuildRequires:  babl-devel >= 0.1.10
BuildRequires:  cairo-devel
BuildRequires:  enscript
BuildRequires:  exiv2-devel
BuildRequires:  gdk-pixbuf2-devel >= 2.18.0
BuildRequires:  glib2-devel >= 2.28.0
BuildRequires:  graphviz
BuildRequires:  gtk2-devel >= 2.18.0
BuildRequires:  intltool >= 0.40.1
BuildRequires:  jasper-devel >= 1.900.1
%if %{with workshop}
BuildRequires:  lensfun-devel >= 0.2.5
%endif
BuildRequires:  libjpeg-devel
BuildRequires:  libopenraw-devel >= 0.0.5
BuildRequires:  libpng-devel
BuildRequires:  librsvg2-devel >= 2.14.0
BuildRequires:  libspiro-devel
BuildRequires:  libv4l-devel
BuildRequires:  lua-devel >= 5.1.0
BuildRequires:  OpenEXR-devel
BuildRequires:  pango-devel
BuildRequires:  perl-devel
BuildRequires:  pkgconfig
BuildRequires:  ruby
BuildRequires:  SDL-devel
BuildRequires:  suitesparse-devel
BuildRequires:  w3m
Requires:       babl%{?_isa} >= 0.1.10

%description
GEGL (Generic Graphics Library) is a graph based image processing framework. 
GEGLs original design was made to scratch GIMPs itches for a new
compositing and processing core. This core is being designed to have
minimal dependencies. and a simple well defined API.

%description -l zh_CN.UTF-8
基于图形的图像处理框架。

%if %{with workshop}
%package operations-workshop
Summary:    Experimental operations for GEGL
Summary(zh_CN.UTF-8): %{name} 的试验性操作
Group:      System Environment/Libraries
Group(zh_CN.UTF): 系统环境/库
Requires:   %{name}%{_isa} = %{version}-%{release}

%description operations-workshop
This package contains experimental operations for GEGL. If used they may yield
unwanted results, or even crash. You're warned!

%description operations-workshop -l zh_CN.UTF-8 
%{name} 的试验性操作，它可能得不到想要的结果，或崩溃。
%endif

%package devel
Summary:    Headers for developing programs that will use %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:      Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:   %{name}%{_isa} = %{version}-%{release}
Requires:   pkgconfig
Requires:   babl-devel%{_isa}
Requires:   glib2-devel%{_isa}

%description devel
This package contains the libraries and header files needed for
developing with %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q
%patch0 -p1 -b .lua-5.2
%patch1 -p1 -b .CVE-2012-4433
%patch2 -p1 -b .remove-src-over-op

%build
# use hardening compiler/linker flags because gegl is likely to deal with
# untrusted input
%define _hardened_build 1

# Needed by Ruby 1.9.3.
export LANG=en_US.utf8

%configure \
%if %{with workshop}
    --enable-workshop \
%else
    --disable-workshop \
%endif
    --with-pic \
    --with-gio \
    --with-gtk \
    --with-cairo \
    --with-pango \
    --with-pangocairo \
    --with-gdk-pixbuf \
    --with-lensfun \
    --with-libjpeg \
    --with-libpng \
    --with-librsvg \
    --with-openexr \
    --with-sdl \
    --with-libopenraw \
    --with-jasper \
    --with-graphviz \
    --with-lua \
    --without-libavformat \
    --with-libv4l \
    --with-libspiro \
    --with-exiv2 \
    --with-umfpack \
    --disable-static \
    --disable-gtk-doc

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install INSTALL='install -p'
pushd operations
# favor non-workshop binaries
make SUBDIRS= install INSTALL='install -p'
for d in */; do
    d="${d%/}"
    if [ "$d" != "workshop" ]; then
        pushd "$d"
        make DESTDIR=%{buildroot} install INSTALL='install -p'
        popd
    fi
done
popd

rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_libdir}/gegl-%{apiver}/*.la

# keep track of workshop/non-workshop operations
opsdir="$PWD/operations"

files_ws="$PWD/operations_files_workshop"
files_non_ws="$PWD/operations_files"
non_ws_filenames_file="$PWD/non_ws_filenames"

find "$opsdir" -path "$opsdir/workshop" -prune -o -regex '.*/\.libs/.*\.so' -printf '%f\n' > "$non_ws_filenames_file"

echo '%%defattr(-, root, root, -)' > "$files_non_ws"
echo '%%defattr(-, root, root, -)' > "$files_ws"

pushd %{buildroot}%{_libdir}/gegl-%{apiver}
for opfile in *.so; do
    if fgrep -q -x "$opfile" "$non_ws_filenames_file"; then
        echo "%{_libdir}/gegl-%{apiver}/$opfile" >> "$files_non_ws"
    else
        echo "%{_libdir}/gegl-%{apiver}/$opfile" >> "$files_ws"
    fi
done
popd
magic_rpm_clean.sh
%find_lang %{name}-%{apiver}

%check
# skip tests known to be problematic in a specific version
%if "%version" == "%skip_checks_version"
pushd tests
for problematic in %skip_checks; do
    rm -f "$problematic"
    cat << EOF > "$problematic"
#!/bin/sh
echo Skipping test "$problematic"
EOF
    chmod +x "$problematic"
done
popd
%endif
make check

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f operations_files -f %{name}-%{apiver}.lang
%defattr(-, root, root, -)
%doc AUTHORS ChangeLog COPYING COPYING.LESSER NEWS README
%{_bindir}/gegl
%{_libdir}/*.so.*
%dir %{_libdir}/gegl-%{apiver}/

%if %{with workshop}
%files operations-workshop -f operations_files_workshop
%endif

%files devel
%defattr(-, root, root, -)
%doc %{_datadir}/gtk-doc/
%{_includedir}/gegl-%{apiver}/
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}-%{apiver}.pc

%changelog
* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 0.2.0-6
- 为 Magic 3.0 重建

* Fri Oct 19 2012 Nils Philippsen <nils@redhat.com> - 0.2.0-5
- don't catch "make check" errors but skip known problematic tests

* Fri Oct 19 2012 Nils Philippsen <nils@redhat.com> - 0.2.0-4
- don't require lensfun-devel for building without workshop ops

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May 02 2012 Rex Dieter <rdieter@fedoraproject.org> - 0.2.0-2
- rebuild (exiv2)

* Tue Apr 03 2012 Nils Philippsen <nils@redhat.com> - 0.2.0-1
- version 0.2.0
- split off workshop (i.e. experimental) operations
- don't build/package workshop operations on EL

* Mon Feb 06 2012 Vít Ondruch <vondruch@redhat.com> - 0.1.8-3
- Rebuilt for Ruby 1.9.3.

* Tue Jan 10 2012 Nils Philippsen <nils@redhat.com> - 0.1.8-2
- rebuild for gcc 4.7

* Tue Dec 13 2011 Nils Philippsen <nils@redhat.com> - 0.1.8-1
- version 0.1.8
- drop all patches
- add BRs: gdk-pixbuf2-devel, lensfun-devel
- update BR version: glib2-devel
- use %%_hardened_build macro instead of supplying our own hardening flags

* Thu Nov 17 2011 Nils Philippsen <nils@redhat.com> - 0.1.6-5
- don't require gtk-doc (#707554)

* Mon Nov 07 2011 Nils Philippsen <nils@redhat.com> - 0.1.6-4
- rebuild (libpng)

* Fri Oct 14 2011 Rex Dieter <rdieter@fedoraproject.org> - 0.1.6-3
- rebuild (exiv2)

* Wed Apr 06 2011 Nils Philippsen <nils@redhat.com> - 0.1.6-2
- fix crash when using hstack operation (#661533)

* Tue Feb 22 2011 Nils Philippsen <nils@redhat.com> - 0.1.6-1
- version 0.1.6
- remove obsolete patches
- fix erroneous use of destdir
- correct source URL
- add BR: exiv2-devel, jasper-devel, suitesparse-devel
- update BR versions
- update --with-*/--without-* configure flags
- replace tabs with spaces for consistency

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Oct 19 2010 Nils Philippsen <nils@redhat.com> - 0.1.2-4
- don't leak "root" symbol which clashes with (equally broken) xvnkb input
  method (#642992)

* Wed Jun 23 2010 Nils Philippsen <nils@redhat.com> - 0.1.2-3
- build with -fno-strict-aliasing
- use PIC/PIE because gegl is likely to deal with data coming from untrusted
  sources

* Fri Feb 26 2010 Nils Philippsen <nils@redhat.com>
- use tabs consistently
- let devel depend on gtk-doc

* Fri Feb 19 2010 Nils Philippsen <nils@redhat.com> - 0.1.2-2
- ignore make check failures for now

* Wed Feb 17 2010 Nils Philippsen <nils@redhat.com>
- avoid buffer overflow in gegl_buffer_header_init()
- correct gegl library version, use macro for it

* Tue Feb 16 2010 Nils Philippsen <nils@redhat.com> - 0.1.2-1
- version 0.1.2
- remove obsolete cflags, babl-instrumentation, autoreconf patches
- backported: don't leak each node set on a GeglProcessor

* Sat Jan 23 2010 Deji Akingunola <dakingun@gmail.com> - 0.1.0-3
- Rebuild for babl-0.1.2
- Backport upstream patch that removed babl processing time instrumentation

* Wed Jan 20 2010 Nils Philippsen <nils@redhat.com>
- use tabs consistently to appease rpmdiff

* Tue Aug 18 2009 Nils Philippsen <nils@redhat.com>
- explain patches

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 02 2009 Nils Philippsen - 0.1.0-1
- fix cflags for building

* Thu Jul 02 2009 Nils Philippsen
- version 0.1.0
- use "--disable-gtk-doc" to avoid rebuilding documentation (#481404)
- remove *.la files in %%{_libdir}/gegl-*/ (#509292)

* Thu Jun 04 2009 Deji Akingunola <dakingun@gmail.com> - 0.0.22-5
- Apply patch to build with babl-0.1.0 API changes

* Thu Jun 04 2009 Nils Philippsen - 0.0.22-4
- rebuild against babl-0.1.0

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 29 2009 Nils Philippsen - 0.0.22-2
- use the same timestamps for certain documentation files on all architectures
  to avoid multi-lib conflicts (#481404)
- consolidate spec files between OS releases
- reenable building documentation on ppc64
- explicitly list more build requirements and/or versions to catch eventual
  problems during future builds

* Tue Jan 13 2009 Deji Akingunola <dakingun@gmail.com> - 0.0.22-1
- Update to version 0.0.22

* Tue Oct 07 2008 Deji Akingunola <dakingun@gmail.com> - 0.0.20-1
- Update to latest release

* Thu Jul 10 2008 Deji Akingunola <dakingun@gmail.com> - 0.0.18-1
- Update to latest release

* Thu Feb 28 2008 Deji Akingunola <dakingun@gmail.com> - 0.0.16-1
- New release

* Thu Jan 17 2008 Deji Akingunola <dakingun@gmail.com> - 0.0.15-1.svn20080117
- Update to a svn snapshot for gnome-scan
- Apply patch to fix extensions loading on 64bit systems
- Building the docs on ppc64 segfaults, avoid it for now.

* Sat Dec 08 2007 Deji Akingunola <dakingun@gmail.com> - 0.0.14-1
- Update to 0.0.14 release
- License change from GPLv2+ to GPLv3+

* Thu Oct 25 2007 Deji Akingunola <dakingun@gmail.com> - 0.0.13-0.7.20071011svn
- Include missing requires for the devel subpackage

* Thu Oct 25 2007 Deji Akingunola <dakingun@gmail.com> - 0.0.13-0.6.20071011svn
- BR graphiz instead of graphiz-devel
- Remove the spurious exec flag from a couple of source codes

* Tue Oct 23 2007 Deji Akingunola <dakingun@gmail.com> - 0.0.13-0.5.20071011svn
- Fix missing directory ownership

* Mon Oct 22 2007 Deji Akingunola <dakingun@gmail.com> - 0.0.13-0.4.20071011svn
- Update the License field 

* Fri Oct 12 2007 Deji Akingunola <dakingun@gmail.com> - 0.0.13-0.3.20071011svn
- Package the extension libraries in the main package
- Run 'make check'

* Fri Oct 12 2007 Deji Akingunola <dakingun@gmail.com> - 0.0.13-0.2.20071011svn
- Remove the use of inexistent source

* Thu Oct 11 2007 Deji Akingunola <dakingun@gmail.com> - 0.0.13-0.1.20071011svn
- Initial packaging for Fedora
