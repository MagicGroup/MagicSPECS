# RPM spec file for Allegro.
%define soft_version 4.4.2
%define betaversion beta4
Summary: A game programming library.
Summary(zh_CN.UTF-8): 一个游戏程序库。
Name: allegro
Version: %{soft_version}
Release: 7%{?dist}
License: Gift Ware
Packager: Allegro development team
Group:          System Environment/Libraries
Group(zh_CN.UTF-8):   系统环境/库
Source: ftp://sunsite.dk/allegro/%{name}-%{version}.tar.gz
Patch1:         allegro-4.0.3-cfg.patch
Patch2:         allegro-4.0.3-libdir.patch
Patch3:         allegro-4.2.3-pack-formatstring.patch
Patch4:         allegro-4.4.2-dynamic-addons.patch
Patch5:         allegro-4.4.2-doc-install.patch
Patch6:         allegro-4.4.2-buildsys-fix.patch
URL: http://alleg.sourceforge.net
# If you don't have the icon, just comment it out.
# Icon: alex.xpm
Buildroot: %{_tmppath}/%{name}-buildroot
# Older rpms don't support this; just make sure you have it.
#BuildRequires: texinfo
# Automatic dependency generation picks up module dependencies
# which is exactly what we don't want...
# But which you *need* for compiling on other platforms ...
Autoreqprov: on
Requires: /sbin/ldconfig, /usr/sbin/install-info

%description
Allegro is a cross-platform library intended for use in computer games
and other types of multimedia programming.

%description -l zh_CN.UTF-8
Allegro是一个用来开发计算机游戏或其它类型的多媒体程序的跨平台的库。

%package devel
Summary: A game programming library.
Summary(zh_CN.UTF-8): 一个游戏开发库。
Group:          Development/Libraries
Group(zh_CN.UTF-8):   开发/库
Prereq: %{name} = %{version}
Autoreqprov: on

%description devel
Allegro is a cross-platform library intended for use in computer games
and other types of multimedia programming. This package is needed to
build programs written with Allegro.

%description devel -l zh_CN.UTF-8
Allegro是一个用来开发计算机游戏或其它类型的多媒体程序的跨平台的库。
用Allegro编写的程序编译需要这个包。

%package tools
Summary: Extra tools for the Allegro programming library.
Group: Development/Tools
Group(zh_CN.UTF-8): 开发/工具
Prereq: allegro
Autoreq: on

%description tools
Allegro is a cross-platform library intended for use in computer games
and other types of multimedia programming. This package contains extra
tools which are useful for developing Allegro programs.

%description tools -l zh_CN.UTF-8
Allegro是一个用来开发计算机游戏或其它类型的多媒体程序的跨平台的库。
这个包包含了对开发Allegro程序非常有用的额外工具。

%package jack-plugin
Summary:        Allegro JACK (Jack Audio Connection Kit) plugin
Summary(zh_CN.UTF-8): Allegro 的 JACK 音频插件
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Requires:       %{name} = %{version}-%{release}

%description jack-plugin
This package contains a plugin for Allegro which enables Allegro to playback
sound through JACK (Jack Audio Connection Kit).

%description jack-plugin -l zh_CN.UTF-8
这个包包含了可以使 Allegro 通过 JACK 回放声音的一个插件。

%package -n alleggl
Summary:        OpenGL support library for Allegro
Summary(zh_CN.UTF-8): Allegro 的 OpenGL 支持库
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        zlib or GPL+
URL:            http://allegrogl.sourceforge.net/
Requires:       %{name} = %{version}-%{release}

%description -n alleggl
AllegroGL is an Allegro add-on that allows you to use OpenGL alongside Allegro.
You use OpenGL for your rendering to the screen, and Allegro for miscellaneous
tasks like gathering input, doing timers, getting cross-platform portability,
loading data, and drawing your textures. So this library fills the same hole
that things like glut do.

%description -n alleggl -l zh_CN.UTF-8
这个包是允许你一起使用 Allegro 和 OpenGL。
你可以使用 OpenGL 来渲染屏幕，其它的比如收集输入，设定时器，获得跨平台能力，
载入数据等，使用 Allegro。就类似于 glut 做的一样。

%package -n alleggl-devel
Summary:        Development files for alleggl
Summary(zh_CN.UTF-8): alleggl 的开发文件
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License:        zlib or GPL+
Requires:       alleggl = %{version}-%{release}

%description -n alleggl-devel
The alleggl-devel package contains libraries and header files for
developing applications that use alleggl.

%description -n alleggl-devel -l zh_CN.UTF-8
alleggl 的开发文件。

%package -n jpgalleg
Summary:        JPEG library for the Allegro game library
Summary(zh_CN.UTF-8): Allegro 游戏库的 JPEG 库
Group:          System Environment/Libraries
Group(zh_CN):	系统环境/库
License:        zlib
URL:            http://www.ecplusplus.com/index.php?page=projects&pid=1
Requires:       %{name} = %{version}-%{release}

%description -n jpgalleg
jpgalleg is a jpeg library for use with the Allegro game library. It allows
using jpeg's as Allegro bitmaps.

%description -n jpgalleg -l zh_CN.UTF-8
Allegro 游戏库的 jpeg 库。

%package -n jpgalleg-devel
Summary:        Development files for jpgalleg
Summary(zh_CN.UTF-8): jpgalleg 的开发文件
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License:        zlib
Requires:       jpgalleg = %{version}-%{release}

%description -n jpgalleg-devel
The jpgalleg-devel package contains libraries and header files for
developing applications that use jpgalleg.

%description -n jpgalleg-devel -l zh_CN.UTF-8
jpgalleg 的开发文件。

%package loadpng
Summary:        PNG library for the Allegro game library
Summary(zh_CN.UTF-8): Allegro 游戏库的 PNG 库
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        Public Domain
URL:            http://wiki.allegro.cc/index.php?title=LoadPNG
Requires:       %{name} = %{version}-%{release}

%description loadpng
loadpng is some glue that makes it easy to use libpng to load and
save bitmaps from Allegro programs.

%description loadpng -l zh_CN.UTF-8
Allegro 游戏库的 PNG 库，使用 libpng 来载入和保存图像。

%package loadpng-devel
Summary:        Development files for loadpng
Summary(zh_CN.UTF-8): loadpng 的开发文件
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License:        Public Domain
Requires:       %{name}-loadpng = %{version}-%{release}

%description loadpng-devel
The loadpng-devel package contains libraries and header files for
developing applications that use loadpng.

%description loadpng-devel -l zh_CN.UTF-8
loadpng 的开发文件。

%package logg
Summary:        OGG/Vorbis library for the Allegro game library
Summary(zh_CN.UTF-8): Allegro 游戏库的 OGG/Vorbis 库
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        MIT
URL:            http://trent.gamblin.ca/logg/
Requires:       %{name} = %{version}-%{release}

%description logg
LOGG is an Allegro add-on library for playing OGG/Vorbis audio files.

%description logg -l zh_CN.UTF-8
Allegro 游戏库的 OGG/Vorbis 库，可以播放 OGG/Vorbis 音频文件。

%package logg-devel
Summary:        Development files for logg
Summary(zh_CN.UTF-8): logg 的开发文件
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License:        MIT
Requires:       %{name}-logg = %{version}-%{release}

%description logg-devel
The logg-devel package contains libraries and header files for
developing applications that use logg.

%description logg-devel -l zh_CN.UTF-8
logg 的开发文件。

%prep
%setup -q
%patch1 -p1 
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
%cmake
make %{?_smp_mflags}

# Converting text documentation to UTF-8 encoding.
for f in docs/AUTHORS docs/CHANGES docs/THANKS \
        docs/info/*.info docs/txt/*.txt docs/man/get_camera_matrix.3 \
        addons/allegrogl/changelog; do
    dirname=$(dirname "$f");
    basename=$(basename "$f");
    tmppath="${dirname}/${basename}.tmp";
    iconv -f 'iso-8859-1' -t 'utf-8' "$f" > "$tmppath";
    mv "$tmppath" "$f";
done

%install
make install DESTDIR=$RPM_BUILD_ROOT
# installation of these is broken, because they use a cmake GLOB, but
# that gets "resolved" when runnning cmake, and at that time the files
# to install aren't generated yet ...
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man3
mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/html
install -p -m 644 docs/man/*.3 $RPM_BUILD_ROOT%{_mandir}/man3
install -p -m 644 docs/html/*.{html,css} \
    $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/html
# Install some extra files
install -Dpm 644 allegro.cfg $RPM_BUILD_ROOT%{_sysconfdir}/allegrorc
install -pm 755 tools/x11/xfixicon.sh $RPM_BUILD_ROOT%{_bindir}
install -m 755 docs/makedoc $RPM_BUILD_ROOT%{_bindir}/allegro-makedoc
install -dm 755 $RPM_BUILD_ROOT%{_datadir}/allegro
install -pm 644 keyboard.dat language.dat $RPM_BUILD_ROOT%{_datadir}/allegro
magic_rpm_clean.sh

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post devel
/usr/sbin/install-info %{_infodir}/allegro.info %{_infodir}/dir 2>/dev/null || :

%preun devel
if [ $1 -eq 0 ] ; then
  /usr/sbin/install-info --delete %{_infodir}/allegro.info %{_infodir}/dir \
    2>/dev/null || :
fi

%post -n alleggl -p /sbin/ldconfig
%postun -n alleggl -p /sbin/ldconfig

%post -n jpgalleg -p /sbin/ldconfig
%postun -n jpgalleg -p /sbin/ldconfig

%post loadpng -p /sbin/ldconfig
%postun loadpng -p /sbin/ldconfig

%post logg -p /sbin/ldconfig
%postun logg -p /sbin/ldconfig

%clean
rm -rf %{buildroot}
rm -rf %{builddir}/%{name}-%{version}

%files
%defattr(-,root,root,-)
%doc %{_docdir}/%{name}-%{version}/AUTHORS
%doc %{_docdir}/%{name}-%{version}/CHANGES
%doc %{_docdir}/%{name}-%{version}/THANKS
%doc %{_docdir}/%{name}-%{version}/addons.txt
%doc %{_docdir}/%{name}-%{version}/faq.txt
%doc %{_docdir}/%{name}-%{version}/license.txt
%doc %{_docdir}/%{name}-%{version}/readme.txt
%config(noreplace) %{_sysconfdir}/allegrorc
%{_libdir}/liballeg.so.4*
%{_libdir}/allegro
%{_datadir}/allegro
%exclude %{_libdir}/allegro/%{version}/alleg-jack.so

%files devel
%defattr(-,root,root,-)
%doc %{_docdir}/%{name}-%{version}/abi.txt
%doc %{_docdir}/%{name}-%{version}/ahack.txt
%doc %{_docdir}/%{name}-%{version}/allegro.txt
%doc %{_docdir}/%{name}-%{version}/api.txt
%doc %{_docdir}/%{name}-%{version}/const.txt
%doc %{_docdir}/%{name}-%{version}/faq.txt
%doc %{_docdir}/%{name}-%{version}/help.txt
%doc %{_docdir}/%{name}-%{version}/html
%doc %{_docdir}/%{name}-%{version}/makedoc.txt
%doc %{_docdir}/%{name}-%{version}/mistakes.txt
%doc %{_docdir}/%{name}-%{version}/packfile.txt
%{_bindir}/allegro-config
%{_bindir}/allegro-makedoc
%{_libdir}/liballeg.so
%{_libdir}/pkgconfig/allegro.pc
%{_includedir}/allegro
%{_includedir}/allegro.h
%{_includedir}/xalleg.h
%{_infodir}/allegro.info*
%{_mandir}/man3/*

%files tools
%defattr(-,root,root,-)
%doc %{_docdir}/%{name}-%{version}/dat*.txt
%doc %{_docdir}/%{name}-%{version}/grabber.txt
%{_bindir}/colormap
%{_bindir}/dat
%{_bindir}/dat2s
%{_bindir}/dat2c
%{_bindir}/exedat
%{_bindir}/grabber
%{_bindir}/pack
%{_bindir}/pat2dat
%{_bindir}/rgbmap
%{_bindir}/textconv
%{_bindir}/xfixicon.sh

%files jack-plugin
%defattr(-,root,root,-)
%{_libdir}/allegro/%{version}/alleg-jack.so

%files -n alleggl
%doc addons/allegrogl/changelog
%doc addons/allegrogl/faq.txt
%doc addons/allegrogl/gpl.txt
%doc addons/allegrogl/readme.txt
%doc addons/allegrogl/zlib.txt
%{_libdir}/liballeggl.so.4*

%files -n alleggl-devel
%doc addons/allegrogl/bugs.txt
%doc addons/allegrogl/extensions.txt
%doc addons/allegrogl/howto.txt
%doc addons/allegrogl/quickstart.txt
%doc addons/allegrogl/todo.txt
%{_libdir}/liballeggl.so
%{_libdir}/pkgconfig/allegrogl.pc
%{_includedir}/alleggl.h
%{_includedir}/allegrogl

%files -n jpgalleg
%doc addons/jpgalleg/license.txt
%doc addons/jpgalleg/readme.txt
%{_libdir}/libjpgalleg.so.4*

%files -n jpgalleg-devel
%{_libdir}/libjpgalleg.so
%{_libdir}/pkgconfig/jpgalleg.pc
%{_includedir}/jpgalleg.h

%files loadpng
%doc addons/loadpng/CHANGES.txt
%doc addons/loadpng/README.txt
%doc addons/loadpng/THANKS.txt
%{_libdir}/libloadpng.so.4*

%files loadpng-devel
%{_libdir}/libloadpng.so
%{_libdir}/pkgconfig/loadpng.pc
%{_includedir}/loadpng.h

%files logg
%doc addons/logg/LICENSE.txt
%{_libdir}/liblogg.so.4*

%files logg-devel
%{_libdir}/liblogg.so
%{_libdir}/pkgconfig/logg.pc
%{_includedir}/logg.h

%changelog
* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 4.4.2-7
- 为 Magic 3.0 重建

* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 4.4.2-6
- 为 Magic 3.0 重建

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 4.4.2-4
- 为 Magic 3.0 重建

* Tue Dec 04 2012 Liu Di <liudidi@gmail.com> - 4.4.2-3
- 为 Magic 3.0 重建

* Fri Oct 26 2012 Liu Di <liudidi@gmail.com> - 4.4.2-2
- 为 Magic 3.0 重建

* Fri Oct 28 2011 Liu Di <liudidi@gmail.com> - 4.4.2-1
- 更新到 4.4.2

* Fri Oct 31 2008 Liu Di <liudidi@gmail.com> - 4.2.2-1mgc
- 更新到 4.2.2

* Mon Aug 29 2005 sejishikong <sejishikong@263.net> 4.2.0-beta4
- add svgalib support
- add zh_CN.UTF-8
