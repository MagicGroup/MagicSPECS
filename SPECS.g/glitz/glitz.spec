Name:           glitz
Version:        0.5.6
Release:        11%{?dist}
Summary:        OpenGL image compositing library
Summary(zh_CN.UTF-8): OpenGL 图像合成库
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        BSD
URL:            http://www.freedesktop.org/Software/glitz
Source:         http://cairographics.org/snapshots/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  libX11-devel, libXt-devel, libICE-devel, libGL-devel

%description
Glitz is an OpenGL image compositing library. Glitz provides Porter/Duff
compositing of images and implicit mask generation for geometric primitives
including trapezoids, triangles, and rectangles.

%description -l zh_CN.UTF-8
OpenGL 图像合成库。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package        glx
Summary:        GLX extensions for %{name}
Summary(zh_CN.UTF-8): %{name} 的 GLX 扩展
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}

%description    glx
The %{name}-glx package contains GLX extensions for %{name}.

%description glx -l zh_CN.UTF-8 
%{name} 的 GLX 扩展

%package        glx-devel
Summary:        Development files for %{name}-glx
Summary(zh_CN.UTF-8): %{name}-glx 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name}-glx = %{version}-%{release}
Requires:       %{name}-devel = %{version}-%{release}
Requires:       libX11-devel, libGL-devel, pkgconfig

%description    glx-devel
The %{name}-glx-devel package contains libraries and header files for
developing applications that use %{name}-glx.

%description glx-devel -l zh_CN.UTF-8
%{name}-glx 的开发包。

%prep
%setup -q

%build
%configure --disable-static --enable-glx --disable-agl \
           --disable-egl --disable-wgl
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
install -D -m 644 ./src/glitz.man \
        $RPM_BUILD_ROOT%{_mandir}/man3/glitz.3
install -D -m 644 ./src/glx/glitz-glx.man \
        $RPM_BUILD_ROOT%{_mandir}/man3/glitz-glx.3
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post glx -p /sbin/ldconfig
%postun glx -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING INSTALL NEWS README TODO
%{_libdir}/libglitz.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/glitz.h
%{_libdir}/libglitz.so
%{_libdir}/pkgconfig/glitz.pc
%{_mandir}/man3/glitz.3.gz

%files glx
%defattr(-,root,root,-)
%{_libdir}/libglitz-glx.so.*

%files glx-devel
%defattr(-,root,root,-)
%{_includedir}/glitz-glx.h
%{_libdir}/libglitz-glx.so
%{_libdir}/pkgconfig/glitz-glx.pc
%{_mandir}/man3/glitz-glx.3.gz

%changelog
* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.6-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.5.6-6
- Autorebuild for GCC 4.3

* Sat Nov 11 2006 Eric Work <work.eric@gmail.com> 0.5.6-5
- bump EVR to assure devel replaces FC6

* Fri Sep 15 2006 Eric Work <work.eric@gmail.com> 0.5.6-4
- bumped version to prepare for FC6

* Wed Jun 07 2006 Eric Work <work.eric@gmail.com> 0.5.6-3
- added missing requires to devel packages
- moved man pages to devel packages

* Mon Jun 05 2006 Eric Work <work.eric@gmail.com> 0.5.6-2
- added configure flags for build consistency
- added man pages for glitz and glitz-glx
- split package into subpackages glitz and glitz-glx

* Wed May 31 2006 Eric Work <work.eric@gmail.com> 0.5.6-1
- initial release

