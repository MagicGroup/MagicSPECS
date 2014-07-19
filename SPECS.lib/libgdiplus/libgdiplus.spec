Name:           libgdiplus
Version: 2.10.9
Release:        1%{?dist}
Summary:        An Open Source implementation of the GDI+ API
Summary(zh_CN.UTF-8): GDI+ API 的开源实现

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        MIT
URL:            http://www.mono-project.com/Main_Page
Source0:        http://download.mono-project.com/sources/%{name}/%{name}-%{version}.tar.bz2
# Patch for linking against libpng 1.5 (BZ #843330)
# https://github.com/mono/libgdiplus/commit/506df13e6e1c9915c248305e47f0b67549732566
Patch0:         libgdiplus-2.10.9-libpng15.patch
# Fix build with Freetype 2.5
# https://github.com/mono/libgdiplus/commit/180c02e0f2a2016eba8520b456ca929e9dcf03db
Patch1:         libgdiplus-2.10.9-freetype25.patch
# drop -Wno-format so the default -Werror=format-security works
Patch2:         libgdiplus-2.10.9-format.patch
# https://github.com/mono/libgdiplus/commit/1fa831c7440f1985d2b730211bbf8a059c10a63b
Patch3:         libgdiplus-2.10.9-tests.patch
BuildRequires:  freetype-devel glib2-devel libjpeg-devel libtiff-devel
BuildRequires:  libungif-devel libpng-devel fontconfig-devel
BuildRequires:  cairo-devel giflib-devel libexif-devel
BuildRequires:  zlib-devel

%description
An Open Source implementation of the GDI+ API, it is part of the Mono 
Project

%description -l zh_CN.UTF-8
GDI+ API 的开源实现，这是 Mono 项目的一部分。

%package devel
Summary: Development files for libgdiplus
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}

%description devel
Development files for libgdiplus

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q 
%patch0 -p1 -b .libpng15
%patch1 -p1 -b .freetype25
%patch2 -p1 -b .format
%patch3 -p1 -b .tests

%build
%configure --disable-static 
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} INSTALL="install -p"
find %{buildroot} -name '*.la' -exec rm -f {} ';'
magic_rpm_clean.sh

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING NEWS README TODO AUTHORS ChangeLog
%{_libdir}/lib*.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/*
%{_libdir}/lib*.so

%changelog
* Wed Jul 16 2014 Liu Di <liudidi@gmail.com> - 2.10.9-1
- 更新到 2.10.9

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 2.10-5
- 为 Magic 3.0 重建

* Wed Mar 28 2012 Liu Di <liudidi@gmail.com> - 2.10-4
- 为 Magic 3.0 重建

* Thu Dec 08 2011 Liu Di <liudidi@gmail.com> - 2.10-3
- 为 Magic 3.0 重建

