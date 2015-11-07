%define		soname 1

Name:		libindicate-qt
Version:	0.2.5.91
Release:	22.1
License:	LGPL-2.0 and LGPL-3.0
Summary:	Qt bindings fo libindicate
Url:		http://launchpad.net/libindicate-qt
Group:		System/Libraries
Source:		https://launchpad.net/ubuntu/+archive/primary/+files/libindicate-qt_%{version}.orig.tar.gz

Patch0:		0001_fix_pkgconfig_libindicate_version.patch
# Ubuntu patch to build with -fvisiblity=hidden
Patch1:		0002_build_with_fvisibility_hidden.patch

BuildRequires:	cmake

BuildRequires:	pkgconfig(indicate-0.7) >= 0.6.90
BuildRequires:	pkgconfig(QtCore)

%description
This package provides a set of Qt bindings for libindicate, the indicator system
developed by Canonical Desktop Experience team.


%package -n %{name}%{soname}
Summary:	Qt bindings fo libindicate
Group:		System/Libraries

%description -n %{name}%{soname}
This package provides a set of Qt bindings for libindicate, the indicator system
developed by Canonical Desktop Experience team.


%package devel
Summary:	Development files for libindicate-qt
Group:		Development/Libraries/C and C++

Requires:	%{name}%{soname} = %{version}-%{release}
 
%description devel
This package contains the development files for the indicate-qt library.


%prep
%setup -q
%patch0 -p1 -b .pkgconfig
%patch1 -p1 -b .fvisibility


%build
mkdir build
cd build

cmake .. \
  -DCMAKE_BUILD_TYPE=release \
  -DCMAKE_C_FLAGS_RELEASE:STRING="%{optflags}" \
  -DCMAKE_CXX_FLAGS_RELEASE:STRING="%{optflags}" \
  -DLIB_SUFFIX=$(echo %{_lib} | sed 's/lib//') \
  -DCMAKE_INSTALL_PREFIX:PATH="%{_prefix}"

make %{?_smp_mflags}


%install
cd build
%make_install


%post -n %{name}%{soname} -p /sbin/ldconfig
 
%postun -n %{name}%{soname} -p /sbin/ldconfig


%files -n %{name}%{soname}
%defattr(-,root,root)
%doc NEWS README
%{_libdir}/libindicate-qt.so.*


%files devel
%defattr(-,root,root)
%dir %{_includedir}/libindicate-qt/
%{_includedir}/libindicate-qt/*
%{_libdir}/libindicate-qt.so
%{_libdir}/pkgconfig/indicate-qt.pc


%changelog
* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 0.2.5.91-22.1
- 为 Magic 3.0 重建

* Fri Jul 18 2014 Liu Di <liudidi@gmail.com> - 0.2.5.91-21.1
- 为 Magic 3.0 重建

* Sat Aug 18 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.2.5.91-1
- Remove unnecessary dependencies
- Fix groups
- Fix descriptions (<= 80 characters per line)
- Fix source line
- Fix files lists (non-versioned libraries go in *-devel packages)
