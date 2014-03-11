Summary: A toolkit for RTMP streams
Name: rtmpdump
Version: 2.3
Release: 3%{?dist}
License: GPLv2
Group: System Environment/Libraries
URL: http://rtmpdump.mplayerhq.hu/
Source0: http://rtmpdump.mplayerhq.hu/download/rtmpdump-%{version}.tgz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: openssl-devel

%description
rtmpdump is a toolkit for RTMP streams. All forms of RTMP are
supported, including rtmp://, rtmpt://, rtmpe://, rtmpte://, and
rtmps://.

%package libs
Summary: Shared libs for %{name}
Summary(zh_CN.UTF-8): %{name} 的共享库
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}

%description libs
Shared libraries for %{name}.

%description libs -l zh_CN.UTF-8
%{name} 的动态共享库。

%package static
Summary: Static libs for %{name}
Summary(zh_CN.UTF-8): %{name} 的静态库
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}

%description static
Static libraries for %{name}.

%description static -l zh_CN.UTF-8
%{name} 的静态库。

%package devel
Summary: Devel files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发文件
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}

%description devel
Devel files for %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发文件。

%prep
%setup -q

%build
make

%install
rm -rf %{buildroot}
make install \
  bindir=%{_bindir} \
  sbindir=%{_sbindir} \
  mandir=%{_mandir} \
  incdir=%{_includedir}/librtmp \
  libdir=%{_libdir} \
  DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc ChangeLog COPYING README
%{_bindir}/rtmpdump
%{_sbindir}/rtmpgw
%{_sbindir}/rtmpsrv
%{_sbindir}/rtmpsuck
%{_mandir}/man1/rtmpdump.1*
%{_mandir}/man8/rtmpgw.8*
%{_mandir}/man3/librtmp.3*

%files libs
%defattr(-,root,root,-)
%{_libdir}/librtmp.so.*

%files static
%defattr(-,root,root,-)
%{_libdir}/librtmp.a

%files devel
%defattr(-,root,root,-)
%{_libdir}/librtmp.so
%{_includedir}/librtmp/*.h
%{_libdir}/pkgconfig/*.pc

%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 2.3-3
- 为 Magic 3.0 重建

* Sun Feb 05 2012 Liu Di <liudidi@gmail.com> - 2.3-2
- 为 Magic 3.0 重建

* Mon Mar 14 2011 Axel Thimm <Axel.Thimm@ATrpms.net> - 2.3-1
- Initial build.

