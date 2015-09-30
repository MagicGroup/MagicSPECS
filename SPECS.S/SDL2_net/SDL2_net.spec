Name:		SDL2_net
Version:	2.0.0
Release:	6%{?dist}
Summary:	SDL portable network library
Summary(zh_CN.UTF-8): SDL 可移植网络库
License:	zlib
URL:		http://www.libsdl.org/projects/SDL_net/
Source0:	http://www.libsdl.org/projects/SDL_net/release/%{name}-%{version}.tar.gz
BuildRequires:	SDL2-devel >= 2.0

%description
This is a portable network library for use with SDL.
%description -l zh_CN.UTF-8
SDL 可移植网络库。

%package	devel
Summary:	Libraries and includes to develop SDL networked applications
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	SDL2-devel%{?_isa} >= 2.0

%description	devel
This is a portable network library for use with SDL.

This is the libraries and include files you can use to develop SDL
networked applications.
%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q
# Fix end-of-line encoding
sed -i 's/\r//' README.txt CHANGES.txt COPYING.txt

%build
%configure --disable-static --disable-gui
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -exec rm -f {} ';'
magic_rpm_clean.sh

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc README.txt CHANGES.txt COPYING.txt
%{_libdir}/lib*.so.*

%files devel
%{_libdir}/lib*.so
%{_includedir}/SDL2/*
%{_libdir}/pkgconfig/*.pc

%changelog
* Wed Sep 30 2015 Liu Di <liudidi@gmail.com> - 2.0.0-6
- 为 Magic 3.0 重建

* Wed Sep 30 2015 Liu Di <liudidi@gmail.com> - 2.0.0-5
- 为 Magic 3.0 重建

* Mon Sep 07 2015 Liu Di <liudidi@gmail.com> - 2.0.0-4
- 为 Magic 3.0 重建

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jun 9 2014 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.0.0-1
- Initial spec based on upstream provided sample spec file (#1107250)
