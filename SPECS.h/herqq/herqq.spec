Name:           herqq
Version:        1.0.0
Release:        6%{?dist}
Summary:        A software library for building UPnP devices and control points
Summary(zh_CN.UTF-8): 创建 UPnP 设备和控制点的软件库
# test application is GPLv3 but we do not ship it
License:        LGPLv3+
URL:            http://herqq.org/
Source0:        http://downloads.sourceforge.net/project/hupnp/hupnp/%{name}-%{version}.zip
Patch2:         herqq-1.0.0-qtsoap-library.patch


BuildRequires:  desktop-file-utils
BuildRequires:  qt4-devel
BuildRequires:  qtsoap-devel


%description
Herqq UPnP (HUPnP) is a software library for building UPnP 
devices and control points conforming to the UPnP Device 
Architecture version 1.1. 

%description -l zh_CN.UTF-8
创建 UPnP 设备和控制点的软件库.

%package devel
Summary:  Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires: %{name} = %{version}-%{release}
Provides: hupnp-devel = %{version}-%{release}
%description devel
Header files for developing applications using %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

# lQtSolutions to lqtsoap
%patch2 -p1 -b .qtsoap-library

%build
# we have to disable bundled QtSOAP library
qmake-qt4 PREFIX=%{_prefix} -config DISABLE_QTSOAP \
  -config DISABLE_TESTAPP -config USE_QT_INSTALL_LOC
make %{?_smp_mflags}
magic_rpm_clean.sh

%install
make INSTALL_ROOT=%{buildroot} install


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%doc hupnp/ChangeLog hupnp/LICENSE_LGPLv3.txt
%{_qt4_libdir}/libHUpnp.so.1*

%files devel
%{_qt4_libdir}/libHUpnp.so
%{_qt4_headerdir}/HUpnpCore/

%changelog
* Thu Apr 17 2014 Liu Di <liudidi@gmail.com> - 1.0.0-6
- 为 Magic 3.0 重建

* Tue Apr 15 2014 Liu Di <liudidi@gmail.com> - 1.0.0-5
- 为 Magic 3.0 重建

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Aug 06 2011 Rex Dieter <rdieter@fedoraproject.org> 1.0.0-2
- Provides: hupnp(-devel)

* Wed Jul 20 2011 Jaroslav Reznik <jreznik@redhat.com> - 1.0.0-1
- post-review update to 1.0.0

* Wed Jul 20 2011 Jaroslav Reznik <jreznik@redhat.com> - 0.9.1-3
- fix license to LGPLv3+
- qt4 header dir for consistency
- shlib soname tracked in %files
- -devel should not duplicate COPYING

* Tue Jul 19 2011 Jaroslav Reznik <jreznik@redhat.com> - 0.9.1-2
- qtsoap library
- cleanup SPEC file

* Tue Feb 22 2011 Jaroslav Reznik <jreznik@redhat.com> - 0.9.1-1
- Initial spec file 
