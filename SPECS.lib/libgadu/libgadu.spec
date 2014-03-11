Name:       libgadu
Version:    1.11.0
Release:    3%{?dist}
Summary:    A Gadu-gadu protocol compatible communications library
Summary(zh_CN.UTF-8): Gadu-gadu 协议兼容通讯库
License:    LGPLv2
Group:      System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Source0:    http://toxygen.net/libgadu/files/%{name}-%{version}.tar.gz
URL:        http://toxygen.net/libgadu/
BuildRequires:  openssl-devel
BuildRoot:  %{_tmppath}/%{name}-%{version}-root-%(id -u -n)

%description
libgadu is intended to make it easy to add Gadu-Gadu communication
support to your software.

%description -l zh_CN.UTF-8
libgadu 旨在让您向您的软件添加 Gadu-gadu 通讯支持更加容易简单。

%package devel
Summary:    Libgadu development library
Summary(zh_CN.UTF-8): Libgadu 开发库
Group:      Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:   %{name} = %{version}-%{release}
Requires:   openssl-devel
Requires:   pkgconfig

%description devel
The %{name}-devel package contains the header files and some
documentation needed to develop application with %{name}.

%description devel -l zh_CN.UTF-8
%{name}-devel 软件包包含了使用 %{name} 开发应用程序所需的
头文件和一些文档。

%prep
%setup -q

%build
%configure \
    --disable-static \
    --with-pthread

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}
%{__make} install INSTALL="install -p" DESTDIR=%{buildroot}

rm -f %{buildroot}%{_libdir}/*.la

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING
%attr(755,root,root) %{_libdir}/libgadu.so.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgadu.so
%{_includedir}/libgadu.h
%{_libdir}/pkgconfig/*

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.11.0-3
- 为 Magic 3.0 重建

* Sat Jan 07 2012 Liu Di <liudidi@gmail.com> - 1.11.0-2
- 为 Magic 3.0 重建

* Sat Apr 4 2009 Ni Hui <shuizhuyuanluo@126.com> - 1.8.2-1mgc
- rebuild for Magic Linux 2.4+(imported from fedora project)
- 己丑  三月初九  [清明]
