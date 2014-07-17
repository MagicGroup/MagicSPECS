%define git 1
%define gitdate 20111209

Name: libkipi
Version: 0.1.6
%if %git
Release: 0.git%{gitdate}%{?dist}
%else
Release: 3%{?dist}
%endif
Summary: Common plugin infrastructure for KDE image applications
Summary(zh_CN.UTF-8): KDE 图像程序的公共插件基础构架
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License: LGPL
URL: http://extragear.kde.org/apps/kipi
%if %git
Source0: %{name}-git%{gitdate}.tar.xz
%else
Source0: %{name}-%{version}.tar.bz2
%endif
Source1: make_libkipi_git_package.sh
Patch1:	libkipi-libtool.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: kdelibs-devel >= 3.0
BuildRequires: gettext, libacl-devel

%description
Kipi (KDE Image Plugin Interface) is an effort to develop a common plugin
structure for Digikam, KimDaBa, Showimg and Gwenview. Its aim is to share
image plugins among graphic applications.

%description -l zh_CN.UTF-8
Kipi (KDE 图像插件接口) 是为 Digikam，KimDaBa，Showimg 和 Gwenview 开发公共插件构架的。其旨在和图像程序之间共享图像插件。

%package devel
Summary: Common plugin infrastructure for KDE image applications
Summary(zh_CN.UTF-8): KDE 图像程序的公共插件基础构架
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}
Requires: kdelibs-devel
Requires: pkgconfig

%description devel
Kipi (KDE Image Plugin Interface) is an effort to develop a common plugin
structure for Digikam, KimDaBa, Showimg and Gwenview. Its aim is to share
image plugins among graphic applications.
This package contains the files needed to build applications with Kipi
support

%description devel -l zh_CN.UTF-8
Kipi (KDE 图像插件接口) 是为 Digikam，KimDaBa，Showimg 和 Gwenview 开发公共插件构架的。其旨在和图像程序之间共享图像插件。
本软件包包含需要 Kipi 支持构建程序用的开发文件

%prep
%if %{git}
%setup -q -n %{name}-git%{gitdate}
%else
%setup -q
%endif
#临时修正
%patch1 -p1

%build
unset QTDIR && . %{_sysconfdir}/profile.d/qt.sh
# work around an improper ${kdelibsuff}
export QTLIB=${QTDIR}/lib QTINC=${QTDIR}/include
%if %git
make -f admin/Makefile.common
%endif
%configure --disable-rpath --disable-debug --enable-final
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} DESTDIR=%{buildroot} install
mv %{buildroot}%{_libdir}/pkgconfig/libkipi.pc %{buildroot}%{_libdir}/pkgconfig/tde-libkipi.pc
magic_rpm_clean.sh
%find_lang %{name}
# 删除包中的 *.la 文件（非开发必需）
find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'

%clean
%{__rm} -rf %{buildroot} %{_builddir}/%{buildsubdir}

%post 
/sbin/ldconfig
touch --no-create %{_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:

%postun
/sbin/ldconfig
touch --no-create %{_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog README TODO
%{_libdir}/*.so.*
%{_datadir}/apps/kipi
%{_datadir}/icons/hicolor/*/apps/kipi.png
%{_datadir}/servicetypes/*.desktop

%files devel
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/libkipi

%changelog
* Fri Dec 09 2011 Liu Di <liudidi@gmail.com> - 0.1.5-3
- 为 Magic 3.0 重建

* Tue Oct 2 2007 Ni Hui <shuizhuyuanluo@126.com> - 0.1.5-0.1mgc
- first spec file and package for MagicLinux-2.1
- update to 0.1.5
