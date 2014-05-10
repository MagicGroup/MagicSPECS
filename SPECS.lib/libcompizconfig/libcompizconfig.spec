%global         basever 0.8.8

Name:           libcompizconfig
Version:        0.8.8
Release:        11%{?dist}
Epoch:          1
Summary:        Configuration back end for compiz

Group:          System Environment/Libraries
# backends/libini.so is GPLv2+, other parts are LGPLv2+
License:        LGPLv2+ and GPLv2+
URL:            http://www.compiz.org
Source0:        http://releases.compiz.org/%{version}/%{name}-%{version}.tar.bz2

# libdrm is not available on these arches
ExcludeArch:    s390 s390x
BuildRequires:  compiz-devel >= %{basever}
BuildRequires:  compiz-bcop >= %{basever}
BuildRequires:  libX11-devel
BuildRequires:  gettext
BuildRequires:  intltool
BuildRequires:  perl(XML::Parser)
BuildRequires:  mesa-libGL-devel
BuildRequires:  protobuf-devel

Patch0:         libcompizconfig_new_mate.patch
Patch1:         libcompizconfig_fix-intltoolize-ftbfs.patch
Patch2:         libcompizconfig_default_backend_for_mate-session.patch
Patch3:         libcompizconfig_primary-is-control.patch

%description
The Compiz Project brings 3D desktop visual effects that improve
usability of the X Window System and provide increased productivity
through plugins and themes contributed by the community giving a
rich desktop experience.

This package contains the library for plugins to configure compiz 
settings.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{epoch}:%{version}-%{release}
Requires:       compiz-devel >= %{version}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
%patch0 -p1 -b .mate
%patch1 -p1 -b .intltoolize-ftbfs
%patch2 -p1 -b .default_backend
%patch3 -p1 -b .primary-is-control

%build
%configure --disable-static

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool
           
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
find $RPM_BUILD_ROOT -name '*.a' -exec rm -f {} ';'


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc AUTHORS COPYING NEWS VERSION
%config(noreplace) %{_sysconfdir}/compizconfig/
%{_libdir}/*.so.*
%{_datadir}/compiz/ccp.xml
%{_libdir}/compiz/*.so
%dir %{_libdir}/compizconfig/
%dir %{_libdir}/compizconfig/backends/
%{_libdir}/compizconfig/backends/libini.so

%files devel
%{_includedir}/compizconfig/
%{_libdir}/*.so
%{_libdir}/pkgconfig/libcompizconfig.pc


%changelog
* Wed May 07 2014 Liu Di <liudidi@gmail.com> - 1:0.8.8-11
- 为 Magic 3.0 重建

* Wed May 07 2014 Liu Di <liudidi@gmail.com> - 1:0.8.8-10
- 为 Magic 3.0 重建

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.8.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Apr 24 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-8
- rework mate patch

* Sun Mar 10 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-7
- rebuild for protobuf ABI change to 8 for rawhide

* Sun Feb 10 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-6
- add libcompizconfig_primary-is-control.patch
- fix (#909657)

* Sat Dec 08 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-5
- change default backend for mate-session
- with libcompizconfig_default_backend_for_mate-session.patch

* Sat Dec 08 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-4
- fix incoherent-version-in-changelog
- remove requires pkgconfig
- fix mixed-use-of-spaces-and-tabs

* Sun Dec 02 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-3
- add patch from Jasmine Hassan jasmine.aura@gmail.com
- fix binary-or-shlib-defines-rpath
- initial build for fedora
- add epoch

* Tue May 15 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 0.8.8-2
- add libcompizconfig_mate.patch

* Tue May 15 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 0.8.8-1
- build for mate

