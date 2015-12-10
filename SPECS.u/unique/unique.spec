Name:           unique
Version:        1.1.6
Release:        6%{?dist}
Summary:        Single instance support for applications
Summary(zh_CN.UTF-8):	应用程序的单一实例支持

Group:          System Environment/Libraries
Group(zh_CN.UTF-8):	系统环境/库
License:        LGPLv2+
URL:            http://www.gnome.org/~ebassi/source/
Source0:        http://www.gnome.org/~ebassi/source/libunique-%{version}.tar.bz2

# Fix build -- upstream dead (replaced with GtkApplication)
Patch0:    fix-unused-but-set-variable.patch
Patch1:    fix-disable-deprecated.patch
Patch2:	   libunique-1.1.6-format-security.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  dbus-glib-devel
BuildRequires:  gnome-doc-utils >= 0.3.2
BuildRequires:  libtool
BuildRequires:  glib2-devel >= 2.12.0
BuildRequires:  gtk2-devel >= 2.11.0

%description
Unique is a library for writing single instance applications, that is
applications that are run once and every further call to the same binary
either exits immediately or sends a command to the running instance.

%description -l zh_CN.UTF-8
Unique 是一个编写单一实例程序的库。

%package devel
Summary: Libraries and headers for Unique
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig
Requires: gtk-doc
Requires: dbus-glib-devel
Requires: gtk2-devel

%description devel
Headers and libraries for Unique.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n libunique-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%configure --enable-gtk-doc --disable-static --enable-introspection=no --enable-maintainer-flags=no
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README
%{_libdir}/lib*.so.*

%files devel
%defattr(-,root,root,-)
%doc %{_datadir}/gtk-doc/html/unique/
%{_includedir}/unique-1.0/
%{_libdir}/pkgconfig/*
%{_libdir}/lib*.so

%changelog
* Sat Nov 14 2015 Liu Di <liudidi@gmail.com> - 1.1.6-6
- 为 Magic 3.0 重建

* Thu Nov 05 2015 Liu Di <liudidi@gmail.com> - 1.1.6-5
- 为 Magic 3.0 重建

* Fri Oct 16 2015 Liu Di <liudidi@gmail.com> - 1.1.6-4
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1.1.6-3
- 为 Magic 3.0 重建

* Fri Oct 26 2012 Liu Di <liudidi@gmail.com> - 1.1.6-2
- 为 Magic 3.0 重建


