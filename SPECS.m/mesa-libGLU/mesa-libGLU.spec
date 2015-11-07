#define gitdate 20120904

Name:           mesa-libGLU
Version:        9.0.0
Release:        2%{?dist}
Summary:        Mesa libGLU library

License:        MIT
URL:            http://mesa3d.org/
Source0:        ftp://ftp.freedesktop.org/pub/mesa/glu/glu-%{version}.tar.bz2
Source2:        make-git-snapshot.sh

%if 0%{?gitdate}
BuildRequires:  autoconf automake libtool
%endif
BuildRequires:  mesa-libGL-devel
#Requires:       
Provides: libGLU

%description
Mesa implementation of the standard GLU OpenGL utility API.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       gl-manpages
Provides:	libGLU-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n glu-%{?gitdate:%{gitdate}}%{?!gitdate:%{version}}

%build
%if 0%{?gitdate}
autoreconf -v -i -f
%endif
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
rm -rf $RPM_BUILD_ROOT%{_datadir}/man/man3/gl[A-Z]*

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_libdir}/libGLU.so.1
%{_libdir}/libGLU.so.1.3.*

%files devel
%{_includedir}/GL/glu*.h
%{_libdir}/libGLU.so
%{_libdir}/pkgconfig/glu.pc

%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 9.0.0-2
- 为 Magic 3.0 重建

* Tue Sep 18 2012 Adam Jackson <ajax@redhat.com> 9.0.0-1
- libGLU 9.0

* Mon Sep 10 2012 Dave Airlie <airlied@redhat.com> 9.0-0.2
- add back libGLU provides for now

* Tue Sep 04 2012 Adam Jackson <ajax@redhat.com> 9.0-0.1
- Initial packaging for split libGLU

