Summary: Unicode manipulation library
Summary(zh_CN.UTF-8): Unicode处理库
Name: libunicode
Version: 0.7
Release: 7%{?dist}
License: LGPL
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL: http://www.pango.org/

Source: http://dl.sf.net/libunicode/libunicode-%{version}.tar.gz
Packager: Liu Di <liudidi@gmail.com>
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: automake, autoconf, libtool

%description
A library to handle unicode strings

%description -l zh_CN.UTF-8
一个控制unicode字符串的库。

%package devel
Summary: Header files, libraries and development documentation for %{name}
Summary(zh_CN.UTF-8): %{name}的头文件，库和开发文档
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%description devel -l zh_CN.UTF-8
这个包包含了%{name}的头文件，库和开发文档。如果你想用%{name}开发程序，你
将需要安装%{name}-devel

%prep
%setup
#%patch -p0 -b .64bit
sed -i -e "/testsuite/d" configure.in

%build
#%{__libtoolize} --copy --force
#%{__aclocal}-1.4
#%{__automake}-1.4
#%{__autoconf}
autoreconf -fisv
%configure
%{__make} %{?_smp_mflags} \
	RPM_OPT_FLAGS="%{optflags}"

%install
%{__rm} -rf %{buildroot}
#mkdir -p $RPM_BUILD_ROOT%{_prefix}
%makeinstall

### Clean up buildroot
%{__rm} -f %{buildroot}%{_libdir}/*.la

%clean
%{__rm} -rf %{buildroot}

%post
/sbin/ldconfig 2>/dev/null

%postun
/sbin/ldconfig 2>/dev/null

%files
%defattr(-, root, root, 0755)
%doc AUTHORS ChangeLog COPYING NEWS README
%{_libdir}/*.so.*

%files devel
%defattr(-, root, root, 0755)
#%{_bindir}/*
%{_libdir}/*.a
%{_libdir}/*.so
%{_includedir}/*.h

%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 0.7-7
- 为 Magic 3.0 重建

* Fri Aug 01 2014 Liu Di <liudidi@gmail.com> - 0.7-6
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.7-5
- 为 Magic 3.0 重建

* Thu Jan 12 2012 Liu Di <liudidi@gmail.com> - 0.7-4
- 为 Magic 3.0 重建

* Fri Jan 05 2007 Liu Di <liudidi@gmail.com> - 0.7-1.2mgc
- rebuild for Magic

* Sat Apr 08 2006 Dries Verachtert <dries@ulyssis.org> - 0.7-1.2 #4303
- Rebuild for Fedora Core 5.

* Sun Nov 13 2005 Dries Verachtert <dries@ulyssis.org> - 0.7-2
- Some fixes.

* Wed Sep 14 2005 Dries Verachtert <dries@ulyssis.org> - 0.7-1
- Updated to release 0.7.

* Sat Jan 03 2004 Dag Wieers <dag@wieers.com> - 0.4-12.0
- Initial package. (using DAR)
