%define library_version 1.0.6
Summary: A file compression utility
Summary(zh_CN.UTF-8): 一个文件压缩工具
Name: bzip2
Version: 1.0.6
Release: 9%{?dist}
License: BSD
Group: Applications/File
Group(zh_CN.UTF-8): 应用程序/文件
URL: http://www.bzip.org/
Source: http://www.bzip.org/%{version}/bzip2-%{version}.tar.gz
Patch0: bzip2-1.0.4-saneso.patch
Patch5: bzip2-1.0.4-cflags.patch
Patch6: bzip2-1.0.4-bzip2recover.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Bzip2 is a freely available, patent-free, high quality data compressor.
Bzip2 compresses files to within 10 to 15 percent of the capabilities 
of the best techniques available.  However, bzip2 has the added benefit 
of being approximately two times faster at compression and six times 
faster at decompression than those techniques.  Bzip2 is not the 
fastest compression utility, but it does strike a balance between speed 
and compression capability.

Install bzip2 if you need a compression utility.

%description -l zh_CN.UTF-8
这是一个自由的，高压缩率的压缩程序。它不是最快的压缩工具，但它在速度和压缩
率间取得了一个平衡。

一般来讲，这个包应该是系统必须安装的包。

%package devel
Summary: Header files developing apps which will use bzip2
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: bzip2-libs = %{version}-%{release}

%description devel

Header files and a library of bzip2 functions, for developing apps
which will use the library.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package static
Summary: Static Libraries for applications using bzip2
Summary(zh_CN.UTF-8): %{name} 的静态库
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: bzip2-devel = %{version}-%{release}

%description static
Static Libraries for applications using bzip2.

%description static -l zh_CN.UTF-8
%{name} 的静态库。

%package libs
Summary: Libraries for applications using bzip2
Summary(zh_CN.UTF-8): %{name} 的动态库
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%description libs

Libraries for applications using the bzip2 compression format.

%description libs -l zh_CN.UTF-8
%{name} 的动态库。

%prep
%setup -q 
%patch0 -p1 -b .saneso
%patch5 -p1 -b .cflags
%patch6 -p1 -b .bz2recover

%build

make -f Makefile-libbz2_so CC="%{__cc}" AR="%{__ar}" RANLIB="%{__ranlib}" \
	CFLAGS="$RPM_OPT_FLAGS -D_FILE_OFFSET_BITS=64 -fpic -fPIC" \
	%{?_smp_mflags} all

rm -f *.o
make CC="%{__cc}" AR="%{__ar}" RANLIB="%{__ranlib}" \
	CFLAGS="$RPM_OPT_FLAGS -D_FILE_OFFSET_BITS=64" \
	%{?_smp_mflags} all

%install
rm -rf ${RPM_BUILD_ROOT}

chmod 644 bzlib.h 
mkdir -p $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1,%{_libdir},%{_includedir}}
cp -p bzlib.h $RPM_BUILD_ROOT%{_includedir}
install -m 755 libbz2.so.%{library_version} $RPM_BUILD_ROOT/%{_libdir}
install -m 755 libbz2.a $RPM_BUILD_ROOT/%{_libdir}
install -m 755 bzip2-shared  $RPM_BUILD_ROOT%{_bindir}/bzip2
install -m 755 bzip2recover bzgrep bzdiff bzmore  $RPM_BUILD_ROOT%{_bindir}/
cp -p bzip2.1 bzdiff.1 bzgrep.1 bzmore.1  $RPM_BUILD_ROOT%{_mandir}/man1/
ln -s bzip2 $RPM_BUILD_ROOT%{_bindir}/bunzip2
ln -s bzip2 $RPM_BUILD_ROOT%{_bindir}/bzcat
ln -s bzdiff $RPM_BUILD_ROOT%{_bindir}/bzcmp
ln -s bzmore $RPM_BUILD_ROOT%{_bindir}/bzless
ln -s libbz2.so.%{library_version} $RPM_BUILD_ROOT/%{_libdir}/libbz2.so.1
ln -s libbz2.so.1 $RPM_BUILD_ROOT/%{_libdir}/libbz2.so
ln -s bzip2.1 $RPM_BUILD_ROOT%{_mandir}/man1/bzip2recover.1
ln -s bzip2.1 $RPM_BUILD_ROOT%{_mandir}/man1/bunzip2.1
ln -s bzip2.1 $RPM_BUILD_ROOT%{_mandir}/man1/bzcat.1
ln -s bzdiff.1 $RPM_BUILD_ROOT%{_mandir}/man1/bzcmp.1
ln -s bzmore.1 $RPM_BUILD_ROOT%{_mandir}/man1/bzless.1

magic_rpm_clean.sh

%post libs -p /sbin/ldconfig

%postun libs  -p /sbin/ldconfig

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root,-)
%doc LICENSE CHANGES README 
%{_bindir}/*
%{_mandir}/*/*

%files libs
%defattr(-,root,root,-)
%doc LICENSE
%{_libdir}/*so.*

%files devel
%defattr(-,root,root,-)
%doc manual.html manual.pdf
%{_includedir}/*
%{_libdir}/*so

%files static
%defattr(-,root,root,-)
%{_libdir}/*.a

%changelog
* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 1.0.6-9
- 为 Magic 3.0 重建

* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 1.0.6-8
- 为 Magic 3.0 重建

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 1.0.6-6
- 为 Magic 3.0 重建

* Thu Apr 12 2012 Liu Di <liudidi@gmail.com> - 1.0.6-5
- 为 Magic 3.0 重建


