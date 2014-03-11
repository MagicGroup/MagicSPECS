Summary: Fast Assembly MPEG Encoding library
Summary(zh_CN.UTF-8): 快速汇编MPEG编码库
Name: libfame
Version: 0.9.1
Release: 5%{?dist}
License: LGPL
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL: http://fame.sourceforge.net/
Packager: Liu Di <liudidi@gmail.com>
Vendor: MagicGroup

Source: http://dl.sf.net/fame/libfame-%{version}.tar.gz
Patch0: libfame-0.9.1-fstrict-aliasing.patch
Patch1: http://www.linuxfromscratch.org/blfs/downloads/svn/libfame-0.9.1-gcc34-1.patch
Patch2: libfame-0.9.1-underquoted.patch
Patch3: libfame-0.9.1-x86_64.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: autoconf, automake, libtool

%description
A library for fast (real-time) MPEG video encoding, written in C and assembly.
It currently allows encoding of fast MPEG-1 video, as well as MPEG-4 (OpenDivX
compatible) rectangular and arbitrary shaped video.

%description -l zh_CN.UTF-8
一个快速(实时)MPEG视频编码库，用C和汇编写成。
它当前可以快速编码MPEG-1视频，也可以编码矩形或任意形状的MPEG-4（兼容OpenDivX）。


%package devel
Summary: Development files and static libraries for libfame
Summary(zh_CN.UTF-8): libfame的开发文件和静态库
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}

%description devel
A library for fast (real-time) MPEG video encoding, written in C and assembly.
It currently allows encoding of fast MPEG-1 video, as well as MPEG-4 (OpenDivX
compatible) rectangular and arbitrary shaped video.

This package contains the files necessary to build programs that use the
libfame library.

%description devel -l zh_CN.UTF-8
一个快速(实时)MPEG视频编码库，用C和汇编写成。
它当前可以快速编码MPEG-1视频，也可以编码矩形或任意形状的MPEG-4（兼容OpenDivX）。

这个包包含了建立使用libfame库的程序所需要的文件。

%prep
%setup
%patch0 -p1 -b .fstrict-aliasing
%patch1 -p1 -b .mmxone
%patch2 -p1 -b .m4
%patch3 -p1 -b .x86_64
# This is required since the included libtool stuff is too old and breaks
# linking (-lm and -lc functions not found!) on FC5 x86_64.
%{__rm} -f acinclude.m4 aclocal.m4
%{__cp} -f /usr/share/aclocal/libtool.m4 libtool.m4
touch NEWS ChangeLog
autoreconf --force --install

# Fix lib stuff for lib64
%{__perl} -pi.orig -e 's|/lib"|/%{_lib}"|g' configure.in


%build
# Compile a special MMX & SSE enabled lib first
%ifarch %{ix86}
    %configure --enable-sse --enable-mmx
    %{__make} %{?_smp_mflags}
    %{__mkdir} sse2/
    %{__mv} src/.libs/libfame*.so.* sse2/
    %{__make} clean

# Now, the normal build
    %configure --disable-mmx
%else
    %configure
%endif

%{__make} %{?_smp_mflags}


%install
%{__rm} -rf %{buildroot}
%makeinstall

# Install the MMX & SSE build in its special dir
%ifarch %{ix86}
    %{__mkdir_p} %{buildroot}%{_libdir}/sse2
    %{__cp} -ap sse2/* %{buildroot}%{_libdir}/sse2/
%endif

# Workaround for direct <libfame/fame.h> includes (include/libfame -> .)
%{__ln_s} . %{buildroot}%{_includedir}/%{name}


%clean
%{__rm} -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-, root, root, 0755)
%doc AUTHORS BUGS CHANGES COPYING README TODO
%{_libdir}/*.so.*
%ifarch %{ix86}
    %{_libdir}/sse2/*.so.*
%endif

%files devel
%defattr(-, root, root, 0755)
%{_bindir}/%{name}-config
%{_libdir}/*.a
%exclude %{_libdir}/*.la
%{_libdir}/*.so
%{_includedir}/*
%{_datadir}/aclocal/%{name}.m4
%{_mandir}/man3/*


%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.9.1-5
- 为 Magic 3.0 重建

* Sat Jan 07 2012 Liu Di <liudidi@gmail.com> - 0.9.1-4
- 为 Magic 3.0 重建

* Mon Oct 09 2006 Liu Di <liudidi@gmail.com> - 0.9.1-1mgc
- rebuild for Magic
