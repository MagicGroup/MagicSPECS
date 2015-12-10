%define api_version		1.0

Summary:	OpenGL Extension to GTK
Summary(zh_CN.UTF-8): GTK 的 OpenGL 扩展
Name:		gtkglext
Version:	1.2.0
Release:	21%{?dist}

License:	LGPLv2+ or GPLv2+
Group:		System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL:		http://gtkglext.sourceforge.net/
Source0:	ftp://ftp.gnome.org/pub/gnome/sources/gtkglext/1.2/gtkglext-%{version}.tar.bz2
# Upstream changes, addressing BZ 677457
Patch0:		gtkglext-1.2.0-bz677457.diff

BuildRequires:	gtk2-devel
BuildRequires:	libGLU-devel
BuildRequires:	libGL-devel
# Conditional build feature
BuildRequires:	libXmu-devel
# The configure script checks for X11/Intrinsic.h
BuildRequires:	libXt-devel

Requires(postun):	/sbin/ldconfig
Requires(post):		/sbin/ldconfig

%description
GtkGLExt is an OpenGL extension to GTK. It provides the GDK objects
which support OpenGL rendering in GTK, and GtkWidget API add-ons to
make GTK+ widgets OpenGL-capable.

%description -l zh_CN.UTF-8 
GTK 的 OpenGL 扩展。

%package libs
Summary:	OpenGL Extension to GTK
Summary(zh_CN.UTF-8): %{name} 的运行库
Group:		System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:	LGPLv2+

%description libs
GtkGLExt is an OpenGL extension to GTK. It provides the GDK objects
which support OpenGL rendering in GTK, and GtkWidget API add-ons to
make GTK+ widgets OpenGL-capable.

%description libs -l zh_CN.UTF-8 
%{name} 的运行库。

%package devel
Summary:	Development tools for GTK-based OpenGL applications
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License:	LGPLv2+

Requires:	%{name}-libs = %{version}
Requires:	gtk2-devel
Requires:	libGL-devel
Requires:	libGLU-devel
Requires:	libXmu-devel
Requires:	pkgconfig

%description devel
The gtkglext-devel package contains the header files, static libraries,
and developer docs for GtkGLExt.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n gtkglext-%{version}
%patch0 -p1

%build
%configure --disable-gtk-doc --disable-static
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make

%install
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
magic_rpm_clean.sh

%post libs
/sbin/ldconfig

%postun libs
/sbin/ldconfig

%files libs
%defattr(-,root,root,-)

%doc AUTHORS COPYING COPYING.LIB ChangeLog README TODO
%{_libdir}/libgdkglext-x11-%{api_version}.so.*
%{_libdir}/libgtkglext-x11-%{api_version}.so.*

%files devel
%defattr(-,root,root,-)

%{_includedir}/*
%{_libdir}/gtkglext-%{api_version}
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*
%{_datadir}/aclocal/*
%doc %{_datadir}/gtk-doc/html/*

%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 1.2.0-21
- 为 Magic 3.0 重建

* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 1.2.0-20
- 为 Magic 3.0 重建

* Fri Apr 11 2014 Liu Di <liudidi@gmail.com> - 1.2.0-19
- 为 Magic 3.0 重建

* Mon Jul 23 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.2.0-18
- Remove hard-coded rpath (BZ 828527).
- Reflect Source0:-URL having changed.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 1.2.0-15
- Rebuild for new libpng

* Thu Feb 17 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.2.0-14
- Apply %%patch0.

* Thu Feb 17 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 1.2.0-13
- Fix dependency in gtkglext-devel (-> gtkglext-libs).

* Wed Feb 16 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.2.0-12
- Add gtkglext-1.2.0-bz677457.diff (BZ 677457).
- Spec file cleanup.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Dec 08 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.2.0-8
- Rebuild for pkgconfig provides

* Tue Jun 03 2008 Ralf Corsépius <rc040203@freenet.de> - 1.2.0-7
- Use 0%%{?fedora} conditionals instead of "%%{fedora}" (BZ 449635).

* Sun Feb 10 2008 Ralf Corsépius <rc040203@freenet.de> - 1.2.0-6
- Rebuild for gcc43.

* Wed Aug 22 2007 Ralf Corsépius <rc040203@freenet.de> - 1.2.0-5
- Don't install *.la's for fedora >= 8.
- Update license tags.
- Split out *-libs.

* Tue Sep 05 2006 Ralf Corsépius <rc040203@freenet.de> - 1.2.0-4
- Mass rebuild.

* Mon Aug 14 2006 Ralf Corsépius <rc040203@freenet.de> - 1.2.0-3
- BR: libXmu-devel (Braden McDaniel).
- *-devel: R: libXmu-devel. 
- *-devel: R: pkgconfig.

* Tue Feb 14 2006 Ralf Corsépius <rc040203@freenet.de> - 1.2.0-2
- Require: libGLU-devel (PR 181018)

* Mon Feb 06 2006 Ralf Corsépius <rc040203@freenet.de> - 1.2.0-1
- Upstream update.
- Spec file cleanup.
- Disable static libs.

* Thu Jan 05 2006 Ralf Corsepius <ralf@links2linux.de> - 1.0.6-3
- Add %%dist.
- Adaptations to modular X .
- Remove gcc-c++ (Already in default deps).

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Fri Jun 07 2004 Ralf Corsepius <ralf@links2linux.de> - 1.0.6-0.fdr.1
- Spec cleanups.

* Fri Jun 04 2004 Ralf Corsepius <ralf@links2linux.de> - 1.0.6-0.fdr.0
- Initial fedora rpm spec, loosely derived from the version shipped
  with gtkglext.
