Name:           ftgl
Version:        2.1.3
Release:        0.5.rc5%{?dist}
Summary:        OpenGL frontend to Freetype 2
Summary(zh_CN.UTF-8): Freetype 2 的 OpenGL 前端

Group:          System Environment/Libraries
Group(zh_CN.UTF-8):	系统环境/库
License:        LGPLv2
URL:            http://ftgl.wiki.sourceforge.net/
Source0:        http://downloads.sourceforge.net/ftgl/ftgl-%{version}-rc5.tar.bz2
Patch0:         ftgl-2.1.3-rc5-ttf_font.patch
Patch1:		ftgl-2.1.3-rc5-ldflags.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  doxygen

BuildRequires:  freeglut-devel
BuildRequires:  freetype-devel
BuildRequires:  libXi-devel
BuildRequires:  libXmu-devel
BuildRequires:  cppunit-devel

Obsoletes: ftgl-utils < %{version}


%description
FTGL is a free open source library to enable developers to use arbitrary
fonts in their OpenGL (www.opengl.org)  applications.
Unlike other OpenGL font libraries FTGL uses standard font file formats
so doesn't need a preprocessing step to convert the high quality font data
into a lesser quality, proprietary format.
FTGL uses the Freetype (www.freetype.org) font library to open and 'decode'
the fonts. It then takes that output and stores it in a format most 
efficient for OpenGL rendering.

%description -l zh_CN.UTF-8
Freetype 2 的 OpenGL 前端，可以在 OpenGL 程序中使用字体。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8):	%name 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8):	开发/库
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig
Requires:       freetype-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%name 的开发包。

%package docs
Summary:        Documentation for %{name}
Summary(zh_CN.UTF-8):	%name 的文档
Group:          Documentation
Group(zh_CN.UTF-8):	文档

%description docs
This package contains documentation files for %{name}.

%description docs -l zh_CN.UTF-8
%name 的开发包。

%prep
%setup -q -n ftgl-%{version}~rc5
%patch0 -p1 -b .destdir
%patch1 -p1

%build
%configure \
  --enable-shared \
  --disable-static \
  --with-gl-inc=%{_includedir} \
  --with-gl-lib=%{_libdir} \
  --with-glut-inc=%{_includedir} \
  --with-glut-lib=%{_libdir} \
  --with-x

# Remove the ~rc5 from the pc file, as this causes rpm to a%description -l zh_CN.UTF-8 a
# Requires: rpmlib(TildeInVersions) <= 4.10.0-1 
# Which breaks installing ftgl-devel into a koji buildroot (rhbz#843460)
sed -i 's/2\.1\.3~rc5/2.1.3/' ftgl.pc

make all %{?_smp_mflags} 

%install
rm -rf $RPM_BUILD_ROOT __doc
make install INSTALL="%{__install} -p" DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# Doc fixes
mkdir -p __doc/html
install -pm 0644 $RPM_BUILD_ROOT%{_datadir}/doc/ftgl/html/* __doc/html
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc

magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS BUGS ChangeLog COPYING NEWS README TODO
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/FTGL/
%{_libdir}/*.so
%{_libdir}/pkgconfig/*

%files docs
%defattr(-,root,root,-)
%doc __doc/*


%changelog
* Thu Apr 17 2014 Liu Di <liudidi@gmail.com> - 2.1.3-0.5.rc5
- 为 Magic 3.0 重建

* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 2.1.3-0.4.rc5
- 为 Magic 3.0 重建


