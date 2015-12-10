Name: plib
Version: 1.8.5
Release: 9%{?dist}
Summary: A Suite of Portable Game Libraries
Summary(zh_CN.UTF-8): 一套可移植游戏库
License: GPL
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
URL: http://plib.sourceforge.net
Source: http://plib.sourceforge.net/dist/%{name}-%{version}.tar.gz
# what provides libgl* currently? mesa
Patch1:         plib-1.8.4-fullscreen.patch
Patch3:         plib-1.8.4-autorepeat.patch
Patch4:         plib-1.8.5-CVE-2011-4620.patch
Patch5:         plib-1.8.5-CVE-2012-4552.patch
BuildRequires: mesa-libGL-devel, mesa-libGLU-devel
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: binutils
#BuildRequires: g++
BuildRequires: gcc
BuildRequires: glibc-devel
BuildRequires: libstdc++-devel
BuildRequires: freeglut-devel
BuildRequires: libtool
BuildRequires: make
Requires: freeglut, mesa-libGL, mesa-libGLU
Provides: plib-devel plib-devel-static
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)

%description
PLIB includes sound effects, music, a complete 3D engine, font rendering,
a GUI, networking, 3D math library and a collection of handy utility functions.
All are 100% portable across nearly all modern computing platforms. What's
more, it's all available on line - and completely free. 

%description -l zh_CN.UTF-8
PLIB 包括声音效果、音乐、完整的 3D 引擎、字体渲染、图形用户界面 (GUI)、
网络、3D 数学库和一批便利实用的功能。所有这些都是 100% 可移植到几乎
所有现代计算机平台上的。而且它是完全可以在线获取的──并且完全自由。

%package devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}
Requires:       libGL-devel

%description devel
This package contains the header files and libraries needed to write
or compile programs that use plib.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q
%patch1 -p1 -b .fs
%patch3 -p1 -b .autorepeat
%patch4 -p1
%patch5 -p1
# for some reason this file has its x permission sets, which makes rpmlint cry
chmod -x src/sg/sgdIsect.cxx

%build
export CFLAGS="%{optflags}"
%configure CXXFLAGS="$RPM_OPT_FLAGS -fPIC -DXF86VIDMODE" \
	--enable-shared \
	--includedir=%{_includedir}/plib \
	--enable-fnt \
	--enable-js \
	--enable-pw \
	--enable-net \
	--enable-pui \
	--enable-sg \
	--enable-psl \
	--enable-sl \
	--enable-ssg \
	--enable-puaux \
	--enable-ssgaux \
	--enable-ul

make RPM_OPT_FLAGS="%{optflags}"  %{?_smp_mflags}

# and below is a somewhat dirty hack inspired by debian to build shared libs
# instead of static. Notice that the a%description -l zh_CN.UTF-8ing of -fPIC to CXXFLAGS above is part
# of the hack.
dirnames=(util sg ssg fnt js net psl pui puAux pw sl sl ssgAux)
libnames=(ul sg ssg fnt js net psl pu puaux pw sl sm ssgaux)
libdeps=("" \
  "-L../util -lplibul" \
  "-L../util -lplibul -L../sg -lplibsg -lGL" \
  "-L../util -lplibul -L../sg -lplibsg -lGL" \
  "-L../util -lplibul" \
  "-L../util -lplibul" \
  "-L../util -lplibul" \
  "-L../util -lplibul -L../sg -lplibsg -L../fnt -lplibfnt -lGL" \
  "-L../util -lplibul -L../sg -lplibsg -L../fnt -lplibfnt -L../pui -lplibpu -lGL" \
  "-L../util -lplibul -lX11 -lGL -lXxf86vm" \
  "-L../util -lplibul" \
  "-L../util -lplibul" \
  "-L../util -lplibul -L../sg -lplibsg -L../ssg -lplibssg -lGL")

for (( i = 0; i < 13; i++ )) ; do
  pushd src/${dirnames[$i]}
  gcc -shared -Wl,-soname,libplib${libnames[$i]}.so.%{version} \
    -o libplib${libnames[$i]}.so.%{version} `ar t libplib${libnames[$i]}.a` \
    ${libdeps[$i]}
  ln -s libplib${libnames[$i]}.so.%{version} libplib${libnames[$i]}.so
  popd
done

%install
# %%makeinstall overrides directory locations we provide in %%configure,
# like --includedir. It's evil.
make DESTDIR=%{buildroot} install

# we don't want the static libs
rm $RPM_BUILD_ROOT%{_libdir}/*.a
# instead do a DIY install of the shared libs we created
cp -a `find . -name "libplib*.so*"` $RPM_BUILD_ROOT%{_libdir}

%clean
#rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files
%doc AUTHORS COPYING ChangeLog NOTICE README
%{_libdir}/libplib*.so.%{version}

%files devel
%{_includedir}/*
%{_libdir}/libplib*.so

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 1.8.5-9
- 为 Magic 3.0 重建

* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1.8.5-8
- 为 Magic 3.0 重建

* Fri Jul 24 2015 Liu Di <liudidi@gmail.com> - 1.8.5-7
- 为 Magic 3.0 重建

* Fri Jul 24 2015 Liu Di <liudidi@gmail.com> - 1.8.5-6
- 为 Magic 3.0 重建

* Fri Jul 24 2015 Liu Di <liudidi@gmail.com> - 1.8.5-5
- 为 Magic 3.0 重建

* Fri Jul 24 2015 Liu Di <liudidi@gmail.com> - 1.8.5-4
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 1.8.5-3
- 为 Magic 3.0 重建

* Thu Jan 26 2012 Liu Di <liudidi@gmail.com> - 1.8.5-2
- 为 Magic 3.0 重建

* Tue Jul 10 2007 kde <athena_star {at} 163 {dot} com> -  1.8.4-2mgc
- simplify and standardize the spec file for magic linux

* Mon Feb 7 2005 kde <jack@linux.net.cn>
- modify the spec file and rebuild
