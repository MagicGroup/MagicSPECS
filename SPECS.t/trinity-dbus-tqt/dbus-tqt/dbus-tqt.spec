%define dbus_version		0.92
%define qt_version              3.3.6
%define qt_dir			%{_prefix}/lib/qt-3.3

%define lib_api 1
%define lib_qt_major 0

%define git 1
%define gitdate 20111214

Name: dbus-tqt
Version: 0.70
%if %{git}
Release: 6.git%{gitdate}%{?dist}
%else
Release: 5%{?dist}
%endif
URL: http://www.freedesktop.org/Software/dbus
%if %{git}
Source0: %{name}-git%{gitdate}.tar.xz
%else
Source0: %{name}-%{version}.tar.bz2
%endif
Source1: make_dbus-tqt_git_package.sh
License: AFL/GPL
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: qt-devel    >= %{qt_version}
BuildRequires: dbus-devel >= %{dbus_version}
Provides: dbus-qt = %{version}-%{release}
Summary: Qt-based library for using D-BUS
Summary(zh_CN.UTF-8): D-Bus的Qt3绑定
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%description
D-BUS add-on library to integrate the standard D-BUS library with
the Qt thread abstraction and main loop.

%description -l zh_CN.UTF-8
在Qt3程序中使用D-Bus的库

%package devel
Summary: Qt-based library for using D-BUS
Summary(zh_CN.UTF-8): D-Bus的Qt3绑定的开发文件
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: dbus-tqt = %version

%description devel
D-BUS add-on library to integrate the standard D-BUS library with the
Qt thread abstraction and main loop. This contains the Qt specific
headers and libraries.

%description devel -l zh_CN.UTF-8
D-Bus的Qt3绑定的静态库和头文件。

%prep
%if %{git}
%setup -q -n %{name}-git%{gitdate}
%else
%setup -q 
%endif

%build
#gw so we can find moc
export PATH=%qt_dir/bin:$PATH
export QTDIR=%qt_dir
mkdir build
cd build
%cmake ..
%{__make}

%install
rm -rf %{buildroot}
cd build
make install DESTDIR=%{buildroot}

#remove unpackaged file
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf %{buildroot}

%post  -p /sbin/ldconfig
%postun  -p /sbin/ldconfig

%files 
%defattr(-,root,root)
%{_libdir}/*qt*.so.%{lib_qt_major}*

%files devel
%defattr(-,root,root)
%{_libdir}/*qt*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/dbus-1.0/dbus/dbus-qt.h
%{_includedir}/dbus-1.0/dbus/connection.h
%{_includedir}/dbus-1.0/dbus/message.h
%{_includedir}/dbus-1.0/dbus/server.h


%changelog
* Fri Aug 25 2006 Liu Di <liudidi@gmail.com> 0.70-1mgc
- port to Magic

* Mon Jul 31 2006 Frederic Crozat <fcrozat@mandriva.com> 0.70-1mdv2007.0
- Initial package (splitted from dbus 0.62)
