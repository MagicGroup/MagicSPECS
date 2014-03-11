Summary: Convenience library for kernel netlink sockets
Summary(zh_CN.UTF-8): 内核网络链接套接字的易用库
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License: LGPLv2
Name: libnl
Version: 1.1
Release: 10%{?dist}
URL: http://people.suug.ch/~tgr/libnl/
Source: http://people.suug.ch/~tgr/libnl/files/libnl-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: doxygen
Patch1: libnl-1.0-pre5-static.patch
Patch2: libnl-1.0-pre5-debuginfo.patch
Patch3: libnl-1.0-pre8-use-vasprintf-retval.patch
Patch4: libnl-1.0-pre8-more-build-output.patch
Patch5: libnl-1.1-include-limits-h.patch
Patch6: libnl-1.1-doc-inlinesrc.patch

%description
This package contains a convenience library to simplify
using the Linux kernel's netlink sockets interface for
network manipulation

%description -l zh_CN.UTF-8
内核网络链接套接字的易用库。

%package devel
Summary: Libraries and headers for using libnl
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}
Requires: kernel-headers

%description devel
This package contains various headers for using libnl

%description devel -l zh_CN.UTF-8
%{name} 的开发包

%prep
%setup -q -n %{name}-%{version}
%patch1 -p1 -b .build-static
%patch2 -p1 -b .debuginfo
%patch3 -p1 -b .use-vasprintf-retval
%patch4 -p1 -b .more-build-output
%patch5 -p1 -b .limits
%patch6 -p1 -b .doc-inlinesrc

# a quick hack to make doxygen stripping builddir from html outputs.
sed -i.org -e "s,^STRIP_FROM_PATH.*,STRIP_FROM_PATH = `pwd`," doc/Doxyfile.in

%build
%configure
make
make gendoc

%install
%{__rm} -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/%{name}.so.*
%doc COPYING

%files devel
%defattr(-,root,root,0755)
%{_includedir}/netlink/
%doc doc/html
%{_libdir}/%{name}.so
%{_libdir}/%{name}.a
%{_libdir}/pkgconfig/%{name}-1.pc

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.1-10
- 为 Magic 3.0 重建

* Fri Mar 30 2012 Liu Di <liudidi@gmail.com> - 1.1-9
- 为 Magic 3.0 重建

