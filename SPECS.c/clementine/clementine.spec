#先使用内置的依赖库
#define use_external_dependence 0

%define _unpackaged_files_terminate_build	0

#undefine _hardened_build

Name:           clementine
Version:	1.2.3
Release:        9%{?dist}
Summary:        A music player and library organiser
Summary(zh_CN.UTF-8):	一个音乐播放器和曲库管理工具

Group:          Applications/Multimedia
Group(zh_CN.UTF-8):	应用程序/多媒体
License:        GPLv3 and GPLv2+
URL:            http://www.clementine-player.org/
Source0:        https://github.com/clementine-player/Clementine/archive/%{version}.tar.gz

# fix libmygpo-qt header references
Patch0:         clementine-mygpo.patch
# desktop file fixes:
# * categories (+Audio)
# * non-compliant groups, https://code.google.com/p/clementine-player/issues/detail?id=2690
Patch3:         clementine-desktop.patch
Patch4:         clementine-udisks-headers.patch

# Use bundled sha2 library
# https://github.com/clementine-player/Clementine/issues/4217
Patch5:         clementine-do-not-use-system-sha2.patch
# fix compiler flag handling in gst/moodbar, upstreamable --rex
Patch6:         clementine-moodbar_flags.patch

Patch7: 	fix_gcc5_ftbfs.patch
Patch8:		freebsd_isnt_kfreebsd.patch
Patch9:		hide_boost_includes_from_q_moc.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  desktop-file-utils
BuildRequires:  liblastfm-devel
BuildRequires:  taglib-devel
BuildRequires:  xine-lib-devel
BuildRequires:  libnotify-devel
BuildRequires:  qt4-devel
BuildRequires:  boost-devel
BuildRequires:  notification-daemon
BuildRequires:  cmake
BuildRequires:  sqlite-devel
BuildRequires:  protobuf-devel
BuildRequires:  protobuf-compiler
BuildRequires:  qt4-linguist

%if 0%{?use_external_dependence}
BuildRequires:  qtsingleapplication-devel
BuildRequires:  libqxt-devel
BuildRequires:  gtest-devel
%endif

%description
Clementine is a modern music player and library organiser.
It is largely a port of Amarok 1.4, with some features rewritten to take
advantage of Qt4.

%description -l zh_CN.UTF-8
Clementine 是一个新潮的音乐播放器和曲库管理工具。它大体上是
Amarok 1.4 的一个移植版，捎带一些特性的重写以便得益于Qt4。

%prep
%setup -q -n Clementine-%{version}
%patch0 -p1 -b .mygpo
%patch3 -p1 -b .desktop
%patch4 -p1 -b .udisks-headers
%patch5 -p1 -b .do-not-use-system-sha2
%patch6 -p1 -b .moodbar_flags
%patch7 -p1
%patch8 -p1
%patch9 -p1

# Remove most 3rdparty libraries
mv 3rdparty/{gmock,qocoa,qsqlite,sha2}/ .
rm -fr 3rdparty/*
mv {gmock,qocoa,qsqlite,sha2}/ 3rdparty/

# Can't run all the unit tests
#   songloader requires internet connection
for test in songloader; do
    sed -i -e "/${test}_test/d" tests/CMakeLists.txt
done

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} \
  -DBUILD_WERROR:BOOL=OFF \
  -DCMAKE_BUILD_TYPE:STRING=Release \
  -DUSE_SYSTEM_QTSINGLEAPPLICATION=1 \
  -DUSE_SYSTEM_PROJECTM=1 \
  -DUSE_SYSTEM_QXT=1 \
  ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install DESTDIR=%{buildroot} -C %{_target_platform}


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/clementine.desktop
pushd %{_target_platform}
# Run a fake X session since some tests check for X, tests still fail sometimes
xvfb-run -a dbus-launch --exit-with-session make test ||:
popd

%clean
rm -rf %{buildroot}

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/icons/hicolor &>/dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
  update-desktop-database &> /dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
update-desktop-database &> /dev/null || :

%files
%defattr(-,root,root,-)
%doc Changelog COPYING
%{_bindir}/clementine
%{_datadir}/applications/clementine.desktop
%{_datadir}/icons/hicolor/*/apps/application-x-clementine.*
#%{_datadir}/clementine/projectm-presets/*
%{_bindir}/clementine-tagreader
%{kde4_servicesdir}/clementine-*.protocol

%changelog
* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 1.2.3-9
- 为 Magic 3.0 重建

* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 1.2.3-8
- 为 Magic 3.0 重建

* Tue Sep 22 2015 Liu Di <liudidi@gmail.com> - 1.2.3-7
- 为 Magic 3.0 重建

* Thu Aug 06 2015 Liu Di <liudidi@gmail.com> - 1.2.3-6
- 为 Magic 3.0 重建

* Tue Jul 15 2014 Liu Di <liudidi@gmail.com> - 1.2.3-5
- 为 Magic 3.0 重建

* Tue May 27 2014 Liu Di <liudidi@gmail.com> - 1.2.3-4
- 更新到 1.2.3

* Tue Mar 11 2014 Liu Di <liudidi@gmail.com> - 1.2.2-4
- 更新到 1.2.2

* Sun Apr 28 2013 Liu Di <liudidi@gmail.com> - 1.1.1-4
- 为 Magic 3.0 重建

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 1.1.1-2
- 为 Magic 3.0 重建

* Mon Nov 07 2011 Liu Di <liudidi@gmail.coM> - 0.7.1-1
- 更新到 0.7.1

* Sun May 30 2010 Liu Songhe <athena_star {at} 163 {dot} com> - 0.3-0.1
- Port to magic linux 2.5

* Sat Apr 17 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.2-2
- Patch out the external libraries
- Build the libclementine_lib into the final executable

* Sat Mar 27 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.2-1
- Fedorized the upstream specfile

* Mon Mar 22 2010 David Sansome <me@davidsansome.com> - 0.2
- Version 0.2

* Sun Feb 21 2010 David Sansome <me@davidsansome.com> - 0.1-5
- Various last-minute bugfixes

* Sun Jan 17 2010 David Sansome <me@davidsansome.com> - 0.1-1
- Initial package
