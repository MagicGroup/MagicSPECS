%define uvt .git86d101c96defee6b4f48416cf008ed670e051e03
%define checkout git86d101c9
%define XULRUNNER_VERSION 27

Name:		chmsee
Version:	2.0.2
Release:	7.%{checkout}%{?dist}
Summary(zh_CN):	CHM 文件阅读工具, 基于 XULRunner
Summary:	HTML Help viewer for Unix/Linux
Group:		Applications/Publishing
License:	GPLv2
URL:		http://code.google.com/p/chmsee
# with `git describe HEAD`.git`git rev-parse HEAD`
Source0:	%{name}-v%{version}%{uvt}.tar.gz

BuildRequires:	desktop-file-utils
BuildRequires:	xulrunner-devel >= %{XULRUNNER_VERSION} chmlib-devel cmake
Requires:		xulrunner >= %{XULRUNNER_VERSION}

%description
ChmSee is an HTML Help viewer for Unix/Linux. It is based on CHMLIB
and use GTK+ as its front end toolkit. Because of using gecko HTML
rendering engine, ChmSee can support rich features of modern HTML
page, specially CSS.

Homepage: http://code.google.com/p/chmsee

Hint
* Unlike other chm viewers, chmsee extracts files from chm file, and then read
and display them. The extracted files could be found in $HOME/.chmsee/bookshelf
directory. You can clean those files at any time and there is a special config
option for that.
* The bookmark is related to each file so not all bookmarks will be loaded,
only current file's.
* Try to remove $HOME/.chmsee if you encounter any problem after an upgrade.

About ChmSee logo
ChmSee logo comes from Open Clip Art Library. The author is AJ Ashton.
http://www.openclipart.org/detail/17922

%description -l zh_CN
HTML 帮助文件阅读工具

使用提示
* 与有些 chm 阅读工具不同，ChmSee 采用的是
先将 chm 文件解压，再读取 html 文件的方式。
解压后的文件保存在 $HOME/.chmsee/bookshelf 
目录下面。如果您想清空这些解压后的文件，可以
按下“设置”按钮，在打开的对话框里面使用“清除”
功能。
* ChmSee 的书签功能与各个 chm 文件挂钩，打开
一个 chm 文件后，只会显示当前文件的书签。
* 试用新版本时，如果程序无法运行或在打开文件
时退出，请先清空一下 $HOME/.chmsee 目录。


%prep
%setup -q -c
sed -i.orig -e 's/^\(MaxVersion=\).*/\1%{XULRUNNER_VERSION}.*/' application.ini
sed -e 's/^_\+\([^=]\+\)/\1/' data/%{name}.desktop.in > data/%{name}.desktop
cat > %{name} <<'END'
#!/bin/sh
case `uname -m` in
	x86_64 | ia64 | s390 )
		XUL_LIB_DIR="/usr/lib64"
		;;
	* )
		XUL_LIB_DIR="/usr/lib"
		;;
esac
exec xulrunner $XUL_LIB_DIR/%{name}/application.ini "$@"
END

%build
cd src
CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS" LDFLAGS="$RPM_LD_FLAGS" \
make -f *.fedora

%install
install -m 755 -d $RPM_BUILD_ROOT%{_libdir}/chmsee
install -p -m 644 -D *.ini *.manifest $RPM_BUILD_ROOT%{_libdir}/chmsee
cp -ar chrome $RPM_BUILD_ROOT%{_libdir}/chmsee
cp -ar components $RPM_BUILD_ROOT%{_libdir}/chmsee
install -m 755 -d $RPM_BUILD_ROOT%{_datadir}/chmsee/data
install -p -m 644 -D data/*.png $RPM_BUILD_ROOT%{_datadir}/chmsee/data
cp -ar defaults $RPM_BUILD_ROOT%{_libdir}/chmsee
mv data/icons -t $RPM_BUILD_ROOT%{_datadir}
install -p -m 644 -D data/chmsee-icon.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps/chmsee-icon.png
install -m 755 -d $RPM_BUILD_ROOT%{_datadir}/mime-info
install -p -m 644 -D data/*.keys data/*.mime $RPM_BUILD_ROOT%{_datadir}/mime-info
install -p -m 755 -D %{name} $RPM_BUILD_ROOT%{_bindir}/%{name}

desktop-file-install --remove-key=Version \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  --add-category "GTK;Office;Viewer;" \
  data/%{name}.desktop

%post
update-desktop-database %{_datadir}/applications &>/dev/null || :
update-mime-database %{_datadir}/mime &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor || :
%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :

%postun
update-desktop-database %{_datadir}/applications &>/dev/null || :
update-mime-database %{_datadir}/mime &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor || :
%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :

%files
%doc AUTHORS ChangeLog* COPYING NEWS README* HACKING
%{_datadir}/applications/chmsee.desktop
%{_bindir}/chmsee
%{_libdir}/chmsee/
%{_datadir}/chmsee/
%{_datadir}/icons/hicolor/*/apps/chmsee-icon.png
%{_datadir}/mime-info/chmsee.keys
%{_datadir}/mime-info/chmsee.mime
%{_datadir}/icons/hicolor/*/mimetypes/chm.png
%{_datadir}/icons/hicolor/*/mimetypes/chm.svg

%changelog
* Mon Feb 10 2014 Yijun Yuan <bbbush.yuan@gmail.com> - 2.0.2-7.git86d101c9
- add missing requires, rhbz1063459

* Mon Feb 03 2014 Yijun Yuan <bbbush.yuan@gmail.com> - 2.0.2-6.git86d101c9
- rebuild for xulrunner 27

* Mon Dec 09 2013 Yijun Yuan <bbbush.yuan@gmail.com> - 2.0.2-5.git86d101c9
- rebuild for xulrunner 26

* Sun Nov 03 2013 bbbush <bbbush.yuan@gmail.com> - 2.0.2-4.git86d101c9
- rebuild for xulrunner 25

* Fri Sep 13 2013 bbbush <bbbush.yuan@gmail.com> - 2.0.2-3.git86d101c9
- rebuild for xulrunner 24

* Mon Aug 05 2013 bbbush <bbbush.yuan@gmail.com> - 2.0.2-1.git86d101c9
- rebuild for xulrunner 23

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-4.gitde57c427
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 25 2013 bbbush <bbbush.yuan@gmail.com> - 2.0.1-3.gitde57c427
- rebuild for xulrunner 22

* Sun May 12 2013 bbbush <bbbush.yuan@gmail.com> - 2.0.1-1.gitde57c427
- rebuild for xulrunner 21

* Mon Apr 01 2013 bbbush <bbbush.yuan@gmail.com> - 2.0-5.git0acc572a
- rebuild for xulrunner 20

