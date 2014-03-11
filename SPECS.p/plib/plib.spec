Name: plib
Version: 1.8.5
Release: 3%{?dist}
Summary: A Suite of Portable Game Libraries
Summary(zh_CN.UTF-8): 一套可移植游戏库
License: GPL
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
URL: http://plib.sourceforge.net
Source: http://plib.sourceforge.net/dist/%{name}-%{version}.tar.gz
# what provides libgl* currently? mesa
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

%prep
%setup -q

%build
export CFLAGS="%{optflags}"
%configure \
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

%install
# %%makeinstall overrides directory locations we provide in %%configure,
# like --includedir. It's evil.
make DESTDIR=%{buildroot} install



%clean
#rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files
%defattr(0644,root,root,0755)
%doc NEWS README COPYING AUTHORS
%doc ChangeLog TODO* README.*
%{_includedir}
%{_libdir}


%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 1.8.5-3
- 为 Magic 3.0 重建

* Thu Jan 26 2012 Liu Di <liudidi@gmail.com> - 1.8.5-2
- 为 Magic 3.0 重建

* Tue Jul 10 2007 kde <athena_star {at} 163 {dot} com> -  1.8.4-2mgc
- simplify and standardize the spec file for magic linux

* Mon Feb 7 2005 kde <jack@linux.net.cn>
- modify the spec file and rebuild
