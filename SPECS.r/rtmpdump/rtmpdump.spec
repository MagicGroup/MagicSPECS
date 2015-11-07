%global commit dc76f0a8461e6c8f1277eba58eae201b2dc1d06a
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global gitdate 20131205

Name:           rtmpdump
Version:        2.4
Release:        5.%{gitdate}.git%{shortcommit}%{?dist}
Summary:        Toolkit for RTMP streams
Summary(zh_CN.UTF-8): RTMP 流媒体工具

Group:          Applications/Internet
Group(zh_CN.UTF-8): 应用程序/互联网
# The tools are GPLv2+. The library is LGPLv2+, see below.
License:        GPLv2+
URL:            http://rtmpdump.mplayerhq.hu/
Source0:        http://repo.or.cz/w/rtmpdump.git/snapshot/%{commit}.tar.gz

BuildRequires:  gnutls-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  zlib-devel
BuildRequires:  nettle-devel

%description
rtmpdump is a toolkit for RTMP streams. All forms of RTMP are supported,
including rtmp://, rtmpt://, rtmpe://, rtmpte://, and rtmps://. 

%description -l zh_CN.UTF-8
RTMP 流媒体工具。

%package -n librtmp
Summary:        Support library for RTMP streams
Summary(zh_CN.UTF-8): %{name} 的运行库
Group:          Applications/Internet
Group(zh_CN.UTF-8): 应用程序/互联网
License:        LGPLv2+

%description -n librtmp
librtmp is a support library for RTMP streams. All forms of RTMP are supported,
including rtmp://, rtmpt://, rtmpe://, rtmpte://, and rtmps://. 

%description -n librtmp -l zh_CN.UTF-8
%{name} 的运行库。

%package -n librtmp-devel
Summary:        Files for librtmp development
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Applications/Internet
Group(zh_CN.UTF-8): 应用程序/互联网
License:        LGPLv2+
Requires:       librtmp%{?_isa} = %{version}-%{release}

%description -n librtmp-devel
librtmp is a support library for RTMP streams. The librtmp-devel package
contains include files needed to develop applications using librtmp.
%description -n librtmp-devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n %{name}

%build
# The fact that we have to add -ldl for gnutls is Fedora bug #611318
make SYS=posix CRYPTO=GNUTLS SHARED=yes OPT="%{optflags}" LIB_GNUTLS="-lgnutls -lgcrypt -ldl"

%install
make CRYPTO=GNUTLS SHARED=yes DESTDIR=%{buildroot} prefix=%{_prefix} mandir=%{_mandir} libdir=%{_libdir} install
rm -f %{buildroot}%{_libdir}/librtmp.a

%post -n librtmp -p /sbin/ldconfig
%postun -n librtmp -p /sbin/ldconfig

%files
%doc COPYING README
%{_bindir}/rtmpdump
%{_sbindir}/rtmpsrv
%{_sbindir}/rtmpgw
%{_sbindir}/rtmpsuck
%{_mandir}/man1/rtmpdump.1*
%{_mandir}/man8/rtmpgw.8*

%files -n librtmp
%doc librtmp/COPYING ChangeLog
%{_libdir}/librtmp.so.1

%files -n librtmp-devel
%{_includedir}/librtmp/
%{_libdir}/librtmp.so
%{_libdir}/pkgconfig/librtmp.pc
%{_mandir}/man3/librtmp.3*

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 2.4-5.20131205.gitdc76f0a
- 为 Magic 3.0 重建

* Wed Oct 21 2015 Liu Di <liudidi@gmail.com> - 2.4-4.20131205.gitdc76f0a
- 为 Magic 3.0 重建

* Mon Sep 01 2014 Sérgio Basto <sergio@serjux.com> - 2.4-3.20131205.gitdc76f0a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Apr 26 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.4-2.20131205.gitdc76f0a
- Rebuilt for libgcrypt

* Sun Jan 5 2014 Susi Lehtola <jussilehtola@fedoraproject.org> - 2.4-1.20131205.gitdc76f0a
- Update to newest snapshot.
- Clean up spec file.

* Sun Mar 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.4-0.3.20110811gitc58cfb3e
- Mass rebuilt for Fedora 19 Features

* Wed Jan 25 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.4-0.2.20110811gitc58cfb3e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Aug 29 2011 David Woodhouse <dwmw2@infradead.org> 2.4-0.1.20110811gitc58cfb3e
- Update to almost-2.4 snapshot

* Sun Jul 04 2010 Dominik Mierzejewski <rpm@greysector.net> 2.3-2
- call ldconfig in post(un) scripts for the shared library
- add strict dependency on the library to -devel

* Sun Jul 04 2010 David Woodhouse <dwmw2@infradead.org> 2.3-1
- Update to 2.3; build shared library

* Fri Apr 30 2010 David Woodhouse <dwmw2@infradead.org> 2.2d-1
- Update to 2.2d

* Tue Apr 20 2010 David Woodhouse <dwmw2@infradead.org> 2.2c-2
- Link with libgcrypt explicitly since we call it directly

* Mon Apr 19 2010 David Woodhouse <dwmw2@infradead.org> 2.2c-1
- Initial package
