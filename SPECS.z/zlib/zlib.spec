Summary: The zlib compression and decompression library
Summary(zh_CN.UTF-8): zlib 压缩和解压库
Name: zlib
Version: 1.2.5
Release: 5%{?dist}
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Source: http://www.zlib.net/zlib-%{version}.tar.bz2
Patch3: zlib-1.2.4-autotools.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=591317
Patch4: zlib-1.2.5-gentoo.patch
URL: http://www.gzip.org/zlib/
# /contrib/dotzlib/ have Boost license
License: zlib and Boost
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: automake, autoconf, libtool

%description
Zlib is a general-purpose, patent-free, lossless data compression
library which is used by many different programs.

%description -l zh_CN.UTF-8
Zlib 是一个通用的、无专利、无数据丢失的压缩库。它被许多不同的
程序所使用。

%package devel
Summary: Header files and libraries for Zlib development
Summary(zh_CN.UTF-8): Zlib 开发的头文件和库
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}

%description devel
The zlib-devel package contains the header files and libraries needed
to develop programs that use the zlib compression and decompression
library.

%description devel -l zh_CN.UTF-8
Zlib 开发的头文件和库。

%package static
Summary: Static libraries for Zlib development
Summary(zh_CN.UTF-8): Zlib 开发的静态库
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name}-devel = %{version}-%{release}

%description static
The zlib-static package includes static libraries needed
to develop programs that use the zlib compression and
decompression library.

%description static -l zh_CN.UTF-8
Zlib 开发的静态库。

%package -n minizip
Summary: Minizip manipulates files from a .zip archive
Summary(zh_CN.UTF-8): Minizip 处理 .zip 包中的文件
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Requires: zlib = %{version}-%{release}

%description -n  minizip
Minizip manipulates files from a .zip archive.

%description -n minizip -l zh_CN.UTF-8
Minizip 处理 .zip 包中的文件。

%package -n minizip-devel
Summary: Development files for the minizip library
Summary(zh_CN.UTF-8): minizip 库的开发文件
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: minizip = %{version}-%{release}
Requires: zlib-devel = %{version}-%{release}
Requires: pkgconfig

%description -n minizip-devel
This package contains the libraries and header files needed for
developing applications which use minizip.

%description -n minizip-devel -l zh_CN.UTF-8
minizip 库的开发文件。

%prep
%setup -q
%patch3 -p1 -b .atools
%patch4 -p1 -b .g
# patch cannot create an empty dir
mkdir contrib/minizip/m4
cp minigzip.c contrib/minizip
iconv -f windows-1252 -t utf-8 <ChangeLog >ChangeLog.tmp
mv ChangeLog.tmp ChangeLog

%build
CFLAGS=$RPM_OPT_FLAGS ./configure --libdir=%{_libdir} --includedir=%{_includedir} --prefix=%{_prefix}
make %{?_smp_mflags}

cd contrib/minizip
autoreconf --install
%configure  CPPFLAGS="-I/$RPM_BUILD_DIR/%{name}-%{version}-%{release}"
      LDFLAGS="-L/$RPM_BUILD_DIR/%{name}-%{version}-%{release}"

make %{?_smp_mflags}

%check
make test

%install
rm -rf ${RPM_BUILD_ROOT}

make install DESTDIR=$RPM_BUILD_ROOT

cd contrib/minizip
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

magic_rpm_clean.sh

%clean
rm -rf ${RPM_BUILD_ROOT}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post -n minizip -p /sbin/ldconfig

%postun -n minizip -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README FAQ
%{_libdir}/libz.so.*

%files devel
%defattr(-,root,root,-)
%doc doc/algorithm.txt example.c
%{_libdir}/libz.so
%{_includedir}/zconf.h
%{_includedir}/zlib.h
%{_mandir}/man3/zlib.3*
%{_libdir}/pkgconfig/zlib.pc

%files static
%defattr(-,root,root,-)
%{_libdir}/libz.a

%files -n minizip
%defattr(-,root,root,-)
%doc contrib/minizip/MiniZip64_info.txt contrib/minizip/MiniZip64_Changes.txt
%{_libdir}/libminizip.so.*

%files -n minizip-devel
%defattr(-,root,root,-)
%dir %{_includedir}/minizip
%{_includedir}/minizip/*.h
%{_libdir}/libminizip.so
%{_libdir}/pkgconfig/minizip.pc

%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1.2.5-5
- 为 Magic 3.0 重建

* Mon Apr 23 2012 Liu Di <liudidi@gmail.com> - 1.2.5-4
- 为 Magic 3.0 重建

* Tue Feb 28 2012 Liu Di <liudidi@gmail.com> - 1.2.5-3
- 为 Magic 3.0 重建

