# Patented subpixel rendering disabled by default.
# Pass '--with subpixel_rendering' on rpmbuild command-line to enable.
%{!?_with_subpixel_rendering: %{!?_without_subpixel_rendering: %define _without_subpixel_rendering --without-subpixel_rendering}}
%define _with_subpixel_rendering 1
%{!?with_xfree86:%define with_xfree86 1}

Summary: A free and portable font rendering engine
Summary(zh_CN.UTF-8): 自由的可移植的 TrueType 字体绘制引擎。
Name: freetype
Version:	2.6.1
Release: 4%{?dist}
License: FTL or GPLv2+
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL: http://www.freetype.org
Source:  http://download.savannah.gnu.org/releases/freetype/freetype-%{version}.tar.bz2
Source1: http://download.savannah.gnu.org/releases/freetype/freetype-doc-%{version}.tar.bz2
Source2: http://download.savannah.gnu.org/releases/freetype/ft2demos-%{version}.tar.bz2
Source3: ftconfig.h

Patch21:  freetype-2.3.0-enable-spr.patch

# Enable otvalid and gxvalid modules
Patch46:  freetype-2.2.1-enable-valid.patch
# Enable additional demos
Patch47:  freetype-2.5.2-more-demos.patch

# Fix multilib conflicts
Patch88:  freetype-multilib.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1161963
Patch92:  freetype-2.5.3-freetype-config-prefix.patch

Buildroot: %{_tmppath}/%{name}-%{version}-root-%(%{__id_u} -n)

BuildRequires: libX11-devel

Provides: %{name}-bytecode
%if %{?_with_subpixel_rendering:1}%{!?_with_subpixel_rendering:0}
Provides: %{name}-subpixel
%endif

%description
The FreeType engine is a free and portable font rendering
engine, developed to provide advanced font support for a variety of
platforms and environments. FreeType is a library which can open and
manages font files as well as efficiently load, hint and render
individual glyphs. FreeType is not a font server or a complete
text-rendering library.

%description -l zh_CN.UTF-8
FreeType 引擎是一个免费的可移植的 TrueType 字体绘制引擎。它被开发来为
各类平台和环境提供 TrueType 字体支持。FreeType 是一个能够打开并管理字
体文件的库，它还能有效地载入、提示并绘制单独 glyphs。FreeType 不是一
个字体服务器或一个完整的文字绘制库

%package demos
Summary: A collection of FreeType demos
Summary(zh_CN.UTF-8): FreeType 演示集合
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Requires: %{name} = %{version}-%{release}

%description demos
The FreeType engine is a free and portable font rendering
engine, developed to provide advanced font support for a variety of
platforms and environments.  The demos package includes a set of useful
small utilities showing various capabilities of the FreeType library.

%description demos -l zh_CN.UTF-8
FreeType 引擎是一个免费的可移植的TrueType字体绘制引擎。它被开发来为
多种平台和环境提供TrueType字体支持。FreeType 是一个能够打开和管理字
体的库，它还能够有效地载入、提示和绘制单个的 glyph。 FreeType 不是
一个字体服务器或一个完整的文本绘制库。

%package devel
Summary: FreeType development libraries and header files
Summary(zh_CN.UTF-8): 用于 FreeType 开发的头文件和静态库
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}
Requires: zlib-devel
Requires: pkgconfig

%description devel
The freetype-devel package includes the static libraries and header files
for the FreeType font rendering engine.

Install freetype-devel if you want to develop programs which will use
FreeType.

%description devel -l zh_CN.UTF-8
freetype-devel 软件包包括开发或编译要使用 FreeType TrueType 字体绘制
库所需的头文件和静态库。
如果您想开发 FreeType 程序，请安装freetype-devel 软件包。如果您只想运
行现存的程序，则不需要这个软件包。

%package static
Summary: FreeType development libraries and header files
Summary(zh_CN.UTF-8): 用于 FreeType 开发的静态库
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}
Requires: %{name}-devel = %{version}-%{release}
Requires: zlib-devel
Requires: pkgconfig

%description static
The freetype-static package includes the static libraries and header files
for the FreeType font rendering engine.

Install freetype-satic if you want to develop programs which will use
FreeType.

%description static -l zh_CN.UTF-8
freetype-static 软件包包括开发或编译要使用 FreeType TrueType 字体绘制
库所需的静态库。
如果您想开发静态链接到 FreeType 程序，请安装freetype-devel 软件包。如
果您只想运行现存的程序，则不需要这个软件包。

%prep
%setup -q -b 1 -a 2

%if %{?_with_subpixel_rendering:1}%{!?_with_subpixel_rendering:0}
%patch21  -p1 -b .enable-spr
%endif

%patch46  -p1 -b .enable-valid

pushd ft2demos-%{version}
%patch47  -p1 -b .more-demos
popd

%patch88 -p1 -b .multilib

%patch92 -p1 -b .pkgconfig

%build

%configure --enable-static \
           --with-zlib=yes \
           --with-bzip2=yes \
           --with-png=yes \
           --with-harfbuzz=no
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' builds/unix/libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' builds/unix/libtool
make %{?_smp_mflags}

%if %{with_xfree86}
# Build demos
pushd ft2demos-%{version}
make TOP_DIR=".."
popd
%endif

# Convert FTL.txt and example3.cpp to UTF-8
pushd docs
iconv -f latin1 -t utf-8 < FTL.TXT > FTL.TXT.tmp && \
touch -r FTL.TXT FTL.TXT.tmp && \
mv FTL.TXT.tmp FTL.TXT

iconv -f iso-8859-1 -t utf-8 < "tutorial/example3.cpp" > "tutorial/example3.cpp.utf8"
touch -r tutorial/example3.cpp tutorial/example3.cpp.utf8 && \
mv tutorial/example3.cpp.utf8 tutorial/example3.cpp
popd

%install
rm -rf $RPM_BUILD_ROOT


%makeinstall gnulocaledir=$RPM_BUILD_ROOT%{_datadir}/locale

{
  for ftdemo in ftbench ftchkwd ftmemchk ftpatchk fttimer ftdump ftlint ftmemchk ftvalid ; do
      builds/unix/libtool --mode=install install -m 755 ft2demos-%{version}/bin/$ftdemo $RPM_BUILD_ROOT/%{_bindir}
  done
}
%if %{with_xfree86}
{
  for ftdemo in ftdiff ftgamma ftgrid ftmulti ftstring fttimer ftview ; do
      builds/unix/libtool --mode=install install -m 755 ft2demos-%{version}/bin/$ftdemo $RPM_BUILD_ROOT/%{_bindir}
  done
}
%endif

# fix multilib issues
%ifarch x86_64 s390x ia64 ppc64 ppc64le alpha sparc64 aarch64 mips64el
%define wordsize 64
%else
%define wordsize 32
%endif

mv $RPM_BUILD_ROOT%{_includedir}/freetype2/freetype/config/ftconfig.h \
   $RPM_BUILD_ROOT%{_includedir}/freetype2/freetype/config/ftconfig-%{wordsize}.h
install -p -m 644 %{SOURCE3} $RPM_BUILD_ROOT%{_includedir}/freetype2/freetype/config/ftconfig.h

# Don't package static .la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%triggerpostun -- freetype < 2.0.5-3
{
  # ttmkfdir updated - as of 2.0.5-3, on upgrades we need xfs to regenerate
  # things to get the iso10646-1 encoding listed.
  for I in %{_datadir}/fonts/*/TrueType /usr/share/X11/fonts/TTF; do
      [ -d $I ] && [ -f $I/fonts.scale ] && [ -f $I/fonts.dir ] && touch $I/fonts.scale
  done
  exit 0
}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/libfreetype.so.*
%doc README
%doc docs/LICENSE.TXT docs/FTL.TXT docs/GPLv2.TXT
%doc docs/CHANGES docs/VERSION.DLL docs/formats.txt docs/ft2faq.html

%files demos
%defattr(-,root,root)
%{_bindir}/ftbench
%{_bindir}/ftchkwd
%{_bindir}/ftpatchk
%{_bindir}/fttimer
%{_bindir}/ftdump
%{_bindir}/ftlint
%{_bindir}/ftmemchk
%{_bindir}/ftvalid
%if %{with_xfree86}
%{_bindir}/ftdiff
%{_bindir}/ftgamma
%{_bindir}/ftgrid
%{_bindir}/ftmulti
%{_bindir}/ftstring
%{_bindir}/ftview
%endif
%doc ChangeLog README

%files devel
%defattr(-,root,root)
%dir %{_includedir}/freetype2
%{_datadir}/aclocal/freetype2.m4
%{_includedir}/freetype2/*
#%{_includedir}/*.h
%{_libdir}/libfreetype.so
%{_bindir}/freetype-config
%{_libdir}/pkgconfig/freetype2.pc
%{_mandir}/man1/freetype-config.1*
%doc docs/design
%doc docs/glyphs
%doc docs/reference
%doc docs/tutorial

%files static
%defattr(-,root,root)
%{_libdir}/libfreetype.a

%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 2.6.1-4
- 为 Magic 3.0 重建

* Thu Oct 29 2015 Liu Di <liudidi@gmail.com> - 2.6.1-3
- 更新到 2.6.1

* Tue Jun 24 2014 Liu Di <liudidi@gmail.com> - 2.5.3-2
- 为 Magic 3.0 重建

* Fri Apr 04 2014 Liu Di <liudidi@gmail.com> - 2.5.3-1
- 更新到 2.5.3

* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 2.4.8-3
- 为 Magic 3.0 重建

* Fri Nov 25 2011 Liu Di <liudidi@gmail.com> - 2.4.8-2
- 为 Magic 3.0 重建

* Thu Feb 12 2009 Liu Di <liudidi@gmail.com> - 2.3.8-1
- 更新到 2.3.8

* Thu Sep 04 2008 Liu Di <liudidi@gmail.com> - 2.3.7-1mgc
- 更新到 2.3.7

* Fri Oct 12 2006 Liu Di <Liudidi@gmail.com> - 2.2.1-3mgc
- update to 2.2.1

* Mon May 1 2006 KanKer <kanker@163.com>
- update 20060501cvs

* Sun Apr 23 2006 KanKer <kanker@163.com>
- add a patch to reduce embolden distance

* Sun Dec 4 2005 KanKer <kanker@163.com>
- update 20051204cvs

* Sat Dec 3 2005 KanKer <kanker@163.com>
- rebuild on new libXft

* Sat Oct 15 2005 KanKer <kanker@163.com>
- update freetype-2.1.10-cvsfixes.patch

* Mon Sep 26 2005 KanKer <kanker@163.com>
- add some patches from mandriva

* Mon Jun 13 2005 KanKer <kanker@163.com>
- update 2.1.10

* Thu May 31 2005 KanKer <kanker@163.com>
- update 2.1.9
