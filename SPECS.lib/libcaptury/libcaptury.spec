%define svn_version 20080323

Summary: X11/GLX Video Capturing Framework
Summary(zh_CN.UTF-8): X11/GLX 视频捕捉构架
Name: libcaptury
Version: 0.3.0
Release: 0.%{svn_version}.0.1%{?dist}.2
URL: http://rm-rf.in/captury
Source: libcaptury-%{version}-%{svn_version}.tar.bz2
License: GPL
Group: System/Libraries
Group(zh_CN.UTF-8): 系统/库
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: capseo-devel

%description
libcaptury is a movie capturing framework with its primary goal
to capture the screen of OpenGL games (running on Linux systems).

this framework's goal is, to provide an easy to understand and 
easy to use C API that can be quickly integrated into already 
existing applications that need capturing capabilities.

%description -l zh_CN.UTF-8
X11/GLX 视频捕捉构架。

%package devel
Summary: Library and include files for libcaptury
Summary(zh_CN.UTF-8): libcaptury 的库和头文件
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}

%description devel
Library and include files for applications that want to use libcaptury.

%description devel -l zh_CN.UTF-8
libcaptury 的库和头文件。

%prep
%setup -q 

%build
./autogen.sh
%configure
make CFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

# 无用文件
rm -f %{buildroot}%{_libdir}/*.la

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog README NEWS TODO COPYING
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/captury/captury.h
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/pkgconfig/libcaptury.pc

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.3.0-0.20080323.0.1.2
- 为 Magic 3.0 重建

* Thu Jan 05 2012 Liu Di <liudidi@gmail.com> - 0.3.0-0.20080323.0.1.1
- 为 Magic 3.0 重建

* Wed Feb 6 2008 Ni Hui <shuizhuyuanluo@126.com> - 0.3.0-0.svn20070725.0.2mgc
- 重建

* Sat Dec 15 2007 Ni Hui <shuizhuyuanluo@126.com> - 0.3.0-0.svn20070725.0.1mgc
- 首次制作 rpm 包 for MagicLinux-2.1
