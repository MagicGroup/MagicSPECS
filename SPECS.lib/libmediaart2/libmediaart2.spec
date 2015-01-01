%define real_name libmediaart
Name:           libmediaart2
Version:	1.9.0
Release:        2%{?dist}
Summary:        Library for managing media art caches
Summary(zh_CN.UTF-8): 管理媒体缓存的库

License:        LGPLv2+
URL:            https://github.com/curlybeast/libmediaart
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source0:        https://download.gnome.org/sources/%{real_name}/%{majorver}/%{real_name}-%{version}.tar.xz

BuildRequires:  pkgconfig(glib-2.0) pkgconfig(gio-2.0) pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
BuildRequires:  vala-tools vala-devel
#for the autoreconf
BuildRequires:  automake autoconf libtool


%description
Library tasked with managing, extracting and handling media art caches.

%description -l zh_CN.UTF-8
管理媒体缓存的库。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n %{real_name}-%{version}
autoreconf -fi


%build
%configure --disable-static \
  --enable-gdkpixbuf \
  --disable-qt
make %{?_smp_mflags}


%install
%make_install
find $RPM_BUILD_ROOT -name '*.la' -delete -print
#与 libmediaart 冲突
mv %{buildroot}%{_datadir}/gtk-doc/html/libmediaart %{buildroot}%{_datadir}/gtk-doc/html/libmediaart2
magic_rpm_clean.sh

#check
# requires X
#make check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc AUTHORS COPYING.LESSER NEWS
%{_libdir}/libmediaart-2.0.so.*
%{_libdir}/girepository-1.0/MediaArt-2.0.typelib

%files devel
%{_includedir}/libmediaart-2.0
%{_libdir}/libmediaart-2.0.so
%{_libdir}/pkgconfig/libmediaart-2.0.pc
%{_datadir}/gir-1.0/MediaArt-2.0.gir
%{_datadir}/gtk-doc/html/libmediaart2
%{_datadir}/vala/vapi/libmediaart-2.0.vapi


%changelog
* Thu Dec 25 2014 Liu Di <liudidi@gmail.com> - 1.9.0-2
- 为 Magic 3.0 重建

* Thu Dec 25 2014 Liu Di <liudidi@gmail.com> - 1.9.0-1
- 更新到 1.9.0

* Fri Jul 18 2014 Liu Di <liudidi@gmail.com> - 0.4.0-1
- 更新到 0.4.0

* Sat Feb  8 2014 Yanko Kaneti <yaneti@declera.com> - 0.2.0-4
- Add patches to avoid unnecessary linkage

* Sat Feb  8 2014 Yanko Kaneti <yaneti@declera.com> - 0.2.0-3
- Incorporate most changes suggested in the review (#1062686)

* Fri Feb  7 2014 Yanko Kaneti <yaneti@declera.com> - 0.2.0-2
- Qt can be ignored, its only there for systems without gdk-pixbuf

* Fri Feb  7 2014 Yanko Kaneti <yaneti@declera.com> - 0.2.0-1
- Initial attempt
