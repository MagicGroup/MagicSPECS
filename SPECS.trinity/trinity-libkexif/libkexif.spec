Name: libkexif
Version: 0.2.5
Release: 1%{?dist}
Summary: Allow Kipi plugins to extract EXIF information
Summary(zh_CN): 允许 Kipi 插件提取 EXIF 信息
Group: System Environment/Libraries
Group(zh_CN): 系统环境/库
License: GPL
URL: http://www.kipi-plugins.org/
Source0: %{name}-%{version}.tar.bz2
Patch0: libkexif-0.2.5-admin.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: libexif-devel >= 0.5.7, kdelibs-devel >= 3.0
BuildRequires: gettext

%description
This library allows Kipi plugins to extract EXIF information from JPEG files.

%description -l zh_CN
这个库允许 Kipi 插件从 JPEG 文件中提取 EXIF 信息。

%package devel
Summary: Allow Kipi plugins to extract EXIF information
Summary(zh_CN): 允许 Kipi 插件提取 EXIF 信息
Group: Development/Libraries
Group(zh_CN): 开发/库
Requires: %{name} = %{version}-%{release}
Requires: kdelibs-devel
Requires: pkgconfig

%description devel
libkexif allows Kipi plugins to extract EXIF information from JPEG files.
This package contains the files needed to build applications with libkexif
support.

%description devel -l zh_CN
libkexif 允许 Kipi 插件从 JPEG 文件中提取 EXIF 信息。
本软件包包含需要 libkexif 支持构建程序所需的文件。

%prep
%setup -q
%patch0 -p1 
chmod 777 admin/*

%build
unset QTDIR && . %{_sysconfdir}/profile.d/qt.sh
# work around an improper ${kdelibsuff}
export QTLIB=${QTDIR}/lib QTINC=${QTDIR}/include
make -f admin/Makefile.common
%configure --disable-rpath --disable-debug --enable-final
%{__make} %{?_smp_mflags}


%install
%{__rm} -rf %{buildroot}
%{__make} DESTDIR=%{buildroot} install

%find_lang %{name}

find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'

%clean
%{__rm} -rf %{buildroot} %{_builddir}/%{buildsubdir}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog README
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/libkexif

%changelog
* Tue Oct 2 2007 Ni Hui <shuizhuyuanluo@126.com> - 0.2.5-0.1mgc
- first spec file for MagicLinux-2.1
