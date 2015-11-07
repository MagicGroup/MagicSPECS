Name:           celt051
Version:        0.5.1.3
Release:        7%{?dist}
Summary:        An audio codec for use in low-delay speech and audio communication

Group:          System Environment/Libraries
License:        BSD
# Files without license header are confirmed to be BSD. Will be fixed in later release
# http://lists.xiph.org/pipermail/celt-dev/2009-February/000063.html
URL:            http://www.celt-codec.org/
Source0:        http://downloads.us.xiph.org/releases/celt/celt-%{version}.tar.gz

BuildRequires: libogg-devel

%description
CELT (Constrained Energy Lapped Transform) is an ultra-low delay audio
codec designed for realtime transmission of high quality speech and audio.
This is meant to close the gap between traditional speech codecs
(such as Speex) and traditional audio codecs (such as Vorbis).

The CELT bitstream format is not yet stable, this package is a special
version of 0.5.1 that has the same bitstream format, but symbols and files
renamed from 'celt*' to 'celt051*' so that it is parallel installable with
the normal celt for packages requiring this particular bitstream format.

%package devel
Summary: Development package for %{name}
Group: Development/Libraries
Requires: libogg-devel
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n celt-%{version}

%build
%configure --disable-static
# Remove rpath as per https://fedoraproject.org/wiki/Packaging/Guidelines#Beware_of_Rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/libcelt051.la

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING README TODO
%{_bindir}/celtenc051
%{_bindir}/celtdec051
%{_libdir}/libcelt051.so.0
%{_libdir}/libcelt051.so.0.0.0

%files devel
%defattr(-,root,root,-)
%doc COPYING README
%{_includedir}/celt051
%{_libdir}/pkgconfig/celt051.pc
%{_libdir}/libcelt051.so

%changelog
* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 0.5.1.3-7
- 为 Magic 3.0 重建

* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 0.5.1.3-6
- 为 Magic 3.0 重建

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 0.5.1.3-5
- 为 Magic 3.0 重建

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul  9 2010 Alexander Larsson <alexl@redhat.com> - 0.5.1.3-2
- Update according to review (#612979)

* Fri Jul  9 2010 Alexander Larsson <alexl@redhat.com> - 0.5.1.3-1
- First fedora package, based on RHEL package version 0.5.1.3-0
