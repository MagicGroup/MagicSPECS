Summary: Decoder of various derivatives of MPEG standards
Summary(zh_CN.UTF-8): 多种 MPEG 衍生标准的解码器
Name: libmpeg3
Version: 1.8
Release: 1%{?dist}
License: GPL
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL: http://heroinewarrior.com/libmpeg3.php3
Source0: http://dl.sf.net/heroines/libmpeg3-%{version}-src.tar.bz2
Source1: libmpeg3.pc
Patch0: libmpeg3.sharedlibs.patch
Patch2:	libmpeg3-1.8-fixformatsecurity.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: nasm

%description
LibMPEG3 decodes the many many derivatives of MPEG standards into
uncompressed data suitable for editing and playback.

libmpeg3 currently decodes:
 - MPEG-1 Layer II/III Audio and program streams
 - MPEG-2 Layer III Audio, program streams and transport streams
 - MPEG-1 and MPEG-2 Video
 - AC3 Audio
 - IFO files
 - VOB files

%description -l zh_CN.UTF-8
LibMPEG3解码许多MPEG标准派生出的标准到未压缩数据以便于编辑和播放。

libmpeg3当前解码：
 - MPEG-1 层 II/II 音频和程序流
 - MPEG-2 层 III 音频，程序流和传输流
 - MPEG-1 和 MPEG-2 视频
 - AC3音频
 - IFO文件
 - VOB文件

%package devel
Summary: Development files for libmpeg3
Summary(zh_CN.UTF-8): libmpeg3的开发文件
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库

%description devel
LibMPEG3 decodes the many many derivatives of MPEG standards into
uncompressed data suitable for editing and playback.

This package contains files needed to build applications that will use
libmpeg3.

%description devel -l zh_CN.UTF-8
LibMPEG3解码许多MPEG标准派生出的标准到未压缩数据以便于编辑和播放。

这个包包含了使用libmpeg3开发应用程序所需要的文件。

%prep
%setup
%patch0 -p1 -b .makefile
%patch2 -p1

%build
export OBJDIR=i686
export CFLAGS="%{optflags} -fPIC"

#./configure --prefix=/usr
make

%install
%{__rm} -rf %{buildroot}
%ifarch %{ix86}
export OBJDIR=i686
%endif
%{__make} install \
    DESTDIR=%{buildroot} LIBDIR=%{_lib}

mkdir -p %{buildroot}%{_libdir}/pkgconfig
%ifarch x86_64
sed -i 's/\/usr\/lib/\/usr\/lib64/g' %{SOURCE1}
%endif
install -m 0644 %{SOURCE1} %{buildroot}%{_libdir}/pkgconfig/libmpeg3.pc

%clean
%{__rm} -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-, root, root, 0755)
%doc COPYING
%{_bindir}/*
%{_libdir}/libmpeg3.so.*

%files devel
%defattr(-, root, root, 0755)
%doc docs/*
%{_libdir}/*.so
%{_includedir}/*.h
%{_includedir}/audio/*.h
%{_includedir}/video/*.h
%{_libdir}/pkgconfig/libmpeg3.pc


%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.7-3
- 为 Magic 3.0 重建

* Tue Jan 10 2012 Liu Di <liudidi@gmail.com> - 1.7-2
- 为 Magic 3.0 重建

* Thu Jan 04 2007 Liu Di <liudidi@gmail.com> - 1.7-1mgc
- update to 1.7

* Tue May 11 2006 KanKer <kanker@163.com> 1.6-1mgc
- Initial package.
