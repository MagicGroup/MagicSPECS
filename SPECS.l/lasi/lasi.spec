Name:           lasi
Version:	1.1.2
Release:        10%{?dist}
Summary:        C++ library for creating Postscript documents
Summary(zh_CN.UTF-8): 创建 PostScript 文档的 C++ 库

Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License:        LGPLv2+
URL:            http://www.unifont.org/lasi/
Source0:        http://downloads.sourceforge.net/lasi/libLASi-%{version}.tar.gz
Patch0:         lasi-multilib.patch
Patch1:		lasi-freetype.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  pango-devel, cmake
# For testing
BuildRequires:  dejavu-sans-mono-fonts


%description
LASi is a library written by Larry Siden  that provides a C++ stream output
interface ( with operator << ) for creating Postscript documents that can
contain characters from any of the scripts and symbol blocks supported in
Unicode  and by Owen Taylor's Pango layout engine. The library accommodates
right-to-left scripts such as Arabic and Hebrew as easily as left-to-right
scripts. Indic and Indic-derived Complex Text Layout (CTL) scripts, such as
Devanagari, Thai, Lao, and Tibetan are supported to the extent provided by
Pango and by the OpenType fonts installed on your system. All of this is
provided without need for any special configuration or layout calculation on
the programmer's part.

Although the capability to produce Unicode-based multilingual Postscript
documents exists in large Open Source application framework libraries such as
GTK+, QT, and KDE, LASi was designed for projects which require the ability
to produce Postscript independent of any one application framework.

%description -l zh_CN.UTF-8
创建 PostScript 文档的 C++ 库。

%package        devel
Summary:        Development headers and libraries for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}
Requires:       pango-devel

%description    devel
%{summary}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n libLASi-%{version}
%patch0 -p1 -b .multilib
%patch1 -p0 -b .freetype2

%build
mkdir magic
cd magic
export CFLAGS="$RPM_OPT_FLAGS"
export CXXFLAGS="$RPM_OPT_FLAGS"
export FFLAGS="$RPM_OPT_FLAGS"
%cmake -DUSE_RPATH=OFF -DCMAKE_INSTALL_LIBDIR=%{_libdir} ..
make VERBOSE=1 %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
cd magic
make install DESTDIR=$RPM_BUILD_ROOT VERBOSE=1


%check
cd magic
ctest --verbose


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README
%{_libdir}/libLASi.so.*


%files devel
%defattr(-,root,root,-)
%{_includedir}/LASi.h
%{_libdir}/libLASi.so
%{_libdir}/pkgconfig/lasi.pc
%doc %{_datadir}/lasi%{version}/
%{_docdir}/*

%changelog
* Tue Nov 10 2015 Liu Di <liudidi@gmail.com> - 1.1.2-10
- 为 Magic 3.0 重建

* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 1.1.2-9
- 更新到 1.1.2

* Wed Apr 16 2014 Liu Di <liudidi@gmail.com> - 1.1.1-8
- 为 Magic 3.0 重建

* Wed Apr 16 2014 Liu Di <liudidi@gmail.com> - 1.1.1-7
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.1.1-6
- 为 Magic 3.0 重建

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Orion Poplawski <orion@cora.nwra.com> - 1.1.1-4
- Fix multilib conflict (Bug 831398)

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-3
- Rebuilt for c++ ABI breakage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Sep 22 2011 - Orion Poplawski <orion@cora.nwra.com> - 1.1.1-1
- Update to 1.1.1

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 14 2009 - Orion Poplawski <orion@cora.nwra.com> - 1.1.0-5
- Fix font BR

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 - Orion Poplawski <orion@cora.nwra.com> - 1.1.0-3
- Change BR to dejavu-fonts-compat
- Add -DCMAKE_SKIP_RPATH:BOOL=OFF -DUSE_RPATH=OFF to cmake to
  use rpath during build, but not install

* Tue Aug  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.1.0-2
- fix license tag

* Sat Feb  9 2008 - Orion Poplawski <orion@cora.nwra.com> - 1.1.0-1
- Update to 1.1.0

* Tue Aug 29 2006 - Orion Poplawski <orion@cora.nwra.com> - 1.0.6-1
- Update to 1.0.6
- Remove pkg-config patch applied upstream

* Mon May  8 2006 - Orion Poplawski <orion@cora.nwra.com> - 1.0.5-2
- Disable static libs
- Patch pc file to return -lLASi

* Thu May  4 2006 - Orion Poplawski <orion@cora.nwra.com> - 1.0.5-1
- Update to 1.0.5
- Remove unneeded patches and autotools
- Move doc dir to -devel package
- Make -devel package require pango-devel, included in LASi.h

* Mon Apr 24 2006 - Orion Poplawski <orion@cora.nwra.com> - 1.0.4-1
- Initial Fedora Extras version
