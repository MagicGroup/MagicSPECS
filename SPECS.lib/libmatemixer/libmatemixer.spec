# Conditional for release and snapshot builds. Uncomment for release-builds.
%global rel_build 1

# This is needed, because src-url contains branched part of versioning-scheme.
%global branch 1.12

# Settings used for build from snapshots.
%{!?rel_build:%global commit ee0a62c8759040d84055425954de1f860bac8652}
%{!?rel_build:%global commit_date 20140223}
%{!?rel_build:%global shortcommit %(c=%{commit};echo ${c:0:7})}
%{!?rel_build:%global git_ver git%{commit_date}-%{shortcommit}}
%{!?rel_build:%global git_rel .git%{commit_date}.%{shortcommit}}
%{!?rel_build:%global git_tar %{name}-%{version}-%{git_ver}.tar.xz}

Name:        libmatemixer
Summary:     Mixer library for MATE desktop
Version:     %{branch}.1
%if 0%{?rel_build}
Release:     1%{?dist}
%else
Release:     0.1%{?git_rel}%{?dist}
%endif
License:     GPLv2+
URL:         http://mate-desktop.org

# for downloading the tarball use 'spectool -g -R libmatemixer.spec'
# Source for release-builds.
%{?rel_build:Source0:     http://pub.mate-desktop.org/releases/%{branch}/%{name}-%{version}.tar.xz}
# Source for snapshot-builds.
%{!?rel_build:Source0:    http://git.mate-desktop.org/%%{name}/snapshot/%%{name}-%%{commit}.tar.xz#/%%{git_tar}}

BuildRequires:  mate-common
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  alsa-lib-devel


%description
libmatemixer is a mixer library for MATE desktop.
It provides an abstract API allowing access to mixer functionality
available in the PulseAudio, ALSA and OSS sound systems.

%package devel
Summary:  Development libraries for libmatemixer
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Development libraries for libmatemixer

%prep
%setup -q%{!?rel_build:n %{name}-%{commit}}

%if 0%{?rel_build}
#NOCONFIGURE=1 ./autogen.sh
%else # 0%{?rel_build}
# for snapshots
# needed for git snapshots
NOCONFIGURE=1 ./autogen.sh
%endif # 0%{?rel_build}

%build
%configure \
        --disable-static \
        --enable-pulseaudio \
        --enable-alsa \
        --enable-gtk-doc

#drop unneeded direct library deps with --as-needed
# libtool doesn't make this easy, so we do it the hard way
sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0 /g' libtool

make %{?_smp_mflags} V=1

%install
%{make_install}

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%find_lang %{name} --with-gnome --all-name


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files -f %{name}.lang
%doc AUTHORS COPYING NEWS README
%{_libdir}/libmatemixer.so.*
%{_libdir}/libmatemixer/

%files devel
%{_includedir}/mate-mixer/
%{_libdir}/pkgconfig/*
%{_libdir}/*.so
%{_datadir}/gtk-doc/html/libmatemixer/


%changelog
* Fri Dec 04 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.12.1-1
- update to 1.12.1 release

* Fri Nov 06 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.12.0-1
- update to 1.12.0 release

* Wed Oct 21 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.11.0-1
- update to 1.11.0 release

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Apr 06 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.0-1
- update to 1.10.0 release

* Wed Feb 25 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.90.1
- update to 1.9.90 release

* Sun Nov 23 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.2-1
- update to 1.9.2 release

* Tue Nov 11 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.1-1
- update to 1.9.1 release

* Mon Oct 27 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.0-1
- initial build

