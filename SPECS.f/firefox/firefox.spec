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

# Build for Gtk3?
%if 0%{?fedora} <= 21
%define toolkit_gtk3      0
%else
%define toolkit_gtk3      1
%endif

# Use system cairo?
%define system_cairo      0

# Hardened build?
%if 0%{?fedora} > 20
%define hardened_build    1
%else
%define hardened_build    0
%endif

%define system_jpeg       1

%define enable_gstreamer  1

# Separated plugins are supported on x86(64) only
%ifarch %{ix86} x86_64
%define separated_plugins 1
%else
%define separated_plugins 0
%endif

%ifarch %{ix86} x86_64
%define run_tests         0
%else
%define run_tests         0
%endif

# Build as a debug package?
%define debug_build       0

%define default_bookmarks_file %{_datadir}/bookmarks/default-bookmarks.html
%define firefox_app_id  \{ec8030f7-c20a-464f-9b0e-13a3a9e97384\}
# Minimal required versions
%global cairo_version 1.13.1
%global freetype_version 2.1.9
%global libnotify_version 0.7.0
%global libvpx_version 1.3.0

%if %{?system_nss}
%global nspr_version 4.10.8
%global nspr_build_version %(pkg-config --silence-errors --modversion nspr 2>/dev/null || echo 65536)
%global nss_version 3.19.2
%global nss_build_version %(pkg-config --silence-errors --modversion nss 2>/dev/null || echo 65536)
%endif

%if %{?system_sqlite}
%global sqlite_version 3.8.4.2
# The actual sqlite version (see #480989):
%global sqlite_build_version %(pkg-config --silence-errors --modversion sqlite3 2>/dev/null || echo 65536)
%endif

%global mozappdir     %{_libdir}/%{name}
%global mozappdirdev  %{_libdir}/%{name}-devel-%{version}
%global langpackdir   %{mozappdir}/langpacks
%global tarballdir    mozilla-release

%define official_branding       1
%define build_langpacks         1

%define enable_mozilla_crashreporter       0
%if !%{debug_build}
%ifarch %{ix86} x86_64
%define enable_mozilla_crashreporter       1
%endif
%endif

Summary:        Mozilla Firefox Web browser
Name:           firefox
Version:        41.0
Release:        6%{?pre_tag}%{?dist}
URL:            http://www.mozilla.org/projects/firefox/
License:        MPLv1.1 or GPLv2+ or LGPLv2+
Group:          Applications/Internet
Source0:        ftp://ftp.mozilla.org/pub/firefox/releases/%{version}%{?pre_version}/source/firefox-%{version}%{?pre_version}.source.tar.xz
%if %{build_langpacks}
Source1:        firefox-langpacks-%{version}%{?pre_version}-20150918.tar.xz
%endif
Source10:       firefox-mozconfig
Source12:       firefox-redhat-default-prefs.js
Source20:       firefox.desktop
Source21:       firefox.sh.in
Source23:       firefox.1
Source24:       mozilla-api-key
Source25:       firefox-symbolic.svg

#Build patches
Patch0:         firefox-install-dir.patch
Patch1:         firefox-build.patch
Patch3:         mozilla-build-arm.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=814879#c3
Patch18:        xulrunner-24.0-jemalloc-ppc.patch
# workaround linking issue on s390 (JSContext::updateMallocCounter(size_t) not found)
Patch19:        xulrunner-24.0-s390-inlines.patch
Patch20:        firefox-build-prbool.patch
Patch21:        firefox-ppc64le.patch
Patch24:        firefox-debug.patch
Patch25:        rhbz-1219542-s390-build.patch

# Fedora specific patches
# Unable to install addons from https pages
Patch204:        rhbz-966424.patch
Patch215:        firefox-enable-addons.patch
Patch219:        rhbz-1173156.patch
Patch220:        rhbz-1014858.patch
Patch221:        firefox-fedora-ua.patch

# Upstream patches

# Gtk3 upstream patches
Patch420:        mozilla-1160154.patch
Patch425:        mozilla-1192243.patch
Patch426:        mozilla-1180971.patch
Patch427:        mozilla-1190935.patch
Patch428:        mozilla-1205045.patch

# Fix Skia Neon stuff on AArch64
Patch500:        aarch64-fix-skia.patch

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
%if %{toolkit_gtk3}
BuildRequires:  gtk3-devel
%endif
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
BuildRequires:  libicu-devel
BuildRequires:  GConf2-devel
%if !%{?system_jpeg}
BuildRequires:  yasm
%endif

Requires:       mozilla-filesystem
%if %{?system_nss}
Requires:       nspr >= %{nspr_build_version}
Requires:       nss >= %{nss_build_version}
%endif

BuildRequires:  desktop-file-utils
BuildRequires:  system-bookmarks
%if %{?enable_gstreamer}
BuildRequires:  gstreamer1-devel
BuildRequires:  gstreamer1-plugins-base-devel
%endif
%if %{?system_sqlite}
BuildRequires:  sqlite-devel >= %{sqlite_version}
Requires:       sqlite >= %{sqlite_build_version}
%endif

%if %{?system_ffi}
BuildRequires:  libffi-devel
%endif

Requires:       system-bookmarks

%if %{?run_tests}
BuildRequires:  xorg-x11-server-Xvfb
%endif

Obsoletes:      mozilla <= 37:1.7.13
Provides:       webclient

%description
Mozilla Firefox is an open-source web browser, designed for standards
compliance, performance and portability.

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
This package provides debug information for Firefox, for use by
Mozilla's crash reporter servers.  If you are trying to locally
debug %{name}, you want to install %{name}-debuginfo instead.
%files -n %{crashreporter_pkg_name} -f debugcrashreporter.list
%defattr(-,root,root)
%endif

%if %{run_tests}
%global testsuite_pkg_name mozilla-%{name}-testresults
%package -n %{testsuite_pkg_name}
Summary: Results of testsuite
Group: Development/Debug
%description -n %{testsuite_pkg_name}
This package contains results of tests executed during build.
%files -n %{testsuite_pkg_name}
/test_results
%defattr(-,root,root)
%endif

#---------------------------------------------------------------------

%prep
%setup -q -c
cd %{tarballdir}

# Build patches, can't change backup suffix from default because during build
# there is a compare of config and js/config directories and .orig suffix is
# ignored during this compare.
%patch0 -p1
%patch1 -p2 -b .build

%patch18 -p2 -b .jemalloc-ppc
%patch19 -p2 -b .s390-inlines
%patch20 -p1 -b .prbool
%patch21 -p2 -b .ppc64le
%patch24 -p1 -b .debug
%ifarch s390
%patch25 -p1 -b .rhbz-1219542-s390
%endif

%patch3  -p2 -b .arm

# For branding specific patches.

# Fedora patches
%patch204 -p2 -b .966424
%patch215 -p1 -b .addons
%patch219 -p2 -b .rhbz-1173156
%patch220 -p1 -b .rhbz-1014858
%patch221 -p2 -b .fedora-ua

# Upstream patches
%if %{toolkit_gtk3}
%patch420 -p1 -b .1160154
%patch425 -p1 -b .1192243
%patch426 -p1 -b .1180971
%patch427 -p1 -b .1190935
#%patch428 -p1 -b .1205045
%endif

%patch500 -p1

%{__rm} -f .mozconfig
%{__cp} %{SOURCE10} .mozconfig
%if %{official_branding}
echo "ac_add_options --enable-official-branding" >> .mozconfig
%endif
%{__cp} %{SOURCE24} mozilla-api-key

%if %{toolkit_gtk3}
echo "ac_add_options --enable-default-toolkit=cairo-gtk3" >> .mozconfig
%else
echo "ac_add_options --enable-default-toolkit=cairo-gtk2" >> .mozconfig
%endif

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

%if %{?enable_gstreamer}
echo "ac_add_options --enable-gstreamer=1.0" >> .mozconfig
%else
echo "ac_add_options --disable-gstreamer" >> .mozconfig
%endif

%if !%{?separated_plugins}
echo "ac_add_options --disable-ipc" >> .mozconfig
%endif

%ifarch %{arm}
echo "ac_add_options --disable-elf-hack" >> .mozconfig
%endif

%if %{?debug_build}
echo "ac_add_options --enable-debug" >> .mozconfig
echo "ac_add_options --disable-optimize" >> .mozconfig
echo "ac_add_options --enable-dtrace" >> .mozconfig
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
echo "ac_add_options --disable-ion" >> .mozconfig
echo "ac_add_options --disable-yarr-jit" >> .mozconfig
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

%if !%{enable_mozilla_crashreporter}
echo "ac_add_options --disable-crashreporter" >> .mozconfig
%endif

%if %{?run_tests}
echo "ac_add_options --enable-tests" >> .mozconfig
%endif

%if !%{?system_jpeg}
echo "ac_add_options --without-system-jpeg" >> .mozconfig
%else
echo "ac_add_options --with-system-jpeg" >> .mozconfig
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
#rhbz#1037063
# -Werror=format-security causes build failures when -Wno-format is explicitly given
# for some sources
# Explicitly force the hardening flags for Firefox so it passes the checksec test;
# See also https://fedoraproject.org/wiki/Changes/Harden_All_Packages
MOZ_OPT_FLAGS="$MOZ_OPT_FLAGS -Wformat-security -Wformat -Werror=format-security"
# Use hardened build?
%if %{?hardened_build}
MOZ_OPT_FLAGS="$MOZ_OPT_FLAGS -fPIC -Wl,-z,relro -Wl,-z,now"
%endif
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
export CFLAGS=$MOZ_OPT_FLAGS
export CXXFLAGS=$MOZ_OPT_FLAGS
export LDFLAGS=$MOZ_LINK_FLAGS

export PREFIX='%{_prefix}'
export LIBDIR='%{_libdir}'

MOZ_SMP_FLAGS=-j1
# On x86 architectures, Mozilla can build up to 4 jobs at once in parallel,
# however builds tend to fail on other arches when building in parallel.
%ifarch %{ix86} x86_64 ppc ppc64 ppc64le aarch64
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

%if %{?run_tests}
%if %{?system_nss}
ln -s /usr/bin/certutil objdir/dist/bin/certutil
ln -s /usr/bin/pk12util objdir/dist/bin/pk12util

%endif
mkdir test_results
./mach --log-no-times check-spidermonkey &> test_results/check-spidermonkey || true
./mach --log-no-times check-spidermonkey &> test_results/check-spidermonkey-2nd-run || true
./mach --log-no-times cppunittest &> test_results/cppunittest || true
xvfb-run ./mach --log-no-times crashtest &> test_results/crashtest || true
./mach --log-no-times gtest &> test_results/gtest || true
xvfb-run ./mach --log-no-times jetpack-test &> test_results/jetpack-test || true
# not working right now ./mach marionette-test &> test_results/marionette-test || true
xvfb-run ./mach --log-no-times mochitest-a11y &> test_results/mochitest-a11y || true
xvfb-run ./mach --log-no-times mochitest-browser &> test_results/mochitest-browser || true
xvfb-run ./mach --log-no-times mochitest-chrome &> test_results/mochitest-chrome || true
xvfb-run ./mach --log-no-times mochitest-devtools &> test_results/mochitest-devtools || true
xvfb-run ./mach --log-no-times mochitest-plain &> test_results/mochitest-plain || true
xvfb-run ./mach --log-no-times reftest &> test_results/reftest || true
xvfb-run ./mach --log-no-times webapprt-test-chrome &> test_results/webapprt-test-chrome || true
xvfb-run ./mach --log-no-times webapprt-test-content &> test_results/webapprt-test-content || true
./mach --log-no-times webidl-parser-test &> test_results/webidl-parser-test || true
xvfb-run ./mach --log-no-times xpcshell-test &> test_results/xpcshell-test || true
%if %{?system_nss}
rm -f  objdir/dist/bin/certutil
rm -f  objdir/dist/bin/pk12util
%endif

%endif
#---------------------------------------------------------------------

%install
cd %{tarballdir}

# set up our default bookmarks
%{__cp} -p %{default_bookmarks_file} objdir/dist/bin/browser/defaults/profile/bookmarks.html

# Make sure locale works for langpacks
%{__cat} > objdir/dist/bin/browser/defaults/preferences/firefox-l10n.js << EOF
pref("general.useragent.locale", "chrome://global/locale/intl.properties");
EOF

DESTDIR=$RPM_BUILD_ROOT make -C objdir install

%{__mkdir_p} $RPM_BUILD_ROOT{%{_libdir},%{_bindir},%{_datadir}/applications}

desktop-file-install --dir $RPM_BUILD_ROOT%{_datadir}/applications %{SOURCE20}

# set up the firefox start script
%{__rm} -rf $RPM_BUILD_ROOT%{_bindir}/firefox
%{__cat} %{SOURCE21} > $RPM_BUILD_ROOT%{_bindir}/firefox
%{__chmod} 755 $RPM_BUILD_ROOT%{_bindir}/firefox

%{__install} -p -D -m 644 %{SOURCE23} $RPM_BUILD_ROOT%{_mandir}/man1/firefox.1

%{__rm} -f $RPM_BUILD_ROOT/%{mozappdir}/firefox-config
%{__rm} -f $RPM_BUILD_ROOT/%{mozappdir}/update-settings.ini

for s in 16 22 24 32 48 256; do
    %{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${s}x${s}/apps
    %{__cp} -p browser/branding/official/default${s}.png \
               $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${s}x${s}/apps/firefox.png
done

# Install hight contrast icon
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/symbolic/apps
%{__cp} -p %{SOURCE25} \
           $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/symbolic/apps

# Register as an application to be visible in the software center
#
# NOTE: It would be *awesome* if this file was maintained by the upstream
# project, translated and installed into the right place during `make install`.
#
# See http://www.freedesktop.org/software/appstream/docs/ for more details.
#
mkdir -p $RPM_BUILD_ROOT%{_datadir}/appdata
cat > $RPM_BUILD_ROOT%{_datadir}/appdata/%{name}.appdata.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!-- Copyright 2014 Richard Hughes <richard@hughsie.com> -->
<!--
BugReportURL: https://bugzilla.mozilla.org/show_bug.cgi?id=1071061
SentUpstream: 2014-09-22
-->
<application>
  <id type="desktop">firefox.desktop</id>
  <metadata_license>CC0-1.0</metadata_license>
  <description>
    <p>
      Bringing together all kinds of awesomeness to make browsing better for you.
      Get to your favorite sites quickly – even if you don’t remember the URLs.
      Type your term into the location bar (aka the Awesome Bar) and the autocomplete
      function will include possible matches from your browsing history, bookmarked
      sites and open tabs.
    </p>
    <!-- FIXME: Needs another couple of paragraphs -->
  </description>
  <url type="homepage">http://www.mozilla.org/en-US/</url>
  <screenshots>
    <screenshot type="default">https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/firefox/a.png</screenshot>
    <screenshot>https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/firefox/b.png</screenshot>
    <screenshot>https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/firefox/c.png</screenshot>
  </screenshots>
  <!-- FIXME: change this to an upstream email address for spec updates
  <updatecontact>someone_who_cares@upstream_project.org</updatecontact>
   -->
</application>
EOF

echo > ../%{name}.lang
%if %{build_langpacks}
# Extract langpacks, make any mods needed, repack the langpack, and install it.
%{__mkdir_p} $RPM_BUILD_ROOT%{langpackdir}
%{__tar} xf %{SOURCE1}
for langpack in `ls firefox-langpacks/*.xpi`; do
  language=`basename $langpack .xpi`
  extensionID=langpack-$language@firefox.mozilla.org
  %{__mkdir_p} $extensionID
  unzip -qq $langpack -d $extensionID
  find $extensionID -type f | xargs chmod 644

  cd $extensionID
  zip -qq -r9mX ../${extensionID}.xpi *
  cd -

  %{__install} -m 644 ${extensionID}.xpi $RPM_BUILD_ROOT%{langpackdir}
  language=`echo $language | sed -e 's/-/_/g'`
  echo "%%lang($language) %{langpackdir}/${extensionID}.xpi" >> ../%{name}.lang
done
%{__rm} -rf firefox-langpacks

# Install langpack workaround (see #707100, #821169)
function create_default_langpack() {
language_long=$1
language_short=$2
cd $RPM_BUILD_ROOT%{langpackdir}
ln -s langpack-$language_long@firefox.mozilla.org.xpi langpack-$language_short@firefox.mozilla.org.xpi
cd -
echo "%%lang($language_short) %{langpackdir}/langpack-$language_short@firefox.mozilla.org.xpi" >> ../%{name}.lang
}

# Table of fallbacks for each language
# please file a bug at bugzilla.redhat.com if the assignment is incorrect
create_default_langpack "bn-IN" "bn"
create_default_langpack "es-AR" "es"
create_default_langpack "fy-NL" "fy"
create_default_langpack "ga-IE" "ga"
create_default_langpack "gu-IN" "gu"
create_default_langpack "hi-IN" "hi"
create_default_langpack "hy-AM" "hy"
create_default_langpack "nb-NO" "nb"
create_default_langpack "nn-NO" "nn"
create_default_langpack "pa-IN" "pa"
create_default_langpack "pt-PT" "pt"
create_default_langpack "sv-SE" "sv"
create_default_langpack "zh-TW" "zh"
%endif # build_langpacks


%{__mkdir_p} $RPM_BUILD_ROOT/%{mozappdir}/browser/defaults/preferences

# System extensions
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/mozilla/extensions/%{firefox_app_id}
%{__mkdir_p} $RPM_BUILD_ROOT%{_libdir}/mozilla/extensions/%{firefox_app_id}

# Copy over the LICENSE
%{__install} -p -c -m 644 LICENSE $RPM_BUILD_ROOT/%{mozappdir}

# Use the system hunspell dictionaries
%{__rm} -rf ${RPM_BUILD_ROOT}%{mozappdir}/dictionaries
ln -s %{_datadir}/myspell ${RPM_BUILD_ROOT}%{mozappdir}/dictionaries

# Enable crash reporter for Firefox application
%if %{enable_mozilla_crashreporter}
sed -i -e "s/\[Crash Reporter\]/[Crash Reporter]\nEnabled=1/" $RPM_BUILD_ROOT/%{mozappdir}/application.ini
# Add debuginfo for crash-stats.mozilla.com
%{__mkdir_p} $RPM_BUILD_ROOT/%{moz_debug_dir}
%{__cp} objdir/dist/%{symbols_file_name} $RPM_BUILD_ROOT/%{moz_debug_dir}
%endif

%if %{run_tests}
# Add debuginfo for crash-stats.mozilla.com
%{__mkdir_p} $RPM_BUILD_ROOT/test_results
%{__cp} test_results/* $RPM_BUILD_ROOT/test_results
%endif

# Default
%{__cp} %{SOURCE12} ${RPM_BUILD_ROOT}%{mozappdir}/browser/defaults/preferences

# Remove copied libraries to speed up build
rm -f ${RPM_BUILD_ROOT}%{mozappdirdev}/sdk/lib/libmozjs.so
rm -f ${RPM_BUILD_ROOT}%{mozappdirdev}/sdk/lib/libmozalloc.so
rm -f ${RPM_BUILD_ROOT}%{mozappdirdev}/sdk/lib/libxul.so
#---------------------------------------------------------------------

# Moves defaults/preferences to browser/defaults/preferences
%pretrans -p <lua>
require 'posix'
require 'os'
if (posix.stat("%{mozappdir}/browser/defaults/preferences", "type") == "link") then
  posix.unlink("%{mozappdir}/browser/defaults/preferences")
  posix.mkdir("%{mozappdir}/browser/defaults/preferences")
  if (posix.stat("%{mozappdir}/defaults/preferences", "type") == "directory") then
    for i,filename in pairs(posix.dir("%{mozappdir}/defaults/preferences")) do
      os.rename("%{mozappdir}/defaults/preferences/"..filename, "%{mozappdir}/browser/defaults/preferences/"..filename)
    end
    f = io.open("%{mozappdir}/defaults/preferences/README","w")
    if f then
      f:write("Content of this directory has been moved to %{mozappdir}/browser/defaults/preferences.")
      f:close()
    end
  end
end


%preun
# is it a final removal?
if [ $1 -eq 0 ]; then
  %{__rm} -rf %{mozappdir}/components
  %{__rm} -rf %{mozappdir}/extensions
  %{__rm} -rf %{mozappdir}/plugins
  %{__rm} -rf %{langpackdir}
fi

%post
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang
%defattr(-,root,root,-)
%{_bindir}/firefox
%{mozappdir}/firefox
%{mozappdir}/firefox-bin
%doc %{_mandir}/man1/*
%dir %{_datadir}/mozilla/extensions/*
%dir %{_libdir}/mozilla/extensions/*
%{_datadir}/appdata/*.appdata.xml
%{_datadir}/applications/*.desktop
%dir %{mozappdir}
%doc %{mozappdir}/LICENSE
%{mozappdir}/browser/chrome
%{mozappdir}/browser/chrome.manifest
%dir %{mozappdir}/browser/components
%{mozappdir}/browser/components/*.so
%{mozappdir}/browser/components/components.manifest
%{mozappdir}/browser/defaults/preferences/firefox-redhat-default-prefs.js
%attr(644, root, root) %{mozappdir}/browser/blocklist.xml
%dir %{mozappdir}/browser/extensions
%{mozappdir}/browser/extensions/*
%if %{build_langpacks}
%dir %{langpackdir}
%endif
%{mozappdir}/browser/omni.ja
%{mozappdir}/browser/icons
%{mozappdir}/run-mozilla.sh
%{mozappdir}/application.ini
%exclude %{mozappdir}/removed-files
%{_datadir}/icons/hicolor/16x16/apps/firefox.png
%{_datadir}/icons/hicolor/22x22/apps/firefox.png
%{_datadir}/icons/hicolor/24x24/apps/firefox.png
%{_datadir}/icons/hicolor/256x256/apps/firefox.png
%{_datadir}/icons/hicolor/32x32/apps/firefox.png
%{_datadir}/icons/hicolor/48x48/apps/firefox.png
%{_datadir}/icons/hicolor/symbolic/apps/firefox-symbolic.svg
%{mozappdir}/webapprt-stub
%dir %{mozappdir}/webapprt
%{mozappdir}/webapprt/omni.ja
%{mozappdir}/webapprt/webapprt.ini
%if %{enable_mozilla_crashreporter}
%{mozappdir}/crashreporter
%{mozappdir}/crashreporter.ini
%{mozappdir}/Throbber-small.gif
%{mozappdir}/browser/crashreporter-override.ini
%endif
%{mozappdir}/*.so
%{mozappdir}/chrome.manifest
%{mozappdir}/components
%{mozappdir}/defaults/pref/channel-prefs.js
%{mozappdir}/dependentlibs.list
%{mozappdir}/dictionaries
%{mozappdir}/omni.ja
%{mozappdir}/platform.ini
%{mozappdir}/plugin-container
%{mozappdir}/gmp-clearkey
%exclude %{_includedir}
%exclude %{_libdir}/firefox-devel-%{version}
%exclude %{_datadir}/idl
%if !%{?system_nss}
%{mozappdir}/libfreebl3.chk
%{mozappdir}/libnssdbm3.chk
%{mozappdir}/libsoftokn3.chk
%endif

#---------------------------------------------------------------------

%changelog
* Fri Sep 25 2015 Martin Stransky <stransky@redhat.com> - 41.0-6
- Rebuilt for old sqlite which is available in updates

* Thu Sep 24 2015 Martin Stransky <stransky@redhat.com> - 41.0-5
- Explicitly add "layers.use-image-offscreen-surfaces" config key
  to allow to experiment with that.

* Tue Sep 22 2015 Martin Stransky <stransky@redhat.com> - 41.0-4
- Added OMTC stability patches (mozbz#1180971, mozbz#1190935)

* Thu Sep 17 2015 Martin Stransky <stransky@redhat.com> - 41.0-3
- Update to 40.0 Build 3

* Tue Sep 15 2015 Martin Stransky <stransky@redhat.com> - 41.0-2
- Enabled OMTC
- Disabled system cairo

* Tue Sep 15 2015 Martin Stransky <stransky@redhat.com> - 41.0-1
- Update to 40.0 Build 1

* Thu Sep 3 2015 Martin Stransky <stransky@redhat.com> - 40.0.3-3
- Removed the dom.ipc.plugins.asyncInit hack, it's already in tarball

* Wed Sep 2 2015 Martin Stransky <stransky@redhat.com> - 40.0.3-2
- ppc64le build fix

* Thu Aug 27 2015 Martin Stransky <stransky@redhat.com> - 40.0.3-1
- Updated to latest upstream (40.0.3)

* Wed Aug 26 2015 Martin Stransky <stransky@redhat.com> - 40.0-10
- Added a fix for mozbz#1127752 (rhbz#1256875) - Gtk3&OMTC crashes

* Tue Aug 25 2015 Martin Stransky <stransky@redhat.com> - 40.0-9
- Enabled hardened builds

* Thu Aug 20 2015 Martin Stransky <stransky@redhat.com> - 40.0-7
- Enabled pie - rhbz#1246287

* Thu Aug 20 2015 Petr Jasicek <pjasicek@redhat.com> - 40.0-6
- Fix crash reporter layout under GTK3 - mozbz#1192243

* Wed Aug 19 2015 Martin Stransky <stransky@redhat.com> - 40.0-5
- Disable async addons init - mozbz#1196000

* Wed Aug 12 2015 Jan Horak <jhorak@redhat.com> - 40.0-4
- Workaround for reported crashes (layers.offmainthreadcomposition.enabled set to false)

* Tue Aug 11 2015 Jan Horak <jhorak@redhat.com> - 40.0-3
- Update to 40.0 Build 5

* Fri Aug 07 2015 Martin Stransky <stransky@redhat.com> - 40.0-2
- Patches updated (GtkEntry padding patch, toolbar button patch)

* Fri Aug 07 2015 Martin Stransky <stransky@redhat.com> - 40.0-1
- Update to 40.0 Build 4

* Thu Aug 06 2015 Martin Stransky <stransky@redhat.com> - 39.0.3-1
- Updated to 39.0.3

* Mon Jul 06 2015 Martin Stransky <stransky@redhat.com> - 39.0-8
- Added a fix for rhbz#1240259 - Firefox 39 does not open
  home page but "restore session"

* Thu Jul 02 2015 Martin Stransky <stransky@redhat.com> - 39.0-6
- Added symbolic (high contrast) icon

* Thu Jun 25 2015 Martin Stransky <stransky@redhat.com> - 39.0-5
- Update to 39.0 Build 6
- Update nss/nspr versions

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 38.0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun  8 2015 Jan Horak <jhorak@redhat.com> - 38.0.5-3
- System application picker dialog (mozbz#1129873)

* Fri Jun 5 2015 Martin Stransky <stransky@redhat.com> - 38.0.5-2
- Disabled system colors by default (rhbz#1226489)

* Wed Jun  3 2015 Jan Horak <jhorak@redhat.com> - 38.0.5-1
- Update to 38.0.5

* Mon Jun 1 2015 Martin Stransky <stransky@redhat.com> - 38.0.1-6
- Added fix for rhbz#1226868 - [GTK3] regression: bad colors
  make notifications unreadable

* Fri May 29 2015 Martin Stransky <stransky@redhat.com> - 38.0.1-5
- Added patch for mozbz#1169233 - Disabled menu items
  are not greyed out

* Fri May 29 2015 Martin Stransky <stransky@redhat.com> - 38.0.1-4
- Added patch for mozbz#1160154 - huge bookmark padding

* Tue May 26 2015 Martin Stransky <stransky@redhat.com> - 38.0.1-3
- spec clean up

* Fri May 22 2015 Moez Roy <moez.roy@gmail.com> - 38.0.1-2
- Rebuilt with hardening flags so it passes the checksec test;
- See also https://fedoraproject.org/wiki/Changes/Harden_All_Packages

* Mon May 18 2015 Martin Stransky <stransky@redhat.com> - 38.0.1-1
- Update to 38.0.1

* Wed May 13 2015 Martin Stransky <stransky@redhat.com> - 38.0-5
- Added patch for mozilla#1144745 - HiDPI Gtk3 fixes

* Mon May 11 2015 Martin Stransky <stransky@redhat.com> - 38.0-4
- Update to 38.0 Build 3
- Added fix for rhbz#1219542

* Wed May 6 2015 Martin Stransky <stransky@redhat.com> - 38.0-2
- Added fix for mozbz#1161056 - combobox background color

* Tue May 5 2015 Martin Stransky <stransky@redhat.com> - 38.0-1
- Update to 38.0 Build 2

* Wed Apr 22 2015 Martin Stransky <stransky@redhat.com> - 37.0.2-3
- Fedora-bookmarks rebuild (rhbz#1210474)

* Thu Apr 16 2015 Martin Stransky <stransky@redhat.com> - 37.0.2-2
- Update to 37.0.2

* Tue Apr 7 2015 Martin Stransky <stransky@redhat.com> - 37.0.1-2
- Fixed debug builds

* Tue Apr 7 2015 Martin Stransky <stransky@redhat.com> - 37.0.1-1
- Update to 37.0.1

* Mon Apr  6 2015 Tom Callaway <spot@fedoraproject.org> - 37.0-4
- rebuild for libvpx 1.4.0

* Tue Mar 31 2015 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 37.0-3
- Fix build on AArch64 (based on upstream skia changes)

* Fri Mar 27 2015 Martin Stransky <stransky@redhat.com> - 37.0-2
- Added tooltip patch (mozbz#1144643)

* Fri Mar 27 2015 Martin Stransky <stransky@redhat.com> - 37.0-1
- Update to 37.0 Build 2

* Thu Mar 26 2015 Richard Hughes <rhughes@redhat.com> - 36.0.4-2
- Add an AppData file for the software center

* Sat Mar 21 2015 Martin Stransky <stransky@redhat.com> - 36.0.4-1
- Update to 36.0.4

* Fri Mar 20 2015 Martin Stransky <stransky@redhat.com> - 36.0.3-1
- Update to 36.0.3

* Tue Mar 17 2015 Martin Stransky <stransky@redhat.com> - 36.0.1-6
- Fixed rhbz#1201527 - [GTK3] Scrollbars in Firefox
  are not consistent with the rest of the desktop

* Tue Mar 10 2015 Martin Stransky <stransky@redhat.com> - 36.0.1-5
- Arm build fix

* Mon Mar  9 2015 Jan Horak <jhorak@redhat.com> - 36.0.1-1
- Update to 36.0.1

* Fri Mar 6 2015 Martin Stransky <stransky@redhat.com> - 36.0-4
- ppc64le build fix

* Thu Mar 5 2015 Martin Stransky <stransky@redhat.com> - 36.0-3
- Added back the removed "-remote" option
- Fixed rhbz#1198965 - mozilla-xremote-client has been removed,
  langpack installation may be broken

* Tue Mar 3 2015 Martin Stransky <stransky@redhat.com> - 36.0-2
- Enable Skia for all arches (rhbz#1197007)

* Fri Feb 20 2015 Jan Horak <jhorak@redhat.com> - 36.0-1
- Update to 36.0

* Mon Feb 9 2015 Martin Stransky <stransky@redhat.com> - 35.0.1-5
- Fixed rhbz#1190774 - update usear agent string for Fedora

* Wed Feb 04 2015 Petr Machata <pmachata@redhat.com> - 35.0.1-4
- Bump for rebuild.

* Tue Jan 27 2015 Martin Stransky <stransky@redhat.com> - 35.0.1-3
- Backed out the flash click-to-play setup

* Mon Jan 26 2015 David Tardon <dtardon@redhat.com> - 35.0.1-2
- rebuild for ICU 54.1

* Fri Jan 23 2015 Martin Stransky <stransky@redhat.com> - 35.0.1-1
- New upstream version

* Thu Jan 22 2015 Martin Stransky <stransky@redhat.com> - 35.0-7
- Updated hiDPI patch to upstream version (mozbz#975919)

* Thu Jan 22 2015 Martin Stransky <stransky@redhat.com> - 35.0-6
- Disabled flash by default because of 0day live flash exploit
  (see https://isc.sans.edu/diary/Flash+0-Day+Exploit+Used+by+Angler+Exploit+Kit/19213)

* Mon Jan 19 2015 Martin Stransky <stransky@redhat.com> - 35.0-5
- Enable release build config
- Gtk3 - added patch for HiDPI support (mozbz#975919)

* Mon Jan 19 2015 Martin Stransky <stransky@redhat.com> - 35.0-4
- Gtk3 - fixed tabs rendering

* Wed Jan 14 2015 Martin Stransky <stransky@redhat.com> - 35.0-3
- Gtk3 - replaced obsoleted focus properties
- Make start.fedoraproject.org the homepage

* Mon Jan 12 2015 Martin Stransky <stransky@redhat.com> - 35.0-2
- Update to 35.0 Build 3
- Gtk3 - added fix for button/entry box sizes
- Gtk3 - added fix for button/entry focus sizes
- Spec clean-up (by moez.roy@gmail.com)

* Tue Jan 6 2015 Martin Stransky <stransky@redhat.com> - 35.0-1
- Update to 35.0 Build 1

* Mon Jan 5 2015 Martin Stransky <stransky@redhat.com> - 34.0-12
- Fixed rhbz#1014858 - GLib-CRITICAL **: g_slice_set_config:
  assertion `sys_page_size == 0' failed

* Fri Jan 2 2015 Martin Stransky <stransky@redhat.com> - 34.0-11
- Build with system jpeg on rawhide
- Updated ATK patch for gtk3

* Tue Dec 23 2014 Martin Stransky <stransky@redhat.com> - 34.0-9
- Added fix for rhbz#1173156 - Native NTLM authentication
  on Linux unsupported
- Added fix for rhbz#1170109 - data corruption bug on armhfp

* Sat Dec 13 2014 Martin Stransky <stransky@redhat.com> - 34.0-8
- Gtk3 - Workaround for Firefox freeze when accessibility is enabled

* Fri Dec 12 2014 Martin Stransky <stransky@redhat.com> - 34.0-7
- Added fix for mozbz#1097592 - Firefox freeze in Gtk3

* Thu Dec 11 2014 Martin Stransky <stransky@redhat.com> - 34.0-6
- Disabled Gtk3 on Fedora 21 and earlier (rhbz#1172926)

* Wed Dec 10 2014 Martin Stransky <stransky@redhat.com> - 34.0-5
- Disabled flash plugin instllation pop-up (mozbz#1108645)

* Mon Dec 8 2014 Jiri Vanek  <jvanek@redhat.com> - 34.0-4
- added and applied patch218, java-plugin-url.patch
- fixed url for java plugin installation guide
- resolves rhbz#979985

* Mon Dec 8 2014 Martin Stransky <stransky@redhat.com> - 34.0-3
- Gtk3 flash plugin fix (rhbz#1171457)
- Gtk3 theme fixes

* Wed Dec  3 2014 Jan Horak <jhorak@redhat.com> - 34.0-2
- Fix for mozbz#1097550 - wrong default dictionary

* Mon Dec 1 2014 Martin Stransky <stransky@redhat.com> - 34.0-1
- Update to 34.0 build 2

* Thu Nov 13 2014 Martin Stransky <stransky@redhat.com> - 33.1-2
- Disabled downloads non-free OpenH264 blob on first start
  (rhbz#1155499)

* Tue Nov 11 2014 Martin Stransky <stransky@redhat.com> - 33.1-1
- Update to 33.1 build 3

* Mon Nov 10 2014 Martin Stransky <stransky@redhat.com> - 33.0-5
- Fixed rhbz#1161110 - /usr/bin/firefox should not mess with TMPDIR

* Tue Nov 4 2014 Martin Stransky <stransky@redhat.com> - 33.0-4
- Do not use system libjpeg-turbo on rawhide

* Mon Nov 3 2014 Martin Stransky <stransky@redhat.com> - 33.0-3
- Added Gtk3 support

* Wed Oct 15 2014 Martin Stransky <stransky@redhat.com> - 33.0-2
- Added patches from mozbz#858919

* Tue Oct 14 2014 Martin Stransky <stransky@redhat.com> - 33.0-1
- Update to 33.0 build 2

* Fri Sep 19 2014 Jan Horak <jhorak@redhat.com> - 32.0.2-2
- Added support for Mozilla tests

* Thu Sep 18 2014 Martin Stransky <stransky@redhat.com> - 32.0.2-1
- Update to 32.0.2 build 1

* Tue Sep 16 2014 Martin Stransky <stransky@redhat.com> - 32.0.1-2
- disable baseline JIT on i686 (rhbz#1047079)

* Mon Sep 15 2014 Martin Stransky <stransky@redhat.com> - 32.0.1-1
- Update to 32.0.1 build 2
- Patch from rhbz#1140157

* Wed Sep 10 2014 Jan Horak <jhorak@redhat.com> - 32.0-2
- Fix for geolocation API (rhbz#1063739)

* Tue Aug 26 2014 Martin Stransky <stransky@redhat.com> - 32.0-1
- Update to 32.0 build 1

* Tue Aug 26 2014 David Tardon <dtardon@redhat.com> - 31.0-4
- rebuild for ICU 53.1

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 31.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 30 2014 Martin Stransky <stransky@redhat.com> - 31.0-2
- Added patch for mozbz#858919

* Thu Jul 17 2014 Martin Stransky <stransky@redhat.com> - 31.0-1
- Update to 31.0 build 2

* Wed Jun 11 2014 Martin Stransky <stransky@redhat.com> - 30.0-4
- Updated NSPR version

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 30.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jun 5 2014 Martin Stransky <stransky@redhat.com> - 30.0-2
- Enable gstreamer 1.0

* Wed Jun 4 2014 Martin Stransky <stransky@redhat.com> - 30.0-1
- Update to 30.0 build 1

* Fri May 23 2014 Martin Stransky <stransky@redhat.com> - 29.0.1-5
- Added a build fix for ppc64 - rhbz#1100495

* Tue May 20 2014 Martin Stransky <stransky@redhat.com> - 29.0.1-4
- Enabled necko-wifi

* Thu May 15 2014 Peter Robinson <pbrobinson@fedoraproject.org> 29.0.1-3
- Add upstream patches for aarch64 support

* Thu May 15 2014 Martin Stransky <stransky@redhat.com> - 29.0.1-2
- Fixed rhbz#1098090 - Enable plugin-container for nspluginwrapper

* Wed May 14 2014 Martin Stransky <stransky@redhat.com> - 29.0.1-1
- Update to 29.0.1

* Mon Apr 28 2014 Martin Stransky <stransky@redhat.com> - 29.0-5
- An updated ppc64le patch (rhbz#1091054)

* Mon Apr 28 2014 Martin Stransky <stransky@redhat.com> - 29.0-4
- Arm build fixes

* Fri Apr 25 2014 Martin Stransky <stransky@redhat.com> - 29.0-3
- Build with system ICU

* Thu Apr 24 2014 Martin Stransky <stransky@redhat.com> - 29.0-2
- Removed unused patch

* Tue Apr 22 2014 Martin Stransky <stransky@redhat.com> - 29.0-1
- Update to 29.0 Build 1

* Tue Apr  8 2014 Jan Horak <jhorak@redhat.com> - 28.0-4
- Support for ppc64le architecture

* Wed Mar 19 2014 Martin Stransky <stransky@redhat.com> - 28.0-3
- Arm build fix

* Wed Mar 19 2014 Martin Stransky <stransky@redhat.com> - 28.0-2
- NSS version up, disable arm for now

* Tue Mar 18 2014 Martin Stransky <stransky@redhat.com> - 28.0-1
- Update to 28.0

* Thu Mar 6 2014 Martin Stransky <stransky@redhat.com> - 27.0.1-2
- Removed needless build patch

* Mon Feb 24 2014 Martin Stransky <stransky@redhat.com> - 27.0.1-1
- Update to 27.0.1

* Mon Feb 3 2014 Martin Stransky <stransky@redhat.com> - 27.0-1
- Update to 27.0

* Thu Jan 30 2014 Jan Horak <jhorak@redhat.com> - 26.0-7
- Set default homepage to about:newtab and make start.fedoraproject.org page pinned on it
- Disable system cairo because of rhbz#1059076

* Mon Jan 20 2014 Jan Horak <jhorak@redhat.com> - 26.0-6
- Fixed langpack installation

* Thu Jan  9 2014 Jan Horak <jhorak@redhat.com> - 26.0-5
- Build standalone firefox package without dependency on xulrunner

* Tue Dec 17 2013 Martin Stransky <stransky@redhat.com> - 26.0-4
- Added fix for rhbz#1007603 - NSS and cert9 (sql): firefox crash
  on exit with https-everywhere installed (edit)

* Fri Dec 13 2013 Martin Stransky <stransky@redhat.com> - 26.0-3
- Build with -Werror=format-security (rhbz#1037063)

* Mon Dec 9 2013 Martin Stransky <stransky@redhat.com> - 26.0-2
- Update to 26.0 Build 2

* Wed Oct 30 2013 Martin Stransky <stransky@redhat.com> - 25.0-3
- Update to 25.0 Build 3

* Thu Oct 24 2013 Martin Stransky <stransky@redhat.com> - 25.0-2
- Fixed xulrunner dependency

* Thu Oct 24 2013 Martin Stransky <stransky@redhat.com> - 25.0-1
- Update to 25.0 Build 2

* Thu Oct 17 2013 Martin Stransky <stransky@redhat.com> - 24.0-2
- Fixed rhbz#1005611 - BEAST workaround not enabled in Firefox

* Fri Sep 13 2013 Martin Stransky <stransky@redhat.com> - 24.0-1
- Update to 24.0

* Tue Sep  3 2013 Jan Horak <jhorak@redhat.com> - 23.0.1-5
- Fixing rhbz#1003691

* Fri Aug 30 2013 Martin Stransky <stransky@redhat.com> - 23.0.1-3
- Spec tweak (rhbz#991493)

* Fri Aug 30 2013 Jan Horak <jhorak@redhat.com> - 23.0.1-2
- Homepage moved to pref file
- Fixed migration from F18 -> F19 (rhbz#976420)

* Mon Aug 19 2013 Jan Horak <jhorak@redhat.com> - 23.0.1-1
- Update to 23.0.1

* Mon Aug 5 2013 Martin Stransky <stransky@redhat.com> - 23.0-1
- Updated to latest upstream (23.0 Build 2)

* Thu Jul 25 2013 Martin Stransky <stransky@redhat.com> - 22.0-3
- Fixed rhbz#988363 - firefox-redhat-default-prefs.js is not used

* Fri Jun 28 2013 Jan Horak <jhorak@redhat.com> - 22.0-2
- Fixed crashreporter for third arch

* Fri Jun 21 2013 Martin Stransky <stransky@redhat.com> - 22.0-1
- Updated to latest upstream (22.0)

* Thu Jun 13 2013 Jan Horak <jhorak@redhat.com> - 21.0-5
- Enable Mozilla crash report tool

* Thu May 23 2013 Jan Horak <jhorak@redhat.com> - 21.0-4
- Do not override user defined TMPDIR variable

* Thu May 16 2013 Martin Stransky <stransky@redhat.com> - 21.0-3
- Fixed extension compatibility dialog (rhbz#963422)

* Wed May 15 2013 Martin Stransky <stransky@redhat.com> - 21.0-2
- Keep compatibility with old preference dir

* Tue May 14 2013 Martin Stransky <stransky@redhat.com> - 21.0-1
- Updated to latest upstream (21.0)

* Thu May 9 2013 Martin Stransky <stransky@redhat.com> - 20.0-5
- Removed firstrun page (rhbz#864793)
- Made zip/unzip quiet in langpacks processing

* Thu Apr 18 2013 Martin Stransky <stransky@redhat.com> - 20.0-4
- Updated xulrunner check

* Thu Apr 18 2013 Martin Stransky <stransky@redhat.com> - 20.0-3
- Added a workaround for rhbz#907424 - textarea redrawn wrongly
  during edit

* Thu Apr 18 2013 Jan Horak <jhorak@redhat.com> - 20.0-2
- Updated manual page

* Mon Apr 1 2013 Martin Stransky <stransky@redhat.com> - 20.0-1
- Updated to 20.0

* Mon Mar 18 2013 Martin Stransky <stransky@redhat.com> - 19.0.2-2
- Added fix for mozbz#239254 - local cache dir

* Mon Mar 11 2013 Jan Horak <jhorak@redhat.com> - 19.0.2-1
- Update to 19.0.2

* Tue Feb 19 2013 Jan Horak <jhorak@redhat.com> - 19.0-1
- Update to 19.0

* Wed Feb  6 2013 Jan Horak <jhorak@redhat.com> - 18.0.2-1
- Update to 18.0.2

* Fri Jan 25 2013 Jan Horak <jhorak@redhat.com> - 18.0.1-1
- Update to 18.0.1

* Wed Jan 9 2013 Martin Stransky <stransky@redhat.com> - 18.0-1
- Update to 18.0

* Tue Dec 18 2012 Martin Stransky <stransky@redhat.com> - 17.0.1-2
- Fix bug 878831 - Please enable gfx.color_management.enablev4=true

* Thu Nov 29 2012 Jan Horak <jhorak@redhat.com> - 17.0.1-1
- Update to 17.0.1

* Mon Nov 19 2012 Martin Stransky <stransky@redhat.com> - 17.0-1
- Update to 17.0

* Thu Nov 15 2012 Martin Stransky <stransky@redhat.com> - 17.0-0.1b6
- Update to 17.0 Beta 6

* Wed Nov  7 2012 Jan Horak <jhorak@redhat.com> - 16.0.2-4
- Added duckduckgo.com search engine

* Thu Nov  1 2012 Jan Horak <jhorak@redhat.com> - 16.0.2-3
- Added keywords to desktop file (871900)

* Tue Oct 30 2012 Martin Stransky <stransky@redhat.com> - 16.0.2-2
- Updated man page (#800234)

* Fri Oct 26 2012 Jan Horak <jhorak@redhat.com> - 16.0.2-1
- Update to 16.0.2

* Thu Oct 11 2012 Martin Stransky <stransky@redhat.com> - 16.0.1-1
- Update to 16.0.1

* Thu Oct 11 2012 Martin Stransky <stransky@redhat.com> - 16.0.1-1
- Update to 16.0.1

* Mon Oct  8 2012 Jan Horak <jhorak@redhat.com> - 16.0-1
- Update to 16.0
- Use /var/tmp instead of /tmp (rhbz#860814)

* Tue Sep 11 2012 Jan Horak <jhorak@redhat.com> - 15.0.1-1
- Update to 15.0.1

* Tue Aug 28 2012 Martin Stransky <stransky@redhat.com> - 15.0-2
- Added fix for rhbz#851722 - conflict with incompatible xulrunner

* Mon Aug 27 2012 Martin Stransky <stransky@redhat.com> - 15.0-1
- Update to 15.0

* Wed Aug 22 2012 Dan Horák <dan[at]danny.cz> - 14.0.1-3
- add fix for secondary arches from xulrunner

* Wed Aug 1 2012 Martin Stransky <stransky@redhat.com> - 14.0.1-2
- removed StartupWMClass (rhbz#844860)

* Mon Jul 16 2012 Martin Stransky <stransky@redhat.com> - 14.0.1-1
- Update to 14.0.1

* Tue Jul 10 2012 Martin Stransky <stransky@redhat.com> - 13.0.1-2
- Fixed rhbz#707100, rhbz#821169

* Sat Jun 16 2012 Jan Horak <jhorak@redhat.com> - 13.0.1-1
- Update to 13.0.1

* Tue Jun 5 2012 Martin Stransky <stransky@redhat.com> - 13.0-1
- Update to 13.0

* Tue Apr 24 2012 Martin Stransky <stransky@redhat.com> - 12.0-1
- Update to 12.0

* Thu Mar 15 2012 Martin Stransky <stransky@redhat.com> - 11.0-2
- Switched dependency to xulrunner (rhbz#803471)

* Tue Mar 13 2012 Martin Stransky <stransky@redhat.com> - 11.0-1
- Update to 11.0
- Fixed rhbz#800622 - make default home page of fedoraproject.org conditional
- Fixed rhbz#801796 - enable debug build by some simple way

* Mon Feb 27 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 10.0.1-2
- Add ARM config options to fix compile

* Thu Feb  9 2012 Jan Horak <jhorak@redhat.com> - 10.0.1-1
- Update to 10.0.1

* Fri Feb  3 2012 Jan Horak <jhorak@redhat.com> - 10.0-2
- Fixed rhbz#786983

* Tue Jan 31 2012 Jan Horak <jhorak@redhat.com> - 10.0-1
- Update to 10.0

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 23 2011 Jan Horak <jhorak@redhat.com> - 9.0.1-1
- Update to 9.0.1

* Wed Dec 21 2011 Jan Horak <jhorak@redhat.com> - 9.0-3
- Update to 9.0

* Thu Dec 15 2011 Jan Horak <jhorak@redhat.com> - 9.0-1.beta5
- Update to 9.0 Beta 5

* Tue Nov 15 2011 Martin Stransky <stransky@redhat.com> - 8.0-3
- Disabled addon check UI (#753551)

* Tue Nov 15 2011 Martin Stransky <stransky@redhat.com> - 8.0-2
- Temporary workaround for langpacks (#753551)

* Tue Nov  8 2011 Jan Horak <jhorak@redhat.com> - 8.0-1
- Update to 8.0

* Mon Oct 24 2011 Martin Stransky <stransky@redhat.com> - 7.0.1-3
- reverted the desktop file name for Fedora15 & 16

* Mon Oct 24 2011 Martin Stransky <stransky@redhat.com> - 7.0.1-2
- renamed mozilla-firefox.desktop to firefox.desktop (#736558)
- nspluginwrapper is not run in plugin-container (#747981)

* Fri Sep 30 2011 Jan Horak <jhorak@redhat.com> - 7.0.1-1
- Update to 7.0.1

* Tue Sep 27 2011 Jan Horak <jhorak@redhat.com> - 7.0
- Update to 7.0

* Tue Sep  6 2011 Jan Horak <jhorak@redhat.com> - 6.0.2-1
- Update to 6.0.2

* Tue Aug 16 2011 Martin Stransky <stransky@redhat.com> - 6.0-1
- Update to 6.0

* Fri Jun 24 2011 Bill Nottingham <notting@redhat.com> - 5.0-2
- Fix an issue with a stray glyph in the window title

* Tue Jun 21 2011 Martin Stransky <stransky@redhat.com> - 5.0-1
- Update to 5.0

* Tue May 10 2011 Martin Stransky <stransky@redhat.com> - 4.0.1-2
- Fixed rhbz#676183 - "firefox -g" is broken

* Thu Apr 28 2011 Christopher Aillon <caillon@redhat.com> - 4.0.1-1
- Update to 4.0.1

* Thu Apr 21 2011 Christopher Aillon <caillon@redhat.com> - 4.0-4
- Spec file cleanups

* Mon Apr  4 2011 Christopher Aillon <caillon@redhat.com> - 4.0-3
- Updates for NetworkManager 0.9
- Updates for GNOME 3

* Tue Mar 22 2011 Christopher Aillon <caillon@redhat.com> - 4.0-2
- Rebuild

* Tue Mar 22 2011 Christopher Aillon <caillon@redhat.com> - 4.0-1
- Firefox 4

* Fri Mar 18 2011 Christopher Aillon <caillon@redhat.com> - 4.0-0.21
- Firefox 4.0 RC 2

* Thu Mar 17 2011 Jan Horak <jhorak@redhat.com> - 4.0-0.20
- Rebuild against xulrunner with disabled gnomevfs and enabled gio

* Wed Mar  9 2011 Christopher Aillon <caillon@redhat.com> - 4.0-0.19
- Firefox 4.0 RC 1

* Sat Feb 26 2011 Christopher Aillon <caillon@redhat.com> - 4.0-0.18b12
- Switch to using the omni chrome file format

* Fri Feb 25 2011 Christopher Aillon <caillon@redhat.com> - 4.0-0.17b12
- Firefox 4.0 Beta 12

* Thu Feb 10 2011 Christopher Aillon <caillon@redhat.com> - 4.0-0.16b11
- Update gecko-{libs,devel} requires

* Tue Feb 08 2011 Christopher Aillon <caillon@redhat.com> - 4.0-0.15b11
- Firefox 4.0 Beta 11

* Mon Feb 07 2011 Christopher Aillon <caillon@redhat.com> - 4.0-0.14b10
- Bring back the default browser check

* Tue Jan 25 2011 Christopher Aillon <caillon@redhat.com> - 4.0-0.13b10
- Firefox 4.0 Beta 10

* Fri Jan 14 2011 Christopher Aillon <caillon@redhat.com> - 4.0-0.12b9
- Firefox 4.0 Beta 9

* Thu Jan 6 2011 Dan Horák <dan[at]danny.cz> - 4.0-0.11b8
- disable ipc on non-x86 arches to match xulrunner

* Thu Jan 6 2011 Martin Stransky <stransky@redhat.com> - 4.0-0.10b8
- application.ini permission check fix

* Thu Jan 6 2011 Martin Stransky <stransky@redhat.com> - 4.0-0.9b8
- Fixed rhbz#667477 - broken launch script

* Tue Jan 4 2011 Martin Stransky <stransky@redhat.com> - 4.0-0.8b8
- Fixed rhbz#664877 - Cannot read application.ini
