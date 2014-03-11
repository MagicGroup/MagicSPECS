%define _prefix /usr
%define ver  2.8.12
%define ver2 2.8
%define rel  3%{?dist}

# Configurable settings (use --with(out) {unicode,gtk2} on rpmbuild cmd line):
%define unicode 1
%{?_with_unicode: %{expand: %%define unicode 1}}
%{?_without_unicode: %{expand: %%define unicode 0}}

%define gtk2 1
%{?_with_gtk2: %{expand: %%define gtk2 1}}
%{?_without_gtk2: %{expand: %%define gtk2 0}}

# "buildname" needs to be e.g. gtk2ud for debug builds
%if %{gtk2}
    %define gtkver 2
    %define portname gtk2
%if %{unicode}
    %define buildname gtk2u
%else
    %define buildname gtk2
%endif
%else
    %define gtkver 1.2
    %define portname gtk
    %define buildname gtk
%endif

%if %{unicode}
    %define name		wx-%{portname}-unicode
    %define wxconfig		%{portname}-unicode-release-%{ver2}
    %define wxconfigstatic	%{portname}-unicode-release-static-%{ver2}
    %define wxconfiglink	wx%{portname}u-%{ver2}-config
%else
    %define name		wx-%{portname}-ansi
    %define wxconfig		%{portname}-ansi-release-%{ver2}
    %define wxconfigstatic	%{portname}-ansi-release-static-%{ver2}
    %define wxconfiglink	wx%{portname}-%{ver2}-config
%endif

%if %{unicode}
    %define wxbasename		wx-base-unicode
    %define wxbaseconfig	base-unicode-release-%{ver2}
    %define wxbaseconfigstatic	base-unicode-release-static-%{ver2}
    %define wxbaseconfiglink	wxbaseu-%{ver2}-config
%else
    %define wxbasename		wx-base-ansi
    %define wxbaseconfig	base-ansi-release-%{ver2}
    %define wxbaseconfigstatic	base-ansi-release-static-%{ver2}
    %define wxbaseconfiglink	wxbase-%{ver2}-config
%endif

Summary: The GTK+ %{gtkver} port of the wxWidgets library
Summary(zh_CN.UTF-8): wxWidgets的GTK+%{gtkver}移植
Name: %{name}
Version: %{ver}
Release: %{rel}.1
License: wxWindows Licence
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Source: wxWidgets-%{ver}.tar.bz2
Patch: wx_gsockgtk.patch
URL: http://www.wxwidgets.org
Packager: Vadim Zeitlin <vadim@wxwindows.org>
Prefix: %{_prefix}
BuildRoot: %{_tmppath}/%{name}-root
Requires: %{wxbasename} = %{ver}
%if %{portname} == gtk2
# BuildRequires: gtk+-2.0-devel
%else
# BuildRequires: gtk+-devel >= 1.2.0
%endif

BuildRequires: zlib-devel, libjpeg-devel, libpng-devel, libtiff-devel

# all packages providing an implementation of wxWidgets library (regardless of
# the toolkit used) should provide the (virtual) wxwin package, this makes it
# possible to require wxwin instead of requiring "wxgtk or wxmotif or wxuniv..."
Provides: wxwin
Provides: wxWidgets

%description
wxWidgets is a free C++ library for cross-platform GUI development.
With wxWidgets, you can create applications for different GUIs (GTK+,
Motif, MS Windows, MacOS X, Windows CE, GPE) from the same source code.

%description -l zh_CN.UTF-8
wxWidgets是一个自由的跨平台用于界面开发的C++库。
使用wxWidgets，你可以用同一个代码为不同的界面创建程序（GTK+,Motif,
MS Windows, MacOS X, Windows CE, GPE).

%package -n wx-i18n
Summary: The translations for the wxWidgets library.
Summary(zh_CN.UTF-8): wxWidgets库的翻译
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%description -n wx-i18n
The translations files for the wxWidgets library.

%description -n wx-i18n -l zh_CN.UTF-8
wxWidgets库的翻译文件。

%package devel
Summary: The GTK+ %{gtkver} port of the wxWidgets library
Summary(zh_CN.UTF-8): wxWidgets库的GTK+%{gtkver}移植
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Requires: %{name} = %{ver}
Requires: %{wxbasename}-devel = %{ver}
Provides: wxWidgets-devel

%description devel
The GTK+ %{gtkver} port of the wxWidgets library, header files.

%description devel -l zh_CN.UTF-8
wxWidgets的GTK+2移植，头文件。

%package gl
Summary: The GTK+ %{gtkver} port of the wxWidgets library, OpenGL add-on.
Summary(zh_CN.UTF-8): wxWidgets的GTK+%{gtkver}移植，OpenGL附加库。
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Requires: %{name} = %{ver}
Provides: wxWidgets-gl

%description gl
OpenGL add-on library for wxWidgets, the GTK+ %{gtkver} port of the wxWidgets library.

%description gl -l zh_CN.UTF-8
wxWidgets的OpenGL附加库，为wxWidgets的GTK+%{gtkver}移植。

%package -n %{wxbasename}
Summary: wxBase library - non-GUI support classes of the wxWidgets toolkit
Summary(zh_CN.UTF-8): wxBase库 - wxWidgets工具箱的非界面支持库
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Provides: wxBase

%description -n %{wxbasename}
wxBase is a collection of C++ classes providing basic data structures (strings,
lists, arrays), portable wrappers around many OS-specific funstions (file
operations, time/date manipulations, threads, processes, sockets, shared
library loading) as well as other utility classes (streams, archive and
compression). wxBase currently supports Win32, most Unix variants (Linux, 
FreeBSD, Solaris, HP-UX) and MacOS X (Carbon and Mach-0).

%description -n %{wxbasename} -l zh_CN.UTF-8
wxBase是一个C++类的集合，它提供了基本的数据结构（字符串，表，数组），
许多可移植的的系统相关函数（文件操作，时间/日期维护，线程，进程，套接字，
共享库载入），也包括其它的类（流，文档和压缩）。wxBase当前支持Win32，
大部分Unix类（Linux，FreeBSD，Solaris，HP-UX）和MacOS X（Carbon和Mach-0）。

%package -n %{wxbasename}-devel
Summary: wxBase library, header files.
Summary(zh_CN.UTF-8): wxBase库，头文件。
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Provides: wxBase-devel

%description -n %{wxbasename}-devel
wxBase library - non-GUI support classes of the wxWidgets toolkit,
header files.

%description -n %{wxbasename}-devel
wxBase库 - wxWidgets工具箱的非界面支持类头文件。

%package contrib
Summary: The GTK+ %{gtkver} port of the wxWidgets library, contributed libraries.
Summary(zh_CN.UTF-8): wxWidgets库的GTK+%{gtkver}移植，贡献的库。
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Requires: %{name} = %{ver}

%description contrib
Contributed libraries for wxWidgets, the GTK+ %{gtkver} port of the wxWidgets library.

%description contrib -l zh_CN.UTF-8
wxWidgets的贡献库，wxWidgets的GTK+%{gtkver}移植。

%package contrib-devel
Summary: The GTK+ %{gtkver} port of the wxWidgets library
Summary(zh_CN.UTF-8): wxWidgets库的GTK+%{gtkver}移植。
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Requires: %{name}-contrib = %{ver}
Requires: %{name}-devel = %{ver}

%description contrib-devel
Header files for contributed libraries for wxWidgets, the GTK+ %{gtkver} port of the wxWidgets library.

%description contrib-devel -l zh_CN.UTF-8
wxWidgets的贡献库的头文件，wxWidgets库的GTK+%{gtkver}移植。

%prep
%setup -q -n wxWidgets-%{ver}
#%patch -p1
%build
export SMP=16
if [ "$SMP" != "" ]; then
    export MAKE="make -j$SMP"
else
    export MAKE="make"
fi

%define _configure	../configure

mkdir obj-shared-no-gui
cd obj-shared-no-gui
%configure --prefix=%{_prefix} \
			      --disable-gui \
                              --with-libpng \
                              --with-libjpeg \
                              --with-libtiff \
			      --with-sdl \
			      --enable-largefile \
%if %{unicode}
                              --enable-unicode
%else
                              --disable-unicode
%endif
$MAKE
cd ..

mkdir obj-shared
cd obj-shared
%configure --prefix=%{_prefix} \
%if ! %{gtk2}
			      --with-gtk=1 \
%else
			      --with-gtk=2 \
%endif
%if %{unicode}
			      --enable-unicode \
%else
			      --disable-unicode \
			      --with-odbc \
%endif
			      --with-opengl \
                              --with-libpng \
                              --with-libjpeg \
                              --with-libtiff \
			      --with-sdl \
			      --enable-largefile
$MAKE

cd contrib/src
$MAKE
cd ../../..

mkdir obj-static-no-gui
cd obj-static-no-gui
%configure --prefix=%{_prefix} \
			      --disable-gui \
                              --with-libpng \
                              --with-libjpeg \
                              --with-libtiff \
			      --with-sdl \
			      --enable-largefile \
      			      --disable-shared \
%if %{unicode}
                              --enable-unicode
%else
                              --disable-unicode
%endif
$MAKE
cd ..

mkdir obj-static
cd obj-static
%configure --prefix=%{_prefix} \
%if ! %{gtk2}
			      --with-gtk=1 \
%else
			      --with-gtk=2 \
%endif
			      --disable-shared \
%if %{unicode}
                	      --enable-unicode \
%else
            		      --disable-unicode \
			      --with-odbc \
%endif
            		      --with-opengl \
			      --with-libpng \
			      --with-libjpeg \
			      --with-libtiff \
			      --with-sdl \
			      --enable-largefile
$MAKE

cd contrib/src
$MAKE
cd ../../..

%install
rm -rf $RPM_BUILD_ROOT
(cd obj-static-no-gui; make DESTDIR=$RPM_BUILD_ROOT install)
(cd obj-static; make DESTDIR=$RPM_BUILD_ROOT install)
(cd obj-shared-no-gui; make DESTDIR=$RPM_BUILD_ROOT install)
(cd obj-shared; make DESTDIR=$RPM_BUILD_ROOT install)

# --- wxBase headers list begins here ---
cat <<EOF >wxbase-headers-list
wx/afterstd.h
wx/app.h
wx/apptrait.h
wx/archive.h
wx/arrimpl.cpp
wx/arrstr.h
wx/beforestd.h
wx/buffer.h
wx/build.h
wx/chkconf.h
wx/clntdata.h
wx/cmdline.h
wx/confbase.h
wx/config.h
wx/containr.h
wx/datetime.h
wx/datstrm.h
wx/dde.h
wx/debug.h
wx/defs.h
wx/dir.h
wx/dlimpexp.h
wx/dynarray.h
wx/dynlib.h
wx/dynload.h
wx/encconv.h
wx/event.h
wx/except.h
wx/features.h
wx/ffile.h
wx/file.h
wx/fileconf.h
wx/filefn.h
wx/filename.h
wx/filesys.h
wx/fontenc.h
wx/fontmap.h
wx/fs_mem.h
wx/fs_zip.h
wx/hash.h
wx/hashmap.h
wx/hashset.h
wx/html/forcelnk.h
wx/iconloc.h
wx/init.h
wx/intl.h
wx/iosfwrap.h
wx/ioswrap.h
wx/ipc.h
wx/ipcbase.h
wx/isql.h
wx/isqlext.h
wx/list.h
wx/listimpl.cpp
wx/log.h
wx/longlong.h
wx/math.h
wx/memconf.h
wx/memory.h
wx/memtext.h
wx/mimetype.h
wx/module.h
wx/msgout.h
wx/msgout.h
wx/mstream.h
wx/object.h
wx/platform.h
wx/process.h
wx/ptr_scpd.h
wx/regex.h
wx/scopeguard.h
wx/snglinst.h
wx/sstream.h
wx/stack.h
wx/stackwalk.h
wx/stdpaths.h
wx/stockitem.h
wx/stopwatch.h
wx/strconv.h
wx/stream.h
wx/string.h
wx/sysopt.h
wx/textbuf.h
wx/textfile.h
wx/thread.h
wx/thrimpl.cpp
wx/timer.h
wx/tokenzr.h
wx/txtstrm.h
wx/types.h
wx/uri.h
wx/utils.h
wx/variant.h
wx/vector.h
wx/version.h
wx/volume.h
wx/wfstream.h
wx/wx.h
wx/wxchar.h
wx/wxprec.h
wx/xti.h
wx/xtistrm.h
wx/zipstrm.h
wx/zstream.h
wx/msw/apptrait.h
wx/msw/apptbase.h
wx/msw/chkconf.h
wx/msw/crashrpt.h
wx/msw/dde.h
wx/msw/debughlp.h
wx/msw/gccpriv.h
wx/msw/mimetype.h
wx/msw/stackwalk.h
wx/msw/stdpaths.h
wx/msw/winundef.h
wx/msw/wrapcctl.h
wx/msw/wrapcdlg.h
wx/msw/wrapwin.h
wx/fs_inet.h
wx/gsocket.h
wx/protocol/file.h
wx/protocol/ftp.h
wx/protocol/http.h
wx/protocol/protocol.h
wx/sckaddr.h
wx/sckipc.h
wx/sckstrm.h
wx/socket.h
wx/url.h
wx/msw/gsockmsw.h
wx/xml/xml.h
wx/xtixml.h
wx/db.h
wx/dbkeyg.h
wx/dbtable.h
EOF
# --- wxBase headers list ends here ---
cat <<EOF >wxbase-headers.paths
%{_includedir}/wx-%{ver2}/wx/afterstd.h
%{_includedir}/wx-%{ver2}/wx/app.h
%{_includedir}/wx-%{ver2}/wx/apptrait.h
%{_includedir}/wx-%{ver2}/wx/archive.h
%{_includedir}/wx-%{ver2}/wx/arrimpl.cpp
%{_includedir}/wx-%{ver2}/wx/arrstr.h
%{_includedir}/wx-%{ver2}/wx/beforestd.h
%{_includedir}/wx-%{ver2}/wx/buffer.h
%{_includedir}/wx-%{ver2}/wx/build.h
%{_includedir}/wx-%{ver2}/wx/chkconf.h
%{_includedir}/wx-%{ver2}/wx/clntdata.h
%{_includedir}/wx-%{ver2}/wx/cmdline.h
%{_includedir}/wx-%{ver2}/wx/confbase.h
%{_includedir}/wx-%{ver2}/wx/config.h
%{_includedir}/wx-%{ver2}/wx/containr.h
%{_includedir}/wx-%{ver2}/wx/datetime.h
%{_includedir}/wx-%{ver2}/wx/datstrm.h
%{_includedir}/wx-%{ver2}/wx/dde.h
%{_includedir}/wx-%{ver2}/wx/debug.h
%{_includedir}/wx-%{ver2}/wx/defs.h
%{_includedir}/wx-%{ver2}/wx/dir.h
%{_includedir}/wx-%{ver2}/wx/dlimpexp.h
%{_includedir}/wx-%{ver2}/wx/dynarray.h
%{_includedir}/wx-%{ver2}/wx/dynlib.h
%{_includedir}/wx-%{ver2}/wx/dynload.h
%{_includedir}/wx-%{ver2}/wx/encconv.h
%{_includedir}/wx-%{ver2}/wx/event.h
%{_includedir}/wx-%{ver2}/wx/except.h
%{_includedir}/wx-%{ver2}/wx/features.h
%{_includedir}/wx-%{ver2}/wx/ffile.h
%{_includedir}/wx-%{ver2}/wx/file.h
%{_includedir}/wx-%{ver2}/wx/fileconf.h
%{_includedir}/wx-%{ver2}/wx/filefn.h
%{_includedir}/wx-%{ver2}/wx/filename.h
%{_includedir}/wx-%{ver2}/wx/filesys.h
%{_includedir}/wx-%{ver2}/wx/fontenc.h
%{_includedir}/wx-%{ver2}/wx/fontmap.h
%{_includedir}/wx-%{ver2}/wx/fs_mem.h
%{_includedir}/wx-%{ver2}/wx/fs_zip.h
%{_includedir}/wx-%{ver2}/wx/hash.h
%{_includedir}/wx-%{ver2}/wx/hashmap.h
%{_includedir}/wx-%{ver2}/wx/hashset.h
%{_includedir}/wx-%{ver2}/wx/html/forcelnk.h
%{_includedir}/wx-%{ver2}/wx/iconloc.h
%{_includedir}/wx-%{ver2}/wx/init.h
%{_includedir}/wx-%{ver2}/wx/intl.h
%{_includedir}/wx-%{ver2}/wx/iosfwrap.h
%{_includedir}/wx-%{ver2}/wx/ioswrap.h
%{_includedir}/wx-%{ver2}/wx/ipc.h
%{_includedir}/wx-%{ver2}/wx/ipcbase.h
%{_includedir}/wx-%{ver2}/wx/isql.h
%{_includedir}/wx-%{ver2}/wx/isqlext.h
%{_includedir}/wx-%{ver2}/wx/list.h
%{_includedir}/wx-%{ver2}/wx/listimpl.cpp
%{_includedir}/wx-%{ver2}/wx/log.h
%{_includedir}/wx-%{ver2}/wx/longlong.h
%{_includedir}/wx-%{ver2}/wx/math.h
%{_includedir}/wx-%{ver2}/wx/memconf.h
%{_includedir}/wx-%{ver2}/wx/memory.h
%{_includedir}/wx-%{ver2}/wx/memtext.h
%{_includedir}/wx-%{ver2}/wx/mimetype.h
%{_includedir}/wx-%{ver2}/wx/module.h
%{_includedir}/wx-%{ver2}/wx/msgout.h
%{_includedir}/wx-%{ver2}/wx/mstream.h
%{_includedir}/wx-%{ver2}/wx/object.h
%{_includedir}/wx-%{ver2}/wx/platform.h
%{_includedir}/wx-%{ver2}/wx/process.h
%{_includedir}/wx-%{ver2}/wx/ptr_scpd.h
%{_includedir}/wx-%{ver2}/wx/regex.h
%{_includedir}/wx-%{ver2}/wx/scopeguard.h
%{_includedir}/wx-%{ver2}/wx/snglinst.h
%{_includedir}/wx-%{ver2}/wx/sstream.h
%{_includedir}/wx-%{ver2}/wx/stack.h
%{_includedir}/wx-%{ver2}/wx/stackwalk.h
%{_includedir}/wx-%{ver2}/wx/stdpaths.h
%{_includedir}/wx-%{ver2}/wx/stockitem.h
%{_includedir}/wx-%{ver2}/wx/stopwatch.h
%{_includedir}/wx-%{ver2}/wx/strconv.h
%{_includedir}/wx-%{ver2}/wx/stream.h
%{_includedir}/wx-%{ver2}/wx/string.h
%{_includedir}/wx-%{ver2}/wx/sysopt.h
%{_includedir}/wx-%{ver2}/wx/textbuf.h
%{_includedir}/wx-%{ver2}/wx/textfile.h
%{_includedir}/wx-%{ver2}/wx/thread.h
%{_includedir}/wx-%{ver2}/wx/thrimpl.cpp
%{_includedir}/wx-%{ver2}/wx/timer.h
%{_includedir}/wx-%{ver2}/wx/tokenzr.h
%{_includedir}/wx-%{ver2}/wx/txtstrm.h
%{_includedir}/wx-%{ver2}/wx/types.h
%{_includedir}/wx-%{ver2}/wx/uri.h
%{_includedir}/wx-%{ver2}/wx/utils.h
%{_includedir}/wx-%{ver2}/wx/variant.h
%{_includedir}/wx-%{ver2}/wx/vector.h
%{_includedir}/wx-%{ver2}/wx/version.h
%{_includedir}/wx-%{ver2}/wx/volume.h
%{_includedir}/wx-%{ver2}/wx/wfstream.h
%{_includedir}/wx-%{ver2}/wx/wx.h
%{_includedir}/wx-%{ver2}/wx/wxchar.h
%{_includedir}/wx-%{ver2}/wx/wxprec.h
%{_includedir}/wx-%{ver2}/wx/xti.h
%{_includedir}/wx-%{ver2}/wx/xtistrm.h
%{_includedir}/wx-%{ver2}/wx/zipstrm.h
%{_includedir}/wx-%{ver2}/wx/zstream.h
%{_includedir}/wx-%{ver2}/wx/fs_inet.h
%{_includedir}/wx-%{ver2}/wx/gsocket.h
%{_includedir}/wx-%{ver2}/wx/protocol/file.h
%{_includedir}/wx-%{ver2}/wx/protocol/ftp.h
%{_includedir}/wx-%{ver2}/wx/protocol/http.h
%{_includedir}/wx-%{ver2}/wx/protocol/protocol.h
%{_includedir}/wx-%{ver2}/wx/sckaddr.h
%{_includedir}/wx-%{ver2}/wx/sckipc.h
%{_includedir}/wx-%{ver2}/wx/sckstrm.h
%{_includedir}/wx-%{ver2}/wx/socket.h
%{_includedir}/wx-%{ver2}/wx/url.h
%{_includedir}/wx-%{ver2}/wx/xml/xml.h
%{_includedir}/wx-%{ver2}/wx/xtixml.h
%{_includedir}/wx-%{ver2}/wx/db.h
%{_includedir}/wx-%{ver2}/wx/dbkeyg.h
%{_includedir}/wx-%{ver2}/wx/dbtable.h
%{_includedir}/wx-%{ver2}/wx/unix/apptbase.h
%{_includedir}/wx-%{ver2}/wx/unix/apptrait.h
%{_includedir}/wx-%{ver2}/wx/unix/execute.h
%{_includedir}/wx-%{ver2}/wx/unix/gsockunx.h
%{_includedir}/wx-%{ver2}/wx/unix/mimetype.h
%{_includedir}/wx-%{ver2}/wx/unix/pipe.h
%{_includedir}/wx-%{ver2}/wx/unix/stackwalk.h
%{_includedir}/wx-%{ver2}/wx/unix/stdpaths.h
EOF
# --- wxBase headers list ends here ---

# temporarily remove base headers
mkdir $RPM_BUILD_ROOT/_save_dir
cp -r $RPM_BUILD_ROOT%{_includedir}/wx-%{ver2} $RPM_BUILD_ROOT/_save_dir
for f in `cat wxbase-headers.files` ; do
    rm -f $RPM_BUILD_ROOT%{_includedir}/wx-%{ver2}/$f
done
# list of all core headers:
find $RPM_BUILD_ROOT%{_includedir}/wx-%{ver2} -type f | sed -e "s,$RPM_BUILD_ROOT,,g" >core-headers.files
# move base headers (actually all headers) back again
cp -f -r $RPM_BUILD_ROOT/_save_dir/* $RPM_BUILD_ROOT%{_includedir}
rm -rf $RPM_BUILD_ROOT/_save_dir

# contrib stuff:
(cd obj-shared/contrib/src; make DESTDIR=$RPM_BUILD_ROOT install)
(cd obj-shared/utils/wxrc; make DESTDIR=$RPM_BUILD_ROOT install)

magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post
/usr/sbin/ldconfig

%postun
/usr/sbin/ldconfig

%post devel
# link wx-config when you install RPM.
%if %{unicode}
    ln -sf %{_libdir}/wx/config/%{wxconfig} %{_bindir}/wx-config
%endif
# link wx-config with explicit name.
ln -sf %{_libdir}/wx/config/%{wxconfig} %{_bindir}/%{wxconfiglink}
/usr/sbin/ldconfig

%postun devel
/usr/sbin/ldconfig

%preun devel
%if %{unicode}
    rm -f %{_bindir}/wx-config
%endif
rm -f %{_bindir}/%{wxconfiglink}

%post -n %{wxbasename}
/usr/sbin/ldconfig

%postun -n %{wxbasename}
/usr/sbin/ldconfig

%post -n %{wxbasename}-devel
# link wx-config with explicit name.
ln -sf %{_libdir}/wx/config/%{wxbaseconfig} %{_bindir}/%{wxbaseconfiglink}
/usr/sbin/ldconfig

%postun  -n %{wxbasename}-devel
/usr/sbin/ldconfig

%preun  -n %{wxbasename}-devel
rm -f %{_bindir}/%{wxbaseconfiglink}

%post gl
/usr/sbin/ldconfig

%postun gl
/usr/sbin/ldconfig

%post contrib
/usr/sbin/ldconfig

%postun contrib
/usr/sbin/ldconfig

%post contrib-devel
/usr/sbin/ldconfig

%postun contrib-devel
/usr/sbin/ldconfig

%files
%defattr(-,root,root)
%doc *.txt
%{_libdir}/libwx_%{buildname}_adv-%{ver2}.so.*
%{_libdir}/libwx_%{buildname}_core-%{ver2}.so.*
%if !%{unicode}
    %{_libdir}/libwx_%{buildname}_dbgrid-%{ver2}.so.*
%endif
%{_libdir}/libwx_%{buildname}_html-%{ver2}.so.*
%{_libdir}/libwx_%{buildname}_aui-%{ver2}.so.*
%{_libdir}/libwx_%{buildname}_qa-%{ver2}.so.*
%{_libdir}/libwx_%{buildname}_xrc-%{ver2}.so.*
%{_libdir}/libwx_%{buildname}_richtext-%{ver2}.so.*
%files -n wx-i18n
%defattr(-,root,root)
%{_datadir}/locale/*/*

%files devel -f core-headers.files
%defattr(-,root,root)
# shared libs
%{_libdir}/libwx_%{buildname}_adv-%{ver2}.so
%{_libdir}/libwx_%{buildname}_core-%{ver2}.so
%if !%{unicode}
    %{_libdir}/libwx_%{buildname}_dbgrid-%{ver2}.so
%endif
%{_libdir}/libwx_%{buildname}_gl-%{ver2}.so
%{_libdir}/libwx_%{buildname}_html-%{ver2}.so
%{_libdir}/libwx_%{buildname}_aui-%{ver2}.so
%{_libdir}/libwx_%{buildname}_qa-%{ver2}.so
%{_libdir}/libwx_%{buildname}_xrc-%{ver2}.so
%{_libdir}/libwx_%{buildname}_richtext-%{ver2}.so
# static libs
%{_libdir}/libwx_%{buildname}_adv-%{ver2}.a
%{_libdir}/libwx_%{buildname}_core-%{ver2}.a
%if !%{unicode}
    %{_libdir}/libwx_%{buildname}_dbgrid-%{ver2}.a
%endif
%{_libdir}/libwx_%{buildname}_gl-%{ver2}.a
%{_libdir}/libwx_%{buildname}_html-%{ver2}.a
%{_libdir}/libwx_%{buildname}_aui-%{ver2}.a
%{_libdir}/libwx_%{buildname}_qa-%{ver2}.a
%{_libdir}/libwx_%{buildname}_xrc-%{ver2}.a
%{_libdir}/libwx_%{buildname}_richtext-%{ver2}.a
%dir %{_libdir}/wx
%{_libdir}/wx/config/%{wxconfig}
%{_libdir}/wx/include/%{wxconfig}/wx/setup.h
%{_libdir}/wx/config/%{wxconfigstatic}
%{_libdir}/wx/include/%{wxconfigstatic}/wx/setup.h
%{_bindir}/wxrc*
%{_bindir}/wx-config
%{_datadir}/bakefile/*

%files -n %{wxbasename}
%defattr(-,root,root)
%{_libdir}/libwx_base*-%{ver2}.so.*

%files -n %{wxbasename}-devel -f wxbase-headers.paths
%defattr (-,root,root)
%dir %{_includedir}/wx-%{ver2}
%{_libdir}/libwx_base*-%{ver2}.so
%{_libdir}/libwx_base*-%{ver2}.a
%if %{unicode}
    %{_libdir}/libwxregexu-%{ver2}.a
%endif
%dir %{_libdir}/wx
%{_libdir}/wx/config/%{wxbaseconfig}
%{_libdir}/wx/include/%{wxbaseconfig}/wx/setup.h
%{_libdir}/wx/config/%{wxbaseconfigstatic}
%{_libdir}/wx/include/%{wxbaseconfigstatic}/wx/setup.h
%{_datadir}/aclocal/*.m4

%files gl
%defattr(-,root,root)
%{_libdir}/libwx_%{buildname}_gl-%{ver2}.so.*

%files contrib
%defattr(-,root,root)
#%{_libdir}/libwx_%{buildname}_animate-%{ver2}.so.*
#%{_libdir}/libwx_%{buildname}_deprecated-%{ver2}.so.*
%{_libdir}/libwx_%{buildname}_fl-%{ver2}.so.*
%{_libdir}/libwx_%{buildname}_gizmos-%{ver2}.so.*
%{_libdir}/libwx_%{buildname}_gizmos_xrc-%{ver2}.so.*
#%{_libdir}/libwx_%{buildname}_mmedia-%{ver2}.so.*
%{_libdir}/libwx_%{buildname}_ogl-%{ver2}.so.*
%{_libdir}/libwx_%{buildname}_plot-%{ver2}.so.*
%{_libdir}/libwx_%{buildname}_stc-%{ver2}.so.*
%{_libdir}/libwx_%{buildname}_svg-%{ver2}.so.*

%files contrib-devel
%defattr(-,root,root)
#%dir %{_includedir}/wx-%{ver2}/wx/animate
#%{_includedir}/wx-%{ver2}/wx/animate/*
#%{_libdir}/libwx_%{buildname}_animate-%{ver2}.so

#%dir %{_includedir}/wx-%{ver2}/wx/deprecated
#%{_includedir}/wx-%{ver2}/wx/deprecated/*
#%{_libdir}/libwx_%{buildname}_deprecated-%{ver2}.so

%dir %{_includedir}/wx-%{ver2}/wx/fl
%{_includedir}/wx-%{ver2}/wx/fl/*
%{_libdir}/libwx_%{buildname}_fl-%{ver2}.so

%dir %{_includedir}/wx-%{ver2}/wx/gizmos
%{_includedir}/wx-%{ver2}/wx/gizmos/*
%{_libdir}/libwx_%{buildname}_gizmos-%{ver2}.so
%{_libdir}/libwx_%{buildname}_gizmos_xrc-%{ver2}.so

%if 0
%dir %{_includedir}/wx-%{ver2}/wx/mmedia
%{_includedir}/wx-%{ver2}/wx/mmedia/*
%{_libdir}/libwx_%{buildname}_mmedia-%{ver2}.so
%endif

%dir %{_includedir}/wx-%{ver2}/wx/ogl
%{_includedir}/wx-%{ver2}/wx/ogl/*
%{_libdir}/libwx_%{buildname}_ogl-%{ver2}.so

%dir %{_includedir}/wx-%{ver2}/wx/plot
%{_includedir}/wx-%{ver2}/wx/plot/*
%{_libdir}/libwx_%{buildname}_plot-%{ver2}.so

%dir %{_includedir}/wx-%{ver2}/wx/stc
%{_includedir}/wx-%{ver2}/wx/stc/*
%{_libdir}/libwx_%{buildname}_stc-%{ver2}.so

%dir %{_includedir}/wx-%{ver2}/wx/svg
%{_includedir}/wx-%{ver2}/wx/svg/*
%{_libdir}/libwx_%{buildname}_svg-%{ver2}.so

%changelog 
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 2.8.12-3.1
- 为 Magic 3.0 重建

* Wed Sep 23 2008 Liu Di <liudidi@gmail.com> - 2.8.9-1mgc
- 更新到 2.8.9

* Fri Nov 09 2007 Liu Di <liudidi@gmail.com> - 2.8.6-1mgc
- update to 2.8.6

* Tue Aug 21 2007 Liu Di <liudidi@gmail.com> - 2.8.4-1mgc
- update to 2.8.4

* Mon Jan 29 2007 Liu Di <liudidi@gmail.com> - 2.8.0-1mgc
- update to 2.8.0
