%global apiver 1.0
%define cairover 1.12.14

Summary:          C++ API for the cairo graphics library
Name:             cairomm
Version:	1.11.2
Release:          3%{?dist}
URL:              http://www.cairographics.org
License:          LGPLv2+
Group:            System Environment/Libraries
Source:           http://www.cairographics.org/releases/%{name}-%{version}.tar.gz
BuildRequires:    cairo-devel >= %{cairover}
BuildRequires:    pkgconfig
BuildRequires:    libsigc++20-devel

%description
Cairomm is the C++ API for the cairo graphics library. It offers all the power
of cairo with an interface familiar to C++ developers, including use of the 
Standard Template Library where it makes sense.

%package        devel
Summary:        Headers for developing programs that will use %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       cairo-devel >= %{cairover}
Requires:       libsigc++20-devel

%description    devel
Cairomm is the C++ API for the cairo graphics library. It offers all the power
of cairo with an interface familiar to C++ developers, including use of the 
Standard Template Library where it makes sense.

This package contains the libraries and header files needed for
developing %{name} applications.

%package        doc
Summary:        Developer's documentation for the cairomm library
Group:          Documentation
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Requires:       libsigc++20-doc

%description      doc
This package contains developer's documentation for the cairomm
library. Cairomm is the C++ API for the cairo graphics library.

The documentation can be viewed either through the devhelp
documentation browser or through a web browser.

If using a web browser the documentation is installed in the gtk-doc
hierarchy and can be found at /usr/share/doc/cairomm-1.0

%prep
%setup -q 

%build
%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc AUTHORS COPYING README NEWS
%{_libdir}/lib*.so.*

%files devel
%doc ChangeLog
%{_includedir}/%{name}-%{apiver}
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_libdir}/%{name}-%{apiver}

%files doc
%doc %{_datadir}/doc/%{name}-%{apiver}/
%doc %{_datadir}/devhelp/

%changelog
* Fri Mar 07 2014 Liu Di <liudidi@gmail.com> - 1.11.2-3
- 更新到 1.11.2

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 1.10.0-3
- 为 Magic 3.0 重建

* Sat Nov 03 2012 Liu Di <liudidi@gmail.com> - 1.10.0-2
- 为 Magic 3.0 重建

* Fri Jul 29 2011 Kalev Lember <kalevlember@gmail.com> - 1.10.0-1
- Update to 1.10.0
- Have the -doc subpackage depend on the base package
- Modernize the spec file
- Really own /usr/share/devhelp directory

* Mon Feb 21 2011 Haïkel Guémar <hguemar@fedoraproject.org> - 1.9.8-2
- fix documentation location
- co-own /usr/share/devhelp

* Mon Feb 14 2011 Haïkel Guémar <hguemar@fedoraproject.org> - 1.9.8-1
- upstream 1.9.8
- fix issues with f15/rawhide (RHBZ #676878)
- drop gtk-doc dependency (RHBZ #604169)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 14 2010 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 1.9.1-1
- New upstream release
- Removed html docs from -devel package
- Seperated requires into one per line
- Fixed devhelp docs

* Tue Nov 17 2009 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 1.8.4-1
- New upstream release
- Added cairommconfig.h file
- Added doc subpackage

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 1.8.0-1
- Update to 1.8.0
- Added libsigc++20-devel dependency

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Aug 29 2008 Denis Leroy <denis@poolshark.org> - 1.6.2-1
- Update to upstream 1.6.2
- atsui patch upstreamed

* Sun Mar 23 2008 Denis Leroy <denis@poolshark.org> - 1.5.0-1
- Update to 1.5.0
- Added patch from Mamoru Tasaka to fix font type enum (#438600)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.4.4-2
- Autorebuild for GCC 4.3

* Fri Aug 17 2007 Denis Leroy <denis@poolshark.org> - 1.4.4-1
- Update to upstream version 1.4.4
- Fixed License tag

* Fri Jul 20 2007 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 1.4.2-1
- New upstream release
- Changed install to preserve timestamps
- Removed mv of docs/reference and include files directly

* Wed Jan 17 2007 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 1.2.4-1
- New release

* Sat Oct 14 2006 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 1.2.2-1
- New upstream release

* Sun Aug 27 2006 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 1.2.0-4
- Bumped release for make tag

* Sun Aug 27 2006 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 1.2.0-3
- Bumped release for mass rebuild

* Sun Aug 20 2006 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 1.2.0-2
- Bumped release for make tag

* Sun Aug 20 2006 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 1.2.0-1
- New upstream release
- Updated summary and description

* Thu Aug  3 2006 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 1.1.10-1
- First release for cairo 1.2
- Adjusted cairo dependencies for new version
- Docs were in html, moved to reference/html

* Sun Apr  9 2006 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 0.6.0-1
- New upstream version should fix the upstream issues like AUTHORS and README
- Added pkgconfig to cairomm BuildRequires and cairomm-devel Requires
- Replaced makeinstall
- Fixed devel package description
- Modified includedir syntax
- docs included via the mv in install and in the devel files as html dir

* Sun Mar  5 2006 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 0.5.0-10
- Removed duplicate Group tag in devel
- Disabled docs till they're fixed upstream 

* Sun Mar  5 2006 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 0.5.0-9
- Removed requires since BuildRequires is present
- Cleaned up Source tag

* Fri Feb 24 2006 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 0.5.0-7
- Fixed URL and SOURCE tags
- Fixed header include directory

* Fri Feb 24 2006 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 0.5.0-6
- Fixed URL tag

* Wed Feb 22 2006 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 0.5.0-5
- Remove epoch 'leftovers'

* Wed Feb 22 2006 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 0.5.0-4
- Cleanup for FE

* Wed Feb 22 2006 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 0.5.0-3
- Added pre-release alphatag

* Wed Feb 22 2006 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 0.5.0-2
- Updated to current cairomm CVS
- Added documentation to devel package

* Fri Feb 03 2006 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 0.5.0-1
- Updated to current cairomm CVS

* Fri Jan 27 2006 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 0.4.0-1
- Initial creation from papyrus.spec.in

