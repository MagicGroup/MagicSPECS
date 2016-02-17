%define binname aria2c

Name:           aria2
Version:	1.19.3
Release:        1%{?dist}
Summary:        High speed download utility with resuming and segmented downloading
Summary(zh_CN): 可续传和分段下载的高速下载工具
Group:          Applications/Internet
Group(zh_CN):	应用程序/互联网
License:        GPLv2
URL:            http://aria2.sourceforge.net/
Source0:        https://github.com/tatsuhiro-t/%{name}/releases/download/release-%{version}/%{name}-%{version}.tar.xz
Patch0:		aria2-1.19.3-use-system-wide-crypto-policies.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  bison
BuildRequires:  c-ares-devel cppunit-devel
BuildRequires:  gettext gnutls-devel
BuildRequires:  libgcrypt-devel libxml2-devel
BuildRequires:  sqlite-devel

%description
aria2 is a download utility with resuming and segmented downloading.
Supported protocols are HTTP/HTTPS/FTP/BitTorrent. It also supports Metalink
version 3.0.

Currently it has following features:
- HTTP/HTTPS GET support
- HTTP Proxy support
- HTTP BASIC authentication support
- HTTP Proxy authentication support
- FTP support(active, passive mode)
- FTP through HTTP proxy(GET command or tunneling)
- Segmented download
- Cookie support(currently aria2 ignores "expires")
- It can run as a daemon process.
- BitTorrent protocol support with fast extension.
- Selective download in multi-file torrent
- Metalink version 3.0 support(HTTP/FTP/BitTorrent).
- Limiting download/upload speed

%description -l zh_CN
可续传和分段下载的高速下载工具。

%prep
%setup -q
%patch0 -p1

%build
autoreconf -fisv
%configure --enable-bittorrent \
           --enable-metalink \
           --enable-epoll\
	   --enable-threads=posix \
           --disable-rpath \
           --with-gnutls \
           --with-libcares \
           --with-libxml2 \
           --with-openssl \
           --with-libz \
           --with-sqlite3 \
           --disable-dependency-tracking \


make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
magic_rpm_clean.sh
%find_lang %{name}
rm -f $RPM_BUILD_ROOT%{_datadir}/locale/locale.alias
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/%{name}

%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README 
%{_bindir}/%{binname}
%{_mandir}/man*/*



%changelog
* Sat Feb 06 2016 Liu Di <liudidi@gmail.com> - 1.19.0-8
- 为 Magic 3.0 重建

* Sat Feb 06 2016 Liu Di <liudidi@gmail.com> - 1.19.0-7
- 为 Magic 3.0 重建

* Sat Feb 06 2016 Liu Di <liudidi@gmail.com> - 1.19.0-6
- 为 Magic 3.0 重建

* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 1.19.0-5
- 为 Magic 3.0 重建

* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 1.19.0-4
- 更新到 1.19.0

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 1.13.0-2
- 为 Magic 3.0 重建

* Sun Oct 30 2011 Liu Di <liudidi@gmail.com> - 1.13.0
- 升级到 1.13.0
