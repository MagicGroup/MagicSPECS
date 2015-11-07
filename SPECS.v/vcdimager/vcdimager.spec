Summary: VideoCD (pre-)mastering and ripping tool
Summary(zh_CN): 视频光盘处理和抓取工具
Name: vcdimager
Version: 0.7.24
Release: 7%{?dist}
License: GPLv2+
Group: Applications/Multimedia
Group(zh_CN): 应用程序/多媒体
URL: http://www.gnu.org/software/vcdimager/
Source: ftp://ftp.gnu.org/pub/gnu/vcdimager/vcdimager-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires(post): info
Requires(preun): info
BuildRequires: libcdio-devel >= 0.72
BuildRequires: libxml2-devel >= 2.3.8
BuildRequires: zlib-devel
BuildRequires: pkgconfig >= 0.9
BuildRequires: popt-devel

Requires: %{name}-libs = %{version}-%{release}

%description
VCDImager allows you to create VideoCD BIN/CUE CD images from MPEG
files. These can be burned with cdrdao or any other program capable of
burning BIN/CUE files.

Also included is VCDRip which does the reverse operation, that is to
rip MPEG streams from images or burned VideoCDs and to show
information about a VideoCD.

%description -l zh_CN
VCDImager 允许你从 MPEG 文件建立 VideoCD 类似的 BIN/CUE 镜像，以便于
刻录。

同时也包括了做相反事情的 VCDRip。

%package libs
Summary:        Libraries for %{name}
Summary(zh_CN): %name 的库
Group:          System Environment/Libraries
Group(zh_CN):	系统环境/库
Requires:       %{name} = %{version}-%{release}
# Introduced in F-9 to solve multilibs transition
Obsoletes:      vcdimager < 0.7.23-8

%description libs
The %{name}-libs package contains shared libraries for %{name}.

%description libs -l zh_CN
%name 的库

%package devel
Summary: Header files and static library for VCDImager
Summary(zh_CN): %name 的开发包
Group: Development/Libraries
Group(zh_CN): 开发/库
Requires: %{name}-libs = %{version}-%{release}

Requires: pkgconfig
Requires: libcdio-devel

%description devel
VCDImager allows you to create VideoCD BIN/CUE CD images from mpeg
files which can be burned with cdrdao or any other program capable of
burning BIN/CUE files.

This package contains the header files and a static library to develop
applications that will use VCDImager.

%description devel -l zh_CN
%name 的开发包。

%prep
%setup -q


%build
%configure --disable-static --disable-dependency-tracking
%{__make} %{?_smp_mflags}


%install
%{__rm} -rf %{buildroot}
%{__make} DESTDIR=%{buildroot} install INSTALL="install -p"
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'

# Sometimes this file gets created... but we don't want it!
%{__rm} -f %{buildroot}%{_infodir}/dir


%clean
%{__rm} -rf %{buildroot}


%post libs -p /sbin/ldconfig

%post
for infofile in vcdxrip.info vcdimager.info vcd-info.info; do
  /sbin/install-info %{_infodir}/${infofile} %{_infodir}/dir 2>/dev/null || :
done

%preun
if [ $1 -eq 0 ]; then
  for infofile in vcdxrip.info vcdimager.info vcd-info.info; do
    /sbin/install-info --delete %{_infodir}/${infofile} %{_infodir}/dir \
      2>/dev/null || :
  done
fi

%postun libs -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS BUGS ChangeLog* COPYING FAQ NEWS README THANKS TODO
%doc frontends/xml/videocd.dtd
%{_bindir}/*
%{_infodir}/vcdxrip.info*
%{_infodir}/vcdimager.info*
%{_infodir}/vcd-info.info*
%{_mandir}/man1/*

%files libs
%defattr(-,root,root,-)
%{_libdir}/libvcdinfo.so.*

%files devel
%defattr(-,root,root,-)
%doc HACKING
%{_includedir}/libvcd/
%{_libdir}/libvcdinfo.so
%{_libdir}/pkgconfig/libvcdinfo.pc


%changelog
* Thu Nov 05 2015 Liu Di <liudidi@gmail.com> - 0.7.24-7
- 为 Magic 3.0 重建

* Sat Oct 17 2015 Liu Di <liudidi@gmail.com> - 0.7.24-6
- 为 Magic 3.0 重建

* Tue Sep 22 2015 Liu Di <liudidi@gmail.com> - 0.7.24-5
- 为 Magic 3.0 重建

* Sun May 04 2014 Liu Di <liudidi@gmail.com> - 0.7.24-4
- 为 Magic 3.0 重建

* Tue Jan 15 2013 Liu Di <liudidi@gmail.com> - 0.7.24-3
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 0.7.24-2
- 为 Magic 3.0 重建


