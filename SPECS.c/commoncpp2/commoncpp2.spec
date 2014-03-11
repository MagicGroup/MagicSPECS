Summary: GNU Common C++ class framework
Summary(zh_CN.UTF-8): GNU 通用 C++ 类框架
Name: commoncpp2
Version: 1.8.1
Release: 2%{?dist}
License: GPLv2+ with exceptions
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Source0: http://www.gnutelephony.org/dist/tarballs/commoncpp2-%{version}.tar.gz
Patch0:  commoncpp-1.8.1-include.patch
URL: http://www.gnu.org/software/commoncpp/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: libxml2-devel, zlib-devel, doxygen

%description
GNU Common C++ is a portable and highly optimized class framework for writing
C++ applications that need to use threads, sockets, XML parsing,
serialization, config files, etc. This framework offers a class foundation
that hides platform differences from your C++ application so that you need
not write platform specific code. GNU Common C++ has been ported to compile
natively on most platforms which support posix threads.

%description -l zh_CN.UTF-8
GNU 通用 C++ 类框架。

%package devel
Summary: Header files and libraries for %{name} development
Summary(zh_CN.UTF-8): %name 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig, libxml2-devel, zlib-devel
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description devel
The %{name}-devel package contains the header files and libraries needed
to develop programs that use the %{name} library.

%description devel -l zh_CN.UTF-8
%name 的开发包。

%prep
%setup -q
%patch0 -p1

%build
%configure \
	--disable-static \
	--disable-dependency-tracking
%{__make} #%%{?_smp_mflags} smp building disabled

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_infodir}/dir
find %{buildroot} -name '*.la' -exec rm -f {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%post -n %{name}-devel
/sbin/install-info %{_infodir}/commoncpp2.info %{_infodir}/dir || :

%preun -n %{name}-devel
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_infodir}/commoncpp2.info %{_infodir}/dir || :
fi

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING README ChangeLog
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%doc doc/html
%dir %{_includedir}/cc++
%{_includedir}/cc++/*
%{_bindir}/ccgnu2-config
%{_libdir}/*.so
%{_libdir}/pkgconfig/libccext2.pc
%{_libdir}/pkgconfig/libccgnu2.pc
%{_datadir}/aclocal/ost_check2.m4
%{_infodir}/commoncpp2.info*

%changelog
* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 1.8.1-2
- 为 Magic 3.0 重建

* Mon Nov 07 2011 Liu Di <liudidi@gmail.com> - 1.8-1
- 更新到 1.8
