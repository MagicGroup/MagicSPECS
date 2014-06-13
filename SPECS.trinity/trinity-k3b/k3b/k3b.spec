%define git 1
%define gitdate 20111215
%define name	k3b
%define version	1.0.6
%define testver	%{nil}
%if %{git}
%define release 0.git%{gitdate}%{?dist}
%else
%define release	4%{?dist}
%endif

Summary:        Excellent CD-Burner for KDE3
Summary(zh_CN.UTF-8): KDE3 下优秀的 CD/DVD 刻录程序
Name:           k3b
Version:        %{version}
Release:        %{release}
License:        GPL
Vendor:         Magic Linux
URL:            http://www.k3b.org
Packager:       KanKer <kanker@163.com>
Group:          Applications/Multimedia
Group(zh_CN.UTF-8):	应用程序/多媒体
%if %{git}
Source:		k3b-git%{gitdate}.tar.xz
%else
Source:         k3b-%{version}%{testver}.tar.bz2
%endif
Source1:	make_k3b_git_package.sh
Patch0:		k3b-libtool.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)
Prefix:         %(kde-config --prefix)
Provides:       cd-burner
Requires:       cdrecord >= 2.0, mkisofs >= 2.0, cdrdao >= 1.1, dvd+rw-tools >= 7.0
Requires:       libdvdread, kdelibs >= 3.1, flac, hal, ffmpeg, libsndfile
Requires:	libmad, libogg, lame, libmpcdec, taglib
BuildRequires:	kdelibs-devel >= 3.1, qt-devel, audiofile-devel, alsa-driver-devel
BuildRequires:	libdvdread-devel, flac-devel, hal-devel, ffmpeg, libsndfile-devel
BuildRequires:	libmad-devel, libogg-devel, lame-devel, taglib-devel, libmpcdec-devel
BuildRequires:	libart_lgpl-devel, libpng-devel, flac-devel, autoconf, automake16
#BuildRequires:	XFree86-devel

# Unfortunately the --without-libmad and --without-libvorbis options do not work
# because Sebastian always enables it if it's available.
# ( also the --without-arts parameter seems to be ignored, so actually only
#   --without-k3bsetup does work )
%{!?_without_libmad:Requires: libmad, id3lib}
%{!?_without_libmad:BuildRequires: libmad-devel, id3lib-devel}
%{!?_without_libogg:Requires: libvorbis, libogg}
%{!?_without_libogg:BuildRequires: libvorbis-devel, libogg-devel}
%{!?_without_arts:Requires: arts}
%{!?_without_arts:BuildRequires: arts-devel}


%description
K3b - The CD Creator - Writing cds under linux made easy. It has an extremely
easy to use interface and supports many features: data/audio/video/mixed
[on-the-fly] CD burning, CD copying, erasing and ripping, CD-text writing,
burning iso/bin-cue images and many more.

%description -l zh_CN.UTF-8
K3b - CD/DVD 创建器 - 使得在 linux下写入 CD/DVD 易如反掌。它有一个
非常易用的界面并且支持许多特性：数据/音频/视频/混合 [一次成型] CD/DVD
刻录、复制、擦除、提取、CD-text 写入、刻录 iso/bin-cue 镜像和许多其它特性。

%prep
%if %{git}
%setup -q -n %{name}-git%{gitdate}
%else
%setup -q -n %{name}-%{version}%{testver}
%endif
%patch0 -p1

%build
make -f admin/Makefile.common cvs

CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS" \
%configure \
             --prefix=%{prefix} --libdir=%{_libdir}\
	         %{?_without_k3bsetup:--without-k3bsetup} \
	         %{?_without_libmad:--without-libmad} \
	         %{?_without_arts:--without-arts} \
                $LOCALFLAGS

#NOTE: Because of unsermake, k3b dose not support parallel compiling, e.g. -jN parameter!
#Do not use %{?_smp_mflags}!
#make %{?_smp_mflags}
%{__make}

%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot}



%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files
%doc AUTHORS
%doc COPYING
%doc ChangeLog
%doc FAQ
%doc INSTALL
%doc README
%doc TODO
%{prefix}/*
%exclude %{prefix}/*/debug*
%exclude %{prefix}/src

%changelog
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

