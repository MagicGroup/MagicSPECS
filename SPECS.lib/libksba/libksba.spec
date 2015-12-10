Summary: X.509 library
Summary(zh_CN.UTF-8): X.509 库
Name:    libksba
Version: 1.3.3
Release: 5%{?dist}

License: GPLv3
Group:   System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL:     http://www.gnupg.org/
Source0: ftp://ftp.gnupg.org/gcrypt/libksba/libksba-%{version}.tar.bz2
Source1: ftp://ftp.gnupg.org/gcrypt/libksba/libksba-%{version}.tar.bz2.sig
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Patch1: libksba-1.0.6-multilib.patch

BuildRequires: gawk
BuildRequires: libgpg-error-devel >= 1.8
BuildRequires: libgcrypt-devel >= 1.2.0

%description
KSBA is a library designed to build software based on the X.509 and
CMS protocols.

%description -l zh_CN.UTF-8
KSBA 是基于 X.509 和 CMS 协议的库。

%package devel
Summary: Development headers and libraries for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发头文件和库
Group:   Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
%description devel
%{summary}.
%description devel -l zh_CN.UTF-8
%{name} 的开发头文件和库。

%prep
%setup -q

%patch1 -p1 -b .multilib


%build
%configure \
  --disable-dependency-tracking \
  --disable-static

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_infodir}/dir
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.la


%check
make check


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post devel
install-info %{_infodir}/ksba.info %{_infodir}/dir ||:

%preun devel
if [ $1 -eq 0 ]; then
  install-info --delete %{_infodir}/ksba.info %{_infodir}/dir ||:
fi


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README* THANKS VERSION
%{_libdir}/libksba.so.8*

%files devel
%defattr(-,root,root,-)
%{_bindir}/ksba-config
%{_libdir}/libksba.so
%{_includedir}/ksba.h
%{_datadir}/aclocal/ksba.m4
%{_infodir}/ksba.info*


%changelog
* Mon Nov 09 2015 Liu Di <liudidi@gmail.com> - 1.3.3-5
- 为 Magic 3.0 重建

* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 1.3.3-4
- 更新到 1.3.3

* Fri Jul 18 2014 Liu Di <liudidi@gmail.com> - 1.3.0-3
- 更新到 1.3.0

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.2.0-3
- 为 Magic 3.0 重建

* Tue Jan 10 2012 Liu Di <liudidi@gmail.com> - 1.2.0-2
- 为 Magic 3.0 重建

