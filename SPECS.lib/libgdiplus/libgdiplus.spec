Name:           libgdiplus
Version:        2.10
Release:        5%{?dist}
Summary:        An Open Source implementation of the GDI+ API

Group:          System Environment/Libraries
License:        MIT
URL:            http://www.mono-project.com/Main_Page
Source0:        http://ftp.novell.com/pub/mono/sources/%{name}/%{name}-%{version}.tar.bz2
Patch0:		libgdiplus-2.10.1-libpng15.patch
Patch1:         libgdiplus-2.10-fix-freetype.patch
BuildRequires:  freetype-devel glib2-devel libjpeg-devel libtiff-devel
BuildRequires:  libungif-devel libpng-devel fontconfig-devel
BuildRequires:  cairo-devel giflib-devel libexif-devel
BuildRequires:  zlib-devel

%description
An Open Source implementation of the GDI+ API, it is part of the Mono 
Project

%package devel
Summary: Development files for libgdiplus
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
Development files for libgdiplus

%prep
%setup -q 
%patch0 
%patch1

%build
%configure --disable-static 
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} INSTALL="install -p"
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING NEWS README TODO AUTHORS ChangeLog
%{_libdir}/lib*.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/*
%{_libdir}/lib*.so

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 2.10-5
- 为 Magic 3.0 重建

* Wed Mar 28 2012 Liu Di <liudidi@gmail.com> - 2.10-4
- 为 Magic 3.0 重建

* Thu Dec 08 2011 Liu Di <liudidi@gmail.com> - 2.10-3
- 为 Magic 3.0 重建

