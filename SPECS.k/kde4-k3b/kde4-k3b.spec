# overwrite the default location for installing system-wide configuration
#define kde4_sysconfdir %{_sysconfdir}

%define kde4_enable_final_bool OFF

%define realname k3b
%define testver %{nil}

%define git 1
%define vcsdate 20150330

Summary:        Excellent CD-Burner for KDE4
Summary(zh_CN.UTF-8): KDE4 下优秀的 CD/DVD 刻录程序
Name:           kde4-k3b
Version:        2.0.2
%if 0%{?git}
Release:	10.git%{vcsdate}%{?dist}
%else
Release:        10%{?dist}
%endif
License:        GPL
Vendor:         Magic Linux
URL:            http://www.k3b.org
Group:          Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
%if 0%{?git}
Source0: %{name}-git%{vcsdate}.tar.xz
%else
Source0:  http://ncu.dl.sourceforge.net/sourceforge/k3b/%{realname}-%{version}%{testver}.tar.bz2
%endif

Source1:	make_%{name}_git_package.sh

Patch6:		http://pkgs.fedoraproject.org/cgit/k3b.git/plain/k3b-2.0.2-use_vartmp_instead_of_tmp.patch
Patch7:		http://pkgs.fedoraproject.org/cgit/k3b.git/plain/k3b-2.0.2-no-webkit.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)

Provides:       cd-burner
Requires:       cdrecord >= 2.0, mkisofs >= 2.0, cdrdao >= 1.1, dvd+rw-tools >= 7.0
Requires:       libdvdread, kdelibs4 >= 4.2, flac, ffmpeg, libsndfile
Requires:	libmad, libogg, lame, libmpcdec, taglib

BuildRequires:  polkit-qt-1-devel
BuildRequires:	kdelibs4-devel >= 4.2, qt4-devel, audiofile-devel
BuildRequires:	libdvdread-devel, flac-devel, ffmpeg, libsndfile-devel
BuildRequires:	libmad-devel, libogg-devel, lame-devel, taglib-devel, libmpcdec-devel
BuildRequires:	libart_lgpl-devel, libpng-devel, flac-devel
BuildRequires:	kde4-libkcddb-devel, libmusicbrainz-devel

# Unfortunately the --without-libmad and --without-libvorbis options do not work
# because Sebastian always enables it if it's available.
# ( also the --without-arts parameter seems to be ignored, so actually only
#   --without-k3bsetup does work )
%{!?_without_libmad:Requires: libmad, id3lib}
%{!?_without_libmad:BuildRequires: libmad-devel, id3lib-devel}
%{!?_without_libogg:Requires: libvorbis, libogg}
%{!?_without_libogg:BuildRequires: libvorbis-devel, libogg-devel}


%description
K3b - The CD Creator - Writing cds under linux made easy. It has an extremely
easy to use interface and supports many features: data/audio/video/mixed
[on-the-fly] CD burning, CD copying, erasing and ripping, CD-text writing,
burning iso/bin-cue images and many more.

%description -l zh_CN.UTF-8
K3b - CD/DVD 创建器 - 使得在 linux下写入 CD/DVD 易如反掌。它有一个
非常易用的界面并且支持许多特性：数据/音频/视频/混合 [一次成型] CD/DVD
刻录、复制、擦除、提取、CD-text 写入、刻录 iso/bin-cue 镜像和许多其它特性。

%package devel
Summary: Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发文件
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}

%description devel
Contains the development files.

%description devel -l zh_CN.UTF-8
%{name} 的开发文件。

%prep
%if 0%{?git}
%setup -q -n %{name}-git%{vcsdate}
%else
%setup -q -n %{realname}-%{version}
%endif

%patch6 -p1
%patch7 -p1

rm -rf doc-translations/*

%build
mkdir build
cd build
%cmake_kde4 ..

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
cd build
make install DESTDIR=%{buildroot}

#%move_kde4_polkit_files

magic_rpm_clean.sh

%clean_kde4_desktop_files
%clean_kde4_notifyrc_files

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING
%{_sysconfdir}/dbus-1/system.d/org.kde.k3b.conf
%{_datadir}/dbus-1/system-services/org.kde.k3b.service
%{kde4_datadir}/polkit-1/actions/org.kde.k3b.policy
%{kde4_datadir}/appdata/k3b.appdata.xml
%{kde4_iconsdir}/hicolor/*/mimetypes/application-x-k3b.*
%{kde4_bindir}/*
%{kde4_plugindir}/*
%{kde4_libdir}/*.so.*
%{kde4_appsdir}/k3b
%{kde4_appsdir}/konqsidebartng/virtual_folders/services/videodvd.desktop
%{kde4_appsdir}/solid/actions/k3b_*.desktop
%{kde4_iconsdir}/hicolor/*/apps/k3b*
%{kde4_xdgappsdir}/k3b.desktop
%{kde4_servicesdir}/*
%{kde4_servicetypesdir}/*
#%{kde4_datadir}/sounds/*
%{kde4_datadir}/mime/packages/x-k3b.xml
#%{kde4_localedir}/*
%doc %lang(en) %{kde4_htmldir}/en/k3b

%files devel
%defattr(-,root,root,-)
%{kde4_includedir}/*
%{kde4_libdir}/*.so

%changelog
* Mon Mar 30 2015 Liu Di <liudidi@gmail.com> - 2.0.2-10.git20150330
- 更新到 20150330 日期的仓库源码

* Mon Mar 30 2015 Liu Di <liudidi@gmail.com> - 2.0.2-10.git20140524
- 为 Magic 3.0 重建

* Sat May 24 2014 Liu Di <liudidi@gmail.com> - 2.0.2-9.git20140524
- 为 Magic 3.0 重建

* Sat May 24 2014 Liu Di <liudidi@gmail.com> - 2.0.2-8.git20140524
- 为 Magic 3.0 重建

* Sat May 24 2014 Liu Di <liudidi@gmail.com> - 2.0.2-7.git20140524
- 为 Magic 3.0 重建

* Sat May 24 2014 Liu Di <liudidi@gmail.com> - 2.0.2-6.git20140524
- 更新到 20140524 日期的仓库源码

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 2.0.2-2
- 为 Magic 3.0 重建

* Tue Aug 11 2009 Ni Hui <shuizhuyuanluo@126.com> - 1.66.0-0.5mgc
- 拆出开发包
- 添加中文翻译文件
- 己丑  六月廿一

* Wed Jun 17 2009 Liu Di <liudidi@gmail.com> - 1.66.0-1
- 更新到 KDE4 版本

* Tue Jun 10 2008 Liu Di <liudidi@gmail.com> - 1.0.5-1mgc
- 更新到 1.0.5

* Fri Nov 09 2007 Liu Di <liudidi@gmail.com> - 1.0.4-1mgc
- update to 1.0.4

* Tue May 29 2007 kde <athena_star {at} 163 {dot} com> - 1.0.1-1mgc
- update to 1.0.1

* Wed Feb 28 2007 Liu Di <liudidi@gmail.com> - 0.1-0.rc6mgc
- update to 1.0 rc6

* Fri Aug 25 2006 Liu Di <liudidi@gmail.com> - 0.12.17-1mgc
- 0.12.17

* Fri Dec 16 2005 KanKer <kanker@163.com>
- 0.12.9
* Sat Nov 26 2005 KanKer <kanker@163.com>
- 0.12.8
* Fri Nov 4 2005 KanKer <kanker@163.com>
- 0.12.7
* Mon Oct 31 2005 KanKer <kanker@163.com>
- 0.12.6
* Wed Oct 19 2005 KanKer <kanker@163.com>
- 0.12.5
* Wed Sep 21 2005 KanKer <kanker@163.com>
- 0.12.4a
* Sat Jul 30 2005 KanKer <kanker@163.com>
- 0.12.3
* Sun Jul 3 2005 KanKer <kanker@163.com>
- 0.12.2
* Sat Jun 18 2005 KanKer <kanker@163.com>
- 0.12.1
* Thu Jun 14 2005 KanKer <kanker@163.com>
- 0.12
* Wed May 12 2005 KanKer <kanker@163.com>
- 0.11.24
* Sun Mar 27 2005 KanKer <kanker@163.com>
- 0.11.23
* Thu Jan 27 2005 KanKer <kanker@163.com>
- 0.11.19
- patch to use joliet default.
* Sun Dec 12 2004 KanKer <kanker@163.com>
- 0.11.18
* Thu Sep 23 2004 KanKer <kanker@163.com>
- 0.11.17
* Fri Sep 17 2004 KanKer <kanker@163.com>
- build

* Sat Jun 12 2004 KanKer <kanker@163.com>
- rebuild on qt-3.3.2
* Wed May 26 2004 - Mihai Maties <mihai@xcyb.org> - k3b-0.11.10-1.xcyb*
- apply a patch to compile K3b on qt-3.1
- rebuild

