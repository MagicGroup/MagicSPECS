%global glib2_version 2.31.0
%global libsoup_version 2.37.91

# Packagers: This is the API version of libuhttpmock, as it allows
# for parallel installation of different major API versions (e.g. like
# GTK+ 2 and 3).
%global uhm_api_version 0.0

Name:           uhttpmock
Version:	0.5.0
Release:	3%{?dist}
Summary:        HTTP web service mocking library
Summary(zh_CN.UTF-8): HTTP 网页服务模仿库
License:        LGPLv2
URL:            https://gitlab.com/groups/uhttpmock
Source0:        https://tecnocode.co.uk/downloads/uhttpmock/uhttpmock-%{version}.tar.xz

BuildRequires:  glib2-devel >= %{glib2_version}
BuildRequires:  libsoup-devel >= %{libsoup_version}
BuildRequires:  intltool
BuildRequires:  gobject-introspection-devel
BuildRequires:  gtk-doc
BuildRequires:  vala-tools
BuildRequires:  vala-devel

Requires:       glib2%{?_isa} >= %{glib2_version}
Requires:       libsoup%{?_isa} >= %{libsoup_version}

%description
uhttpmock is a project for mocking web service APIs which use HTTP or HTTPS.
It provides a library, libuhttpmock, which implements recording and
playback of HTTP request–response traces.

%description -l zh_CN.UTF-8
HTTP 网页服务模仿库。

%package devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains libraries, header files and documentation for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

%build
%configure \
    --enable-gtk-doc \
    --enable-introspection \
    --enable-vala=yes \
    --disable-static
make %{?_smp_mflags}

%check
make check

%install
make DESTDIR=$RPM_BUILD_ROOT install

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
magic_rpm_clean.sh

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%license COPYING
%doc README NEWS AUTHORS
%{_libdir}/libuhttpmock-%{uhm_api_version}.so.0*
%{_libdir}/girepository-1.0/Uhm-%{uhm_api_version}.typelib

%files devel
%{_libdir}/libuhttpmock-%{uhm_api_version}.so
%{_includedir}/libuhttpmock-%{uhm_api_version}/
%{_libdir}/pkgconfig/libuhttpmock-%{uhm_api_version}.pc
%{_datadir}/gir-1.0/Uhm-%{uhm_api_version}.gir
%{_datadir}/vala/vapi/libuhttpmock-%{uhm_api_version}.deps
%{_datadir}/vala/vapi/libuhttpmock-%{uhm_api_version}.vapi
%doc %{_datadir}/gtk-doc/html/libuhttpmock-%{uhm_api_version}/


%changelog
* Sat Nov 14 2015 Liu Di <liudidi@gmail.com> - 0.5.0-3
- 为 Magic 3.0 重建

* Thu Nov 05 2015 Liu Di <liudidi@gmail.com> - 0.5.0-2
- 为 Magic 3.0 重建

* Fri Oct 16 2015 Liu Di <liudidi@gmail.com> - 0.5.0-1
- 更新到 0.5.0

* Wed Jul 16 2014 Liu Di <liudidi@gmail.com> - 0.3.0-2
- 为 Magic 3.0 重建

* Sun Jun 22 2014 Philip Withnall <philip@tecnocode.co.uk> - 0.3.0-1
- Update to 0.3.0

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Nov 05 2013 Philip Withnall <philip.withnall@collabora.co.uk> - 0.2.0-1
- Initial spec file for version 0.2.0.
