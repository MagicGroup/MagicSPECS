Name:           liblqr-1
Version:        0.4.2
Release:        4%{?dist}
Summary:        LiquidRescale library
Summary(zh_CN.UTF-8): LiquidRescale 库
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        GPLv3
URL:            http://liquidrescale.wikidot.com/
Source0:        http://liblqr.wikidot.com/local--files/en:download-page/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-%(%{__id_u} -n)
BuildRequires:  glib2-devel

%description
The LiquidRescale (lqr) library provides a C/C++ API for
performing non-uniform resizing of images by the seam-carving
technique.

%description -l zh_CN.UTF-8
LiquidRescale (lqr) 库为提供 C/C++ API 用以使用 seam-carving 技术调整图像。

%package devel
Summary:        LiquidRescale library  development kit
Summary(zh_CN.UTF-8): LiquidRescale 库的开发文件
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License:        GPLv3
Requires:       %{name} = %{version}-%{release}
Requires:       glib2-devel, pkgconfig

%description devel
The libqr-devel package contains the header files
needed to develop applications with liblqr.

%description devel -l zh_CN.UTF-8
%{name}-devel 软件包包含了使用 liblqr 库开发应用程序所需的头文件。

%prep
%setup -q

%build
export LDFLAGS="`pkg-config --libs glib-2.0` -lm"
%configure
%{__make} %{?_smp_mflags}


%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

# remove .la files
find $RPM_BUILD_ROOT -name \*.la -exec %{__rm} -f {} \;

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files 
%defattr(-,root,root,-)
%doc README COPYING
%{_libdir}/liblqr-1.so.*

%files devel
%defattr (-, root, root,-)
%doc docs/liblqr_manual.docbook
%{_libdir}/liblqr-1.so
%{_includedir}/lqr-1/
%{_libdir}/pkgconfig/lqr-1.pc

%changelog
* Mon Nov 09 2015 Liu Di <liudidi@gmail.com> - 0.4.2-4
- 为 Magic 3.0 重建

* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 0.4.2-3
- 为 Magic 3.0 重建

* Fri Jul 18 2014 Liu Di <liudidi@gmail.com> - 0.4.2-2
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.4.1-3
- 为 Magic 3.0 重建



