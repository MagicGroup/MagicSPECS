
%define pkgname libmpeg2

Summary: libmpeg2 - Das MPEG2 Video Format
Summary(zh_CN.UTF-8): libmpeg2 - 处理MPEG2视频格式
Name: libmpeg2
Epoch: 1
Version: 0.5.1
Release: 6%{?dist}
License: GPL
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库 
Source: http://libmpeg2.sourceforge.net/files/%{pkgname}-%{version}.tar.gz
BuildRoot:     %{_tmppath}/%{name}-buildroot

%description
libmpeg2 is a free library for decoding mpeg-2 and mpeg-1 video streams.

%description -l zh_CN.UTF-8
libmpeg2是一个自由的库，可以解码mpeg-2和mpeg-1视频流。

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description    devel
This package contains libraries and header files for developing applications
that use %{name}

%prep
%setup -q -n %{pkgname}-%{version}

%build
%configure --enable-shared --enable-static
make

%install
make DESTDIR=$RPM_BUILD_ROOT install
rm -rf $RPM_BUILD_ROOT%{_libdir}/*.la

	   
%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man1/*1*

%changelog
* Mon Jan 07 2013 Liu Di <liudidi@gmail.com> - 1:0.5.1-6
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1:0.5.1-5
- 为 Magic 3.0 重建

* Sat Apr 07 2012 Liu Di <liudidi@gmail.com> - 1:0.5.1-4
- 为 Magic 3.0 重建

* Tue Jan 10 2012 Liu Di <liudidi@gmail.com> - 1:0.5.1-3
- 为 Magic 3.0 重建

* Wed Nov 08 2006 Liu Di <liudidi@gmail.com>
- update to 0.4.1

* Mon Oct 24 2005 KanKer <kanker@163.com>
- first spec
