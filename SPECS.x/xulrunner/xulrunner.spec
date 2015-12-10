# Use system nspr/nss?
%define system_nss        1

# Use system sqlite?
%if 0%{?fedora} < 20
%define system_sqlite     0
%define system_ffi        0
%else
%define system_sqlite     1
%define system_ffi        1
%endif

# Use system cairo?
%define system_cairo      0

# Build as a debug package?
%define debug_build       0

# Minimal required versions
%global cairo_version 1.10.2
%global freetype_version 2.1.9
%global libnotify_version 0.7.0
%global libvpx_version 1.0.0

%if %{?system_nss}
%global nspr_version 4.10.2
%global nspr_build_version %(pkg-config --silence-errors --modversion nspr 2>/dev/null || echo 65536)
%global nss_version 3.15.4
%global nss_build_version %(pkg-config --silence-errors --modversion nss 2>/dev/null || echo 65536)
%endif

%if %{?system_sqlite}
%global sqlite_version 3.7.13
# The actual sqlite version (see #480989):
%global sqlite_build_version %(pkg-config --silence-errors --modversion sqlite3 2>/dev/null || echo 65536)
%endif

# gecko_dir_ver should be set to the version in our directory names
# alpha_version should be set to the alpha number if using an alpha, 0 otherwise
# beta_version  should be set to the beta number if using a beta, 0 otherwise
# rc_version    should be set to the RC number if using an RC, 0 otherwise
%global gecko_dir_ver %{version}
%global alpha_version 0
%global beta_version  0
%global rc_version    0

%global tarballname   firefox
%global mozappdir     %{_libdir}/%{name}
%global tarballdir    mozilla-release

# crash reporter work only on x86/x86_64
%ifarch %{ix86} x86_64
%global enable_mozilla_crashreporter 1
%else
%global enable_mozilla_crashreporter 0
%endif

%if %{alpha_version} > 0
%global pre_version a%{alpha_version}
%global tarballdir  mozilla-beta
%endif
%if %{beta_version} > 0
%global pre_version b%{beta_version}
%global tarballdir  mozilla-beta
%endif
%if %{rc_version} > 0
%global pre_version rc%{rc_version}
%global tarballdir  mozilla-release
%endif

%if %{defined pre_version}
%global gecko_verrel %{expand:%%{version}}-%{pre_version}
%global pre_tag .%{pre_version}
%else
%global gecko_verrel %{expand:%%{version}}
%endif

Summary:        XUL Runtime for Gecko Applications
Name:           xulrunner
Version:        40.0
Release:        5%{?pre_tag}%{?dist}
URL:            http://developer.mozilla.org/En/XULRunner
License:        MPLv1.1 or GPLv2+ or LGPLv2+
Group:          Applications/Internet
Source0:        ftp://ftp.mozilla.org/pub/%{tarballname}/releases/%{version}%{?pre_version}/source/%{tarballname}-%{version}%{?pre_version}.source.tar.bz2
Source10:       %{name}-mozconfig
Source12:       %{name}-redhat-default-prefs.js
Source21:       %{name}.sh.in

# build patches
Patch1:         xulrunner-install-dir.patch
Patch2:         firefox-build.patch
Patch3:         mozilla-build-arm.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=814879#c3
Patch18:        xulrunner-24.0-jemalloc-ppc.patch
# workaround linking issue on s390 (JSContext::updateMallocCounter(size_t) not found)
Patch19:        xulrunner-24.0-s390-inlines.patch
Patch20:        firefox-build-prbool.patch
Patch21:        aarch64-fix-skia.patch
Patch22:        mozilla-1005535.patch
Patch24:        rhbz-1219542-s390-build.patch

# Fedora specific patches
Patch200:        mozilla-193-pkgconfig.patch
# Unable to install addons from https pages
Patch204:        rhbz-966424.patch

# Upstream patches

# ---------------------------------------------------

%if %{?system_nss}
BuildRequires:  nspr-devel >= %{nspr_version}
BuildRequires:  nss-devel >= %{nss_version}
BuildRequires:  nss-static >= %{nss_version}
%endif
%if %{?system_cairo}
BuildRequires:  cairo-devel >= %{cairo_version}
%endif
BuildRequires:  libpng-devel
BuildRequires:  libjpeg-devel
BuildRequires:  zip
BuildRequires:  bzip2-devel
BuildRequires:  zlib-devel
BuildRequires:  libIDL-devel
BuildRequires:  gtk2-devel
BuildRequires:  krb5-devel
BuildRequires:  pango-devel
BuildRequires:  freetype-devel >= %{freetype_version}
BuildRequires:  libXt-devel
BuildRequires:  libXrender-devel
BuildRequires:  hunspell-devel
BuildRequires:  startup-notification-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  libnotify-devel >= %{libnotify_version}
BuildRequires:  mesa-libGL-devel
BuildRequires:  libcurl-devel
BuildRequires:  libvpx-devel >= %{libvpx_version}
BuildRequires:  autoconf213
BuildRequires:  pulseaudio-libs-devel

Requires:       mozilla-filesystem
%if %{?system_nss}
Requires:       nspr >= %{nspr_build_version}
Requires:       nss >= %{nss_build_version}
%endif
Provides:       gecko-libs = %{gecko_verrel}
Provides:       gecko-libs%{?_isa} = %{gecko_verrel}
Conflicts:      firefox < 3.6

%if %{?system_sqlite}
BuildRequires:  sqlite-devel >= %{sqlite_version}
Requires:       sqlite >= %{sqlite_build_version}
%endif

%if %{?system_ffi}
BuildRequires:  libffi-devel
%endif

%description
XULRunner is a Mozilla runtime package that can be used to bootstrap XUL+XPCOM
applications that are as rich as Firefox and Thunderbird. It provides mechanisms
for installing, upgrading, and uninstalling these applications. XULRunner also
provides libxul, a solution which allows the embedding of Mozilla technologies
in other projects and products.

%package devel
Summary: Development files for Gecko
Group: Development/Libraries
Obsoletes: mozilla-devel < 1.9
Obsoletes: firefox-devel < 2.1
Obsoletes: xulrunner-devel-unstable
Provides: gecko-devel = %{gecko_verrel}
Provides: gecko-devel%{?_isa} = %{gecko_verrel}
Provides: gecko-devel-unstable = %{gecko_verrel}
Provides: gecko-devel-unstable%{?_isa} = %{gecko_verrel}

Requires: xulrunner = %{version}-%{release}
%if %{?system_nss}
Requires: nspr-devel >= %{nspr_build_version}
Requires: nss-devel >= %{nss_build_version}
%endif
%if %{?system_cairo}
Requires: cairo-devel >= %{cairo_version}
%endif
Requires: libjpeg-devel
Requires: zip
Requires: bzip2-devel
Requires: zlib-devel
Requires: libIDL-devel
Requires: gtk2-devel
Requires: krb5-devel
Requires: pango-devel
Requires: freetype-devel >= %{freetype_version}
Requires: libXt-devel
Requires: libXrender-devel
Requires: hunspell-devel
%if %{?system_sqlite}
Requires: sqlite-devel
%endif
Requires: startup-notification-devel
Requires: alsa-lib-devel
Requires: libnotify-devel
Requires: mesa-libGL-devel
Requires: libvpx-devel >= %{libvpx_version}

%description devel
This package contains the libraries amd header files that are needed
for writing XUL+XPCOM applications with Mozilla XULRunner and Gecko.

%if %{enable_mozilla_crashreporter}
%global moz_debug_prefix %{_prefix}/lib/debug
%global moz_debug_dir %{moz_debug_prefix}%{mozappdir}
%global uname_m %(uname -m)
%global symbols_file_name %{name}-%{version}.en-US.%{_os}-%{uname_m}.crashreporter-symbols.zip
%global symbols_file_path %{moz_debug_dir}/%{symbols_file_name}
%global _find_debuginfo_opts -p %{symbols_file_path} -o debugcrashreporter.list
%global crashreporter_pkg_name mozilla-crashreporter-%{name}-debuginfo
%package -n %{crashreporter_pkg_name}
Summary: Debugging symbols used by Mozilla's crash reporter servers
Group: Development/Debug
%description -n %{crashreporter_pkg_name}
This package provides debug information for XULRunner, for use by
Mozilla's crash reporter servers.  If you are trying to locally
debug %{name}, you want to install %{name}-debuginfo instead.
%files -n %{crashreporter_pkg_name} -f debugcrashreporter.list
%defattr(-,root,root)
%endif

#---------------------------------------------------------------------

%prep
%setup -q -c
cd %{tarballdir}

%patch1  -p1
%patch2  -p2 -b .build
%patch3  -p2 -b .arm
%patch18 -p2 -b .jemalloc-ppc
%patch19 -p2 -b .s390-inlines
%patch20 -p1 -b .prbool
%patch21 -p1 -b .aarch64-fix-skia
%patch22 -p1 -b .mozilla-1005535
%ifarch s390
%patch24 -p1 -b .rhbz-1219542-s390
%endif

%patch200 -p2 -b .pk
%patch204 -p2 -b .966424

# Upstream patches


%{__rm} -f .mozconfig
%{__cp} %{SOURCE10} .mozconfig

%if %{?system_nss}
echo "ac_add_options --with-system-nspr" >> .mozconfig
echo "ac_add_options --with-system-nss" >> .mozconfig
%else
echo "ac_add_options --without-system-nspr" >> .mozconfig
echo "ac_add_options --without-system-nss" >> .mozconfig
%endif

%if %{?system_sqlite}
echo "ac_add_options --enable-system-sqlite" >> .mozconfig
%else
echo "ac_add_options --disable-system-sqlite" >> .mozconfig
%endif

%if %{?system_cairo}
echo "ac_add_options --enable-system-cairo" >> .mozconfig
%else
echo "ac_add_options --disable-system-cairo" >> .mozconfig
%endif

%if %{?system_ffi}
echo "ac_add_options --enable-system-ffi" >> .mozconfig
%endif


%if %{?debug_build}
echo "ac_add_options --enable-debug" >> .mozconfig
echo "ac_add_options --disable-optimize" >> .mozconfig
%else
echo "ac_add_options --disable-debug" >> .mozconfig
echo "ac_add_options --enable-optimize" >> .mozconfig
%endif

# s390(x) fails to start with jemalloc enabled
%ifarch s390 s390x
echo "ac_add_options --disable-jemalloc" >> .mozconfig
%endif

%ifarch armv7hl
echo "ac_add_options --with-arch=armv7-a" >> .mozconfig
echo "ac_add_options --with-float-abi=hard" >> .mozconfig
echo "ac_add_options --with-fpu=vfpv3-d16" >> .mozconfig
echo "ac_add_options --disable-elf-hack" >> .mozconfig
%endif
%ifarch armv7hnl
echo "ac_add_options --with-arch=armv7-a" >> .mozconfig
echo "ac_add_options --with-float-abi=hard" >> .mozconfig
echo "ac_add_options --with-fpu=neon" >> .mozconfig
echo "ac_add_options --disable-elf-hack" >> .mozconfig
%endif
%ifarch armv5tel
echo "ac_add_options --with-arch=armv5te" >> .mozconfig
echo "ac_add_options --with-float-abi=soft" >> .mozconfig
echo "ac_add_options --disable-elf-hack" >> .mozconfig
echo "ac_add_options --disable-ion" >> .mozconfig
echo "ac_add_options --disable-yarr-jit" >> .mozconfig
%endif

%ifnarch %{ix86} x86_64
echo "ac_add_options --disable-webrtc" >> .mozconfig
%endif

#---------------------------------------------------------------------

%build
%if %{?system_sqlite}
# Do not proceed with build if the sqlite require would be broken:
# make sure the minimum requirement is non-empty, ...
sqlite_version=$(expr "%{sqlite_version}" : '\([0-9]*\.\)[0-9]*\.') || exit 1
# ... and that major number of the computed build-time version matches:
case "%{sqlite_build_version}" in
  "$sqlite_version"*) ;;
  *) exit 1 ;;
esac
%endif

cd %{tarballdir}

# Update the various config.guess to upstream release for aarch64 support
find ./ -name config.guess -exec cp /usr/lib/rpm/config.guess {} ';'

# -fpermissive is needed to build with gcc 4.6+ which has become stricter
# 
# Mozilla builds with -Wall with exception of a few warnings which show up
# everywhere in the code; so, don't override that.
#
# Disable C++ exceptions since Mozilla code is not exception-safe
#
MOZ_OPT_FLAGS=$(echo "$RPM_OPT_FLAGS" | %{__sed} -e 's/-Wall//')
%if %{?debug_build}
MOZ_OPT_FLAGS=$(echo "$MOZ_OPT_FLAGS" | %{__sed} -e 's/-O2//')
%endif
%ifarch s390
MOZ_OPT_FLAGS=$(echo "$MOZ_OPT_FLAGS" | %{__sed} -e 's/-g/-g1/')
# If MOZ_DEBUG_FLAGS is empty, firefox's build will default it to "-g" which
# overrides the -g1 from line above and breaks building on s390
# (OOM when linking, rhbz#1238225)
export MOZ_DEBUG_FLAGS=" "
%endif
%ifarch s390 %{arm} ppc aarch64
MOZ_LINK_FLAGS="-Wl,--no-keep-memory -Wl,--reduce-memory-overheads"
%endif

#rhbz#1037063
MOZ_OPT_FLAGS="$MOZ_OPT_FLAGS -Wformat-security -Wformat -Werror=format-security"

export CFLAGS="$MOZ_OPT_FLAGS"
export CXXFLAGS="$MOZ_OPT_FLAGS -fpermissive"
export LDFLAGS=$MOZ_LINK_FLAGS

export PREFIX='%{_prefix}'
export LIBDIR='%{_libdir}'

MOZ_SMP_FLAGS=-j1
# On x86 architectures, Mozilla can build up to 4 jobs at once in parallel,
# however builds tend to fail on other arches when building in parallel.
%ifarch %{ix86} x86_64 ppc ppc64 ppc64le aarch64 %{arm}
[ -z "$RPM_BUILD_NCPUS" ] && \
     RPM_BUILD_NCPUS="`/usr/bin/getconf _NPROCESSORS_ONLN`"
[ "$RPM_BUILD_NCPUS" -ge 2 ] && MOZ_SMP_FLAGS=-j2
[ "$RPM_BUILD_NCPUS" -ge 4 ] && MOZ_SMP_FLAGS=-j4
[ "$RPM_BUILD_NCPUS" -ge 8 ] && MOZ_SMP_FLAGS=-j8
%endif

make -f client.mk build STRIP="/bin/true" MOZ_MAKE_FLAGS="$MOZ_SMP_FLAGS" MOZ_SERVICES_SYNC="1"

# create debuginfo for crash-stats.mozilla.com
%if %{enable_mozilla_crashreporter}
#cd %{moz_objdir}
make -C objdir buildsymbols
%endif

#---------------------------------------------------------------------

%install
cd %{tarballdir}

# set up our prefs before install, so it gets pulled in to omni.jar
%{__cp} -p %{SOURCE12} objdir/dist/bin/defaults/pref/all-redhat.js

DESTDIR=$RPM_BUILD_ROOT make -C objdir install

# Start script install
%{__rm} -rf $RPM_BUILD_ROOT%{_bindir}/%{name}
%{__cat} %{SOURCE21} | %{__sed} -e 's,XULRUNNER_VERSION,%{gecko_dir_ver},g' > \
  $RPM_BUILD_ROOT%{_bindir}/%{name}
%{__chmod} 755 $RPM_BUILD_ROOT%{_bindir}/%{name}

%{__rm} -f $RPM_BUILD_ROOT%{mozappdir}/%{name}-config

# install install_app.py
%{__cp} objdir/dist/bin/install_app.py $RPM_BUILD_ROOT%{mozappdir}

# Copy pc files (for compatibility with 1.9.1)
%{__cp} $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/libxul.pc \
        $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/libxul-unstable.pc
%{__cp} $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/libxul-embedding.pc \
        $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/libxul-embedding-unstable.pc

# Fix multilib devel conflicts...
function install_file() {
genheader=$*
mv ${genheader}.h ${genheader}%{__isa_bits}.h
cat > ${genheader}.h << EOF
/* This file exists to fix multilib conflicts */
#if defined(__x86_64__) || defined(__ia64__) || defined(__s390x__) || defined(__powerpc64__) || (defined(__sparc__) && defined(__arch64__)) || defined(__aarch64__)
#include "${genheader}64.h"
#else
#include "${genheader}32.h"
#endif
EOF
}

INTERNAL_APP_NAME=%{name}-%{gecko_dir_ver}

pushd $RPM_BUILD_ROOT/%{_includedir}/${INTERNAL_APP_NAME}
install_file "mozilla-config"
install_file "js-config"
popd

# Link libraries in sdk directory instead of copying them:
pushd $RPM_BUILD_ROOT%{_libdir}/%{name}-devel-%{gecko_dir_ver}/sdk/lib
for i in *.so; do
     rm $i
     ln -s %{mozappdir}/$i $i
done
popd

# Move sdk/bin to xulrunner libdir
pushd $RPM_BUILD_ROOT%{_libdir}/%{name}-devel-%{gecko_dir_ver}/sdk/bin
mv ply *.py $RPM_BUILD_ROOT%{mozappdir}
popd
rm -rf $RPM_BUILD_ROOT%{_libdir}/%{name}-devel-%{gecko_dir_ver}/sdk/bin

# Library path
LD_SO_CONF_D=%{_sysconfdir}/ld.so.conf.d
LD_CONF_FILE=xulrunner-%{__isa_bits}.conf

%{__mkdir_p} ${RPM_BUILD_ROOT}${LD_SO_CONF_D}
%{__cat} > ${RPM_BUILD_ROOT}${LD_SO_CONF_D}/${LD_CONF_FILE} << EOF
%{mozappdir}
EOF

# Copy over the LICENSE
%{__install} -p -c -m 644 LICENSE $RPM_BUILD_ROOT%{mozappdir}

# Install xpcshell
%{__cp} objdir/dist/bin/xpcshell $RPM_BUILD_ROOT/%{mozappdir}

# Install run-mozilla.sh
%{__cp} objdir/dist/bin/run-mozilla.sh $RPM_BUILD_ROOT/%{mozappdir}

# Use the system hunspell dictionaries
%{__rm} -rf ${RPM_BUILD_ROOT}%{mozappdir}/dictionaries
ln -s %{_datadir}/myspell ${RPM_BUILD_ROOT}%{mozappdir}/dictionaries

# Remove tmp files
find $RPM_BUILD_ROOT/%{mozappdir} -name '.mkdir.done' -exec rm -rf {} \;

# ghost files
%{__mkdir_p} $RPM_BUILD_ROOT%{mozappdir}/components
touch $RPM_BUILD_ROOT%{mozappdir}/components/compreg.dat
touch $RPM_BUILD_ROOT%{mozappdir}/components/xpti.dat

# Add debuginfo for crash-stats.mozilla.com 
%if %{enable_mozilla_crashreporter}
%{__mkdir_p} $RPM_BUILD_ROOT/%{moz_debug_dir}
%{__cp} objdir/dist/%{symbols_file_name} $RPM_BUILD_ROOT/%{moz_debug_dir}
%endif

#---------------------------------------------------------------------

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%preun
# is it a final removal?
if [ $1 -eq 0 ]; then
  %{__rm} -rf %{mozappdir}/components
fi

%files
%defattr(-,root,root,-)
%{_bindir}/xulrunner
%dir %{mozappdir}
%doc %attr(644, root, root) %{mozappdir}/LICENSE
%doc %attr(644, root, root) %{mozappdir}/README.xulrunner
%{mozappdir}/chrome
%{mozappdir}/chrome.manifest
%{mozappdir}/dictionaries
%dir %{mozappdir}/components
%ghost %{mozappdir}/components/compreg.dat
%ghost %{mozappdir}/components/xpti.dat
%{mozappdir}/components/*.so
%{mozappdir}/components/*.manifest
%{mozappdir}/omni.ja
%{mozappdir}/*.so
%{mozappdir}/run-mozilla.sh
%{mozappdir}/xulrunner
%{mozappdir}/xulrunner-stub
%{mozappdir}/platform.ini
%{mozappdir}/dependentlibs.list
%{_sysconfdir}/ld.so.conf.d/xulrunner*.conf
%{mozappdir}/plugin-container
%{mozappdir}/gmp-clearkey
%if !%{?system_nss}
%{mozappdir}/*.chk
%endif
%if %{enable_mozilla_crashreporter}
%{mozappdir}/crashreporter
%{mozappdir}/crashreporter.ini
%{mozappdir}/Throbber-small.gif
%endif
%{mozappdir}/install_app.py
%ghost %{mozappdir}/install_app.pyc
%ghost %{mozappdir}/install_app.pyo
%{mozappdir}/gmp-fake*/*

%files devel
%defattr(-,root,root,-)
%dir %{_libdir}/%{name}-devel-*
%{_datadir}/idl/%{name}*%{gecko_dir_ver}
%{_includedir}/%{name}*%{gecko_dir_ver}
%{_libdir}/%{name}-devel-*/*
%{_libdir}/pkgconfig/*.pc
%{mozappdir}/xpcshell
%{mozappdir}/*.py
%ghost %{mozappdir}/*.pyc
%ghost %{mozappdir}/*.pyo
%dir %{mozappdir}/ply
%{mozappdir}/ply/*.py
%ghost %{mozappdir}/ply/*.pyc
%ghost %{mozappdir}/ply/*.pyo

#---------------------------------------------------------------------

%changelog
* Sun Nov 15 2015 Liu Di <liudidi@gmail.com> - 40.0-5
- 为 Magic 3.0 重建

* Fri Nov 06 2015 Liu Di <liudidi@gmail.com> - 40.0-4
- 为 Magic 3.0 重建

* Thu Oct 01 2015 Liu Di <liudidi@gmail.com> - 40.0-3
- 为 Magic 3.0 重建

* Wed Sep 2 2015 Martin Stransky <stransky@redhat.com> - 40.0-2
- Disable Skia to build on second arches

* Tue Aug 25 2015 Petr Jasicek <pjasicek@redhat.com> - 40.0-1
- Update to 40.0

* Wed Jul 22 2015 Petr Jasicek <pjasicek@redhat.com> - 39.0-3
- Removed unneeded patch files

* Tue Jul 14 2015 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 39.0-2
- fixed build
  - dropped firefox-nss-3.18.0.patch as we have 3.19.2 available
  - refreshed mozilla-1005535.patch patch to apply

* Fri Jul 10 2015 Martin Stransky <stransky@redhat.com> - 39.0-1
- Update to 39.0

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 38.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 7 2015 Martin Stransky <stransky@redhat.com> - 38.0-1
- Update to 38.0 Build 2

* Mon Apr 27 2015 Jan Horak <jhorak@redhat.com> - 37.0.2-2
- Added patch for big endian arches

* Thu Apr 16 2015 Jan Horak <jhorak@redhat.com> - 37.0.2-1
- Update to 37.0.2

* Wed Apr 15 2015 Martin Stransky <stransky@redhat.com> - 37.0.1-1
- Update to 37.0.1

* Mon Apr  6 2015 Tom Callaway <spot@fedoraproject.org> - 33.0-3
- rebuild for libvpx 1.4.0

* Wed Oct 22 2014 Dan Horák <dan[at]danny.cz> - 33.0-2
- Fix filelist for secondary arches

* Thu Oct 16 2014 Martin Stransky <stransky@redhat.com> - 33.0-1
- Update to 33.0

* Sat Sep 20 2014 Peter Robinson <pbrobinson@fedoraproject.org> 32.0.2-1
- Update to 32.0.2
- sync fixes to the same as firefox

* Tue Sep 9 2014 Martin Stransky <stransky@redhat.com> - 32.0-2
- move /sdk/bin to xulrunner libdir

* Tue Aug 26 2014 Martin Stransky <stransky@redhat.com> - 32.0-1
- Update to 32.0 build 1

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 31.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 25 2014 Martin Stransky <stransky@redhat.com> - 31.0-1
- Update to 31.0 build 2

* Fri Jul 25 2014 Yaakov Selkowitz <yselkowi@redhat.com> - 30.0-3
- Fix mozilla-config.h wrapper on aarch64

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 30.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jun 5 2014 Martin Stransky <stransky@redhat.com> - 30.0-1
- Update to 30.0 build 1
- Disabled shared js

* Fri May 23 2014 Martin Stransky <stransky@redhat.com> - 29.0-5
- Added a build fix for ppc64 - rhbz#1100495

* Thu May 15 2014 Peter Robinson <pbrobinson@fedoraproject.org> 29.0-4
- Update aarch64 bits

* Thu May 15 2014 Peter Robinson <pbrobinson@fedoraproject.org> 29.0-3
- Add upstream patches for aarch64 support

* Mon Apr 28 2014 Martin Stransky <stransky@redhat.com> - 29.0-2
- An updated ppc64le patch (rhbz#1091054)

* Mon Apr 28 2014 Martin Stransky <stransky@redhat.com> - 29.0-1
- Update to 29.0

* Tue Mar 18 2014 Martin Stransky <stransky@redhat.com> - 28.0-1
- Update to 28.0
- Fixed arm patch

* Mon Feb 3 2014 Martin Stransky <stransky@redhat.com> - 27.0-1
- Update to 27.0

* Fri Dec 13 2013 Martin Stransky <stransky@redhat.com> - 26.0-2
- rhbz#1037406 - xulrunner FTBFS if "-Werror=format-security"
  flag is used

* Mon Dec 9 2013 Martin Stransky <stransky@redhat.com> - 26.0-1
- Update to 26.0 Build 2

* Thu Nov 21 2013 Martin Stransky <stransky@redhat.com> - 25.0-5
- Fixed rhbz#1007603 - NSS and cert9 (sql): firefox crash on exit
  with https-everywhere installed

* Tue Nov 12 2013 Martin Stransky <stransky@redhat.com> - 25.0-4
- rhbz#1010916 - enabled pluseaudio backend

* Fri Nov 8 2013 Martin Stransky <stransky@redhat.com> - 25.0-3
- Fixed rhbz#974718 - Segfault in FileBlockCache::Run 
  when playing a movie on ppc

* Wed Oct 30 2013 Martin Stransky <stransky@redhat.com> - 25.0-2
- Update to 25.0 Build 3

* Wed Oct 23 2013 Martin Stransky <stransky@redhat.com> - 25.0-1
- Update to 25.0 Build 2

* Tue Oct 15 2013 Karsten Hopp <karsten@redhat.com> 24.0-3
- drop PPC-only rhbz-911314.patch, fixed upstream

* Mon Sep 16 2013 Martin Stransky <stransky@redhat.com> - 24.0.1-2
- Arm build fix

* Fri Sep 13 2013 Martin Stransky <stransky@redhat.com> - 24.0.1-1
- Update to 24.0

* Mon Sep 2 2013 Dan Horák <dan[at]danny.cz> - 23.0.1-4
- Fix build on 64-bit big endian platforms (mozbz#618485)

* Sat Aug 31 2013 Karsten Hopp <karsten@redhat.com> 23.0.1-3
- update rhbz-911314.patch (PPC* only)

* Thu Aug 29 2013 Martin Stransky <stransky@redhat.com> - 23.0.1-2
- Enabled dtrace for debug builds

* Mon Aug 19 2013 Jan Horak <jhorak@redhat.com> - 23.0.1-1
- Update to 23.0.1

* Mon Aug 5 2013 Martin Stransky <stransky@redhat.com> - 23.0-2
- Update to latest upstream (23.0 Build 2)

* Mon Aug 5 2013 Martin Stransky <stransky@redhat.com> - 23.0-1
- Update to latest upstream (23.0)

* Mon Jul 29 2013 Jan Horak <jhorak@redhat.com> - 22.0-7
- Use system libffi for Fedora 19+
- Added fix for mozbz#860213

* Thu Jul 25 2013 Martin Stransky <stransky@redhat.com> - 22.0-6
- Removed already applied patches (rhbz#978123)

* Wed Jul 24 2013 Peter Robinson <pbrobinson@fedoraproject.org> 22.0-5
- Enable web-rtc on ARM now it's fixed upstream (RHBZ 886976)

* Mon Jul  1 2013 Jan Horak <jhorak@redhat.com> - 22.0-4
- Added fix from mozbz#817533 - fix issues with proxy settings
- Fixed missing about:healthreport

* Mon Jun 24 2013 Martin Stransky <stransky@redhat.com> - 22.0-2
- Rebuild

* Fri Jun 21 2013 Martin Stransky <stransky@redhat.com> - 22.0-1
- Update to latest upstream (22.0)

* Wed Jun 12 2013 Jan Horak <jhorak@redhat.com> - 21.0-8
- Fixed rhbz#966424 - unable to install addons

* Mon Jun  3 2013 Jan Horak <jhorak@redhat.com> - 21.0-7
- Using upstream build flags for crashreporter

* Wed May 29 2013 Martin Stransky <stransky@redhat.com> - 21.0-6
- Removed the i686/f19 gcc hack (rhbz#928353)

* Tue May 21 2013 Martin Stransky <stransky@redhat.com> - 21.0-5
- Added ppc(64) patches (rhbz#963907)

* Tue May 21 2013 Martin Stransky <stransky@redhat.com> - 21.0-4
- Added s390(x) patch

* Mon May 13 2013 Martin Stransky <stransky@redhat.com> - 21.0-3
- New upstream tarball (build 4)

* Mon May 13 2013 Martin Stransky <stransky@redhat.com> - 21.0-2
- Updated requested NSS/NSPR versions

* Sun May 12 2013 Martin Stransky <stransky@redhat.com> - 21.0-1
- Update to latest upstream (21.0)

* Fri Apr 5 2013 Martin Stransky <stransky@redhat.com> - 20.0-4
- Updated rhbz-911314.patch for xulrunner 20

* Wed Apr 3 2013 Martin Stransky <stransky@redhat.com> - 20.0-3
- A workaround for Bug 928353 - firefox i686 crashes
  for a number of web pages

* Tue Mar 19 2013 Martin Stransky <stransky@redhat.com> - 20.0-1
- Update to latest upstream (20.0)

* Tue Mar 19 2013 Martin Stransky <stransky@redhat.com> - 19.0.2-4
- Added fix for rhbz#913284 - Firefox segfaults
  in mozilla::gfx::AlphaBoxBlur::BoxBlur_C() on PPC64

* Tue Mar 19 2013 Martin Stransky <stransky@redhat.com> - 19.0.2-3
- Added fix for mozbz#826171/rhbz#922904 - strndup implementation 
  in memory/build/mozmemory_wrap.c is broken

* Mon Mar 11 2013 Martin Stransky <stransky@redhat.com> - 19.0.2-2
- Update to 19.0.2

* Wed Feb 20 2013 Martin Stransky <stransky@redhat.com> - 19.0-2
- Added fix for rhbz#911314 (ppc only)

* Mon Feb 18 2013 Martin Stransky <stransky@redhat.com> - 19.0-1
- Update to 19.0
- Added fix for mozbz#239254

* Wed Feb  6 2013 Jan Horak <jhorak@redhat.com> - 18.0.2-1
- Update to 18.0.2

* Fri Jan 25 2013 Jan Horak <jhorak@redhat.com> - 18.0.1-1
- Update to 18.0.1

* Tue Jan 15 2013 Martin Stransky <stransky@redhat.com> - 18.0-8
- Added fix for NM regression (mozbz#791626)

* Thu Jan 10 2013 Martin Stransky <stransky@redhat.com> - 18.0-7
- Fixed Makefile generator (rhbz#304121)

* Wed Jan 9 2013 Martin Stransky <stransky@redhat.com> - 18.0-6
- Fixed missing libxpcom.so provides

* Wed Jan 9 2013 Martin Stransky <stransky@redhat.com> - 18.0-5
- Added fix for langpacks

* Wed Jan 9 2013 Martin Stransky <stransky@redhat.com> - 18.0-4
- Fixed source files
- Disabled WebRTC due to rhbz#304121

* Wed Jan 9 2013 Martin Stransky <stransky@redhat.com> - 18.0-2
- Disabled system sqlite on Fedora 18

* Mon Jan 7 2013 Martin Stransky <stransky@redhat.com> - 18.0-1
- Update to 18.0

* Thu Dec 13 2012 Peter Robinson <pbrobinson@fedoraproject.org> 17.0.1-3
- Disable webrtc on ARM as it currently tries to build SSE on ARM (fix FTBFS)
- Enable methodjit/tracejit on ARMv7 for more speed :) Fixes RHBZ 870548

* Fri Dec  7 2012 Jan Horak <jhorak@redhat.com> - 17.0.1-2
- Fixed rhbz#879595

* Thu Nov 29 2012 Jan Horak <jhorak@redhat.com> - 17.0.1-1
- Update to 17.0.1

* Tue Nov 27 2012 Jan Horak <jhorak@redhat.com> - 17.0-4
- Rebuild agains older NSS

* Mon Nov 19 2012 Martin Stransky <stransky@redhat.com> - 17.0-3
- Updated second arch patches

* Mon Nov 19 2012 Dan Horák <dan[at]danny.cz> - 17.0-2
- webrtc is available only on selected arches

* Mon Nov 19 2012 Martin Stransky <stransky@redhat.com> - 17.0-1
- Update to 17.0

* Wed Nov 14 2012 Martin Stransky <stransky@redhat.com> - 17.0-0.2b6
- Update to 17.0 Beta 6

* Tue Nov 13 2012 Martin Stransky <stransky@redhat.com> - 17.0-0.1b5
- Update to 17.0 Beta 5

* Tue Nov 6 2012 Martin Stransky <stransky@redhat.com> - 16.0.2-2
- Added fix for rhbz#872752

* Wed Oct 31 2012 Martin Stransky <stransky@redhat.com> - 16.0.2-1
- Updated mozilla-746112.patch for second arches
- Removed unused one (rhbz#855919)

* Fri Oct 26 2012 Jan Horak <jhorak@redhat.com> - 16.0.2-1
- Update to 16.0.2

* Tue Oct 16 2012 Jan Horak <jhorak@redhat.com> - 16.0.1-2
- Fixed required nss and nspr version

* Thu Oct 11 2012 Martin Stransky <stransky@redhat.com> - 16.0.1-1
- Update to 16.0.1

