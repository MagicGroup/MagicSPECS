Name: libkdcraw
Summary: A library for decoding RAW picture files
Summary(zh_CN): 解析 RAW 图片文件的库
Group: Applications/Multimedia
Group(zh_CN): 应用程序/多媒体
Version: 0.1.2
Release: 1%{?dist}
License: GPLv2+
URL: http://www.kipi-plugins.org/
Source0: http://downloads.sourceforge.net/kipi/%{name}-%{version}.tar.bz2
Patch0:	libkdcraw-0.1.2-admin.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: kdelibs-devel lcms-devel gettext pkgconfig

%description
libkdcraw is a C++ interface around dcraw binary program used to decode RAW
picture files. The library documentation is available on header files.

This library is used by kipi-plugins, digiKam and others kipi host programs.

%description -l zh_CN
libkdcraw 是一个调用用来解析 RAW 图片文件的 dcraw 二进制程序的 C++ 接口。库文档可以在头文件中找到。

这个库被 kipi-plugins，digiKam 以及其他调用 kipi 的程序所使用。

%package devel
Summary: Development files for libkdcraw
Summary(zh_CN): libkdcraw 的开发文件
Group: Development/Libraries
Group(zh_CN): 开发/库
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
This package contains the libraries, include files and other resources
needed to develop applications using libkdcraw.

%description devel
本软件包包含使用 libkdcraw 开发程序所需的开发库，头文件以及其它资源。

%prep
%setup -q
%patch0 -p1
chmod 777 admin/*

%build
unset QTDIR || : ; . %{_sysconfdir}/profile.d/qt.sh
make -f admin/Makefile.common
%configure \
	--disable-rpath \
	--disable-debug \
	--disable-dependency-tracking \
	--enable-final \
	--enable-new-ldflags \
	--disable-warnings
#临时措施
sed -i 's/\/include\/tqt/\/include\/tqt \-lm/g' libkdcraw/dcraw/Makefile

%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} DESTDIR=%{buildroot} install

%find_lang %{name}

%{__rm} -f %{buildroot}%{_libdir}/libkdcraw.la

%post
/sbin/ldconfig

touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
	%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%postun
/sbin/ldconfig

touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
	%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%clean
%{__rm} -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files -f %name.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%{_libdir}/libkdcraw.so.*
%{_libdir}/libkdcraw2/
%{_datadir}/icons/hicolor/*/apps/kdcraw.png

%files devel
%defattr(-,root,root,-)
%{_includedir}/libkdcraw/
%{_libdir}/pkgconfig/libkdcraw.pc
%{_libdir}/libkdcraw.so

%changelog
* Tue Oct 2 2007 Ni Hui <shuizhuyuanluo@126.com> - 0.1.2-0.1mgc
- first spec file for MagicLinux-2.1
