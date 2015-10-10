%{!?python_sitelib:%global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch:%global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%define ENABLE_TESTS -DENABLE_TESTS:BOOL=ON

%define main_ver 1_1

Name:           avogadro
Version:	1.1.1
Release:        6%{?dist}
Summary:        An advanced molecular editor for chemical purposes
Summary(zh_CN.UTF-8): 化学用途的高级分子编辑器

Group:          Applications/Editors
Group(zh_CN.UTF-8): 应用程序/编辑器
License:        GPLv2
URL:            http://avogadro.openmolecules.net/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2

## upstreamable patches
# Fix qmake mkspecs installation directory
Patch0:         avogadro-1.1.1-mkspecs-dir.patch
# Remove -Wl,-s from the compiler flags, fixes -debuginfo (#700080)
Patch1:         avogadro-1.1.1-no-strip.patch
# avogadro.pc missing eigen dependency
Patch2:         avogadro-1.1.1-pkgconfig_eigen.patch

## upstream fixes
# fix FTBFS on arm
Patch3:         0029-Fix-compilation-on-ARM-where-qreal-can-be-defined-as.patch

## upstreamable
# fix build with cmake-3.2+
# https://sourceforge.net/p/avogadro/bugs/746/
Patch10:        avogadro-cmake-3.2.patch

# fix Eigen3 support, from OpenMandriva (Bernhard Rosenkränzer, Crispin Boylan)
# disables Eigen2 support, so probably not upstreamable as is
Patch11:        avogadro-1.1.1-eigen3.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  cmake >= 2.6.0
BuildRequires:  qt4-devel >= 4.5.1
BuildRequires:  eigen3-devel >= 3.2.1
BuildRequires:  openbabel-devel >= 2.2.2
BuildRequires:  boost-devel >= 1.35
BuildRequires:  glew-devel >= 1.5.0
BuildRequires:  desktop-file-utils
BuildRequires:  docbook-utils
BuildRequires:  sip-devel
BuildRequires:  numpy >= 1.4.0

Requires: %{name}-libs = %{version}-%{release}

%description
An advanced molecular editor designed for 
cross-platform use in computational chemistry,
molecular modeling, bioinformatics, materials science,
and related areas, which offers flexible rendering and
a powerful plugin architecture.

%description -l zh_CN.UTF-8
跨平台高级分子编辑器，主要用于计算化学、分子建模、生物信息、
材料科学和相关领域，提供了可塑的渲染和强大的插件架构。

%package libs
Summary:        Shared libraries for Avogadro
Summary(zh_CN.UTF-8): Avogadro 的共享库
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%description libs
This package contains the shared libraries for the
molecular editor Avogadro.

%description libs -l zh_CN.UTF-8
本软件包包含了分子编辑器 Avogadro 的共享库。

%package devel
Summary:        Development files for Avogadro
Summary(zh_CN.UTF-8): Avogadro 的开发文件
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name}-libs = %{version}-%{release} 
Requires:       qt4-devel

%description devel
This package contains files to develop applications using 
Avogadros libraries.

%description devel -l zh_CN.UTF-8
本软件包包含了使用 Avogadro 库开发应用程序所需的文件。

%prep
%setup -q
%patch0 -p1 -b .mkspecs-dir
%patch1 -p1 -b .no-strip
%patch2 -p1 -b .pkgconfig_eigen
%patch3 -p1 -b .qreal
%patch10 -p1 -b .cmake_x11
%patch11 -p1 -b .eigen3

%build
# do not use macro cmake here for lib-install-dir problem in cmake file --- nihui
mkdir build
cd build
CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS ;
CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS ;
FFLAGS="${FFLAGS:-%optflags}" ; export FFLAGS ;
%cmake \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DBUILD_SHARED_LIBS:BOOL=ON \
    %{?ENABLE_TESTS} \
    -DENABLE_GLSL:BOOL=ON \
    -DENABLE_PYTHON:BOOL=ON \
    ..

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
cd build
make install/fast DESTDIR=%{buildroot}
mkdir -p %{buildroot}%{_qt4_prefix}/mkspecs
#mv %{buildroot}/usr/features %{buildroot}%{_qt4_prefix}/mkspecs/

for i in af ar bg ca cs da de el en_CA en_GB es fi fr he hr hu id it kn nb nl oc pl pt pt_BR ru sk sv tr uk; do
    rm -fv %{buildroot}%{_datadir}/avogadro/i18n/avogadro_$i.qm;
done
for i in ar bg ca cs da de el en_CA en_GB es fi fr he hi hu id it kn nb nl oc pl pt pt_BR ru sk sv tr uk; do
    rm -fv %{buildroot}%{_datadir}/avogadro/i18n/libavogadro_$i.qm;
done


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/avogadro.desktop
# all of these currently require an active X session, so will fail
# in mock
cd build
%{?ENABLE_TESTS:make test ||:}

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING
%{_bindir}/avogadro
%{_bindir}/avopkg
# TODO: %lang'ify stuff under %%{_datadir}/avogadro/i18n/
%{_datadir}/avogadro/
%{_datadir}/pixmaps/avogadro-icon.png
%{_datadir}/applications/avogadro.desktop
%{_mandir}/man1/avogadro.1*
%{_mandir}/man1/avopkg.1*

%{python_sitearch}/*

%files devel
%defattr(-,root,root,-)
%{_includedir}/avogadro/
%{_libdir}/libavogadro.so
%{_libdir}/avogadro/*.cmake
%{_libdir}/avogadro/%{main_ver}/*.cmake
# these look like dups of system copies?, take a closer look and/or ask upstream -- Rex
%{_libdir}/avogadro/%{main_ver}/cmake/
%{_qt4_prefix}/mkspecs/features/avogadro.prf
%{_libdir}/libavogadro_OpenQube.so
%{_libdir}/pkgconfig/avogadro.pc

%files libs
%defattr(-,root,root,-)
#%{python_sitelib}/Avogadro.so
%{_datadir}/libavogadro/
%{_libdir}/libavogadro.so.1*
%{_libdir}/libavogadro_OpenQube.so.*
#python,应该单独分包
#%{python_sitearch}/Avogadro.so
%dir %{_libdir}/avogadro/
%dir %{_libdir}/avogadro/%{main_ver}/
%{_libdir}/avogadro/%{main_ver}/colors/
%{_libdir}/avogadro/%{main_ver}/extensions/
%{_libdir}/avogadro/%{main_ver}/engines/
%{_libdir}/avogadro/%{main_ver}/tools/

%changelog
* Sat Oct 10 2015 Liu Di <liudidi@gmail.com> - 1.1.1-6
- 为 Magic 3.0 重建

* Fri Dec 26 2014 Liu Di <liudidi@gmail.com> - 1.1.1-5
- 为 Magic 3.0 重建

* Tue May 27 2014 Liu Di <liudidi@gmail.com> - 1.1.1-4
- 为 Magic 3.0 重建

* Tue May 27 2014 Liu Di <liudidi@gmail.com> - 1.1.1-3
- 为 glew 1.10 重编译

* Sun Mar 02 2014 Liu Di <liudidi@gmail.com> - 1.1.1-2
- 更新到 1.1.1

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 1.0.3-2
- 为 Magic 3.0 重建

* Wed Nov 02 2011 Liu Di <liudidi@gmail.com> - 1.0.3-1
- 更新到 1.0.3
