%define git 1
%define	gitdate	20120409

Summary:	Apple RAOP server library
Name:		libshairport
Version:	1.2.1
Release:	0.git%{gitdate}.1%{?dist}.1
License:	MIT
Group:		System/Libraries
URL:		https://github.com/amejia1/libshairport
# git archive --prefix libshairport-20120111/ master | xz > libshairport-20120111.tar.xz
Source:		%{name}-%{gitdate}.tar.xz
BuildRequires:	openssl-devel
BuildRequires:	libao-devel

%description
This library emulates an AirPort Express for the purpose of streaming
music from iTunes and compatible iPods. It implements a server for the
Apple RAOP protocol.

ShairPort does not support AirPlay v2 (video and photo streaming).

%package devel
Summary:	Headers for libshairport development
Group:		Development/C
Requires:	%{name} = %{version}
# we are not actually linking against it (just using the headers), so this
# doesn't get added automatically:
Requires:	libao-devel
Provides:	shairport-devel = %{version}

%description devel
libshairport is an Apple RAOP server library.

This package contains the headers that are needed to compile
applications that use libshairport.

%prep
%setup -q -n %{name}-%{gitdate}

%build
autoreconf -fi
%configure --disable-static
make

%install
rm -rf %{buildroot}
%makeinstall
rm -f %{buildroot}%{_libdir}/*.la

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%doc README
%{_libdir}/*.so
%dir %{_includedir}/shairport
%{_includedir}/shairport/*.h
%{_libdir}/pkgconfig/%{name}.pc



%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.2.1-0.git20120409.1.1
- 为 Magic 3.0 重建

