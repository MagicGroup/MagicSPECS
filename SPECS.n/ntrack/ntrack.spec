Name:           ntrack
Summary:        Network Connectivity Tracking library for Desktop Applications
Summary(zh_CN.UTF-8): 桌面程序的网络连接能力跟踪库
Version: 017
Release: 3%{?dist}
License:        LGPLv3
Url:            https://launchpad.net/%{name}
Source:         http://launchpad.net/%{name}/main/%{version}/+download/%{name}-%{version}.tar.gz
Group:          Development/C
Group(zh_CN.UTF-8): 开发/库
BuildRequires:  autoconf automake libtool
BuildRequires:  qt4-devel
BuildRequires:  libnl-devel
BuildRequires:  python-devel
BuildRequires:	libnl3-devel

%description
ntrack aims to be a lightweight and easy to use library for application
developers that want to get events on network online status changes such
as online, offline or route changes.

The primary goal is to serve desktop applications in a network manager 
and desktop environment independent fashion.
Also its supposed to be lightweight, resource un-intensive and extensible.

%description -l zh_CN.UTF-8
桌面程序的网络连接能力跟踪库。

%files
%defattr(-,root,root)
%doc README NEWS COPYING COPYING.LESSER ChangeLog AUTHORS
%{_libdir}/ntrack/modules/ntrack-libnl1.so
%{_libdir}/ntrack/modules/ntrack-libnl3_x.so
%{_libdir}/libntrack.so.*

%package python
Summary: Network Connectivity Tracking library for Desktop Applications
Group: System/Libraries

%description python
ntrack aims to be a lightweight and easy to use library for application
developers that want to get events on network online status changes such
as online, offline or route changes.

This packages provides the Python bindings for %{name}

%files python
%defattr(-,root,root)
%{python_sitearch}/pyntrack.*

#-------------------------------------------------------------------------------

%package qt4
Summary:   Network Connectivity Tracking library for Desktop Applications
Group: System/Libraries  

%description qt4
ntrack aims to be a lightweight and easy to use library for application
developers that want to get events on network online status changes such
as online, offline or route changes.
 
This packages provides the Qt4 bindings for %{name}
 
%files qt4
%defattr(-,root,root)
%{_libdir}/libntrack-qt4.so.*

#--------------------------------------------------------------------------------

%package qt4-devel
Summary:   Network Connectivity Tracking library for Desktop Applications
Group: Development/Other
Requires:  ntrack = %{version}-%{release}
Provides:  libntrack-qt4-devel = %{version}-%{release}
 
%description qt4-devel
Development files (headers and libraries) for ntrack
 
%files qt4-devel
%defattr(-,root,root)
%{_includedir}/%{name}/qt4/
%{_libdir}/pkgconfig/libntrack-qt4.pc
%{_libdir}/libntrack-qt4.so

 
#------------------------------------------------------------------------------
 
%package gobject
Summary:   Network Connectivity Tracking library for Desktop Applications
Group: System/Libraries  

%description gobject
ntrack aims to be a lightweight and easy to use library for application
developers that want to get events on network online status changes such
as online, offline or route changes.

This package provides the gobject bindings for %{name}

%files gobject
%defattr(-,root,root)
%{_libdir}/libntrack-gobject.so.*


#------------------------------------------------------------------------------ 

%package gobject-devel
Summary:   Network Connectivity Tracking library for Desktop Applications
Group: Development/Other
Requires:  ntrack-gobject = %{version}-%{release}
Provides:  libntrack-gobject-devel = %{version}-%{release}


%description gobject-devel
Development files (headers and libraries) for ntrack
 

%files gobject-devel
%defattr(-,root,root)
%{_includedir}/%{name}/gobject/
%{_libdir}/pkgconfig/libntrack-gobject.pc
%{_libdir}/libntrack-gobject.so 

#------------------------------------------------------------------------------ 

%package glib
Summary:   Network Connectivity Tracking library for Desktop Applications
Group: System/Libraries  

%description glib
ntrack aims to be a lightweight and easy to use library for application
developers that want to get events on network online status changes such
as online, offline or route changes.

This package provides the glib bindings for %{name}

%files glib
%defattr(-,root,root)
%{_libdir}/libntrack-glib.so.* 

#------------------------------------------------------------------------------  
 
%package glib-devel 
Summary:   Network Connectivity Tracking library for Desktop Applications
Group: Development/Other  
Requires: ntrack-glib = %{version}-%{release}
Provides: libntrack-glib-devel = %{version}-%{release}

%description glib-devel 
Development files (headers and libraries) for ntrack
 
%files glib-devel 
%defattr(-,root,root)
%{_includedir}/%{name}/glib/
%{_libdir}/pkgconfig/libntrack-glib.pc
%{_libdir}/libntrack-glib.so
 
#------------------------------------------------------------------------------ 

%package devel
Summary:   Network Connectivity Tracking library for Desktop Applications
Group: Development/Other 
Requires:  ntrack-glib-devel = %{version}-%{release}
Requires:  ntrack-gobject-devel = %{version}-%{release}
Requires:  ntrack-qt4-devel =  %{version}-%{release}

%description devel
Development files (headers and libraries) for ntrack
  
%files devel
%defattr(-,root,root)
%dir %{_includedir}/ntrack
%{_includedir}/ntrack/common/
%{_libdir}/pkgconfig/libntrack.pc
%{_libdir}/libntrack.so

#------------------------------------------------------------------------------
 
%prep
%setup -q 

%build
mkdir -p m4
autoreconf -fi
%configure
make
 
%install
%makeinstall

# Remove .a & .la files
rm -rf %{buildroot}/%{_libdir}/*.a
rm -rf %{buildroot}/%{_libdir}/*.la
rm -rf %{buildroot}/%{_libdir}/ntrack/modules/*.a
rm -rf %{buildroot}/%{_libdir}/ntrack/modules/*.la

# dupes
rm -rf %{buildroot}%{_datadir}/doc/ntrack

%clean
rm -rf %{buildroot}


%changelog
* Wed Nov 11 2015 Liu Di <liudidi@gmail.com> - 017-3
- 为 Magic 3.0 重建

* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 017-2
- 为 Magic 3.0 重建

* Sat Feb 28 2015 Liu Di <liudidi@gmail.com> - 017-1
- 更新到 017

* Mon Dec 31 2012 Liu Di <liudidi@gmail.com> - 016-2
- 为 Magic 3.0 重建


