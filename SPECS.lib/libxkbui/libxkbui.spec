Summary: X.Org X11 libxkbui runtime library
Summary(zh_CN.UTF-8): X.Org X11 libxkbui 运行库
Name: libxkbui
Version: 1.0.2
Release: 7%{?dist}
License: MIT/X11
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL: http://www.x.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0: ftp://ftp.x.org/pub/individual/lib/libxkbui/%{name}-%{version}.tar.bz2

BuildRequires: pkgconfig
BuildRequires: xorg-x11-proto-devel
BuildRequires: libX11-devel

Obsoletes: xorg-x11-libs < 7.1-1mgc

%description
X.Org X11 libxkbui runtime library

%description -l zh_CN.UTF-8
X.Org X11 libxkbui 运行库

%package devel
Summary: X.Org X11 libxkbui development package
Summary(zh_CN.UTF-8): X.Org X11 libxkbui 开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}

# needed by xkbfile.pc
BuildRequires: xorg-x11-proto-devel

Obsoletes: xorg-x11-devel < 7.1-1mgc

%description devel
X.Org X11 libxkbui development package

%description devel -l zh_CN.UTF-8
X.Org X11 libxkbui 开发包

%prep
%setup -q

# Disable static library creation by default.
%define with_static 0

%build
# FIXME: We use -fno-strict-aliasing, to work around the following bug:
# maprules.c:1373: warning: dereferencing type-punned pointer will break strict-aliasing rules)
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
%configure \
%if ! %{with_static}
	--disable-static
%endif
make

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# We intentionally don't ship *.la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README INSTALL ChangeLog
%{_libdir}/libxkbui.so.1
%{_libdir}/libxkbui.so.1.0.0

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/X11
%dir %{_includedir}/X11/extensions
%{_includedir}/X11/extensions/XKBui.h
%if %{with_static}
%{_libdir}/libxkbui.a
%endif
%{_libdir}/libxkbui.so
%{_libdir}/pkgconfig/xkbui.pc

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.0.2-7
- 为 Magic 3.0 重建

* Thu Jan 12 2012 Liu Di <liudidi@gmail.com> - 1.0.2-6
- 为 Magic 3.0 重建

* Thu Jan 12 2012 Liu Di <liudidi@gmail.com> - 1.0.2-5
- 为 Magic 3.0 重建

* Sat Aug 26 2006 KanKer <kanker@163.com> 1.0.1-1mgc
- Initial build.
