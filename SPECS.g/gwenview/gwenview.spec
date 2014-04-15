%define git 1
%define gitdate 20111229
Name:           gwenview
Version:        1.4.3
%if %{git}
Release:	0.git%{gitdate}%{?dist}.2
%else
Release:        9%{?dist}
%endif
Summary:        Simple image viewer for KDE
Summary(zh_CN.UTF-8): KDE下的简单图像查看器

Group:          Applications/Multimedia
Group(zh_CN.UTF-8):   应用程序/多媒体
License:        GPL
URL:            http://gwenview.sf.net
%if %{git}
Source0:	%{name}-git%{gitdate}.tar.xz
%else
Source0:        http://dl.sf.net/gwenview/%{name}-%{version}.tar.bz2
%endif
Source1:        http://dl.sf.net/gwenview/%{name}-i18n-1.4.2.tar.bz2
# Patch for new libtool
%if %{git}
Patch0:         gwenview-libtool.patch
%else
Patch0:		gwenview-1.4.2-exiv2-r2.patch
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  kdelibs-devel >= 3.5
BuildRequires:  desktop-file-utils
BuildRequires:  libkipi-devel
BuildRequires:  gettext
BuildRequires:  libexif-devel
BuildRequires:  libXt-devel

# Maybe I'll split it in the future
Provides:       gwenview-i18n = %{version}-%{release}


%description
Gwenview is an image viewer for KDE.

It features a folder tree window and a file list window to provide easy
navigation in your file hierarchy.  Image loading is done by the Qt library,
so it supports all image formats your Qt installation supports.

%description -l zh_CN.UTF-8
Gwenview是KDE下的一个图像查看器。

它有树形窗口和文件列表窗口以提供简单的访问你的文件层级。使用Qt库载入图像，
所以支持你的安装的Qt支持的所有图像格式。

%prep
%if %{git}
%setup -q -n %{name}-git%{gitdate} -a 1
%patch0 -p1
%else
%setup -q -a 1
%patch0 -p0
%endif

%build
unset QTDIR && . %{_sysconfdir}/profile.d/qt.sh
# work around an improper ${kdelibsuff}
export QTLIB=${QTDIR}/lib QTINC=${QTDIR}/include
%if %{git}
make -f admin/Makefile.common
%endif
%configure --disable-rpath --disable-debug 
#暂时禁用
# --enable-kipi
# --enable-final  \
make %{?_smp_mflags}

cd %{name}-i18n-1.4.2
%configure
make %{?_smp_mflags}
cd ..


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

desktop-file-install --vendor fedora --delete-original \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications/kde \
  --add-category X-Fedora \
  --add-category Application \
  --add-category Viewer \
  $RPM_BUILD_ROOT%{_datadir}/applications/kde/%{name}.desktop

cd %{name}-i18n-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
cd ..

magic_rpm_clean.sh

# Files list
%find_lang %{name}

# HTML help
for lang_dir in $RPM_BUILD_ROOT%{_datadir}/doc/HTML/* ; do
  if [ -d $lang_dir ]; then
    lang=$(basename $lang_dir)
    echo "%lang($lang) %{_datadir}/doc/HTML/$lang/*" >> %{name}.lang
    # replace absolute symlinks with relative ones
    pushd $lang_dir
      for i in *; do
        [ -d $i -a -L $i/common ] && rm -f $i/common && ln -sf ../common $i/common
      done
    popd
  fi
done


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README
%{_bindir}/*
%{_datadir}/applications/kde/*.desktop
%{_datadir}/apps/konqueror/servicemenus/*
%{_datadir}/icons/*/*/apps/*
%{_datadir}/apps/gwenview
%{_datadir}/apps/gvdirpart
%{_datadir}/apps/gvimagepart
%{_datadir}/apps/kconf_update
%{_datadir}/services/*.desktop
%{_datadir}/config.kcfg/*.kcfg
%{_mandir}/man1/*
%{_libdir}/lib*
%{_libdir}/kde3/lib*
%{_libdir}/kde3/gwenview.*


%changelog
* Tue Apr 15 2014 Liu Di <liudidi@gmail.com> - 1.4.3-0.git20111229.2
- 更新到 20140415 日期的仓库源码

* Tue Apr 15 2014 Liu Di <liudidi@gmail.com> - 1.4.3-0.git20111229.1
- 为 Magic 3.0 重建

* Fri Dec 09 2011 Liu Di <liudidi@gmail.com> - 1.4.2-6
- 为 Magic 3.0 重建

* Sat Dec 15 2007 Liu Di <liudidi@gmail.com> - 1.4.2-2mgc
- update chinese translate

* Mon Dec 03 2007 Liu Di <liudidi@gmail.com> - 1.4.2-1mgc
- update to 1.4.2

* Thu Dec 28 2006 Liu Di <liudidi@gamil.com> - 1.4.1-1mgc
- update to 1.4.1

* Mon Oct 09 2006 Liu Di <liudidi@gmail.com> - 1.4.0-1mgc
- rebuild for Magic

* Tue Oct 03 2006 Aurelien Bompard <abompard@fedoraproject.org> 1.4.0-3
- patch for latest libexif-devel
