Summary: Experimental D-Bus bindings for GObject
Summary(zh_CN): GObject 的不稳定 D-Bus 绑定
Name: eggdbus
Version: 0.6
Release: 3%{?dist}
License: LGPLv2
Group: Development/Libraries
Group(zh_CN): 开发/库
URL: http://cgit.freedesktop.org/~david/eggdbus
Source0: http://people.freedesktop.org/~david/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: glib2-devel
BuildRequires: dbus-devel
BuildRequires: dbus-glib-devel
BuildRequires: gtk-doc

%description
Experimental D-Bus bindings for GObject.

%description -l zh_CN
GObject 的不稳定 D-Bus 绑定.

%package devel
Summary: Development files for EggDBus
Summary(zh_CN): %name 的开发包
Group: Development/Libraries
Group(zh_CN): 开发/库
Requires: %name = %{version}-%{release}
Requires: pkgconfig
Requires: glib2-devel
Requires: gtk-doc

%description devel
Development files for EggDBus.

%description devel -l zh_CN
%name 的开发包.

%prep
%setup -q

%build
%configure --enable-gtk-doc --disable-static
make %{?_smp_mflags}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -rf $RPM_BUILD_ROOT%{_datadir}/gtk-doc/html/tests
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING
%{_libdir}/lib*.so.*

%files devel
%defattr(-,root,root)

%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_datadir}/gtk-doc/html/eggdbus
%{_datadir}/man/man1/*
%{_bindir}/*

%changelog
* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 0.6-3
- 为 Magic 3.0 重建


