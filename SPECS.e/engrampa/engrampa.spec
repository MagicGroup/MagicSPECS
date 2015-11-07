# Conditional for release and snapshot builds. Uncomment for release-builds.
%global rel_build 1

# This is needed, because src-url contains branched part of versioning-scheme.
#global branch 1.9

# Settings used for build from snapshots.
%{!?rel_build:%global commit f4611c3411c44e792f729a0780c31b0aa55fe004}
%{!?rel_build:%global commit_date 20131215}
%{!?rel_build:%global shortcommit %(c=%{commit};echo ${c:0:7})}
%{!?rel_build:%global git_ver git%{commit_date}-%{shortcommit}}
%{!?rel_build:%global git_rel .git%{commit_date}.%{shortcommit}}
%{!?rel_build:%global git_tar %{name}-%{version}-%{git_ver}.tar.xz}

Name:          engrampa
Version: 1.11.0
Release: 2%{?dist}
#Release: 1%{?dist}
Summary:       MATE Desktop file archiver
Summary(zh_CN.UTF-8): MATE 桌面的文件归档管理器
License:       GPLv2+ and LGPLv2+
URL:           http://mate-desktop.org

%define branch %(echo %{version} | awk -F. '{print $1"."$2}')
# for downloading the tarball use 'spectool -g -R engrampa.spec'
# Source for release-builds.
%{?rel_build:Source0:     http://pub.mate-desktop.org/releases/%{branch}/%{name}-%{version}.tar.xz}
# Source for snapshot-builds.
%{!?rel_build:Source0:    http://git.mate-desktop.org/%{name}/snapshot/%{name}-%{commit}.tar.xz#/%{git_tar}}

BuildRequires:  mate-common
BuildRequires:  desktop-file-utils
BuildRequires:  gtk2-devel
BuildRequires:  caja-devel
BuildRequires:  mate-desktop-devel
BuildRequires:  libSM-devel

Provides: mate-file-archiver%{?_isa} = %{version}-%{release}
Provides: mate-file-archiver = %{version}-%{release}
Obsoletes: mate-file-archiver < %{version}-%{release}

%description
Mate File Archiver is an application for creating and viewing archives files,
such as zip, xv, bzip2, cab, rar and other compress formats.

%description -l zh_CN.UTF-8
这是一个创建和查看归档文件的程序，支持 zip, xv, bzip2, cab, rar 和其它的压缩格式。

%prep
%setup -q%{!?rel_build:n %{name}-%{commit}}

# nedded to create missing configure and make files
#NOCONFIGURE=1 ./autogen.sh


%build
%configure                 \
   --disable-schemas-compile \
   --disable-static        \
   --with-gtk=2.0          \
   --enable-caja-actions

make %{?_smp_mflags} V=1


%install
%{make_install}

desktop-file-install                                \
    --delete-original                               \
    --dir %{buildroot}%{_datadir}/applications      \
%{buildroot}%{_datadir}/applications/engrampa.desktop

find %{buildroot} -name "*.la" -exec rm -f {} ';'

# remove needless gsettings convert file to avoid slow session start
rm -f  %{buildroot}%{_datadir}/MateConf/gsettings/engrampa.convert
magic_rpm_clean.sh
%find_lang %{name} --with-gnome --all-name

%post
/bin/touch --no-create %{_datadir}/icons/mate &> /dev/null || :
/usr/bin/update-desktop-database &> /dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &> /dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
    /usr/bin/update-desktop-database &> /dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%files -f %{name}.lang
%doc README COPYING NEWS AUTHORS
%{_mandir}/man1/*
%{_bindir}/engrampa
%{_libexecdir}/engrampa
%{_datadir}/engrampa
%{_datadir}/applications/engrampa.desktop
%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/icons/hicolor/scalable/apps/*.svg
%{_datadir}/glib-2.0/schemas/org.mate.engrampa.gschema.xml
%{_libdir}/caja/extensions-2.0/libcaja-engrampa.so


%changelog
* Thu Oct 29 2015 Liu Di <liudidi@gmail.com> - 1.11.0-2
- 更新到 1.11.0

* Mon Aug 11 2014 Liu Di <liudidi@gmail.com> - 1.9.0-2
- 为 Magic 3.0 重建

* Sat Jul 12 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.0-1
- update to 1.9.0 release

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar 05 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.8.0-1
- Update to 1.8.0

* Wed Feb 19 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.90-1
- update to 1.7.90

* Sun Feb 09 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.1-1
- Update to 1.7.1

* Thu Jan 16 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.0-1
- update to 1.7.0 release

* Wed Dec 18 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.0-0.2.git20131215.f4611c3
- make Maintainers life easier and use better git snapshot usage, Thanks to Björn Esser
- use modern 'make install' macro

* Sun Dec 15 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.0-0.1.gitf4611c3
- rename mate-file-archiver to engrampa
- use latest git snapshot from 1.7 branch
- add support for *.ar, *.cab, *.wim, *.swm files
- several zip improvements 

* Sun Oct 13 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-0.1.git95ebd69
- update to latest snapshot
- remove mate-file-archiver_missing_gsettings_schema.patch, already in snapshot
- add support for rar-0.5
- add support for unarchiver

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jun 30 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.0-2
- https://github.com/mate-desktop/mate-file-archiver/issues/19,
- fix add folder to existing archive
- remove BR gsettings-desktop-schemas
- remove BR glib2-devel
- remove needless gsettings convert file

* Wed Apr 03 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.0-1
- Update to latest 1.6.0 stable release.

* Thu Feb 21 2013 Rex Dieter <rdieter@fedoraproject.org> 1.5.1-6
- Obsoletes: mate-file-manager-archiver (#908137)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 23 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.1-4
- Bump release

* Tue Jan 22 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.1-3
- Update BRs
- Convert back to old BR style
- Get rid of separate package for shared library
- Add provides field
- Rebuild against latest version of mate-desktop
- Update icon scriptlets
- Add obsoletes tag

* Thu Nov 22 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.1-2
- Rebuild for f17

* Mon Nov 19 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.1-1
- Update to latest release
- Remove patches that were applied upstream

* Thu Nov 15 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.0-3
- Fix another schema error

* Thu Nov 15 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.0-2
- add patch to fix (rhbz 876354)

* Thu Oct 25 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.0-1
- Initial build

