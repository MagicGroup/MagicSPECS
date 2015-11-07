Name:           libglpng
Version:        1.45
Release:        10%{?dist}
Summary:        Toolkit for loading PNG images as OpenGL textures
Summary(zh_CN.UTF-8): 把 PNG 图像做为 OpenGL 纹理载入的工具集

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        MIT
URL:            https://admin.fedoraproject.org/pkgdb/packages/name/libglpng
# Upstream's dead
Source0:        http://ftp.de.debian.org/debian/pool/main/libg/%{name}/%{name}_%{version}.orig.tar.gz
# From Debian - a Makefile. Yay.
Source1:        libglpng-1.45-makefile
# Debian patch, couple of small fixes.
Patch0:         libglpng-1.45-debian.patch
Patch1:         libglpng-1.45-CVE-2010-1519.patch
Patch2:         libglpng-1.45-libpng15.patch
BuildRequires:  libpng-devel libGL-devel

%description
glpng is a small toolkit to make loading PNG image files as an OpenGL
texture as easy as possible.

%description -l zh_CN.UTF-8
把 PNG 图像做为 OpenGL 纹理载入的工具集。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n %{name}-%{version}.orig
%patch0 -p1
%patch1 -p1
%patch2 -p1
cp %{SOURCE1} Makefile


%build
make %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS -fPIC -Iinclude" libglpng.so.1.45


%install
make install DESTDIR=$RPM_BUILD_ROOT%{_prefix} LIB=%{_lib}
magic_rpm_clean.sh

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc glpng.htm
%{_libdir}/%{name}.so.*

%files devel
%{_includedir}/GL
%{_libdir}/%{name}.so


%changelog
* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 1.45-10
- 为 Magic 3.0 重建

* Wed Jul 16 2014 Liu Di <liudidi@gmail.com> - 1.45-9
- 为 Magic 3.0 重建

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.45-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.45-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Hans de Goede <hdegoede@redhat.com> - 1.45-6
- Fix building with libpng-1.5

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 1.45-5
- Rebuild for new libpng

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.45-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Sep 10 2010 Hans de Goede <hdegoede@redhat.com> 1.45-3
- Fix CVE-2010-1519 (#623831,#623832)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.45-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May 17 2009 Hans de Goede <hdegoede@redhat.com> 1.45-1
- Initial Fedora package, based on Mandriva package
