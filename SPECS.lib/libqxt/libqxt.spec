Name:		libqxt
Version:	0.6.2
Release:	3%{?dist}
Summary:	Qt extension library
Group:		System Environment/Libraries
License:	CPL or LGPLv2
URL:		http://www.libqxt.org/
Source0:	http://bitbucket.org/libqxt/libqxt/get/v%{version}.tar.bz2
# Fix DSO linking
Patch0:		libqxt-linking.patch
# To support multimedia keys when using clementine
# Patch sent to upstream. They want to reimplement it more cleanly.
# We will use this patch until upstream reimplements it.
# http://dev.libqxt.org/libqxt/issue/75
Patch1:		libqxt-media-keys.patch
# Fix wrong header includes RHBZ#733222
# http://dev.libqxt.org/libqxt/issue/112/wrong-include-in-qxtnetworkh
Patch2:		libqxt-header-fix.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	avahi-compat-libdns_sd-devel
BuildRequires:	avahi-devel
BuildRequires:	libdb-devel
BuildRequires:	libXrandr-devel
BuildRequires:	openssl-devel
BuildRequires:	qt4-devel

%{?_qt4_version:Requires: qt4%{?_isa} >= %{_qt4_version}}

%description
LibQxt, an extension library for Qt, provides a suite of cross-platform
utility classes to add functionality not readily available in the Qt toolkit.

%package	devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	avahi-compat-libdns_sd-devel
Requires:	avahi-devel
Requires:	libdb-devel
Requires:	qt4-devel

%description	devel
This package contains libraries and header files for developing applications
that use LibQxt.


%prep
%setup -q -n %{name}-%{name}-v%{version}
%patch0 -p1 -b .linking
%patch1 -p1 -b .mediakeys
%patch2 -p1 -b .includes

# We don't want rpath
sed -i '/RPATH/d' src/qxtlibs.pri


%build
# Does not use GNU configure
./configure -verbose \
	    -qmake-bin %{_qt4_qmake} \
	    -prefix %{_prefix} \
	    -libdir %{_qt4_libdir} \
	    -headerdir %{_qt4_headerdir}
make %{?_smp_mflags}
#make %{?_smp_mflags} docs


%install
rm -rf $RPM_BUILD_ROOT
make install INSTALL_ROOT=$RPM_BUILD_ROOT

# We are installing these to the proper location
rm -fr $RPM_BUILD_ROOT%{_prefix}/doc/

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS CHANGES *.txt LICENSE README
%{_qt4_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%doc examples/
%{_qt4_headerdir}/*
%{_qt4_libdir}/*.so
%{_qt4_plugindir}/designer/*.so
%{_qt4_datadir}/mkspecs/features/qxt*.prf

%changelog
* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Nov 26 2011 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.6.2-1
- Update to 0.6.2

* Thu Aug 25 2011 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.6.1-3
- Fix wrong includes RHBZ#733222

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Nov 25 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.6.1-1
- Update to 0.6.1

* Sun Jul 18 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.6.0-3
- Include patch to support for mod4 in qxtglobalshortcut
- Include patch to support multimedia keys

* Tue Apr 20 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.6.0-2
- This is the real 0.6.0 (upstream changed their tarball)

* Sun Apr 11 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.6.0-1
- Use qt4 macros more extensively.
- Update to 0.6.0 final.

* Wed Apr 07 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.6.0-0.2.20100407hg
- New snapshot. The previous tarball got damaged somehow.
- Remove configure tests hack. Upstream fixed it upon our warning.

* Sat Mar 27 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.6.0-0.1.20100327hg
- Initial build
