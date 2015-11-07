# Conditional for release and snapshot builds. Uncomment for release-builds.
%global rel_build 1

# This is needed, because src-url contains branched part of versioning-scheme.
#global branch 1.9

# Settings used for build from snapshots.
%{!?rel_build:%global commit c1ca209172a8b3a0751ac0a1e2dbec33c1894290}
%{!?rel_build:%global commit_date 20140712}
%{!?rel_build:%global shortcommit %(c=%{commit};echo ${c:0:7})}
%{!?rel_build:%global git_ver git%{commit_date}-%{shortcommit}}
%{!?rel_build:%global git_rel .git%{commit_date}.%{shortcommit}}
%{!?rel_build:%global git_tar %{name}-%{version}-%{git_ver}.tar.xz}

Summary:  Text editor for the MATE desktop
Summary(zh_CN.UTF-8): MATE 桌面的文本编辑器
Name:     pluma
Version: 1.11.0
Release: 2%{?dist}
#Release: 1%{?dist}
License:  GPLv2+ and LGPLv2+
Group:    Applications/Editors
Group(zh_CN.UTF-8): 应用程序/编辑器
URL:      http://mate-desktop.org

# for downloading the tarball use 'spectool -g -R pluma.spec'
# Source for release-builds.
%define branch %(echo %{version} | awk -F. '{print $1"."$2}')
%{?rel_build:Source0:     http://pub.mate-desktop.org/releases/%{branch}/%{name}-%{version}.tar.xz}
# Source for snapshot-builds.
%{!?rel_build:Source0:    http://git.mate-desktop.org/%{name}/snapshot/%{name}-%{commit}.tar.xz#/%{git_tar}}

BuildRequires: desktop-file-utils
BuildRequires: enchant-devel
BuildRequires: libsoup-devel
BuildRequires: gtk2-devel
BuildRequires: gtksourceview2-devel
BuildRequires: iso-codes-devel
BuildRequires: libSM-devel
BuildRequires: mate-common
BuildRequires: pygobject2-devel
BuildRequires: pygtksourceview-devel
BuildRequires: python2-devel
BuildRequires: rarian-compat
BuildRequires: yelp-tools
BuildRequires: mate-desktop-devel

Requires: %{name}-data = %{version}-%{release}
Requires: pygtk2
Requires: pygobject2
Requires: pygtksourceview
# needed to get a gsettings schema, #959607
Requires: mate-desktop-libs
# needed to get a gsettings schema, #959607
Requires: caja-schemas
# the run-command plugin uses zenity
Requires: zenity

Provides:  mate-text-editor%{?_isa} = %{version}-%{release}
Provides:  mate-text-editor = %{version}-%{release}
Obsoletes: mate-text-editor < %{version}-%{release}

%description
mate-text-editor is a small, but powerful text editor designed specifically for
the MATE desktop. It has most standard text editor functions and fully
supports international text in Unicode. Advanced features include syntax
highlighting and automatic indentation of source code, printing and editing
of multiple documents in one window.

mate-text-editor is extensible through a plugin system, which currently includes
support for spell checking, comparing files, viewing CVS ChangeLogs, and
adjusting indentation levels.

%description -l zh_CN.UTF-8
MATE 桌面的文本编辑器。

%package data
Summary:   Data files for pluma
Summary(zh_CN.UTF-8): %{name} 的数据文件
Group:     Applications/Editors
Group(zh_CN.UTF-8): 应用程序/编辑器
BuildArch: noarch
Requires:  %{name} = %{version}-%{release}

%description data
This package contains shared data needed for pluma.

%description data -l zh_CN.UTF-8
%{name} 的数据文件。

%package devel
Summary:   Support for developing plugins for the mate-text-editor text editor
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:     Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:  %{name}%{?_isa} = %{version}-%{release}
Requires:  gtksourceview3-devel
Requires:  pygtk2-devel
Provides:  mate-text-editor-devel%{?_isa} = %{version}-%{release}
Provides:  mate-text-editor-devel = %{version}-%{release}
Obsoletes: mate-text-editor-devel < %{version}-%{release}

%description devel
Development files for mate-text-editor

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q%{!?rel_build:n %{name}-%{commit}}

# needed for git snapshots
#NOCONFIGURE=1 ./autogen.sh

# Fix debug permissions with messy hack 
find ./*/* -type f -exec chmod 644 {} \;
find ./*/*/* -type f -exec chmod 644 {} \;


%build
%configure \
        --disable-static          \
        --enable-gtk-doc-html     \
        --enable-gvfs-metadata    \
        --enable-python           \
        --disable-schemas-compile \
        --with-gtk=2.0

make %{?_smp_mflags} V=1

%install
%{make_install}

desktop-file-install                                \
    --delete-original                               \
    --dir %{buildroot}%{_datadir}/applications      \
%{buildroot}%{_datadir}/applications/*.desktop

# clean up all the static libs for plugins
find %{buildroot} -name '*.la' -exec rm -f {} ';'
find %{buildroot} -name '*.a' -exec rm -f {} ';'

# remove needless gsettings convert file
rm -f  %{buildroot}%{_datadir}/MateConf/gsettings/pluma.convert
magic_rpm_clean.sh
%find_lang %{name} --with-gnome --all-name


%post
/usr/bin/update-desktop-database &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi
/usr/bin/update-desktop-database &> /dev/null || :

%posttrans
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%post data
/bin/touch --no-create %{_datadir}/pluma/icons &> /dev/null || :

%postun data
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/pluma/icons &> /dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/pluma/icons &> /dev/null || :
fi

%posttrans data
/usr/bin/gtk-update-icon-cache %{_datadir}/pluma/icons &>/dev/null || :


%files
%{_bindir}/pluma
%{_libdir}/pluma/
%{_libexecdir}/pluma/
%{_datadir}/applications/pluma.desktop
%{_datadir}/glib-2.0/schemas/org.mate.pluma.gschema.xml
%{_datadir}/glib-2.0/schemas/org.mate.pluma.plugins.filebrowser.gschema.xml
%{_datadir}/glib-2.0/schemas/org.mate.pluma.plugins.time.gschema.xml
%{_datadir}/appdata/pluma.appdata.xml

%files data -f %{name}.lang
%doc README COPYING AUTHORS
%{_datadir}/pluma/
%{_mandir}/man1/pluma.1.*

%files devel
%{_includedir}/pluma/
%{_libdir}/pkgconfig/pluma.pc
%{_datadir}/gtk-doc/html/pluma/

%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1.11.0-2
- 更新到 1.11.0

* Fri Jul 24 2015 Liu Di <liudidi@gmail.com> - 1.10.2-1
- 更新到 1.10.2

* Mon Aug 11 2014 Liu Di <liudidi@gmail.com> - 1.9.0-2
- 为 Magic 3.0 重建

* Tue Jul 15 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.0-1
- update to 1.9.0 release
- enable gtk-docs for release build
- disable autogen for release build

* Sat Jul 12 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.0-0.1.git20131511.c1ca209
- use git snapshot from 2014.07.12
- disable gtk-docs for snapshot build

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun May 04 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.8.1.1
- update to 1.8.1 release

* Wed Mar 05 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.8.0-1
- Update to 1.8.0

* Wed Feb 19 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.90-1
- update to 1.7.90
- remove obsolete mate-text-editor binary from spec file

* Thu Feb 13 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.2-1
- update to 1.7.2 release
- fix rpmlint warning 'can't find source0'
- fix license information
- use a joker for the man file attribute
- move data in a noarch subpackage
- improve obsoletes
- update rpm scriplets

* Wed Dec 25 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.1-1
- update to 1.7.1 release
- add gtk-doc dir to -devel subpackage for release builds

* Wed Dec 25 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.1-0.1.git20131511.7ceb8fe
- rename to pluma
- make maintainers life easier and use better git snapshot usage, thanks to Björn Esser
- simplify remove of static libaries
- use modern 'make install' macro
- add --with-gnome flag to find_language, needed for yelp
- sort file section

* Fri Dec 06 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.0-1
- Update to 1.7.0

* Thu Aug 08 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.0-5
- add runtime require mate-file-manager-schemas to fix #959607

* Thu Aug 08 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.0-4
- switch to runtime require mate-desktop-libs
- remove needless --with-gnome flag in find_language 

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jun 30 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.0-2
- add runtime require mate-desktop, fix rhbz #959607
- remove pluma.convert files
- cleanup BR's
- fix desktop file install command, no needed to add X-MATE
- use runtime require mate-dialogs instead of zenity
- remove BR mate-conf-devel
- add --disable-static configure flag
- general usage of %%{buildroot}
- no need of mimeinfo rpm scriptlets
- fix desktop-database rpm scriptlets
- update BR's 
- add isa tag to -devel subpackage

* Sat Apr 13 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.0-1
- Update to latest 1.6.0 stable release.

* Sun Feb 10 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.1-1
- Update to latest upstream release

* Mon Oct 15 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-2
- Fix build requires

* Sun Oct 14 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-1
- Initial build


